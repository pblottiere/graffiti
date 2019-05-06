import time
from enum import Enum
import csv
import shutil
import os
import requests
from collections import OrderedDict
import psycopg2
from tqdm import trange


class Error(object):

    def __init__(self, name, host, code, text):
        self.name = name
        self.host = host
        self.code = code
        self.text = text

    def tostr(self):
        return ('REQUEST: {}\n'
                'HOST: {}\n'
                'ERROR: {}\n'
                'DESCRIPTION: {}\n'
                .format(self.name, self.host, self.code, self.text))


class Type(Enum):
    GetCapabilities = 1
    GetMap = 2


class Host(object):

    def __init__(self, name, host, payload={}):
        self.host = host
        self.name = name
        self.payload = payload


class Request(object):

    def __init__(self, name, type, hosts, iterations=50, desc='',
                 logdir=None, title='', precision=2):
        self.durations = OrderedDict()
        self.type = type
        self.hosts = hosts
        self.iterations = iterations
        self.name = name
        self.desc = desc
        self.logdir = logdir
        self.title = title
        self.precision = precision
        self.errors = []

    @property
    def hosts(self):
        return self._hosts

    @hosts.setter
    def hosts(self, hosts):
        self._hosts = hosts
        for i in range(0, len(self._hosts)):
            hosts[i].payload['REQUEST'] = self.type.name

            service = ''
            if self.type == Type.GetCapabilities or self.type == Type.GetMap:
                service = 'WMS'
            hosts[i].payload['SERVICE'] = service

    @staticmethod
    def build(cfg):
        iterations = cfg.iterations
        name = cfg.name
        title = cfg.title
        desc = cfg.description
        type = cfg.type
        logdir = cfg.logdir
        precision = cfg.precision

        hosts = []
        for hostCfg in cfg.hosts:
            host = Host(hostCfg.name, hostCfg.host, hostCfg.payload)
            hosts.append(host)

        if cfg.provider == 'POSTGRES':
            return DBRequest(name, type, hosts, iterations, desc, logdir,
                             title, precision, cfg.db_config)
        else:
            return Request(name, type, hosts, iterations, desc, logdir,
                           title, precision)

    def run(self):
        log = None
        if self.logdir:
            logfile = os.path.join(self.logdir, '{}.log'.format(self.name))
            log = open(logfile, 'w')

        for i in trange(len(self.hosts), leave=False, desc='Hosts'):
            host = self.hosts[i]
            dur = []

            if log:
                log.write(host.name)
                log.write('\n')
                log.write('    - HOST: {}\n'.format(host.host))
                for key in host.payload.keys():
                    log.write('    - {}: {}\n'.format(key, host.payload[key]))

            for j in trange(self.iterations, leave=False, desc='Iterations'):

                self.before_request(log)

                start = time.time()

                try:
                    r = requests.get(host.host, params=host.payload,
                                     stream=True)
                except requests.exceptions.RequestException as e:
                    err = Error(self.name, host.name, 'Exception', e)
                    self.errors.append(err)
                    dur.append(0)
                    continue

                if r.status_code != 200:
                    e = Error(self.name, host.name, r.status_code, r.text)
                    self.errors.append(e)
                    dur.append(0)
                    continue

                # log 1st iteration when it's an image (to be able to include
                # the figure in the long description)
                if self.logdir and j == 0 and 'FORMAT' in host.payload \
                        and 'png' in host.payload['FORMAT']:
                    hn = host.name
                    hn = ''.join(c for c in hn if c not in '(){}<>')
                    hn = hn.replace(' ', '_')
                    imname = '{}_{}.png'.format(self.name, hn.lower())
                    logres = os.path.join(self.logdir, imname)
                    with open(logres, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)

                dur.append(round(time.time() - start, self.precision))

                self.after_request(log, host)

            self.durations[host.name] = dur

        if log:
            log.close()

        if self.logdir:
            csvfile = os.path.join(self.logdir, '{}.csv'.format(self.name))
            with open(csvfile, 'w') as f:
                writer = csv.writer(f, delimiter=' ', quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
                writer.writerow(list(self.durations.keys()))

                for i in range(0, self.iterations):
                    row = []
                    for key in self.durations.keys():
                        row.append(self.durations[key][i])
                    writer.writerow(row)

    def before_request(self, log):
        pass

    def after_request(self, log):
        pass

    def save(self, path):
        with open(path, 'w') as f:
            for host in self.hosts:
                f.write(host.name)
                f.write(' ')
                f.write(' '.join(map(str, self.durations[host.name])))
                f.write('\n')


class DBRequest(Request):

    def __init__(self, name, type, hosts, iterations=50, desc='',
                 logdir=None, title='', precision=2, db_config=None):

        super().__init__(name, type, hosts, iterations, desc,
                         logdir, title, precision)

        self.pcon = psycopg2.connect(
            "host={} port={} dbname={} user={} password={}".format(
                db_config.host, db_config.port, db_config.name, db_config.user,
                db_config.password))

        self.pcur = self.pcon.cursor()

    def before_request(self, log):
        # reinit db statistics
        self.pcur.execute("select pg_stat_statements_reset()")
        self.pcon.commit()

    def after_request(self, log, host):
        self.pcur.execute("""
        SELECT sum(total_time), string_agg(query, ',')
        FROM pg_stat_statements
        WHERE query != 'select pg_stat_statements_reset()'
        AND query != 'BEGIN' AND QUERY != 'COMMIT'
        """)

        total_time, query = self.pcur.fetchone()
        name = host.name + " (database)"
        if name not in self.durations:
            self.durations[name] = []
        self.durations[name].append(total_time/1000 if total_time else 0)

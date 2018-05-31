import time
from enum import Enum
from tqdm import trange
import requests


class Type(Enum):
    GetCapabilities = 1
    GetMap = 2


class Host(object):

    def __init__(self, name, host, payload={}):
        self.host = host
        self.name = name
        self.payload = payload


class Request(object):

    def __init__(self, name, type, hosts, iterations=50, short_desc='',
                 long_desc='', logfile='', title=''):
        self.durations = {}
        self.type = type
        self.hosts = hosts
        self.iterations = iterations
        self.name = name
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.logfile = logfile
        self.title = title

    @property
    def hosts(self):
        return self._hosts

    @hosts.setter
    def hosts(self, hosts):
        self._hosts = hosts
        for i in range(0, len(self._hosts)):
            hosts[i].payload['REQUEST'] = self.type.name

            service = ''
            if self.type == Type.GetCapabilities:
                service = 'WMS'
            hosts[i].payload['SERVICE'] = service

    @staticmethod
    def build(cfg):
        hosts = cfg.hosts
        iterations = cfg.iterations
        name = cfg.name
        title = cfg.title
        short_desc = cfg.short_description
        long_desc = cfg.long_description
        type = cfg.type
        logfile = cfg.logfile
        return Request(name, type, hosts, iterations, short_desc, long_desc,
                       logfile, title)

    def run(self):
        log = None
        if self.logfile:
            log = open(self.logfile, 'w')

        for i in trange(len(self.hosts), leave=False, desc='Hosts'):
            host = self.hosts[i]
            dur = []

            if log:
                log.write(host.name)
                log.write('\n')
                log.write('    - HOST: \n'.format(host))
                for key in host.payload.keys():
                    log.write('    - {}: {}\n'.format(key, host.payload[key]))

            for j in trange(self.iterations, leave=False, desc='Iterations'):
                start = time.time()
                r = requests.get(host.host, params=host.payload)

                if r.status_code != 200:
                    print("ERROR")
                    continue

                dur.append(round(time.time() - start, 4))

            self.durations[host.name] = dur

    def save(self, path):
        with open(path, 'w') as f:
            for host in self.hosts:
                f.write(host.name)
                f.write(' ')
                f.write(' '.join(map(str, self.durations[host.name])))
                f.write('\n')

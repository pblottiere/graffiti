import yaml
import shutil
import os
import datetime

from .database import Database
from.request import Type


class ConfigHost(object):

    def __init__(self, cfg):
        self.name = cfg['NAME']
        self.host = cfg['HOST']
        self.payload = {}

        for key in cfg.keys():
            if 'PAYLOAD_' in key:
                newkey = key.replace('PAYLOAD_', '')
                self.payload[newkey] = cfg[key]


class ConfigRequest(object):

    def __init__(self, cfg, basedir, logdir, precision=2):
        self.type = None
        if cfg['TYPE'] == Type.GetCapabilities.name:
            self.type = Type.GetCapabilities
        elif cfg['TYPE'] == Type.GetMap.name:
            self.type = Type.GetMap

        self.title = cfg['TITLE']
        self.description = None
        if cfg['DESCRIPTION']:
            self.description = os.path.join(basedir, cfg['DESCRIPTION'])
        self.iterations = cfg['ITERATIONS']
        self.name = cfg['NAME']
        self.logdir = logdir
        self.precision = precision

        self.hosts = []
        for host in cfg['HOSTS']:
            self.hosts.append(ConfigHost(host))


class Config(object):

    def __init__(self, yml, new=True):
        self.html = None
        self.requests = []
        self.read(yml)

        datefile = os.path.join(self.outdir, 'date')
        format = '%Y-%m-%d %H:%M:%S'
        if new:
            shutil.rmtree(self.outdir, ignore_errors=True)
            os.makedirs(self.outdir)
            os.makedirs(self.imdir)
            os.makedirs(self.logdir)

            self.date = datetime.datetime.now().strftime(format)
            if self.outdir:
                with open(datefile, 'w+') as log:
                    log.write(self.date)
        else:
            if os.path.isfile(datefile):
                with open(datefile, 'r') as f:
                    self.date = f.read()

    def read(self, yml):
        self.requests = []

        with open(yml, 'r') as stream:
            cfg = yaml.load(stream)

            self.title = cfg['TITLE']
            self.precision = cfg['PRECISION']
            self.basedir = os.path.dirname(os.path.abspath(yml))

            self.outdir = cfg['OUTDIR']
            self.imdir = os.path.join(self.outdir, 'graph')
            self.logdir = os.path.join(self.outdir, 'log')
            self.html = os.path.join(self.outdir, cfg['HTML'])

            for request in cfg['REQUESTS']:
                cfgReq = ConfigRequest(request, self.basedir, self.logdir, self.precision)
                self.requests.append(cfgReq)

            self.desc = ''
            if cfg['DESCRIPTION']:
                path = os.path.join(self.basedir, cfg['DESCRIPTION'])
                with open(path) as f:
                    self.desc = f.read()

            self.database = None
            if 'DATABASE' in cfg and cfg['DATABASE']:
                self.database = cfg['DATABASE']

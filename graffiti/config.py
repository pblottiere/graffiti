import yaml
import shutil
import os

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

    def __init__(self, cfg, basedir, logdir):
        self.type = None
        if cfg['TYPE'] == Type.GetCapabilities.name:
            self.type = Type.GetCapabilities
        elif cfg['TYPE'] == Type.GetMap.name:
            self.type = Type.GetMap

        self.title = cfg['TITLE']
        self.short_description = cfg['SHORT_DESCRIPTION']
        self.long_description = os.path.join(basedir, cfg['LONG_DESCRIPTION'])
        self.iterations = cfg['ITERATIONS']
        self.name = cfg['NAME']
        self.logdir = logdir

        self.hosts = []
        for host in cfg['HOSTS']:
            self.hosts.append(ConfigHost(host))


class Config(object):

    def __init__(self, yml):
        self.html = None
        self.svg = True
        self.requests = []
        self.read(yml)

        shutil.rmtree(self.outdir, ignore_errors=True)
        os.makedirs(self.outdir)
        os.makedirs(self.imdir)
        os.makedirs(self.logdir)


    def read(self, yml):
        self.requests = []

        with open(yml, 'r') as stream:
            cfg = yaml.load(stream)

            self.svg = cfg['SVG']
            self.basedir = os.path.dirname(os.path.abspath(yml))

            self.outdir = cfg['OUTDIR']
            self.imdir = os.path.join(self.outdir, 'graph')
            self.logdir = os.path.join(self.outdir, 'log')
            self.html = os.path.join(self.outdir, cfg['HTML'])

            for request in cfg['REQUESTS']:
                self.requests.append(ConfigRequest(request, self.basedir, self.logdir))

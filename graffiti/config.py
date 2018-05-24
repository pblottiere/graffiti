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

    def __init__(self, cfg, basedir):
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
        self.logfile = cfg['LOGFILE']

        self.hosts = []
        for host in cfg['HOSTS']:
            self.hosts.append(ConfigHost(host))


class Config(object):

    def __init__(self, yml):
        self.imdir = None
        self.html = None
        self.svg = True
        self.requests = []
        self.read(yml)

        shutil.rmtree(self.imdir, ignore_errors=True)
        os.makedirs(self.imdir)

    def read(self, yml):
        self.requests = []

        with open(yml, 'r') as stream:
            cfg = yaml.load(stream)

            self.imdir = cfg['IMDIR']
            self.html = cfg['HTML']
            self.svg = cfg['SVG']
            self.basedir = os.path.dirname(yml)

            for request in cfg['REQUESTS']:
                self.requests.append(ConfigRequest(request, self.basedir))

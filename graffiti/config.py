import yaml
import shutil
import os


class ConfigHost(object):

    def __init__(self, cfg):
        self.legend = cfg['LEGEND']
        self.host = cfg['HOST']
        self.project = cfg['PROJECT']
        self.version = cfg['VERSION']


class ConfigHostGetMap(ConfigHost):

    def __init__(self, cfg):
        ConfigHost.__init__(self, cfg)

        self.width = cfg['WIDTH']
        self.height = cfg['HEIGHT']
        self.crs = cfg['CRS']
        self.format = cfg['FORMAT']
        self.layers = ('{},'.format(cfg['LAYERS']))*cfg['DUPLICATE']

class ConfigRequest(object):

    def __init__(self, cfg):
        self.request = cfg['REQUEST']
        self.description = cfg['DESCRIPTION']
        self.iterations = cfg['ITERATIONS']
        self.chart = cfg['CHART']

        self.hosts = []
        for host in cfg['HOSTS']:
            if self.request == 'GetMap':
                self.hosts.append(ConfigHostGetMap(host))
            elif self.request == 'GetCapabilities':
                self.hosts.append(ConfigHost(host))

        if self.request == 'GetCapabilities' \
                or self.request == 'GetMap':
            self.service = 'WMS'


class Config(object):

    def __init__(self, yml):
        self.imdir = None
        self.html = None
        self.svg = True
        self.requests = []
        self.read(yml)

        shutil.rmtree(self.imdir, ignore_errors=True)
        os.makedirs(self.imdir)

        if os.path.isfile(self.html):
            os.remove(self.html)

    def read(self, yml):
        self.requests = []

        with open(yml, 'r') as stream:
            cfg = yaml.load(stream)

            self.imdir = cfg['IMDIR']
            self.html = cfg['HTML']
            self.svg = cfg['SVG']

            for request in cfg['REQUESTS']:
                self.requests.append( ConfigRequest(request) )

import yaml
import shutil
import os


class ConfigHost(object):

    def __init__(self, cfg):
        self.legend = cfg['LEGEND']
        self.host = cfg['HOST']
        self.project = cfg['PROJECT']
        self.version = cfg['VERSION']


class ConfigRequest(object):

    def __init__(self, cfg):
        self.request = cfg['REQUEST']
        self.description = cfg['DESCRIPTION']
        self.iterations = cfg['ITERATIONS']
        self.chart = cfg['CHART']

        self.hosts = []
        for host in cfg['HOSTS']:
            self.hosts.append(ConfigHost(host))

        if self.request == 'GetCapabilities':
            self.service = 'WMS'


class Config(object):

    def __init__(self, yml):
        self.imdir = None
        self.reportdir = None
        self.requests = []
        self.read(yml)

        shutil.rmtree(self.imdir, ignore_errors=True)
        os.makedirs(self.imdir)

    def read(self, yml):
        self.requests = []

        with open(yml, 'r') as stream:
            cfg = yaml.load(stream)

            self.imdir = cfg['IMDIR']
            self.reportdir = cfg['REPORTDIR']

            for request in cfg['REQUESTS']:
                self.requests.append( ConfigRequest(request) )

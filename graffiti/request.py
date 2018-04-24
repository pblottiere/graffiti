import time
from tqdm import trange
import requests


class Payload(object):

    def __init__(self, cfg, host):
        self.payload = {}

        self.payload['MAP'] = host.project
        self.payload['VERSION'] = host.version
        self.payload['REQUEST'] = cfg.request
        self.payload['SERVICE'] = cfg.service

        if cfg.request == 'GetMap':
            self.payload['WIDTH'] = host.width
            self.payload['HEIGHT'] = host.height
            self.payload['CRS'] = host.crs
            self.payload['FORMAT'] = host.format
            self.payload['LAYERS'] = host.layers


class Request(object):

    def __init__(self, cfg):
        self.cfg = cfg
        self.durations = {}

    def run(self):
        for i in trange(len(self.cfg.hosts), leave=False, desc='Hosts'):
            host = self.cfg.hosts[i]
            payload = Payload(self.cfg, host)
            dur = []

            for j in trange(self.cfg.iterations, leave=False, desc='Iterations'):
                start = time.time()
                r = requests.get(host.host, params=payload.payload)

                if r.status_code != 200:
                    print("ERROR")
                    continue

                dur.append(time.time() - start)

            self.durations[host.legend] = dur

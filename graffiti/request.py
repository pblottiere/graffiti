import time
import requests


class Request(object):

    def __init__(self, cfg):
        self.cfg = cfg
        self.durations = {}

    def run(self):
        for host in self.cfg.hosts:
            payload = {}
            payload['MAP'] = host.project
            payload['VERSION'] = host.version
            payload['REQUEST'] = self.cfg.request
            payload['SERVICE'] = self.cfg.service

            dur = []

            for i in range(0, self.cfg.iterations):
                start = time.time()
                r = requests.get(host.host, params=payload)

                if r.status_code != 200:
                    print("ERROR")
                    continue

                dur.append(time.time() - start)

            self.durations[host.legend] = dur

#!/usr/bin/env python

import argparse
import os
from graffiti import (Config,
                      Request,
                      Graph,
                      Report)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Graffiti')
    parser.add_argument('--cfg', type=str, help='YAML configuration file')
    args = parser.parse_args()

    if not args.cfg:
        parser.print_help()
    elif (os.path.isfile(args.cfg)):
        cfg = Config(args.cfg)

        report = Report(svg=cfg.svg)

        for req_cfg in cfg.requests:
            req = Request(req_cfg)
            req.run()

            graph = Graph(req, svg=cfg.svg)
            graph.draw(cfg.imdir)

            report.add(graph)

        report.write(cfg.html)
    else:
        print("Error: '{}' is not a valid configuration file.".format(args.cfg))

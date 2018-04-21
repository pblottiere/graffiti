#!/usr/bin/env python

from graffiti import (Config,
                      Request,
                      Graph,
                      Report)


if __name__ == "__main__":

    cfg = Config('graffiti.yml')
    report = Report(svg=cfg.svg)

    for req_cfg in cfg.requests:
        req = Request(req_cfg)
        req.run()

        graph = Graph(req, svg=cfg.svg)
        graph.draw( cfg.imdir )

        report.add(graph)

    report.write(cfg.html)

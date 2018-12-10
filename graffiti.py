#!/usr/bin/env python

import argparse
import os
import time
import sys
import subprocess
import yaml
import shutil
from tqdm import trange
from graffiti import (Config,
                      Request,
                      Graph,
                      Type,
                      Database,
                      Report)

SPLASH = (''
          '                      _____  _____.__  __  .__\n'
          '   ________________ _/ ____\/ ____\__|/  |_|__|\n'
          '  / ___\_  __ \__  \\\\   __\\\\   __\|  \   __\  |\n'
          ' / /_/  >  | \// __ \|  |   |  |  |  ||  | |  |\n'
          ' \___  /|__|  (____  /__|   |__|  |__||__| |__|\n'
          '/_____/            \/\n\n')


def database(cfg):

    if not cfg.database:
        sys.stdout.write('Cannot open the database!\n')
        sys.exit(1)

    subprocess.run(['sqlite3', Database.path(cfg.database)])
    sys.exit(0)


def scenario(cfg):

    sys.stdout.write(SPLASH)
    report = Report(cfg.date)
    database = Database(cfg.database)

    errors = []
    start = time.time()
    for i in trange(len(cfg.requests), desc='Requests'):
        req = Request.build(cfg.requests[i])
        req.run()
        database.log(req)

        if req.errors:
            errors += req.errors

        graph = Graph(req)
        graph.draw(cfg.imdir)

        report.add(graph)

    report.write(cfg.html, cfg.desc)
    database.close()

    # final log
    dur = round(time.time() - start, 1)
    n = 0
    for req in cfg.requests:
        n += req.iterations * len(req.hosts)

    if errors:
        errlog = os.path.join(cfg.logdir, 'errors.log')
        with open(errlog, 'w') as f:
            for error in errors:
                f.write('--------\n')
                f.write(error.tostr())

        sys.stdout.write('\nTerminated with some errors (see {}) in {} sec'
                         ' for {} requests!\n'
                         .format(errlog, dur, n))
        sys.exit(1)
    else:
        sys.stdout.write('\nTerminated without errors in {} sec for {} '
                         'requests!\n'
                         .format(dur, n))


def summary(cfg):

    config = None
    outdir = None
    imdir = None
    html = None
    with open(cfg, 'r') as stream:
        config = yaml.load(stream)

        outdir = config['OUTDIR']
        shutil.rmtree(outdir, ignore_errors=True)
        os.makedirs(outdir)

        imdir = os.path.join(outdir, 'graph')
        os.makedirs(imdir)

        html = os.path.join(outdir, config['HTML'])

        logdir = os.path.join(outdir, 'log')

    dirname = os.path.dirname(os.path.abspath(cfg))
    report_cfg = Config(os.path.join(dirname, config['CFG']), False)

    if not report_cfg.database:
        sys.stdout.write('Cannot open the database!\n')
        sys.exit(1)

    report = Report(report_cfg.date)

    database = Database(report_cfg.database)
    for request in report_cfg.requests:
        stats = database.stats(request.name)

        if not stats:
            continue

        req = Request.build(request)
        req.durations = stats

        graph = Graph(req)
        graph.draw(imdir)

        report.add(graph)

    report.write(html, report_cfg.desc)
    database.close()

    shutil.copytree(report_cfg.logdir, logdir)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Graffiti')
    parser.add_argument('-c', '--cfg', type=str,
                        help='YAML configuration file')
    parser.add_argument('-d', '--database', action='store_true',
                        help='Open the database')
    parser.add_argument('-s', '--summary', action='store_true',
                        help='Build a summary report based on the database')
    args = parser.parse_args()

    if not args.cfg:
        parser.print_help()
    elif args.summary:
        summary(args.cfg)
    elif (os.path.isfile(args.cfg)):
        cfg = Config(args.cfg)
        if args.database:
            database(cfg)
        else:
            scenario(cfg)
    else:
        sys.stderr.write('Error: \'{}\' is not a valid configuration file.'
                         .format(args.cfg))
        sys.exit(1)

    sys.exit(0)

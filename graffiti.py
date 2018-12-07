#!/usr/bin/env python

import argparse
import os
import time
import sys
import subprocess
from tqdm import trange
from graffiti import (Config,
                      Request,
                      Graph,
                      Database,
                      Report)

SPLASH = (''
          '                      _____  _____.__  __  .__\n'
          '   ________________ _/ ____\/ ____\__|/  |_|__|\n'
          '  / ___\_  __ \__  \\\\   __\\\\   __\|  \   __\  |\n'
          ' / /_/  >  | \// __ \|  |   |  |  |  ||  | |  |\n'
          ' \___  /|__|  (____  /__|   |__|  |__||__| |__|\n'
          '/_____/            \/\n\n')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Graffiti')
    parser.add_argument('-c', '--cfg', type=str, help='YAML configuration file')
    parser.add_argument('-s', '--sqlite', action='store_true', help='Open the database')
    args = parser.parse_args()

    if not args.cfg:
        parser.print_help()
    elif (os.path.isfile(args.cfg)):
        cfg = Config(args.cfg)

        # subcommands
        if args.sqlite:
            if not cfg.database:
                sys.stdout.write('Cannot open the database!\n')
                sys.exit(1)
            subprocess.run(['sqlite3', Database.path(cfg.database)])
            sys.exit(0)

        # scenario
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
    else:
        sys.stderr.write('Error: \'{}\' is not a valid configuration file.'
                         .format(args.cfg))
        sys.exit(1)

    sys.exit(0)

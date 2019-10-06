#!/usr/bin/env python
# coding: utf8

"""
Graffiti, a map server performance reporter.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2019, Paul Blottiere"
__date__ = "2019/06/10"
__email__ = "blottiere.paul@gmail.com"
__license__ = "GPLv3"

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
                      Report,
                      Style)

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
    parser.add_argument('-d', '--db', action='store_true', help='Open the database')
    parser.add_argument('-s', '--style', type=str, help='YAML Style file for histograms')
    args = parser.parse_args()

    if not args.cfg:
        parser.print_help()
    elif (os.path.isfile(args.cfg)):
        cfg = Config(args.cfg, args.style)

        # subcommands
        if args.db:
            if not cfg.database:
                sys.stdout.write('Cannot open the database!\n')
                sys.exit(1)
            subprocess.run(['sqlite3', Database.path(cfg.database)])
            sys.exit(0)

        # scenario
        sys.stdout.write(SPLASH)
        report = Report(cfg.title, cfg.date, cfg.logo, cfg.css)
        database = Database(cfg.database)
        style = Style(cfg.styles)

        errors = []
        start = time.time()
        for i in trange(len(cfg.requests), desc='Requests'):
            req = Request.build(cfg.requests[i])
            req.run()
            database.log(req)

            if req.errors:
                errors += req.errors

            graph = Graph(req, style)
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

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

import os
import yaml
import shutil
import datetime

from .theme import Theme
from .request import Type


class ConfigStyle(object):

    def __init__(self, cfg):
        self.host = cfg['NAME']
        self.color = cfg.get('COLOR', '#000000')
        self.width = cfg.get('WIDTH', 1)
        self.show_dots = cfg.get('SHOW_DOTS', True)
        self.dots_size = cfg.get('DOTS_SIZE', 2)
        self.dasharray = cfg.get('DASHARRAY', '')


class ConfigHost(object):

    def __init__(self, cfg):
        self.name = cfg['NAME']
        self.host = cfg['HOST']
        self.payload = {}

        for key in cfg.keys():
            if 'PAYLOAD_' in key:
                newkey = key.replace('PAYLOAD_', '')
                self.payload[newkey] = cfg[key]


class ConfigDatabase(object):

    def __init__(self, cfg):
        self.host = cfg.get('DB_HOST', '127.0.0.1')
        self.port = cfg.get('DB_PORT', 5432)
        self.name = cfg.get('DB_NAME', '')
        self.user = cfg.get('DB_USER', 'postgres')
        self.password = cfg.get('DB_PASSWORD', '')


class ConfigRequest(object):

    def __init__(self, cfg, basedir, logdir, precision=2, db_config=None):
        self.type = None
        if cfg['TYPE'] == Type.GetCapabilities.name:
            self.type = Type.GetCapabilities
        elif cfg['TYPE'] == Type.GetMap.name:
            self.type = Type.GetMap

        self.title = cfg['TITLE']
        self.description = None
        if cfg['DESCRIPTION']:
            self.description = os.path.join(basedir, cfg['DESCRIPTION'])

        self.jobs = 1
        if 'JOBS' in cfg:
            self.jobs = cfg['JOBS']

        self.iterations = cfg['ITERATIONS']
        self.name = cfg['NAME']
        self.logdir = logdir
        self.precision = precision
        self.provider = cfg.get('PROVIDER')
        self.db_config = db_config

        self.hosts = []
        for host in cfg['HOSTS']:
            self.hosts.append(ConfigHost(host))


class Config(object):

    def __init__(self, yml, yml_style, new=True):
        self.html = None
        self.requests = []
        self.read(yml)

        self.styles = {}
        if yml_style and os.path.isfile(yml_style):
            self.read_style(yml_style)

        datefile = os.path.join(self.outdir, 'date')
        format = '%Y-%m-%d %H:%M:%S'
        if new:
            shutil.rmtree(self.outdir, ignore_errors=True)
            os.makedirs(self.outdir)
            os.makedirs(self.imdir)
            os.makedirs(self.logdir)

            self.date = datetime.datetime.now().strftime(format)
            if self.outdir:
                with open(datefile, 'w+') as log:
                    log.write(self.date)
        else:
            if os.path.isfile(datefile):
                with open(datefile, 'r') as f:
                    self.date = f.read()

    def read(self, yml):
        self.requests = []

        with open(yml, 'r') as stream:
            cfg = yaml.load(stream, Loader=yaml.FullLoader)

            self.title = cfg['TITLE']
            self.precision = cfg['PRECISION']
            self.basedir = os.path.dirname(os.path.abspath(yml))

            if 'LOGO' in cfg:
                self.logo = os.path.join(self.basedir, cfg['LOGO'])

            if 'CSS' in cfg:
                self.css = os.path.join(self.basedir, cfg['CSS'])

            # theme priority over logo/style
            if 'THEME' in cfg:
                theme = Theme(cfg['THEME'])
                self.logo = theme.logo
                self.css = theme.css

            self.db_config = ConfigDatabase(cfg)

            self.outdir = cfg['OUTDIR']
            self.imdir = os.path.join(self.outdir, 'graph')
            self.logdir = os.path.join(self.outdir, 'log')
            self.html = os.path.join(self.outdir, cfg['HTML'])

            for request in cfg['REQUESTS']:
                cfgReq = ConfigRequest(request, self.basedir, self.logdir,
                                       self.precision, self.db_config)
                self.requests.append(cfgReq)

            self.desc = ''
            if cfg['DESCRIPTION']:
                path = os.path.join(self.basedir, cfg['DESCRIPTION'])
                with open(path) as f:
                    self.desc = f.read()

            self.database = None
            if 'DATABASE' in cfg and cfg['DATABASE']:
                self.database = cfg['DATABASE']

    def read_style(self, yml):

        with open(yml, 'r') as stream:
            cfg = yaml.load(stream, Loader=yaml.FullLoader)

            for host in cfg['HOSTS']:
                style = ConfigStyle(host)
                self.styles[style.host] = style

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

import pygal
import os


class Graph(object):

    def __init__(self, req, style, svg=True):
        self.style = style

        self.req = req
        self.imgs = []
        self.svg = svg

    def draw(self, imdir):
        self.draw_temporal(imdir)
        self.draw_box(imdir)

    def draw_box(self, imdir, x_title=None):
        ds = self.req.durations

        graph_x_title = '{} iterations'.format(len(list(ds.values())[0]))
        if x_title:
            graph_x_title = x_title

        box = pygal.Box(x_title=graph_x_title, y_title='Response time in sec',
                        style=self.style.style(ds.keys()), truncate_legend=-1)
        box.title = '{}'.format(self.req.type.name)

        for name in self.req.durations.keys():
            box.add(name, self.req.durations[name])

        img = os.path.join(imdir, '{}_box'.format(self.req.name))

        if self.svg:
            img = '{}.{}'.format(img, 'svg')
            box.render_to_file(img)
        else:
            img = '{}.{}'.format(img, 'png')
            box.render_to_png(img)

        self.imgs.append(os.path.join('graph', os.path.basename(img)))

    def draw_temporal(self, imdir, x_title=None, x_labels=None, x_label_rotation=0):
        ds = self.req.durations
        if len(ds) <= 0:
            return

        graph_x_title = '{} iterations'.format(len(list(ds.values())[0]))
        if x_title:
            graph_x_title = x_title

        line = pygal.Line(x_title=graph_x_title,
                          y_title='Response time in sec',
                          style=self.style.style(ds.keys()),
                          x_label_rotation=x_label_rotation,
                          truncate_legend=-1)
        line.title = '{}'.format(self.req.type.name)

        if x_labels:
            line.x_labels = x_labels

        for name in ds.keys():
            line.add(name, ds[name],
                     stroke_style=self.style.stroke(name),
                     show_dots=self.style.show_dots(name),
                     dots_size=self.style.dots_size(name))

        img = os.path.join(imdir, '{}_temporal'.format(self.req.name))

        if self.svg:
            img = '{}.{}'.format(img, 'svg')
            line.render_to_file(img)
        else:
            img = '{}.{}'.format(img, 'png')
            line.render_to_png(img)

        self.imgs.append(os.path.join('graph', os.path.basename(img)))

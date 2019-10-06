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


class Style(object):

    def __init__(self, styles):
        self.styles = styles

    def style(self, names):
        s = pygal.style.DefaultStyle
        colors = []
        for name in names:
            if name in self.styles.keys():
                colors.append(self.styles[name].color)

        if colors:
            s.colors = tuple(colors)

        return s

    def stroke(self, name):
        style_stroke = None

        if name in self.styles.keys():
            style_stroke = {}
            style = self.styles[name]
            style_stroke['width'] = style.width
            style_stroke['dasharray'] = style.dasharray

        return style_stroke

    def show_dots(self, name):

        show_dots = True

        if name in self.styles.keys():
            show_dots = self.styles[name].show_dots

        return show_dots

    def dots_size(self, name):

        dots_size = 3

        if name in self.styles.keys():
            dots_size = self.styles[name].dots_size

        return dots_size

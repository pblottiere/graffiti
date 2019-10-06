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


class Theme(object):

    def __init__(self, name):
        dirname = os.path.dirname(os.path.abspath(__file__))
        themesdir = os.path.join(dirname, "themes")

        self.logo = os.path.join(themesdir, "default", "graffiti.png")
        self.css = os.path.join(themesdir, "default", "style.css")

        if name.lower() == "qgis":
            self.logo = os.path.join(themesdir, "qgis", "qgis.png")
            self.css = os.path.join(themesdir, "qgis", "style.css")

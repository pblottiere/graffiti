import shutil
import os

from graffiti.request import Request, Type, Host
from graffiti.graph import Graph
from graffiti.style import Style
from graffiti.report import Report

h = Host("master", "http://qgis4.qgis.org:8081/qgisserver_demo/")
h.payload['MAP'] = '/tmp/qgisserver/qgis-server-tutorial-data/world.qgs'
h.payload['VERSION'] = '1.3.0'
h.payload['WIDTH'] = 400
h.payload['HEIGHT'] = 400
h.payload['CRS'] = 'EPSG:4326'
h.payload['LAYERS'] = 'parcelles'
h.payload['FORMAT'] = 'png'
h.payload['BBOX'] = '43.27,3.77,44.70,8.29'

r = Request("master", Type.GetMap, [h], iterations=3, title='My Test', jobs=2, logdir="/tmp/graffiti_example1")
r.run()
r.save('/tmp/graffiti.txt')

imdir = '/tmp/graph'
shutil.rmtree(imdir, ignore_errors=True)
os.makedirs(imdir)

s = Style({})

g = Graph(r, s)
g.draw(imdir)

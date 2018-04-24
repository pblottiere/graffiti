import shutil
import os

from graffiti.request import Request, Type, Host
from graffiti.graph import Graph
from graffiti.report import Report

h = Host("master", "http://37.187.164.233:8080/nightly_master_qgisserver")
h.payload['MAP'] = '/tmp/qgisserver/qgis-server-tutorial-data/world.qgs'
h.payload['VERSION'] = '1.3.0'

r = Request("master", Type.GetCapabilities, [h], iterations=10)
r.run()
r.save('/tmp/graffiti.txt')

imdir = '/tmp/graph'
shutil.rmtree(imdir, ignore_errors=True)
os.makedirs(imdir)

g = Graph(r, svg=False)
g.draw(imdir)

report = Report()
report.add(g)
report.write('/tmp/report.html')

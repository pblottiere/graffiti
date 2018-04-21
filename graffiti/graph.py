import pygal
import os


class Graph(object):

    def __init__(self, req):
        self.req = req

    def draw(self, imdir):
        self.draw_temporal(imdir)

    def draw_temporal(self, imdir):
        line = pygal.Line(x_title='Iterations', y_title='Response time', style=pygal.style.LightGreenStyle)
        line.title = '{}'.format(self.req.cfg.request)

        for host in self.req.cfg.hosts:
            line.add(host.legend, self.req.durations[host.legend])

        line.render_to_png( os.path.join(imdir, '{}_temporal.png'.format(self.req.cfg.chart)) )

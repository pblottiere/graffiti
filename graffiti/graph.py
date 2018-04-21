import pygal
import os


class Graph(object):

    def __init__(self, req):
        self.req = req
        self.imgs = []

    def draw(self, imdir):
        self.draw_temporal(imdir)
        self.draw_box(imdir)

    def draw_box(self, imdir):
        box = pygal.Box(style=pygal.style.LightGreenStyle)
        box.title = '{}'.format(self.req.cfg.request)

        for host in self.req.cfg.hosts:
            box.add(host.legend, self.req.durations[host.legend])

        img = os.path.join(imdir, '{}_box.png'.format(self.req.cfg.chart))
        box.render_to_png( img )
        self.imgs.append(img)

    def draw_temporal(self, imdir):
        line = pygal.Line(x_title='Iterations', y_title='Response time', style=pygal.style.LightGreenStyle)
        line.title = '{}'.format(self.req.cfg.request)

        for host in self.req.cfg.hosts:
            line.add(host.legend, self.req.durations[host.legend])

        img = os.path.join(imdir, '{}_temporal.png'.format(self.req.cfg.chart))
        line.render_to_png( img )
        self.imgs.append(img)

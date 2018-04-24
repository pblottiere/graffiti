import pygal
import os

STYLE=pygal.style.DefaultStyle


class Graph(object):

    def __init__(self, req, svg=True):
        self.req = req
        self.imgs = []
        self.svg = svg

    def draw(self, imdir):
        self.draw_temporal(imdir)
        self.draw_box(imdir)

    def draw_box(self, imdir):
        box = pygal.Box(style=STYLE)
        box.title = '{}'.format(self.req.cfg.request)

        for host in self.req.cfg.hosts:
            box.add(host.legend, self.req.durations[host.legend])

        img = os.path.join(imdir, '{}_box'.format(self.req.cfg.chart))

        if self.svg:
            img = '{}.{}'.format(img, 'svg')
            box.render_to_file(img)
        else:
            img = '{}.{}'.format(img, 'png')
            box.render_to_png(img)

        self.imgs.append(img)

    def draw_temporal(self, imdir):
        line = pygal.Line(x_title='Iterations', y_title='Response time', style=STYLE)
        line.title = '{}'.format(self.req.cfg.request)

        for host in self.req.cfg.hosts:
            line.add(host.legend, self.req.durations[host.legend])

        img = os.path.join(imdir, '{}_temporal'.format(self.req.cfg.chart))

        if self.svg:
            img = '{}.{}'.format(img, 'svg')
            line.render_to_file(img)
        else:
            img = '{}.{}'.format(img, 'png')
            line.render_to_png(img)

        self.imgs.append(img)

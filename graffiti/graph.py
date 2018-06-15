import pygal
import os

STYLE = pygal.style.DefaultStyle


class Graph(object):

    def __init__(self, req, svg=True):
        self.req = req
        self.imgs = []
        self.svg = svg

    def draw(self, imdir):
        self.draw_temporal(imdir)
        self.draw_box(imdir)

    def draw_box(self, imdir):
        ds = self.req.durations
        title = '{} iterations'.format(len(list(ds.values())[0]))
        box = pygal.Box(x_title=title, y_title='Response time in sec',
                        style=STYLE)
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

    def draw_temporal(self, imdir):
        ds = self.req.durations
        if len(ds) <= 0:
            return

        title = '{} iterations'.format(len(list(ds.values())[0]))
        line = pygal.Line(x_title=title, y_title='Response time in sec',
                          style=STYLE)
        line.title = '{}'.format(self.req.type.name)

        for name in ds.keys():
            line.add(name, ds[name])

        img = os.path.join(imdir, '{}_temporal'.format(self.req.name))

        if self.svg:
            img = '{}.{}'.format(img, 'svg')
            line.render_to_file(img)
        else:
            img = '{}.{}'.format(img, 'png')
            line.render_to_png(img)

        self.imgs.append(os.path.join('graph', os.path.basename(img)))

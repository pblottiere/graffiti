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

    def draw_box(self, imdir, x_title=None):
        ds = self.req.durations

        graph_x_title = '{} iterations'.format(len(list(ds.values())[0]))
        if x_title:
            graph_x_title = x_title

        box = pygal.Box(x_title=graph_x_title, y_title='Response time in sec',
                        style=STYLE, truncate_legend=-1)
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

        line = pygal.Line(x_title=graph_x_title, y_title='Response time in sec',
                          style=STYLE, x_label_rotation=x_label_rotation,
                          truncate_legend=-1)
        line.title = '{}'.format(self.req.type.name)

        if x_labels:
            line.x_labels = x_labels

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

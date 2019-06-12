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

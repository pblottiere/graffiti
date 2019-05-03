import fileinput
import shutil
import os
import uuid


class ReportTOCLeaf(object):

    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4().hex

    def tostr(self, href=True):
        h = ''
        if href:
            h = 'href="#{}"'.format(self.id)
        return '<li><a {}>{}</a>'.format(h, self.name)


class ReportTOCNode(object):

    def __init__(self, name):
        self.me = ReportTOCLeaf(name)
        self.leafs = []

    def tostr(self):
        leafs = ''
        for leaf in self.leafs:
            leafs += leaf.tostr()

        s = ('{}'
             '<ul>'
             '{}'
             '</ul>').format(self.me.tostr(False), leafs)
        return s


class ReportTOC(object):

    def __init__(self):
        self.nodes = {}

    def tostr(self):
        leaf = ''
        for n in self.nodes.values():
            leaf += n.tostr()

        s = ('<div id="toc_container">'
             '<ul class="toc_list">'
             '{}'
             '</ul>'
             '</div>'.format(leaf))

        return s


class Report(object):

    def __init__(self, title, date, logo):
        self.date = date
        self.title = title
        self.logo = logo
        self.charts = ''
        self.toc = ReportTOC()

    def write(self, html, desc=''):
        if os.path.isfile(html):
            os.remove(html)

        dirname = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(dirname, 'template.html')
        shutil.copyfile(src, html)

        shutil.copyfile(self.logo, os.path.join(os.path.dirname(html), 'logo.png'))

        src = os.path.join(dirname, 'style.css')
        shutil.copyfile(src, os.path.join(os.path.dirname(html), 'style.css'))

        with fileinput.FileInput(html, inplace=True) as file:
            for line in file:
                tag_title = '{{GRAFFITI_TITLE}}'
                if tag_title in line:
                    print(line.replace(tag_title, self.title), end='')
                    continue

                tag_date = '{{GRAFFITI_DATE}}'
                if tag_date in line:
                    print(line.replace(tag_date, self.date), end='')
                    continue

                tag_charts = '{{GRAFFITI_CHARTS}}'
                if tag_charts in line:
                    print(line.replace(tag_charts, self.charts), end='')
                    continue

                tag_desc = '{{GRAFFITI_DESCRIPTION}}'
                if tag_desc in line:
                    print(line.replace(tag_desc, desc), end='')
                    continue

                tag_toc = '{{GRAFFITI_TOC}}'
                if tag_toc in line:
                    print(line.replace(tag_toc, self.toc.tostr()), end='')
                    continue

                print(line)

    def add(self, graph):
        desc = ''
        if graph.req.desc:
            with open(graph.req.desc) as f:
                desc = f.read()

            if desc:
                desc = ('<h3>Description</h3>\n'
                        '{}\n'
                        .format(desc))

        name = graph.req.type.name
        if name not in self.toc.nodes.keys():
            node = ReportTOCNode(name)
            self.toc.nodes[name] = node

        leaf = ReportTOCLeaf(graph.req.title)
        self.toc.nodes[name].leafs.append(leaf)

        chart = ('<h2 id="{}">{}: {}</h2>\n'
                 '{}\n'
                 '<h3>Results</h3>').format(leaf.id, name, graph.req.title, desc)

        chart += '<div class="row" align="center">'
        tag = ''
        for img in graph.imgs:
            tag += ('<div class="column" style="width:49%">'
                    '<figure>'
                    '<embed type="image/svg+xml" width=100% src="./{}" align="center"/>'
                    '</figure>'
                    '</div>'
                    .format(img))

        chart += tag
        chart += '</div>'

        self.charts += chart

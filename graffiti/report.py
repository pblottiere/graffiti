import fileinput
import shutil
import base64
import os
import datetime


class Report(object):

    def __init__(self):
        self.charts = ''

    def write(self, html):
        if os.path.isfile(html):
            os.remove(html)

        dirname = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(dirname, 'template.html')
        shutil.copyfile(src, html)

        with fileinput.FileInput(html, inplace=True) as file:
            for line in file:
                tag_date = '{{GRAFFITI_DATE}}'

                if tag_date in line:
                    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(line.replace(tag_date, date), end='')
                    continue

                tag_charts = '{{GRAFFITI_CHARTS}}'
                if tag_charts in line:
                    print(line.replace(tag_charts, self.charts), end='')
                    continue

                print(line)

    def add(self, graph):
        if graph.svg:
            self.add_svg(graph)
        else:
            self.add_png(graph)

    def add_png(self, graph):
        chart = ('<hr>\n'
                 '<h2><a>{}</a></h2>\n'
                 '{}\n'
                 '<br/><br/>\n').format(graph.req.title, graph.req.short_desc)

        for img in graph.imgs:
            i = base64.b64encode(open(img, 'rb').read()).decode('utf-8')
            tag = ('<img src="data:image/png;base64,{}" align="center"/>\n'
                   .format(i))
            chart += tag

        self.charts += chart

    def add_svg(self, graph):
        long_desc = ''
        with open(graph.req.long_desc) as f:
            long_desc = f.read()

        chart = ('<hr>\n'
                 '<h2><a>{}</a></h2>\n'
                 '{}\n'
                 '<br/><br/>\n'
                 '{}\n'
                 '<br/><br/>\n').format(graph.req.title, graph.req.short_desc,
                                        long_desc)

        chart += '<figure\n>'
        tag = ''
        for img in graph.imgs:
            tag += ('&emsp;&emsp;&emsp;'
                    '<embed type="image/svg+xml" width=800px src="./{}" '
                    'align="center"/>'
                    .format(img))

        chart += tag
        chart += '</figure>\n'

        self.charts += chart

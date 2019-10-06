<img align="left" width="80" height="80" src="https://raw.githubusercontent.com/pblottiere/graffiti/master/graffiti/themes/default/graffiti.png">

# Graffiti

Graffiti is a simple tool allowing to:
- measure map servers performance (QGIS Server, ...)
- generate CSV files with response times for a later use
- generate a HTML report with interactive SVG graphs (response time and
  statistics) as well as resulting images

A report example is available [here](https://rawgit.com/pblottiere/graffiti/master/examples/html/report.html).

For now, only `GetCapabilities` and `GetMap` requests for WMS services are
supported.

## Install

For now, `graffiti` is not on PyPI so:

````
$ git clone https://github.com/pblottiere/graffiti
$ cd graffiti
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
(venv)$ pip install -e .
````

## Usage

#### Configuration

Mainly, the YAML configuration file allows to describe:
- `i` requests to execute
- `j` hosts per request
- `k` iterations per host (for statistics)

This way, there're finally `i x j x k` requests sent by graffiti.

A  fully commented configuration file `graffiti.yml`:

``` YAML
OUTDIR: /tmp/graffiti/  # output directory
HTML: report.html  # the name of the report generated in OUTDIR
DESCRIPTION: description.html  # main description (included in the report)
PRECISION: 2  # number of digits for response times
REQUESTS:  # your test scenario may contains several tests
  - NAME: test_getcapabilities  # unique name of the first test (internal usage)
    TYPE: GetCapabilities  # type of request
    TITLE: "My GetCapabilities Test"  # title of the test to use in the report
    DESCRIPTION: getcapabilities.html  # test description (include in the report)
    LOG: True  # to generate CSV, resulting images, ...
    ITERATIONS: 5  # the number of times the requests will be sent to the host
    HOSTS:  # the current test may be run against several hosts
      - NAME: "QGIS Server 2.18" # the name of the second host
        HOST: http://myurl/qgisserver_2_18  # the URL
        PAYLOAD_MAP: /tmp/myproject.qgs  # MAP parameter
        PAYLOAD_VERSION: 1.3.0  # VERSION parameter
        PAYLOAD_XXX: XXX  # any parameter you want
      - NAME: "QGIS Server 3.0"  # the name of the first host
        HOST: http://myurl/qgisserver_3_0  # the URL
        PAYLOAD_MAP: /tmp/myproject.qgs  # MAP parameter
        PAYLOAD_VERSION: 1.3.0  # VERSION parameter
        PAYLOAD_XXX: XXX  # any parameter you want
  - NAME: test_getmap  # unique name of the second test (internal usage)
    TYPE: GetMap # type of request
    TITLE: "My GetMap Test"  # title of the test to use in the report
    DESCRIPTION: getmap.html  # test description (include in the report)
    LOG: True  # to generate CSV, resulting images, ...
    ITERATIONS: 50  # the number of times the requests will be sent to the host
    HOSTS:  # the current test may be run against several hosts
      - NAME: "QGIS Server 2.18" # the name of the second host
        HOST: http://myurl/qgisserver_2_18  # the URL
        PAYLOAD_MAP: /tmp/myproject.qgs  # MAP parameter
        PAYLOAD_VERSION: 1.3.0  # VERSION parameter
        PAYLOAD_LAYERS: countries  # LAYERS parameter
        PAYLOAD_FORMAT: png  # any parameter you want
        PAYLOAD_XXX: XXX  # any parameter you want
      - NAME: "QGIS Server Master"  # the name of the first host
        HOST: http://.../qgisserver_3_0  # the URL
        PAYLOAD_MAP: /tmp/myproject.qgs  # MAP parameter
        PAYLOAD_VERSION: 1.3.0  # VERSION parameter
        PAYLOAD_LAYERS: countries  # LAYERS parameter
        PAYLOAD_FORMAT: png  # any parameter you want
        PAYLOAD_XXX: XXX  # any parameter you want
```

In this case, we only have one test per kind of request, but you may write as
much as you want (while the `NAME` parameter of the request is unique).

Regarding HTML description files, they have to be in the same location than
the configuration file. Note that if `LOG` parameter is true for `GetMap`
requests, then the resulting image is stored for the first iteration in the
`OUTDIR/log` directory for each host. This way, you may include some of these
images in the description.

#### Run

To run graffiti with a specific configuration file, you just have to use the
`graffiti.py` script with the `--cfg` option.

This way, with the provided configuration file, you can observe the progress:

```
(venv)$ ./graffiti.py --cfg conf/graffiti.sample.yml
                     _____  _____.__  __  .__
   ________________ _/ ____\/ ____\__|/  |_|__|
  / ___\_  __ \__  \\   __\\   __\|  \   __\  |
 / /_/  >  | \// __ \|  |   |  |  |  ||  | |  |
 \___  /|__|  (____  /__|   |__|  |__||__| |__|
/_____/            \/

Requests:  50%|█████████████████████████████████| 1/2 [00:02<00:02,  2.33s/it]
Hosts: 0%|                                      | 0/2 [00:00<?, ?it/s]
Iterations: 4%|█████▋                           | 1/25 [00:01<00:30,  1.25s/it]
```

#### Results

HTML report, SVG graphs and logs are generated in the output directory
`OUTDIR`:

```
(venv)$ ls /tmp/graffiti
graph  log  report.html  style.css
```

#### Style

Each series may be independently customised thanks to a dedicated YAML style
file. For example, you can update the color for a specific host or configure
the stroke style:

```
HOSTS:
    - NAME: "QGIS Server 2.18"  # As specified in the main configuration file
      COLOR: "#AEBD38"
      WIDTH: 4
      SHOW_DOTS: TRUE
      DOTS_SIZE: 10
      DASHARRAY: "3, 6"
```

Then you can use the `--style` option:

```
(venv)$ ./graffiti.py --cfg conf/graffiti.sample.yml --style conf/style.yml
```

#### Database

Numeric results are stored in a SQLite database as soon as the `DATABASE` entry
is added to the main configuration file. For exemple in
`conf/graffiti.sample.yml`:

```
DATABASE: graffiti.db
```

In this case, the SQLite database `graffiti.db` is available in
`~/.local/share/graffiti/`. Note that you can use the `--db` action to
automatically open the SQLite prompt and explore statistics thanks to SQL
requests:

```
(venv)$ ./graffiti.py --cfg conf/graffiti.sample.yml --db
SQLite version 3.27.2 2019-02-25 16:06:06
Enter ".help" for usage hints.
sqlite> .tables
durations
sqlite> .schema durations
CREATE TABLE durations (request text, host text, date text, min real, mean real, max real);
sqlite> SELECT AVG(mean) FROM durations WHERE host="Master 0" LIMIT 50;
4.31962790697674
```

#### Data provider monitoring

If your map server is serving some data coming from a database provider, you
may monitor the underlying time spent outside of QGIS Server itself and add
this time on graphs. Considering that graffiti has to run specific requests
directly in the database to collect statistics, database access details have to
be indicated in the main configuration file:

```
DB_HOST: localhost
DB_PORT: 55432
DB_NAME: data
DB_USER: root
DB_PASSWORD: root
```

Then, you have to add the provider type for each host you want to monitor:

```
    PROVIDER: POSTGRES
```

Not that for now, it's only implemented for PostgreSQL.

#### Help

Quick reminder:

```
(venv)$ ./graffiti.py --help
usage: graffiti.py [-h] [-c CFG] [-d] [-s STYLE]

Graffiti

optional arguments:
  -h, --help            show this help message and exit
  -c CFG, --cfg CFG     YAML configuration file
  -d, --db              Open the database
  -s STYLE, --style STYLE
                        YAML Style file
```

## API

Instead of using the `graffiti.py` Python script, you can use the graffiti API
(work in progress). For example:

``` Python
import shutil
import os

from graffiti.request import Request, Type, Host
from graffiti.graph import Graph
from graffiti.report import Report

h = Host("master", "http://myurl/qgisserver")
h.payload['MAP'] = '/tmp/myproject.qgs'
h.payload['VERSION'] = '1.3.0'

r = Request("master", Type.GetCapabilities, [h], iterations=10, title='My Test')
r.run()

imdir = '/tmp/graph'
shutil.rmtree(imdir, ignore_errors=True)
os.makedirs(imdir)

g = Graph(r)
g.draw(imdir)

report = Report()
report.add(g)
report.write('/tmp/report.html')
```

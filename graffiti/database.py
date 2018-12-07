import os
import datetime
import sqlite3


class Database(object):

    def __init__(self, name):
        sharedir = os.path.expanduser('~') + os.sep + '.local' \
            + os.sep + 'share' + os.sep + 'graffiti'
        if not os.path.exists(sharedir):
            os.makedirs(sharedir)

        self.table = 'durations'
        self.filename = None
        self.con = None
        if name:
            self.filename = os.path.join(sharedir, name)
            self.con = sqlite3.connect(self.filename)

            self.__init()

    def log(self, request):
        if not self.con:
            return False

        name = request.name
        date = datetime.datetime.now()

        for host in request.hosts:
            durations = request.durations[host.name]
            max_duration = max(durations)
            min_duration = min(durations)
            avg_duration = sum(durations)/len(durations)

            self.__store(name, host.name, date, min_duration, avg_duration,
                         max_duration)

    def close(self):
        if self.con:
            self.con.close()

    def __store(self, request, host, date, min_dur, avg_dur, max_dur):
        sql = ('INSERT INTO {table} values(\'{request}\', \'{host}\', '
               '\'{date}\', {min_dur}, {avg_dur}, {max_dur})'
               .format(table=self.table, request=request, host=host,
                       date=date, min_dur=min_dur, avg_dur=avg_dur,
                       max_dur=max_dur))
        self.__commit(sql)

    def __init(self):
        sql = ('SELECT name FROM sqlite_master WHERE type=\'table\' AND'
               ' name=\'{table_name}\''
               .format(table_name=self.table))

        cur = self.con.cursor()
        cur.execute(sql)

        if not cur.fetchone():
            sql = ('CREATE TABLE {table_name} (request text, host text, '
                   'date text, min real, mean real, max real)'
                   .format(table_name=self.table))
            self.__commit(sql)

    def __commit(self, sql):
        cur = self.con.cursor()
        cur.execute(sql)
        self.con.commit()

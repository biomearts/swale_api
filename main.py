#!/usr/bin/env python3

import os, sys, json
from housepy import config, log, server, util, process, strings

process.secure_pid(os.path.abspath(os.path.join(os.path.dirname(__file__), "run")))

class Home(server.Handler):

    def get(self, start=None, end=None, type_=None):
        self.set_header("Access-Control-Allow-Origin", "*")
        if len(start) and len(end) and len(type_):
            try:
                start = util.parse_date(start, tz="America/New_York")
                start_t = util.timestamp(start)
                end = util.parse_date(end, tz="America/New_York")
                end_t = util.timestamp(end)
                results = self.db.entries.find({'t_utc': {'$gt': start_t, '$lt': end_t}, 'type': type_})
                data = {'query': {'start': start, 'end': end, 'type': type_}}
                data['results'] = list(results)
                return self.json(data)
            except Exception as e:
                log.error(log.exc(e))
                return self.error("Request malformed: %s" % e)        
        return self.render("index.html")

handlers = [
    (r"/?([^/]*)/?([^/]*)/?([^/]*)", Home),
]    

server.start(handlers)

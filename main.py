#!/usr/bin/env python3

import os, sys, json, markdown
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
        readme = "README failed to load"
        try:
            with open("README.md") as f:
                text = f.read()
                readme = markdown.markdown(text)
        except Exception as e:
            log.error(log.exc(e))
        return self.render("index.html", readme=readme)

    def post(self, nop=None, nop2=None, nop3=None):
        log.info("POST")
        try:
            data = json.loads(str(self.request.body, encoding='utf-8'))
            log.info(data)
            log.info(type(data))
        except Exception as e:
            log.error(log.exc(e))
            return self.error()
        for key in data.keys():
            if type(key) is not str:
                del data[key]
            fixed_key = strings.slugify(strings.depunctuate(key, "_"))
            if key != fixed_key:
                data[fixed_key] = data[key]
                del data[key]
        log.info(json.dumps(data, indent=4))
        try:
            entry_id = self.db.entries.insert_one(data).inserted_id
        except Exception as e:
            log.error(log.exc(e))
            return self.error("ERROR: %s" % e)
        return self.text(str(entry_id))
  


handlers = [
    (r"/?([^/]*)/?([^/]*)/?([^/]*)", Home),
]    

server.start(handlers)

#!/usr/bin/env python3

import os, sys, json, markdown, actions
from housepy import config, log, server, util, process, strings

process.secure_pid(os.path.abspath(os.path.join(os.path.dirname(__file__), "run")))

class Home(server.Handler):

    def get(self, type_=None, start=None, end=None, nop=None):
        self.set_header("Access-Control-Allow-Origin", "*")
        if len(type_):
            if not len(start):
                start = "*"
            if not len(end):
                end = "*"
            try:
                filters = {key: strings.as_numeric(value[0]) for (key, value) in self.request.arguments.items()}
                results, start_t, end_t = actions.retrieve(self.db, type_, start, end, filters)
                data = {'query': {'types': type_, 'start': util.datestring(start_t, tz=config['tz']), 'end': util.datestring(end_t, tz=config['tz']), 'filters': filters}}
                # log.info(data)
                data['results'] = results
                data['count'] = len(results)
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

    def post(self, nop=None, nop2=None, nop3=None, nop4=None):
        log.info("POST")
        self.set_header("Access-Control-Allow-Origin", "*")                        
        try:
            data = json.loads(str(self.request.body, encoding='utf-8'))
        except Exception as e:
            log.error(log.exc(e))
            return self.error()
        try:
            entry_id = actions.insert(self.db, data)
        except Exception as e:
            log.error(log.exc(e))
            return self.error("ERROR: %s" % e)
        return self.text(str(entry_id))
  


handlers = [
    (r"/?([^/]*)/?([^/]*)/?([^/]*)/?", Home),
]    

server.start(handlers)

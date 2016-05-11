#!/usr/bin/env python3

import os, sys, json, markdown, actions
from housepy import config, log, server, util, process, strings

process.secure_pid(os.path.abspath(os.path.join(os.path.dirname(__file__), "run")))

class Home(server.Handler):

    def get(self, start=None, end=None, type_=None):
        self.set_header("Access-Control-Allow-Origin", "*")
        if len(start) and len(end) and len(type_):
            try:
                result = actions.retrieve(self.db, start, end, type_)
                data = {'query': {'start': start, 'end': end, 'type': type_}} # field, # output
                log.info(data)
                data['results'] = results
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
        self.set_header("Access-Control-Allow-Origin", "*")                        
        try:
            data = json.loads(str(self.request.body, encoding='utf-8'))
            log.info(data)
            log.info(type(data))
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
    (r"/?([^/]*)/?([^/]*)/?([^/]*)", Home),
]    

server.start(handlers)

#!/usr/bin/env python3

from housepy import config, log
from mongo import db

db.entries.remove()
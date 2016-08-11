import json, sys
from housepy import util, strings, config, log

"""
These functions should not be web specific so that they can be importable.

"""

def insert(db, data):
    for key in data.keys():
        if type(key) is not str:
            del data[key]
            continue
        clean_key = clean(key)
        if key != clean_key:
            data[clean_key] = data[key]
            del data[key]
            key = clean_key
        data[key] = strings.as_numeric(data[key])
    if 't_utc' not in data:
        data['t_utc'] = util.timestamp()
    data['date'] = util.datestring(data['t_utc'], tz=config['tz'])
    log.info(json.dumps(data, indent=4))
    entry_id = db.entries.insert_one(data).inserted_id
    return entry_id

def retrieve(db, source, start, end, filters, page=None):
    if filters == None:
        filters = {}
    sources = [clean(source) for source in source.split(",")]    
    start_t = 0 if start == "*" else util.timestamp(util.parse_date(start, tz=config['tz']))
    end_t = min(2147483647, sys.maxsize) if end == "*" else util.timestamp(util.parse_date(end, tz=config['tz']))
    template = {'t_utc': {'$gt': start_t, '$lt': end_t}, '$or': [{'source': source} for source in sources]}
    template.update(filters)
    log.info("QUERY %s" % template)    
    results = db.entries.find(template).sort('t_utc')
    count = results.count()
    if page is None:
        page = (count // 100) + 1
    skip = (page - 1) * 100
    log.debug('skip %s' % skip)
    results = results.skip(skip).limit(100)    
    log.info("--> done")
    return list(results), start_t, end_t, count, page

def clean(s):
    return strings.slugify(strings.depunctuate(s, "_"))

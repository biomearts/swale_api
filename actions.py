import json
from housepy import util, strings, config, log

def insert(db, data):
    for key in data.keys():
        if type(key) is not str:
            del data[key]
        fixed_key = strings.slugify(strings.depunctuate(key, "_"))
        if key != fixed_key:
            data[fixed_key] = data[key]
            del data[key]
    if 't_utc' not in data:
        data['t_utc'] = util.timestamp()
    log.info(json.dumps(data, indent=4))
    entry_id = db.entries.insert_one(data).inserted_id
    return entry_id

def retrieve(db, start, end, type_):
    start = util.parse_date(start, tz=config['tz'])
    start_t = util.timestamp(start)
    end = util.parse_date(end, tz=config['tz'])
    end_t = util.timestamp(end)
    results = db.entries.find({'t_utc': {'$gt': start_t, '$lt': end_t}, 'type': type_}).sort('t_utc')
    return list(results)


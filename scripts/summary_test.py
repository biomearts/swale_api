#!/usr/bin/env python3

import json, math
import numpy as np
from cli import results
import signal_processing as sp
from housepy import config, log

# print(json.dumps(results, indent=4, default=lambda obj: str(obj)))

interval = 3600
# interval = 200

fields = {}
for result in results:
    for field, value in result.items():
        if field == "_id" or field == "t_utc" or field == "date" or field == "type":
            continue
        if field not in fields:
            fields[field] = [], []
        fields[field][0].append(result['t_utc'])
        fields[field][1].append(value)


for field, (ts, values) in fields.items():

    # separate by interval
    splits = []
    i, j = 0, 1
    while i < len(ts):
        while ts[j] - ts[i] < interval:
            j += 1
            if j == len(ts):
                break
        splits.append((ts[i:j], values[i:j]))
        i = j

    # create signals
    # we do this to essentially weight the averages by time
    out_ts = []    
    for s, (ts, values) in enumerate(splits):
        if len(values) > 1:
            signal = sp.resample(ts, values)    
            splits[s] = np.mean(signal)
        else:
            splits[s] = values[0]
        out_ts.append(ts[0])

    fields[field] = out_ts, splits

# print(json.dumps(fields, indent=4))

output = {}
for field, (ts, data) in fields.items():
    for i, t in enumerate(ts):
        if not t in output:
            output[t] = {}
        output[t].update({field: data[i]})
# print(json.dumps(output, indent=4))

final = [dict(data, t_utc=t, interval=interval) for (t, data) in output.items()]
final.sort(key=lambda d: d['t_utc'])

print(json.dumps(final, indent=4))
print("--> done")


"""

one issue is that if a particular property doesnt occur in an interval, it's not there.
I guess that makes sense.
do we need to preserve "types" or something?

bigger problem is what if the data type isnt averageable? ie, strings / booleans?

how to propagate date?

"""
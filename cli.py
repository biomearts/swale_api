#!/usr/bin/env python3

import argparse, json
import actions
from mongo import db
from housepy import config, log

"""
This is equivalent to the web interface, but if you import it into your script, you can recall the data

"""

parser = argparse.ArgumentParser(description="Retrieve a signal")
parser.add_argument("-t", "--source",  type=str, nargs=1, required=True)
parser.add_argument("-s", "--start", type=str, nargs=1, required=True)
parser.add_argument("-e", "--end", type=str, nargs=1, required=True)
parser.add_argument("-f", "--field",  type=str, nargs="?")
parser.add_argument("-o", "--output",  type=str, nargs="?")
args = vars(parser.parse_args())
args = {key: value[0] if (value is not None) else None for (key, value) in args.items()}
# print(args)



results, start_t, end_t, count, page = actions.retrieve(db, args['source'], args['start'], args['end'], None)


## this is unnecessary
# if args['output'] == "json":
#     print(json.dumps(result, indent=4, default=lambda obj: str(obj)))
# elif args['output'] == "stream":
#     pass
# # png
# # spectrograph
# # audio
# # autocorrelation


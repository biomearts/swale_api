# Swale API

## GET data
`/[start]/[end]/[type]/[output?]/?[field]=[value]`

`start` and `end` are any date format in `America/New_York` timezone. Can be `*` for open ended.
`type` is the primary type, may be a comma-separated list 
`output` is the desired output format, optional (not implemented -- always json)
`field` is a filter by the `value` of some other parameter (not implemented)

(put type first, then start and end, then a resolution zoom)

## POST data

### Required:
- `type`: what's the name of this data type?


### Optional:
- `t_utc` -- timestamp in `UTC`. If not included, the server supplies it (with microseconds)
- anything else

### Note:
- all field names will be automatically stripped of punctuation, spaces replaced with underscores, and lowercased
- any nested types are dropped. Must be a flat hierarchy.
- `t_utc` is `UTC` even though queries are in `America/New_York`


## Command-line interface

Put your scripts in the "scripts" folder and do the following: `from cli import results`

This will run a argument parser identical to the web interface ahead of your script and return a `results` object.    


## Context

Conceptually, this is like the temporal-only version of the Okavango field kit. ie, it's not GeoJSON, doesn't care about location.



### Copyright/License

Copyright (c) 2016 Brian House

This program is free software licensed under the GNU General Public License, and you are welcome to redistribute it under certain conditions. It comes without any warranty whatsoever. See the LICENSE file for details, or see <http://www.gnu.org/licenses/> if it is missing.

Projects that use this software must credit Brian House and link to http://brianhouse.net
# Swale API

## GET data
`/[start]/[end]/[type]/[field?]/[output?]`

`start` and `end` are any date format in `America/New_York` timezone  
`type` is specified in the data  
`field` is a filter by some other parameter (not implemented)
`output` is the desired output format (not implemented -- always json)


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


# Swale API

## GET data
/[start]/[end]/[type1]/[type2]/...

[start] and [end] are any date format in America/New_York timezone

## POST data

### Required:
- type: what's the name of this data type?


### Optional:
- t_utc -- timestamp in UTC. If not included, the server supplies it (with microseconds)
- anything else

### Note:
- all field names will be automatically stripped of punctuation, spaces replaced with underscores, and lowercased
- any nested types are dropped. Must be a flat hierarchy.
- t_utc is UTC even though queries are in America/New_York
# Swale API

## GET data
/[start]/[end]/[type1]/[type2]/...


## POST data

### Required:
- type: what's the name of this data type?


### Optional:
- t_utc -- timestamp in UTC. If not included, the server supplies it (with microseconds)
- anything else

### NOTE:
- all field names will be automatically stripped of punctuation, spaces replaced with underscores, and lowercased
- any nested types are dropped. Must be a flat hierarchy.
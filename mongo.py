#!/usr/bin/env python3

from housepy import config, log
from pymongo import MongoClient, GEOSPHERE, ASCENDING, DESCENDING

mongo = config['mongo']
client = MongoClient(mongo['host'], mongo['port'])
db = client[mongo['database']]

def make_indexes():
  try:
      db.features.create_index("properties.Expedition")
      db.features.create_index("properties.FeatureType")
      db.features.create_index("properties.Member")
      db.features.create_index([("properties.t_utc", ASCENDING)])
      db.features.create_index([("properties.t_utc", DESCENDING)])
      db.features.create_index("properties.EstimatedGeometry")
      db.features.create_index("properties.Satellite")
      db.features.create_index("properties.SpeciesName")
      db.features.create_index([("properties.SpeciesName", "text")])
      db.features.create_index("properties.CoreExpedition")
      db.features.create_index("properties.Team")
      db.features.create_index([("geometry", GEOSPHERE)])
      db.members.create_index("Name")
      db.members.create_index("t_utc")
      db.members.create_index("Core")
      db.members.create_index("Team")
  except Exception as e:
      log.error(log.exc(e))

if __name__ == "__main__":
  make_indexes()

"""

# embedded field
db.people.createIndex( { "address.zipcode": 1 } )

# multi field (sort order matters)
db.products.createIndex( { "item": 1, "stock": 1 } )

http://docs.mongodb.org/manual/core/index-compound/
http://docs.mongodb.org/manual/core/index-intersection/

what's the advantage of compound indexes over single indexes?
seems to be little, in this case

indexes
- expedition
- t_utc
- coordinates


"""
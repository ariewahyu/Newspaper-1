import pymongo

try:
    conn=pymongo.MongoClient()
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: {}".format(e)

db = conn.NewsTheHinduDB
s_coll = db.stories

def add_story(story):
    """Story has to be a dict"""
    s_coll.insert(story)

def num_total_stories():
    return len(list(s_coll.find()))

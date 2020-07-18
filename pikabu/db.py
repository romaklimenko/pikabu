import os
from pymongo import MongoClient

client = MongoClient(os.environ['MONGO'])
db = client['dirty']
urls_collection = db['pikabu']

def can_publish(url):
  return urls_collection.count_documents({ '_id': url }) == 0

def save(url):
  urls_collection.insert_one({
    '_id': url
  })

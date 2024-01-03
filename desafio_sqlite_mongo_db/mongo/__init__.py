from os import environ

import pymongo
from dotenv import load_dotenv

load_dotenv()

client = pymongo.MongoClient(
    'mongodb+srv://pymongo:pymongo@cluster1.f9asews.mongodb.net/?retryWrites=true&w=majority'
)

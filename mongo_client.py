from pymongo import MongoClient

MONGO_HOST = "mongodb"
MONGO_PORT = "27017"
MONGO_DB = "database"
MONGO_USER = "admin"
MONGO_PASS = "S3cret"

uri = "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT, MONGO_DB)
client = MongoClient(uri)

db = client["pokemon"]

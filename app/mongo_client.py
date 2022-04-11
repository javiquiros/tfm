from pymongo import MongoClient

MONGO_HOST = "mongodb"
MONGO_PORT = "27017"
MONGO_DB = "database"
MONGO_USER = "admin"
MONGO_PASS = "S3cret"

uri = "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT, MONGO_DB)
client = MongoClient(uri)

mongo_db = client["pokemon"]

pokemon = mongo_db.pokemon.find_one({"_id": 1})


def count_documents():
    return mongo_db.pokemon.count_documents({})


def list_documents():
    return mongo_db.pokemon.find().sort("_id").limit(5)


def populate_results(results):
    for result in results:
        pokemon = mongo_db.pokemon.find_one({"_id": int(result["id"])})
        result["name"] = pokemon["name"]
    return results

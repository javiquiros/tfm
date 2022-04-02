from app.mongo_client import db
from app.pokemon import pokedex


pokemon_coll = db.pokemon

count = 0
for pokemon in pokemon_coll.find({}):

    # set a new _id on the document
    old_id = pokemon["_id"]

    pokemon["_id"] = int(pokemon["_id"])

    try:
        pokemon_id = pokemon_coll.insert_one(pokemon).inserted_id
        pokemon_coll.delete_one({"_id": old_id})
    except:
        print(f"{old_id} already exists")

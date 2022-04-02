import time

from app.mongo_client import db
from app.pokemon import pokedex


pokemon_coll = db.pokemon

pokemon_counts = pokedex.get_pokemon_counts()

# for i in range(1, pokemon_counts["total"] + 1):
for i in range(1, 102):
    pokemon = pokedex.get_pokemon_by_number(i)[0]
    pokemon["_id"] = int(pokemon["number"])

    print(f'Recopilado pokemon {pokemon["number"]} - {pokemon["name"]}')
    pokemon_id = pokemon_coll.insert_one(pokemon).inserted_id

    time.sleep(3)  # Para evitar lanzar demasiadas peticiones y recibir un error 429 too many requests

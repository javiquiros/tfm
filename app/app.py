from flask import Flask, render_template

from app.elastic_client import ElasticClient
from app.mongo_client import mongo_db
from app.pokemon import pokedex

app = Flask(__name__,
            static_url_path="",
            static_folder='static',
            template_folder='templates')

es_client = ElasticClient()


@app.route("/")
def index():
    pokemon_in_db = mongo_db.pokemon.count_documents({})
    pokemon_in_elastic = es_client.count_documents()
    indexed_images_percentage = round((pokemon_in_elastic / pokemon_in_db) * 100, 2)
    return render_template('dashboard.html', title='Pokemon collection',
                           pokemon_in_db=pokemon_in_db,
                           pokemon_in_elastic=pokemon_in_elastic,
                           indexed_images_percentage=indexed_images_percentage)


@app.route("/pokemon/list")
def pokemon():
    return render_template('pokemon_table.html', title='Pokemon collection',
                           pokemon_coll=mongo_db.pokemon.find().sort("_id").limit(5))


if __name__ == '__main__':
    app.run()

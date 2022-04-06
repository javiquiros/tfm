from flask import Flask, jsonify, render_template, request
from threading import Thread


from app.elastic_client import ElasticClient
from app.mongo_client import mongo_db
from app.pokemon import pokedex
from app.tasks import indexing_task

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


# Ajax requests
@app.route('/count_indexed_images')
def count_indexed_images():
    return jsonify(count=es_client.count_documents())


@app.route('/index_images')
def index_images():
    thread = Thread(target=indexing_task)
    thread.daemon = True
    thread.start()
    return jsonify({'thread_name': str(thread.name),
                    'started': True})


@app.route('/delete_index')
def delete_index():
    es_client.delete_index()
    return jsonify({'ok'})


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template

from app.mongo_client import db
from app.pokemon import pokedex

app = Flask(__name__,
            static_url_path="",
            static_folder='static',
            template_folder='templates')


@app.route("/")
def index():
    return render_template('dashboard.html', title='Pokemon collection')


@app.route("/pokemon/list")
def pokemon():
    return render_template('pokemon_table.html', title='Pokemon collection',
                           pokemon_coll=db.pokemon.find().sort("_id").limit(5))


if __name__ == '__main__':
    app.run()

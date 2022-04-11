import os
import time
from threading import Thread

from flask import Flask, flash, jsonify, render_template, redirect, request
from PIL import Image
from werkzeug.utils import secure_filename

from app import mongo_client
from app.elastic_client import ElasticClient
from app.tasks import image_to_vector, indexing_task

UPLOAD_FOLDER = 'app/static/uploads/'

app = Flask(__name__,
            static_url_path="",
            static_folder='static',
            template_folder='templates')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

es_client = ElasticClient()


@app.route("/")
def index():
    pokemon_in_db = mongo_client.count_documents()
    pokemon_in_elastic = es_client.count_documents()
    indexed_images_percentage = round((pokemon_in_elastic / pokemon_in_db) * 100, 2)
    return render_template('dashboard.html', title='Pokemon collection',
                           pokemon_in_db=pokemon_in_db,
                           pokemon_in_elastic=pokemon_in_elastic,
                           indexed_images_percentage=indexed_images_percentage)


@app.route("/pokemon/list")
def pokemon():
    return render_template('pokemon_table.html', title='Pokemon collection',
                           pokemon_coll=mongo_client.list_documents())


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
    return jsonify({"status": "ok"})


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/search_image', methods=['POST'])
def search_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if not file or not allowed_file(file.filename):
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print('upload_image filename: ' + filename)
    flash('Image successfully uploaded and displayed below')
    image = Image.open(os.path.join("app", "static", "uploads", filename))
    print("Empieza conversión")
    start_time = time.time()
    features = image_to_vector(image)
    mid_time = time.time()
    print(f"Conversión imagen: {mid_time - start_time}")
    results = es_client.search_image(features.tolist())
    print(f"Búsqueda en elastic: {time.time() - mid_time}")
    fetched_pokemon = mongo_client.populate_results(results)
    return jsonify(fetched_pokemon)


if __name__ == '__main__':
    app.run()

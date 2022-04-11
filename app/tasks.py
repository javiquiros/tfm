import json
import os
import time

import numpy as np
from PIL import Image
from tensorflow.keras.applications.efficientnet import EfficientNetB2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input

from app.elastic_client import ElasticClient
from app.mongo_client import mongo_db

es_client = ElasticClient()


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def indexing_task():
    print("start")
    start = time.time()
    es_client.create_index()
    path = os.path.join("app", "static", "images")
    files = os.listdir(path)
    count = 0
    for file in files:
        image = Image.open(os.path.join(path, file))
        filename = os.path.splitext(file)[0]
        print(filename)

        # If already exists, skip
        if es_client.get_document_by_id(filename):
            continue
        image = image.convert('RGBA')
        features = image_to_vector(image)
        doc = {
            "id": filename,
            "image_vector": features.tolist()
        }
        es_client.index_document(doc)
        count += 1
        print(count)
    print(f"Execution time: {time.time() - start}")


def image_to_vector(img: np.ndarray) -> np.ndarray:
    model = EfficientNetB2(weights='imagenet')
    input_shape = 260

    img = img.resize((input_shape, input_shape))
    img = img.convert('RGB')
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)[0]
    return preds / np.linalg.norm(preds)


def populate_db_task():
    mongo_db.pokemon.drop()
    print("Pokemon collection deleted")

    with open('dump_db/pokemon.json') as f:
        file_data = json.load(f)

    mongo_db.pokemon.insert_many(file_data)
    print("Database restored")

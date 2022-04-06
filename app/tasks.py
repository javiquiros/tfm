import os
from PIL import Image

from app.elastic_client import ElasticClient
from app.image_processor import ImageProcessor
from app.mongo_client import mongo_db

es_client = ElasticClient()
image_processor = ImageProcessor()


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def indexing_task():
    path = os.path.join(root_dir(), "static", "images")
    files = os.listdir(path)
    for file in files:
        image = Image.open(os.path.join(path, file))
        features = image_processor.extract_features(image)
        doc = {
            "id": os.path.splitext(file)[0],
            "vector": features
        }
        es_client.index_document(doc)

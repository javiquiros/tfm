from elasticsearch import BadRequestError, Elasticsearch, NotFoundError


class ElasticClient:
    def __init__(self):
        self.host = "http://elasticsearch:9200"
        self.index = "pokemon"
        self.user = "elastic"
        self.password = "secret"
        self.es = Elasticsearch(self.host, http_auth=(self.user, self.password))

    def create_index(self):
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index, body=self.mapping())
            print(f"Index {self.index} created")

    def mapping(self):
        return {
            "mappings": {
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "image_vector": {
                        "type": "dense_vector",
                        "dims": 1000
                    }
                }
            }
        }

    def index_document(self, doc):
        id = doc["id"]
        # try:
        resp = self.es.index(index=self.index, id=id, body=doc)
        self.es.indices.refresh(index=self.index)
        return resp['result']
        # except BadRequestError:
        #     return False

    def get_document_by_id(self, id):
        try:
            resp = self.es.get(index=self.index, id=id)
            return resp['_source']
        except NotFoundError:
            return False

    def get_all(self):
        resp = self.es.search(index=self.index, query={"match_all": {}})
        return resp['hits']['hits']

    def count_documents(self):
        try:
            self.es.indices.refresh(index=self.index)
        except NotFoundError:
            return 0
        return self.es.count(index=self.index)["count"]

    def delete_index(self):
        try:
            self.es.indices.delete(index=self.index)
            print(f"Index {self.index} deleted")
        except NotFoundError:
            pass

    def search_image(self, query_vector, size=4):
        search_body = {
            "size": size,
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'image_vector') + 1.0",
                        "params": {
                            "query_vector": query_vector
                        }
                    }
                }
            }
        }
        res = self.es.search(index=self.index, body=search_body)
        return [{"id": hit["_id"], "score": hit["_score"]} for hit in res["hits"]["hits"]]

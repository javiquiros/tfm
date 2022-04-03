from elasticsearch import Elasticsearch


class ElasticClient:
    def __init__(self):
        self.host = "http://localhost:9200"
        self.index = "pokemon"
        self.user = "elastic"
        self.password = "secret"
        self.es = Elasticsearch(self.host, http_auth=(self.user, self.password))

    def index_document(self, doc):
        resp = self.es.index(index=self.index, id=doc["id"], document=doc)
        self.es.indices.refresh(index=self.index)
        return resp['result']

    def get_document_by_id(self, id):
        resp = self.es.get(index=self.index, id=id)
        return resp['_source']

    def get_all(self):
        resp = self.es.search(index=self.index, query={"match_all": {}})
        return resp['hits']['hits']

    def delete_index(self):
        self.es.indices.delete(index=self.index)

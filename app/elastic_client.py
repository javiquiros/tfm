from elasticsearch import BadRequestError, Elasticsearch, NotFoundError


class ElasticClient:
    def __init__(self):
        self.host = "http://elasticsearch:9200"
        self.index = "pokemon"
        self.user = "elastic"
        self.password = "secret"
        self.es = Elasticsearch(self.host, http_auth=(self.user, self.password))

    def index_document(self, doc):
        if "id" not in doc.keys():
            doc["id"] = doc["_id"]
        doc.pop("_id")
        try:
            resp = self.es.index(index=self.index, id=doc["id"], document=doc)
            self.es.indices.refresh(index=self.index)
            return resp['result']
        except BadRequestError:
            return False
        

    def get_document_by_id(self, id):
        resp = self.es.get(index=self.index, id=id)
        return resp['_source']

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
        except NotFoundError:
            pass

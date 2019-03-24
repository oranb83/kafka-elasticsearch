import logging

from elasticsearch import Elasticsearch, exceptions

logger = logging.Logger(__name__)


class Elastic(object):
    def __init__(self):
        self.es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

    def store_record(self, record, index_name='test'):
        try:
            self.es.index(index=index_name, doc_type='object', body=record)
        except Exception as ex:
            logging.error('Error in indexing data %s', str(ex))

    def search_record(self, search, index_name='test'):
        search_object = {'query': {'match': {'message': search}}}
        try:
            objects = self.es.search(index=index_name, body=search_object)
            return [obj['_source'] for obj in objects['hits']['hits']]
        except exceptions.NotFoundError as ex:
            logger.error('Error in indexing data %s', str(ex))

        return []

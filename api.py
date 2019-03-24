import os
from json import dumps

from flask import Flask, abort, request

from kafka.producer import Producer
from kafka.consumer import Consumer
from elastic.elasticsearch import Elastic

PRODUCER = Producer()
CONSUMER = Consumer()
ELASTIC_SEARCH = Elastic()
CONTENT_TYPE_TEXT = 'text/plain'
DEBUG = os.getenv('DEBUG', False)
app = Flask(__name__)


@app.route('/health')
def hello():
    return 'Strong like a bull!'


@app.route('/message', methods=['POST'])
def post_message():
    if request.content_type != CONTENT_TYPE_TEXT:
        abort(400)

    PRODUCER.send(request.data.decode('utf-8'))
    messages = CONSUMER.get()
    if not messages:
        abort(400)

    for msg in messages:
        ELASTIC_SEARCH.store_record(msg)

    return 'created', 201


@app.route('/message/<msg>')
def get_messages(msg):
    if not msg:
        abort(400)

    results = dumps(ELASTIC_SEARCH.search_record(msg), indent=4)
    status_code = 200
    if not results:
        status_code = 404

    return results, status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG, threaded=True)

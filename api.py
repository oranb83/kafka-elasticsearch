import os
from json import dumps

from flask import Flask, abort, request

from elastic.elasticsearch import Elastic
from controler import Controler

ELASTIC_SEARCH = Elastic()
CONTENT_TYPE_TEXT = 'text/plain'
DEBUG = os.getenv('DEBUG', False)
API_VERSION = 'v1'

app = Flask(__name__)


@app.route('/health')
def hello():
    return 'Strong like a bull!'


@app.route(f'/{API_VERSION}/words/count/', methods=['POST'])
def post_message():
    if request.content_type != CONTENT_TYPE_TEXT:
        abort(400)

    text = request.data.decode('utf-8')
    if not text:
        abort(500)

    print(Controler(text).count_words())

    # for msg in text:
    #     ELASTIC_SEARCH.store_record(msg)

    return 'created', 201


# @app.route(f'/{API_VERSION}/words/stats/?words=foo,bar,hello,worlds')
# def get_messages(msg):
#     if not msg:
#         abort(400)

#     results = dumps(ELASTIC_SEARCH.search_record(msg), indent=4)
#     status_code = 200
#     if not results:
#         status_code = 404

#     return results, status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG, threaded=True)

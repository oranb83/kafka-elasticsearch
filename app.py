import os

from flask import Flask, abort, request

from controler import ControlerPost, ControlerSearch

CONTENT_TYPE_TEXT = 'text/plain'
SEARCH = 'search'
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

    ControlerPost(text).count_words()

    return 'created', 201


@app.route(f'/{API_VERSION}/words/stats/')
def get_messages():
    search = request.args.get(SEARCH)

    if not search:
        abort(400)

    results = ControlerSearch(search).get_stats()

    return str(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG, threaded=True)

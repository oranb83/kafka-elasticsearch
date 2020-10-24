import os
from threading import Thread

from flask import Flask, abort, request

from controler import Controler

CONTENT_TYPE_TEXT = 'text/plain'
DEBUG = os.getenv('DEBUG', False)
API_VERSION = 'v1'

app = Flask(__name__)

@app.route('/')
@app.route('/health/')
def health():
    return 'Strong like a bull!'


@app.route(f'/{API_VERSION}/words/count/', methods=['POST'])
def post_text():
    if request.content_type != CONTENT_TYPE_TEXT:
        abort(400)

    text = request.data.decode('utf-8')
    if not text:
        abort(500)

    # Assumption: this operation can be long (depands on the input), so we will run it on a
    # different thread in the background.
    thread = Thread(target=Controler(text).count_words())
    thread.daemon = True
    thread.start()

    # Assumption: I would normally run another process in the background and send back HTTP 202
    # accepted, but I assumed the user needs to be aware that the operation is completed so he can
    # safely run the stats query.
    return 'created', 201


@app.route(f'/{API_VERSION}/words/<word>/stats/')
def get_word(word):
    if not word:
        abort(400)

    results = Controler.get_stats(word)

    return str(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG, threaded=True)

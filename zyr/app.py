from flask import Flask, jsonify, request, Response, stream_with_context
import os
import logging
import requests

app = Flask(__name__)

hosttorequest = os.environ['HOST']

logging.basicConfig(
    format='%(asctime)-15s %(levelname)s %(message)s',
    level = logging.INFO
    )

app.logger.handlers = []

@app.route('/')
def root():
    req = requests.get('http://'+hosttorequest+'/', stream = True)
    assert req.status_code == 200, req['error']
    return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])

@app.route('/<path:other>')
def other(other):
    req = requests.get('http://'+hosttorequest+'/'+other, stream = True)
    assert req.status_code == 200, req['error']
    return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])

@app.after_request
def log_request(response):
    app.logger.info("[%s] %s %s" % (response.status_code, request.method, request.url))
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5199, debug = True)

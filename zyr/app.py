#from flask import Flask, jsonify, request, Response, stream_with_context
import os
import logging
import requests
from sanic import Sanic
from sanic.response import json, redirect, html, stream

#app = Flask(__name__)
app = Sanic()

hosttorequest = os.environ['HOST']

# logging.basicConfig(
#     format='%(asctime)-15s %(levelname)s %(message)s',
#     level = logging.INFO
#     )
#
# app.logger.handlers = []


@app.route('/')
async def root(request):
    req = requests.get('https://'+hosttorequest+'/', stream = True)
    async def sample_streaming_fn(response):
        response.write(await req.iter_content())
    print(req.headers['content-type'])
    return stream(sample_streaming_fn,content_type = req.headers['content-type'])

    #return stream(req.iter_content(), content_type = req.headers['content-type'])
    #assert req.status_code == 200, req['error']
    #return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])

@app.route('/<path:other>')
async def other(request, other):
    req = requests.get('https://'+hosttorequest+'/'+other, stream = True)
    async def sample_streaming_fn(response):
        print(req.iter_content())
        yield response.write(req.iter_content())

    return stream(sample_streaming_fn,content_type = req.headers['content-type'])
    #return stream(req.iter_content(), content_type = req.headers['content-type'])
    #assert req.status_code == 200, req['error']
    #return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])

# @app.after_request
# def log_request(response):
#     app.logger.info("[%s] %s %s" % (response.status_code, request.method, request.url))
#     return response
#
# @app.errorhandler(AssertionError)
# def handle_assertion(error):
#     response = jsonify(error=error.message)
#     response.status_code = 400
#     return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5199, debug = True)

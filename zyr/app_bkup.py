import requests
from sanic import Sanic
from sanic.response import json, redirect, html, stream

app = Sanic()
CHUNK_SIZE = 1024

@app.route("/public/hc")
async def healthcheck(request):
    return json({"works": "ok"})

def get_source_rsp(url, request):
        url = 'http://%s' % url
        # LOG.info("Fetching %s", url)
        # # Ensure the URL is approved, else abort
        # if not is_approved(url):
        #     LOG.warn("URL is not approved: %s", url)
        #     abort(403)
        # Pass original Referer for subsequent resource requests
        # proxy_ref = proxy_ref_info(request)
        # headers = { "Referer" : "http://%s/%s" % (proxy_ref[0], proxy_ref[1])} if proxy_ref else {}
        # # Fetch the URL, and stream it back
        # LOG.info("Fetching with headers: %s, %s", url, headers)
        return requests.get(url, stream=True , params = request.args)#, headers=headers)


@app.route("/public/proxy")
async def proxy(request):
    """Fetches the specified URL and streams it out to the client.
    If the request was referred by the proxy itself (e.g. this is an image fetch for
    a previously proxied HTML page), then the original Referer is passed."""
    url = 'https://google.com'
    r = get_source_rsp(url, request)
    #LOG.info("Got %s response from %s",r.status_code, url)
    headers = dict(r.headers)
    def generate():
        for chunk in r.iter_content(CHUNK_SIZE):
            yield chunk
    return stream(requests.get(url, stream=True), content_type='text/plain')
#    return Response(generate(), headers = headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, workers=2)

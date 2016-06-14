#!/usr/bin/env python

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    res = processRequest(req)

    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def get_jsonparsed_data(url):
    request = urllib2.request(url)
    response = urllib2.urlopen(request)
    data = response.read()
    return json.loads(data)

def processRequest(req):
    if req.get("result").get("action") != "apiaitest":
        return {}

    res = makeWebhookResult(req)
    return res

def makeWebhookResult(req):
    result = req.get("result")
    parameters = result.get("parameters")
    language = parameters.get("programming")

    url = "http://admin-api.qvcdev.qvc.net/api/sales/presentation/v3/us/products/A274786?response-depth=items"
    data = get_jsonparsed_data(url)

    if (language == "python"):
        speech = "You snake!"
    else:
        speech = "How about no " + language + " " + data.get('productNumber')

    return {
        "speech": speech,
        "displayText": speech,
        # "data": {"slack": speech},
        # "data": {"facebook": speech},
        "source": "apiai-weather-webhook-test"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    app.run(debug=False, port=port, host='0.0.0.0')

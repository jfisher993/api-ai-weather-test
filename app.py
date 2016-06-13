#!/usr/bin/env python

import urllib.request
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


url = "http://admin-api.qvcdev.qvc.net/api/sales/presentation/v3/us/products/A274786?response-depth=items"
response = urllib.request.urlopen(url).read()
data = json.loads(response.decode('utf-8'))


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    res = processRequest(req)

    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "apiaitest":
        return {}

    res = makeWebhookResult(req)
    return res

def makeWebhookResult(req):
    result = req.get("result")
    parameters = result.get("parameters")
    language = parameters.get("programming")

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

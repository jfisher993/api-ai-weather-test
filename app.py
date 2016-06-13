#!/usr/bin/env python

import urllib
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

    url = "http://admin-api.qvcdev.qvc.net/api/sales/presentation/v3/us/products/A274786?response-depth=items"
    response = urllib.urlopen(url).read()
    data = json.loads(response)

    res = processRequest(req, data)

    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req, data):
    if req.get("result").get("action") != "apiaitest":
        return {}

    res = makeWebhookResult(req, data)
    return res

def makeWebhookResult(req, data):
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

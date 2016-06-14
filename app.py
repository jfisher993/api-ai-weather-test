#!/usr/bin/env python
import urllib.request
import json
import os

#print(json.dumps(data, indent=4))

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

def processRequest(req):
    if req.get("result").get("action") != "searchQVC":
        return {}

    res = makeWebhookResult(req)
    return res

def get_jsonparsed_data(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    return json.loads(data.decode('utf-8'))

def makeWebhookResult(req):
    result = req.get("result")
    parameters = result.get("parameters")
    countryCode = parameters.get("countryCode")
    productNumber = parameters.get("productNumer")

    url = 'https://api.qvc.com/api/sales/presentation/v3/' + countryCode + '/products/' + productNumber + '?response-depth=full'
    data = get_jsonparsed_data(url)

    speech = data.get('productNumber') + "\n" + "Brand Name: " + data.get('brandName') + "\n" + data.get('shortDescription')

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

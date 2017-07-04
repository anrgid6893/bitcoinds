#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import requests


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    if req.get("result").get("action") != "bitcoinprice":
        return {}
    
    r = requests.get("https://api.korbit.co.kr/v1/ticker")
    data = r.json()
    #baseurl = "https://blockchain.info/de/ticker"
    #result = urlopen(baseurl).read()
    #data = json.loads(result)
    #res = data["USD"]["last"]
    #r = makeWebhookResult(res)
    
    r = makeWebhookResult(data)

    return r


def makeWebhookResult(data):
    speech = "Now bit coin currency is " + data.get('last') + "!"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        # "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

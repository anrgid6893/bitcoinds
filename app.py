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

    if req.get("result").get("action") == "KorbitBitcoin":
        parameters = req.get("result").get("parameters")
        currency_symbol = parameters.get("currency-name")

        baseurl = "https://blockchain.info/de/ticker"
        result = urllib.urlopen(baseurl).read()
        data = json.loads(result)

        query = data.get(currency_symbol)

        speech = "Bitcoin exchange rates:"

        slack_message = {
            "text": speech,
            "attachments": [
                {
                    "title": "Bitcoin",
                    "title_link": "https://markets.blockchain.info",
                    "color": "#36a64f",

                    "fields": [
                        {
                            "title": "Last",
                            "value": str(query.get('last')) + " " + query.get('symbol'),
                            "short": "false"
                        },
                        {
                            "title": "Buy",
                            "value": str(query.get('buy')) + " " + query.get('symbol'),
                            "short": "false"
                        },
                        {
                            "title": "Sell",
                            "value": str(query.get('sell')) + " " + query.get('symbol'),
                            "short": "false"
                        }
                    ],

                    "thumb_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/440px-Bitcoin.svg.png"
                }
            ]
        }

        res = {
            "speech": speech,
            "displayText": speech,
            "data": {"slack": slack_message},
            "source": "apiai-bitcoin-webhook"
        }

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

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

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)

    print("\nResponse:")
    print(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    reply = "Processing, please wait..."
    # custom reply per client (fb messenger, etc.)
    fb_text = {
        "text": "this is a text message before an image:"
    }
    fb_image = {
        "attachment": {
            "type":"image",
            "payload":{
                "url":"https://placeholdit.imgix.net/~text?txtsize=23&bg=ffffff&txtclr=000000&txt=250%C3%97250&w=250&h=250"
            }
        }
    }
    data = {"facebook": [fb_text, fb_image]}
    return {
        "speech": reply,
        "displayText": reply,
        "data": data,
        "contextOut": [],
        "source": "webhook"
    }

def sendMsgToBot(msg):
    #TODO send a msg directly to the bot (in client format or api.ai format?)
    print("TODO")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

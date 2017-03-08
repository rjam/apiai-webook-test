#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from threading import Timer

import json
import os
import urllib2

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

    # simulate async work by scheduling an event to be fired after 8 seconds
    # handling the response and forwarding it to FB's integration app

    #TODO we'll need to store the session id from this request and pass it onto the event!
    t = Timer(5.0, triggerEvent)
    t.start()

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

def triggerEvent():
    event = {
    "event":
        {
            "name": "my-event",
            "data":
            {
                "text": "example custom event text"
            }
        },
    "lang": "en",
    "sessionId":"3e82039b-d2ba-485e-95af-b86cdc3d50e0",
    "timezone":"America/New_York"
    }

    url = "https://api.api.ai/api/query?v=20160910";
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer e9d2ad4aeba44c068483009befa3d83b'
    }

    req = urllib2.Request(url, json.dumps(event), headers)
    response = urllib2.urlopen(req)
    result = response.read()

    print(result)

    #TODO do we need to inject the "sender" into this response?

    # forward response to client integration app (fb, slack, etc)
    bot_url = "https://api-ai-fb-bot.herokuapp.com/api_ai_response"
    bot_headers = {'Content-Type': 'application/json'}
    bot_req = urllib2.Request(bot_url, result, bot_headers)
    bot_response = urllib2.urlopen(bot_req)
    bot_result = bot_response.read()
    print(bot_result)

def sendMsgToBot(msg):
    #TODO send a msg directly to the bot (in api.ai format)
    print("TODO")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

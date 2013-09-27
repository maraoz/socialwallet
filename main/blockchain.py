"""
Blockchain.info Python Client for the JSON Merchant API for Google App Engine.
Manuel Araoz - 2012
"""

from google.appengine.api import urlfetch
import logging
import json

TX_FEES = 10000
B2S = 100000000 

BLOCKCHAIN_WALLET_GUID = ""
BLOCKCHAIN_PASSWORD = ""
CALLBACK_SECRET = ""
                                                                     
                                             
# debugging
class Mock():
    status_code = 500
def mock(url):
    print url
    return Mock()

# uncomment to debug
# urlfetch.fetch = mock

def btc2satoshi(x):
    return int(x * B2S)

def satoshi2btc(x):
    return x / float(B2S)


BASE_COINBASE_URL = "https://blockchain.info"
def get_base_blockchain_url(command):
    return BASE_COINBASE_URL + "/merchant/%s/%s?password=%s" % (BLOCKCHAIN_WALLET_GUID, command, BLOCKCHAIN_PASSWORD) 

def new_address():
    url = get_base_blockchain_url("new_address")
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        j = json.loads(result.content)
        print j
        return j["address"]
    else:
        logging.error('There was an error contacting the Blockchain.info API')
        return None

def address_balance(addr):
    url = BASE_COINBASE_URL+"/address/%s?format=json&limit=0" % addr
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        return json.loads(result.content)["final_balance"]
    else:
        logging.error('There was an error contacting the Blockchain.info API')
        return None

def payment(to, satoshis, _from):
    url = get_base_blockchain_url("payment")
    url += "&to=%s&amount=%s&from=%s&shared=%s&fee=%s" % (to, satoshis, _from, "false", TX_FEES)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        return json.loads(result.content).get("tx_hash")
    else:
        logging.error('There was an error contacting the Blockchain.info API')
        return None

def sendmany(_from, recipient_list):
    url = get_base_blockchain_url("sendmany")
    # can't do it using python dict because we have repeated addresses
    recipients = "{"
    for addr, satoshis in recipient_list:
        recipients += '"%s":%s,' % (addr, satoshis)
    recipients = recipients[:-1]
    recipients += "}"
    url += "&from=%s&recipients=%s&shared=%s&fee=%s" % (_from, recipients, "false", TX_FEES)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        return json.loads(result.content).get("tx_hash")
    else:
        logging.error('There was an error contacting the Blockchain.info API')
        return None

def get_tx(tx_hash):
    url = BASE_COINBASE_URL+"/rawtx/%s" % (tx_hash)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        return json.loads(result.content)
    else:
        logging.error('There was an error contacting the Blockchain.info API')
        return None
def get_block(height):
    if not height:
        return None
    url = BASE_COINBASE_URL+"/block-height/%s?format=json" % (height)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        return json.loads(result.content).get("blocks")[0]
    else:
        logging.error('There was an error contacting the Blockchain.info API')
        return None
def callback_secret_valid(secret):
    return secret == CALLBACK_SECRET

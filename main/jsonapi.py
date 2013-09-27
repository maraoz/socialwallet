#!/usr/bin/env python


import webapp2, json,


class JsonAPIHandler(webapp2.RequestHandler):
    def post(self):
        self.get()
    def get(self):
        resp = self.handle()
        self.response.write(json.dumps(resp))

class BootstrapHandler(JsonAPIHandler):
    def handle(self):
        return {"success":True}
    
class RegisterHandler(JsonAPIHandler):
    def handle(self):
        username = self.request.get("username")
        password = self.request.get("password")
        
        if not username or not password:
            return {"success":False , "reason" :"Username and password can't be empty"}
        
        
        
        return {"success":True}


class CallbackHandler(JsonAPIHandler):
    
    def process_tx(self, tx):
        return None
    
    def handle(self):
        secret = self.request.get("secret")
        if not callback_secret_valid(secret):
            return "error: secret"
        test = self.request.get("test") == "true"
        try:
            value = long(self.request.get("value"))
            confirmations = int(self.request.get("confirmations"))
            tx = self.request.get("transaction_hash")
        except ValueError, e:
            return "error: value error"
        
        if confirmations < 1:
            return "error: unconfirmed"
        
        if not test:
            result = self.process_tx(tx)
            if not result:
                return "error: process"
        return "*ok*"

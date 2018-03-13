import requests
from requests.auth import HTTPBasicAuth
import logging
import os

logging.basicConfig(level=logging.DEBUG)

class Client:
    def __init__(self,baseURL,appAPIkey):
        self.baseURL = baseURL
        self.appAPIkey = appAPIkey
        #self.appID = os.environ.get('ROOT_APP_ID')
        #self.appSecret = os.environ.get('ROOT_APP_SECRET')
        #self.applications = Applications(self)
        #self.claims = Claims(self)
        #self.policyholders = PolicyHolders(self)
        #self.policies = Policies(self)
        self.gadgets = Gadgets(self)
        #self.quotes = Quotes(self)

    def call(self, method, path, params=None, **kwargs):
        print(self.appAPIkey)
        resp = requests.request(method, f'{self.baseURL}/{path}', params=params, headers={"Content-Type": "application/json"}, auth=HTTPBasicAuth(self.appAPIkey, ''), **kwargs)
        if resp.status_code == 200 or resp.status_code == 201:
            return resp.json()
        raise Exception(resp.status_code, resp.json())


class Resource:
    def __init__(self, client):
        self.client = client
    
    def call(self, method, path, params=None, **kwargs):
        return self.client.call(method, path, params, **kwargs)


class Quotes(Resource):
    def __init__(self, client):
         super().__init__(client)

    def create(self, opts):
        data = {}
        type_ = opts["type"]
        if type_ == "root_gadgets":
            data = self._gadget_quote(opts)
        elif type_ == "root_term":
            data = self._term_quote(opts)
        elif type_ == "root_funeral":
            data = self._funeral_quote(opts)
        else:
            raise Exception("invalid quote type")
        return self.call("post", "quotes", json=data)

    def _gadget_quote(self, opts):
        return {
            "type": "root_gadgets",
            "model_name": opts["model_name"]
            }

class Gadgets(Resource):
    def __init__(self, client):
         super().__init__(client)

    def list_models(self):
        return self.call("get", "gadgets/models")

    def list_phone_brands(self):
        models = self.list_models()
        return set([phone['make'] for phone in models])

    def list_phones_by_brand(self, brand):
        models = self.list_models()
        return set([phone['name'] for phone in models if phone['make'] == brand])

    def get_phone_value(self, phone):
        models = self.list_models()
        return list(filter(lambda p: p['name'] == phone, models))[0]['value']/100

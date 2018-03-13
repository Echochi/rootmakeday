from flask import Flask,Response,request,render_template
from root_insurance import Client
import os
import json

app = Flask(__name__)

type = "root_gadgets"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    try:
        request.get_data()
        output = {'speech': 'hello',
            'displayText': 'world'}
        print('output', request.json.get('result').get('parameters').get('phone_model'))
    except:
        output = "hello world"
    return Response(json.dumps(output), mimetype=u'application/json') 

@app.route('/quote', methods=['GET','POST'])
def quote():
    #model_name = "Galaxy S8 64GB LTE"

    request.get_data()
    model_name = request.json.get('result').get('parameters').get('phone_model')
    print(model_name)
    
    baseURL = "https://sandbox.root.co.za/v1/insurance"
    appAPIkey = "sandbox_NjY2YWZiNWItZjAxMS00ODY4LTg2NjktZjUwYzY0ZTUzYThmLlJub1ZRcHRxRktndEpMdng0VG0wYTRaX1c4dUxYb2hU"
    client = Client(baseURL,appAPIkey)
    value = (client.gadgets.get_phone_value(model_name))/100
    value = "Your quote is R" + str(value)
    output = {'speech': value,
            'displayText': value}
    
    return Response(json.dumps(output), mimetype=u'application/json')  

if __name__ == '__main__':
    app.run()
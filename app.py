import os

from flask import Flask, render_template, request
import requests as req
import hashlib
import json
from urllib.parse import urlparse, quote
from urllib import parse
from utils import *
from config import *

app = Flask(__name__)
# REQ_URL = "http://rubl_backend:8000"
REQ_URL = "http://127.0.0.1:5030"


@app.route("/start_order/<products>/<user_id>", methods=['GET', 'POST'])
def start_order(products, user_id):
    cost = 1
    data={'user_id': user_id, 'invoice': str(cost)}
    id = int(req.post(f"{REQ_URL}/add_invoice", json.dumps(data)).json()['id'])
    
    products = [
            {
              "name": "Название товара 1",
              "quantity": 1,
              "sum": 1,
              "payment_method": "full_payment",
              "payment_object": "commodity",
              "tax": "vat10"
            },
            {
              "name": "Название товара 2",
              "quantity": 1,
              "sum": 1,
              "cost": 1,		  
              "payment_method": "full_prepayment",
              "payment_object": "service",
              "nomenclature_code": "04620034587217"
            }
          ]
    
    total_cost = 0
    total_quan = 0

    for i in products:
        total_cost += i['sum'] * i['quantity']
        total_quan += i['quantity']
        
    merchant_login = LOGIN_ROBOKASSA
    merchant_password_1 = PASSWORD_ROBOKASSA

    print(quote(json.dumps(products)))
        
    link = generate_payment_link(products, merchant_login, merchant_password_1, total_cost, id, 'test')

    data = req.get(f"{REQ_URL}/get_invoice/{id}").json()
    data['invoice_status'] = f'{calculate_signature(merchant_login,total_cost,id,merchant_password_1)} {total_cost}'
    req.put(f"{REQ_URL}/update_invoice/{id}", json.dumps(data))
    
    return render_template('/start_order.html', link=link, products=products, user_id=user_id, total_cost=total_cost, total_quan=total_quan)


@app.route("/success/", methods=['GET', 'POST'])
def success():
    # number = request.form["InvId"]
    params = {}
    for item in urlparse(request.url).query.split('&'):
        key, value = item.split('=')
        params[key] = value

    number = params['InvId']
    telegram_id = req.get(f"{REQ_URL}/get_invoice/{number}").json()["telegram_id"]

    req.get(f"{REQ_URL}/finish_invoice/{telegram_id}")  # определить telegram_id
    return render_template('/success.html')


# ответ от робокассы
@app.route('/finish_order/', methods=['GET', 'POST'])
def result_payment() -> str:
    number = json.loads(request.json)["InvId"]
    print(number)
    return f"OK{number}"


if __name__ == '__main__':
    app.run(debug=True)

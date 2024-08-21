import time
from config import *
import datetime
from Consent import Consent
import requests as req
from datetime import timedelta
import json


REQ_URL = 'http://127.0.0.1:8000'


while True:
      today = datetime.datetime.now().date()
      users = req.get(f"{REQ_URL}/get_consent_by_today/{today}")
      print(users.json())

      for consent_info in users:
            consent_info = dict(consent_info)
            payment_data = {
                  "MerchantLogin": LOGIN_ROBOKASSA,
                  "InvoiceID": consent_info['id'],
                  "PreviousInvoiceID": consent_info['invoice_id'],
                  "Description": consent_info['description'],
                  "SignatureValue": consent_info['signature'],
                  "OutSum": consent_info['price']
            }

            response = req.post("https://auth.robokassa.ru/Merchant/Recurring", data=payment_data)
            print(response)

            if response.status_code == 200:
                  now = datetime.datetime.now()
                  str_date = f'{now.year}.{now.month}.{now.day}'
                  next_date = (datetime.strptime(str_date, '%Y.%m.%d') + timedelta(days=int(consent_info.period))).strftime('%Y.%m.%d')
                  
                  consent_info.next_date = next_date
                  req.put(f"{REQ_URL}/update_consent/{consent_info.id}", json.dumps(consent_info))


      time.sleep(100)

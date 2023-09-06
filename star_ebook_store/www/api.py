import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import frappe

import base64

# This class stores the Mpesa credentials required for generating an access token.
class MpesaC2bCredential:
    # The Consumer Key for the Mpesa API.
    consumer_key = 'ShetFZbeG2YJSXIvUojmgGrzISPjJ4EQ'
    # The Consumer Secret for the Mpesa API.
    consumer_secret = 'd8VqfDwpR6MExxAU'
    # The URL for generating the access token.
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

# This class generates the online password required for processing an Mpesa transaction.
class LipanaMpesaPpassword:
    # Generates the current time in the specified format.
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    # The short code for the business making the transaction.
    Business_short_code = "174379"
    # The passkey for the Mpesa API.
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    # Concatenates the business short code, passkey, and time to form the data to be encoded.
    data_to_encode = Business_short_code + passkey + lipa_time
    # Encodes the data using base64 encoding.
    online_password = base64.b64encode(data_to_encode.encode())
    # Decodes the encoded password to string format.
    decode_password = online_password.decode('utf-8')


def getAccessToken():
    # Mpesa Consumer key and secret
    consumer_key = 'XjWEg9z1ihL9zoXO1JRaCOhfIJAgB8cu'
    consumer_secret = 'y48BAeDDA0AgXqI2'
    # Mpesa OAuth API URL
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    # Make a GET request to the API URL with consumer key and secret as basic auth credentials
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(url, auth=(consumer_key, consumer_secret))

    if response.status_code != 200:
        print(response.content)
        print("No data")
    else:
        data = json.loads(response.content)
        token = data["access_token"]
        return token
    

def push_mpesa_stk(request):
    # Format the phone number and amount
    number = '254740743521'
    amount = 800
    # Get the Mpesa access token
    #access_token = 'KVsZ0izc6IFUmnUPgNwICyuIFEm4'
    access_token = getAccessToken()
    # Set the API URL for STK Push
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    # Set the headers for the request
    headers = {"Authorization": "Bearer %s" % access_token}
    # Set the payload for the request
    payload = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA":  number,
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": number,
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Mania",
        "TransactionDesc": "Payment for services"
    }
    # Make a POST request to the API URL with the headers and payload
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200 and response.json().get('ResponseCode') == '0':
        

        print("Success")
    else:
        print("Fail")


#Creating order without payment methods
@frappe.whitelist(allow_guest=True)
def create_ebook_order(ebook_name):
    #Fetch prices of this book
    ebook_price=frappe.db.get_value("eBook", ebook_name, "price")

    #Create and insert new book
    ebook_order=frappe.get_doc({
        "doctype":"eBook Orders",
        "ebook":ebook_name,
        "order_amount":ebook_price,
        "customer_email":"mania@gmail.com",
        "mpesa_payment_id":"R23454",
        "Mpesa_order_id":"4569"
    }
    )
    ebook_order.insert(ignore_permissions=True)

    return {
        "order_id":ebook_order.name,
        "order_amount":ebook_price,
    }

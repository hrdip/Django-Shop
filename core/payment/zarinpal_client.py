import requests
import json

class ZarinPalSandbox:
    _payment_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'
    _payment_verify_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json'
    _payment_page_url = 'https://sandbox.zarinpal.com/pg/StartPay/'
    _callback_url = 'https://redreseller.com/verify'

    def __init__(self, nerchant_id):
        self.merchant_id = nerchant_id

    def payment_request(self,amount,description="user payment"):
        payload = {
            "MerchantID": self.merchant_id,
            "Amount": str(amount),
            "CallbackURL": self._callback_url,
            "Description": description,
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(self._payment_request_url, headers=headers, data=json.dumps(payload))
        return response.json()

    
    def payment_verify(self,amount,authority):
        payload = {
            "MerchantID": self.merchant_id,
            "Amount": amount,
            "Authority": authority,

        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=json.dumps(payload))
        return response.json()


    # payment address
    def generate_payment_url(self,authority):
        return self._payment_page_url + authority
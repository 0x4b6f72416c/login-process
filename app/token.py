from base64 import encode
import hmac
import hashlib
import base64

SECRET_KEY = "80a528a51c7cf1fd4f73d6a45d55a61f430a1348ca72d8f5dcb4ea377edf07ca" 

class Sign():

 
    def sign_data(data):
        return hmac.new(SECRET_KEY.encode(), msg=data.encode(), digestmod=hashlib.sha256).hexdigest().upper()
        
    def sign_username(data):
        return base64.b64encode(data.encode()).decode() + "." + Sign.sign_data(data)

    def get_username_from_sign(data):
        print(data)
        if '.' not in data:
            return None
        username_base64, sign = data.split('.') 
        username = base64.b64decode(username_base64.encode()).decode()
        valid_sign = Sign.sign_data(username)
        if hmac.compare_digest(valid_sign, sign):
            return username


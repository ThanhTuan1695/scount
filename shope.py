import requests
import random
import hashlib
import json


def csrftoken(length=32):
    # put your letters in the following string
    character='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join((random.choice(character) for i in range(length)))


def encrypt_SHA256(password):
    sha_signature = \
        hashlib.sha256((hashlib.md5(password.encode()).hexdigest()).encode()).hexdigest()
    return sha_signature

def main():        
        session = requests.Session()
        response = session.get('https://banhang.shopee.vn/account/signin?next=%2F')
        # cook = response.cookies.get_dict()
        # cook_addon = { 'csrftoken' : csrftoken() }
        # cook_addon.update(cook)
        csrftoken_gen = csrftoken()
        # print(cook_addon)
        cookie_string = "; ".join([str(x)+"="+str(y) for x,y in response.cookies.get_dict().items()])
        headers = {
            'x-csrftoken'     : csrftoken_gen,
            'x-requested-with': 'XMLHttpRequest',
            'referer'         : 'https://banhang.shopee.vn/account/signin?next=%2F',
            'cookie'          : "csrftoken=" + csrftoken_gen + "; " + cookie_string,
        }
        #print(headers)  
        payload = {
            'phone'    : '84937503940',
            'password_hash': encrypt_SHA256('hQQcAtrwjwS'),
            'remember_me'  : True,
        }
        print(payload)
        url="https://banhang.shopee.vn/api/v2/login/"
        response = session.request("POST",url,headers=headers, data = payload)
        print(response.content)


if __name__ == '__main__':
    main()
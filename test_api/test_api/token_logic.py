import os
import time
import requests
import json
import jwt
import urllib
from dotenv import load_dotenv

def create_signed_jwt(credentials_json, run_service_url):
    iat = time.time()
    exp = iat + 3600
    payload = {
        'iss': credentials_json['client_email'],
        'sub': credentials_json['client_email'],
        'target_audience': run_service_url,
        'aud': 'https://www.googleapis.com/oauth2/v4/token',
        'iat': iat,
        'exp': exp
        }
    additional_headers = {
        'kid': credentials_json['private_key_id']
        }
    signed_jwt = jwt.encode(
        payload,
        credentials_json['private_key'], 
        headers=additional_headers,
        algorithm='RS256'
    )
    return signed_jwt


def exchange_jwt_for_token(signed_jwt):
    body = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': signed_jwt
    }
    token_request = requests.post(
        url='https://www.googleapis.com/oauth2/v4/token',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data=urllib.parse.urlencode(body)
    )
    return token_request.json()['id_token']


def generate_token():
    with open(os.getenv("KEYFILE"), "rb+") as f:
        credentials_json = json.load(f)
    token_jwt = create_signed_jwt(credentials_json, os.getenv("CLOUDRUN_URL"))
    id_token_oauth = exchange_jwt_for_token(token_jwt)
    return id_token_oauth

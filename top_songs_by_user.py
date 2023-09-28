import os
import base64
import requests
import json
import random
import string
import hashlib


CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = "http://localhost:5500/"


# Code Verifier

def generate_random_string(length):
    """The PKCE authorization flow starts with the creation of a code verifier"""
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


async def generate_code_challenge(code_verifier):
    """We must hash the code using the SHA256 algorithm then convert it to base64 encoding"""
    def base64encode(data):
        encoded_bytes = base64.urlsafe_b64encode(data)
        encoded_string = encoded_bytes.decode('utf-8').rstrip('=')
        return encoded_string

    encoder = hashlib.sha256()
    encoder.update(code_verifier.encode('utf-8'))
    digest = encoder.digest()

    return base64encode(digest)


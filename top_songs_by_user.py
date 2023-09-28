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


# Code Challenge
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


# Request User Authorization
async def generate_code_challenge(codeVerifier):
    sha256 = hashlib.sha256()
    sha256.update(codeVerifier.encode())
    code_challenge = base64.urlsafe_b64encode(sha256.digest()).rstrip(b'=').decode()
    return code_challenge


async def main():
    # Generate code verifier
    code_verifier = generate_random_string(128)

    # Generate code challenge
    code_challenge = await generate_code_challenge(code_verifier)

    # Generate state and scope
    state = generate_random_string(16)
    scope = 'user-top-read user-read-email'

    # Prepare URL parameters
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
    }

    # Construct authorization URL
    auth_url = 'https://accounts.spotify.com/authorize?' + '&'.join(f'{key}={value}' for key, value in params.items())

    print(auth_url)  # Redirect user to this URL

# Run the async function
import asyncio
asyncio.run(main())




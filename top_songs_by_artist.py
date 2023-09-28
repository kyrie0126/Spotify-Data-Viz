import os
import base64
import requests
import json

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

def get_token():
    auth_string = f'{CLIENT_ID}:{CLIENT_SECRET}'
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {auth_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    
    data = {'grant_type': 'client_credentials'}
    
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token


def get_auth_header(token):
    return {'Authorization': f'Bearer {token}'}


def search_for_artist(token, artist_name):
    url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1'
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    
    if len(json_result) == 0:
        print(f'No results found for {artist_name}')
        return None
    else:
        return json_result[0]


def get_songs_by_artist(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_results = json.loads(result.content)['tracks']
    return json_results
    

token = get_token()
result = search_for_artist(token, 'The Beatles')
artist_id = result['id']
songs = get_songs_by_artist(token, artist_id)
for song in songs:
    print(song['name'])

    
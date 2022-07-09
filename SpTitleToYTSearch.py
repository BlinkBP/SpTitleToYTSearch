#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 BlinkBP
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import requests
import base64
import os
from dotenv import load_dotenv
from urllib.parse import quote

example_url = "https://open.spotify.com/track/7byGwLkiIzJdHOZKZMS8nd?si=aa14b663692146cd"

search_url = "https://www.youtube.com/results?search_query={}"

api_tracks_url = "https://api.spotify.com/v1/tracks/{}"
api_auth_url = "https://accounts.spotify.com/api/token"

tracks_headers = {"Content-Type": "application/json",
                  "Authorization": "Bearer {}"}
auth_headers = {"Authorization": "Basic {}"}

auth_data = {"grant_type" : "client_credentials"}

def get_filled_auth_header():
    header = auth_headers
    auth_data = f"{os.getenv('SPOTIFY_CLIENT')}:{os.getenv('SPOTIFY_SECRET')}"
    auth_bytes = auth_data.encode('ascii')
    b64_bytes = base64.b64encode(auth_bytes)
    header["Authorization"] = header["Authorization"].format(b64_bytes.decode('ascii'))

    return header

def get_filled_tracks_header(token):
    header = tracks_headers
    header["Authorization"] = header["Authorization"].format(token)

    return header

def auth():
    response = requests.post(api_auth_url, headers=get_filled_auth_header(), data=auth_data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return ""

def get_id_from_url(url):
    return url.split('/')[-1]

def get_track_data(id, token):
    return requests.get(api_tracks_url.format(id), headers=get_filled_tracks_header(token)).json()

def get_track_search_url(artist, title):
    encoded_text = quote(f"{artist} {title}")
    return search_url.format(encoded_text)

def exec(url):
    load_dotenv()
    token = auth()
    if token != "":
        id = get_id_from_url(example_url)
        track_json = get_track_data(id, token)
        track_artist = track_json["artists"][0]["name"]
        track_title = track_json["name"]

        return get_track_search_url(track_artist, track_title)
    else:
        return ""

if __name__ == "__main__":
    print(exec(example_url))
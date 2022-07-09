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
import re
import time
from dotenv import load_dotenv
from urllib.parse import quote

example_url = "https://open.spotify.com/track/7byGwLkiIzJdHOZKZMS8nd?si=aa14b663692146cd"

__search_url = "https://www.youtube.com/results?search_query={}"

__api_tracks_url = "https://api.spotify.com/v1/tracks/{}"
__api_auth_url = "https://accounts.spotify.com/api/token"

__tracks_headers = {"Content-Type": "application/json",
                  "Authorization": "Bearer {}"}
__auth_headers = {"Authorization": "Basic {}"}

__auth_data = {"grant_type" : "client_credentials"}

__max_retries = 3

def match_sp_url(str):
    pattern = r"https:\/\/open\.spotify\.com\/track\/[\w?=\-&]+"
    result = re.search(pattern, str)

    if result is not None:
        return result.group()
    else:
        return ""


def __get_filled_auth_header():
    header = __auth_headers
    auth_data = f"{os.getenv('SPOTIFY_CLIENT')}:{os.getenv('SPOTIFY_SECRET')}"
    auth_bytes = auth_data.encode('ascii')
    b64_bytes = base64.b64encode(auth_bytes)
    header["Authorization"] = header["Authorization"].format(b64_bytes.decode('ascii'))

    return header

def __get_filled_tracks_header(token):
    header = __tracks_headers
    header["Authorization"] = header["Authorization"].format(token)

    return header

def __auth():
    response = requests.post(__api_auth_url, headers=__get_filled_auth_header(), data=__auth_data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return ""

def __get_id_from_url(url):
    return url.split('/')[-1].split('&')[0]

def __get_track_data(id, token):
    return requests.get(__api_tracks_url.format(id), headers=__get_filled_tracks_header(token)).json()

def __get_track_search_url(artist, title):
    encoded_text = quote(f"{artist} {title}")
    return __search_url.format(encoded_text)

def exec(url):
    retries = 0
    load_dotenv()
    token = __auth()
    if token != "":
        id = __get_id_from_url(url)
        while retries < __max_retries:
            track_json = __get_track_data(id, token)
            if ("artists" in track_json) and ("name" in track_json):
                track_artist = track_json["artists"][0]["name"]
                track_title = track_json["name"]

                return __get_track_search_url(track_artist, track_title)
            retries += 1
            time.sleep(0.5)
        return ""
    else:
        return ""

if __name__ == "__main__":
    print(exec("https://open.spotify.com/track/29YNMIIX9BEGaqylUK9JnA?si=01d3b7cb468f4d64"))
# Spotify to YouTube Music Playlist Importer

**ATTENTION: The script is currently under construction; therefore, the information below (particularly regarding script execution) is no longer correct.**

A Python script to export playlists from Spotify (including tracks) and import them into YouTube Music.

This tool allows you to migrate your playlists and liked songs from Spotify to YouTube Music using a JSON intermediate file.

## Features

- Export playlists from Spotify with all track metadata via the official Spotify API.
- Save playlists into a JSON file for portability. 
- Import playlists into YouTube Music using `ytmusicapi`. 
- Allows duplicates to handle same tracks multiple times in a playlist. 
- Supports your own Spotify playlists (private or public).

## Install Requirements

Execute the following command to install all requirements:
```bash
pip install -r requirements.txt
```

## Setup Project

### 1. Spotify API Credentials

Create a Spotify app in the Spotify Developer Dashboard and add its client ID, client secret,
and callback uri in a env file (a sample env file named `.env_sample` is provided).

Your .env file should have the following variables:
```
SPOTIPY_CLIENT_ID="your_client_id"
SPOTIPY_CLIENT_SECRET="your_client_secret"
SPOTIPY_REDIRECT_URI="http://localhost:8888/callback/"
```

### 2. YouTube Music Authentication

`ytmusicapi uses your YouTube Music session headers to authenticate.

1. Open YouTube Music in your browser
2. Open `DevTools` > `Network` tab, and reload the page.
3. Find a request to a `POST /browse` or `POST /player`, and copy the headers having the following information:
   - `Authorization` 
   - `x-goog-authuser` 
   - `x-origin` 
   - `Cookie` 
4. Save them into a file named headers_auth.json:
    ```json
   {
       "cookie": "YOUR_COOKIE_HERE",
       "x-goog-authuser": "0",
       "authorization": "SAPISIDHASH YOUR_HASH_HERE",
       "x-origin": "https://music.youtube.com"
    }
   ```

## Execute the Scripts

Once the setup is complete, you can execute the export script with the following command:
```bash
python3 spotify_playlists_exporter.py
```

The script may take a while depending on the number and size of playlists.

When the export has finished, you can execute the import with the following command:
```bash
python3 ytmusic_playlists_importer.py
```

When execution finishes, you'll see a message in the terminal indicating that the import has completed.
If the script cannot find a song in YouTube Music, it will publish a warning message in the terminal.

After the import, you can open YouTube Music to find your playlists.

## Good To Know

- Matching is based on song title and artist, so some tracks may not be found on YouTube Music. 
- Keep your headers_auth.json private — it contains full access to your account. 
- The SAPISIDHASH may expire if you log out or clear cookies — re-export headers if necessary.
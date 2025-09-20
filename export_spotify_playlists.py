import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


def fetch_playlist_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_items(playlist_id, additional_types=['track'], limit=100)

    while results:
        for item in results['items']:
            track = item.get('track')
            if track:  # sometimes local tracks or unavailable ones may return None
                tracks.append({
                    "name": track["name"],
                    "id": track["id"],
                    "artists": [artist["name"] for artist in track["artists"]],
                    "album": track["album"]["name"],
                    "duration_ms": track["duration_ms"],
                    "spotify_url": track["external_urls"]["spotify"]
                })
        if results['next']:
            results = sp.next(results)
        else:
            break
    return tracks


def fetch_spotify_playlist(sp, user_id):
    playlists = []
    results = sp.current_user_playlists(limit=50)

    while results:
        for playlist in results['items']:
            if playlist["owner"]['id'] == user_id:
                playlists.append({
                    "name": playlist["name"],
                    "id": playlist["id"],
                    "tracks_total": playlist["tracks"]["total"],
                    "owner": playlist["owner"]["display_name"],
                    "tracks": fetch_playlist_tracks(sp, playlist["id"])
                })
        if results['next']:
            results = sp.next(results)
        else:
            break
    return playlists


def export_spotify_playlists():
    # Load credentials from environment variables
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

    if not all([client_id, client_secret, redirect_uri]):
        raise ValueError("Please set SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI")

    # Define scope (permissions we need)
    scope = "playlist-read-private playlist-read-collaborative"

    # Authenticate using SpotifyOAuth
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        open_browser=True  # opens browser for user login
    ))

    # Get current user info
    user = sp.current_user()
    print(f"Authenticated as {user['display_name']} ({user['id']})")

    # Fetch playlists
    playlists = fetch_spotify_playlist(sp, user['id'])

    with open("playlists.json", "w") as f:
        json.dump(playlists, f)


    # Print summary
    print("\n=== Playlists and Tracks ===")
    for pl in playlists:
        print(f"\n▶ {pl['name']} (Tracks: {pl['tracks_total']})")
        for t in pl["tracks"][:5]:  # only show first 5 for brevity
            print(f"   - {t['name']} by {', '.join(t['artists'] if 'artists' in t else [])}")

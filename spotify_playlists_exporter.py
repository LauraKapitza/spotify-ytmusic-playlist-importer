import json
from typing import Any

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from config import SpotifyConfig

from pydantic import BaseModel, ValidationError

# Define scope (permissions we need)
SCOPE = "playlist-read-private playlist-read-collaborative"

PATH_TO_FILE = "exports/spotify_playlists.json"


class SpotifyArtist(BaseModel):
    name: str


class SpotifyAlbum(BaseModel):
    name: str


class SpotifyTrack(BaseModel):
    id: str
    name: str
    artists: list[SpotifyArtist]
    album: SpotifyAlbum


class Playlist(BaseModel):
    name: str
    tracks: list[SpotifyTrack]
    tracks_total: int


class SpotifyExporter:
    config: SpotifyConfig
    spotify_api: spotipy.Spotify
    user_id: Any
    playlists: list[Playlist]

    def __init__(self, config: SpotifyConfig):
        self.config = config
        self.spotify_api = self.create_spotify_api()
        self.user_id = self.spotify_api.current_user()["id"]

    def create_spotify_api(self) -> spotipy.Spotify:
        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=SCOPE,
                client_id=self.config.client_id,
                client_secret=self.config.client_secret,
                redirect_uri=self.config.redirect_uri,
                open_browser=True,  # opens browser for user login
            )
        )

    def fetch_tracks(self, playlist_id: str) -> list[SpotifyTrack]:
        tracks = []
        results = self.spotify_api.playlist_items(
            playlist_id, additional_types=["track"], limit=100
        )

        while results:
            for item in results["items"]:
                track = item.get("track")
                if track:  # sometimes local tracks or unavailable ones may return None
                    try:
                        tracks.append(SpotifyTrack.model_validate(track))
                    except ValidationError as e:
                        print("Error occurred while validating track:", e)
                        continue

            if results["next"]:
                results = self.spotify_api.next(results)
            else:
                break
        return tracks

    def fetch_playlist(self) -> None:
        playlists = []
        results = self.spotify_api.current_user_playlists(limit=1)

        print("\n=== Playlists and Tracks ===")

        while results:
            for playlist in results["items"]:
                if playlist["owner"]["id"] == self.user_id:
                    new_playlist = Playlist(
                        name=playlist["name"],
                        tracks=self.fetch_tracks(playlist_id=playlist["id"]),
                        tracks_total=playlist["tracks"]["total"],
                    )
                    playlists.append(new_playlist)

                    print(f"\n▶ {new_playlist}")

            if results["next"]:
                results = self.spotify_api.next(results)
            else:
                break
        self.playlists = playlists

    def export(self) -> None:
        with open(PATH_TO_FILE, "w") as f:
            json.dump(self.playlists, f)


def main():
    # Load credentials from environment class
    config = SpotifyConfig()

    exporter = SpotifyExporter(config=config)

    exporter.create_spotify_api()
    exporter.fetch_playlist()
    exporter.export()


if __name__ == "__main__":
    main()

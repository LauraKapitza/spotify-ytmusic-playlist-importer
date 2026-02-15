import os
from spotipy import SpotifyOAuth, Spotify, SpotifyException
from utils.exceptions import MusicImporterError, ProviderApiError


class SpotifyClient:
    def __init__(self, logger):
        self.logger = logger
        self.scope = "playlist-read-private playlist-read-collaborative"
        self.spotify = self._authenticate()
        self.user = self.spotify.current_user()
        self.user_id = self.user['id']

        self.logger.info(f"Spotify authenticated as: {self.user['display_name']}")

    def _authenticate(self):
        return Spotify(auth_manager=SpotifyOAuth(
            scope=self.scope,
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            open_browser=True  # opens browser for user login
        ))

    def get_all_playlists(self):
        """
        Fetches all playlists owned by the authenticated user.
        """
        try:
            playlists = []
            results = self.spotify.current_user_playlists(limit=50)

            while results:
                for item in results['items']:
                    if item['owner']['id'] == self.user_id:
                        playlists.append({
                            "name": item["name"],
                            "id": item["id"],
                            "tracks": self.get_playlist_tracks(item["id"])
                        })
                results = self.spotify.next(results) if results['next'] else None

            return playlists

        except SpotifyException as e:
            self.logger.error(f"Spotify API error: {e}")
            raise ProviderApiError(f"Failed to fetch playlists: {e}")

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise MusicImporterError("An unknown error occurred on Spotify side.")

    def get_playlist_tracks(self, playlist_id):
        """
        Fetches all tracks for a specific playlist.
        """
        try:
            tracks = []
            results = self.spotify.playlist_items(playlist_id, limit=100)
        except SpotifyException as e:
            self.logger.error(f"Spotify failed to fetch tracks for {playlist_id}: {e}")
            raise ProviderApiError(f"Spotify track fetch failed: {e.http_status}")
        except Exception as e:
            raise MusicImporterError(f"Unexpected error fetching tracks: {e}")

        while results:
            for item in results['items']:
                track = item.get('track')
                if track:
                    tracks.append({
                        "name": track["name"],
                        "artists": [a["name"] for a in track["artists"]],
                        "album": track["album"]["name"]
                    })
            results = self.spotify.next(results) if results['next'] else None

        return tracks

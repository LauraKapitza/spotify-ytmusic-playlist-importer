from ytmusicapi import YTMusic
import time

from ytmusicapi.exceptions import YTMusicServerError, YTMusicUserError
from utils import ProviderApiError


class YTMusicClient:
    def __init__(self, logger, auth_file="header-auth.json"):
        self.logger = logger
        self.ytmusic = YTMusic(auth_file)
        self.logger.info("YouTube Music client initialized.")

    def search_song(self, track_name, artists):
        """
        Searches for a track and returns the best videoId match.
        """
        query = f"{track_name} {', '.join(artists)}"
        try:
            results = self.ytmusic.search(query, filter="songs")
            return results[0]['videoId'] if results else None
        except YTMusicServerError as e:
            self.logger.error(f"YouTube Server Error during search: {e}")
            return None

        except YTMusicUserError as e:
            self.logger.critical(f"Invalid request sent to YouTube: {e}")
            raise ProviderApiError("Critical error in search request format.")

    def create_playlist_from_tracks(self, playlist_name, tracks):
        """
        Creates a new playlist and populates it with tracks.
        """
        playlist_id = None
        try:
            self.logger.info(f"Creating YouTube playlist: {playlist_name}")
            description = f"Imported from Spotify"
            playlist_id = self.ytmusic.create_playlist(playlist_name, description)
        except (YTMusicServerError, YTMusicUserError) as e:
            self.logger.error(f"CRITICAL: Could not create playlist structure for '{playlist_name}': {e}")
            # We raise here because if the folder isn't created, we can't put items in it.
            raise ProviderApiError(f"Playlist creation failed: {e}")

        video_ids = []
        for track in tracks:
            video_id = self.search_song(track['name'], track['artists'])
            if video_id:
                video_ids.append(video_id)
            else:
                artists = track['artists'] if track['artists'] else []
                self.logger.warning(
                    f"Song not found:: {track['name']} by {', '.join(artists)}"
                )
            time.sleep(0.2)  # Rate limiting

        # TODO check whether to delete playlist if a track insertion failure happens
        # self.yt.delete_playlist(playlist_id)
        # self.logger.warning(f"Deleted empty playlist '{playlist_name}' due to track insertion failure.")
        if video_ids:
            try:
                self.ytmusic.add_playlist_items(playlist_id, video_ids)
                self.logger.info(f"Successfully added {len(video_ids)} tracks to {playlist_name}")
            except (YTMusicServerError, YTMusicUserError) as e:
                self.logger.error(f"ERROR: Created playlist '{playlist_name}', but failed to add tracks: {e}")
                raise ProviderApiError(f"Failed to populate playlist: {e}")

        return playlist_id

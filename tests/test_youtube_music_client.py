import pytest
from ytmusicapi.exceptions import YTMusicServerError
from utils import ProviderApiError


def test_create_playlist_fails_at_creation(yt_client):
    yt_client.yt.create_playlist.side_effect = YTMusicServerError("Server Down")

    with pytest.raises(ProviderApiError) as excinfo:
        yt_client.create_playlist_from_tracks("Test PL", [])

    assert "Playlist creation failed" in str(excinfo.value)


def test_create_playlist_fails_at_adding_tracks(yt_client):
    yt_client.yt.create_playlist.return_value = "new_pl_123"
    yt_client.yt.add_playlist_items.side_effect = YTMusicServerError("Quota Exceeded")

    yt_client.search_song = lambda name, artist: "vid123"

    tracks = [{"name": "Song 1", "artists": ["Art 1"]}]

    with pytest.raises(ProviderApiError) as excinfo:
        yt_client.create_playlist_from_tracks("Test PL", tracks)

    assert "Failed to populate playlist" in str(excinfo.value)

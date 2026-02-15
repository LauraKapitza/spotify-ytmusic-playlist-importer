import pytest
import os
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {
        "SPOTIPY_CLIENT_ID": "fake_id",
        "SPOTIPY_CLIENT_SECRET": "fake_secret",
        "SPOTIPY_REDIRECT_URI": "http://localhost:8888",
        "YT_MUSIC_AUTH": "fake_auth_json"
    }):
        yield


@pytest.fixture
def mock_logger():
    return MagicMock()


@pytest.fixture
def spotify_client(mock_logger):
    with (
        patch('clients.spotify_client.Spotify') as mock_sp_class,
        patch('clients.spotify_client.SpotifyOAuth') as mock_oauth_class
    ):
        mock_instance = mock_sp_class.return_value

        mock_instance.current_user.return_value = {
            'id': 'user123',
            'display_name': 'Tester'
        }

        from clients.spotify_client import SpotifyClient
        yield SpotifyClient(logger=mock_logger)


@pytest.fixture
def yt_client(mock_logger):
    with patch('clients.youtube_music_client.YTMusic') as mock_yt_class:
        from clients.youtube_music_client import YTMusicClient
        client = YTMusicClient(logger=mock_logger)
        client.yt = mock_yt_class.return_value
        yield client

import pytest
from spotipy.exceptions import SpotifyException
from utils.exceptions import ProviderApiError


def test_get_all_playlists_success(spotify_client, mock_logger):
    # Define what the fake Spotify instance should return for playlists
    spotify_client.spotify.current_user_playlists.return_value = {
        'items': [
            {
                'name': 'My Playlist',
                'id': 'pl1',
                'owner': {'id': 'user123'}  # Matches 'user123' from conftest
            }
        ],
        'next': None
    }

    spotify_client.spotify.playlist_items.return_value = {
        'items': [],
        'next': None
    }

    playlists = spotify_client.get_all_playlists()

    assert len(playlists) == 1
    assert playlists[0]["name"] == "My Playlist"


def test_get_all_playlists_api_failure(spotify_client):
    # Simulate an API error
    spotify_client.spotify.current_user_playlists.side_effect = SpotifyException(
        http_status=403, code=-1, msg="Forbidden"
    )

    with pytest.raises(ProviderApiError):
        spotify_client.get_all_playlists()

import json
from ytmusicapi import YTMusic
import time


def search_song(ytmusic, track):
    """
    Search for a song on YouTube Music using name + artist.
    Returns videoId if found, else None.
    """
    query = f"{track['name']} {', '.join(track['artists'])}"
    results = ytmusic.search(query, filter="songs")
    if results:
        return results[0]["videoId"]
    return None


def import_playlists():
    ytmusic = YTMusic("header-auth.json")

    with open("playlists.json", "r", encoding="utf-8") as playlist_file:
        playlists = json.load(playlist_file)

    for pl in playlists:
        print(f"\n▶ Importing playlist: {pl['name']} ({len(pl['tracks'])} tracks)")

        # Create new playlist
        playlist_id = ytmusic.create_playlist(
            pl["name"], f"Imported from Spotify ({pl['owner']})"
        )
        video_ids = []

        for track in pl["tracks"]:
            video_id = search_song(ytmusic, track)
            if video_id:
                video_ids.append(video_id)
            else:
                print(
                    f"⚠️ Could not find: {track['name']} by {', '.join(track['artists'] if track['artists'] else [])}"
                )

            # Be gentle with API calls
            time.sleep(0.2)

        # Add songs to playlist
        if video_ids:
            response = ytmusic.add_playlist_items(playlist_id, video_ids, None, True)
            print(response)
            print(f"✅ Added {len(video_ids)} tracks.")
        else:
            print("❌ No tracks found for this playlist.")


if __name__ == "__main__":
    import_playlists()

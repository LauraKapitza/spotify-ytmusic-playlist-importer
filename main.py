from dotenv import load_dotenv

from import_playlists import import_playlists
from export_spotify_playlists import export_spotify_playlists
load_dotenv()


def main():
    export_spotify_playlists()
    import_playlists()
    print("✅ Import successfully finished.")

if __name__ == "__main__":
    main()


from dotenv import load_dotenv
from clients import SpotifyClient, YTMusicClient
from utils import Logger, ProviderAuthError, MusicImporterError

load_dotenv()


def main():
    log_service = Logger(name="SpotifyYTMusicImporter")
    logger = log_service.get_logger()

    try:
        spotify = SpotifyClient(logger=logger)
        yt_music = YTMusicClient(logger=logger)

        logger.info("Starting migration process...")
        playlists = spotify.get_all_playlists()

        for playlist in playlists:
            yt_music.create_playlist_from_tracks(playlist['name'], playlist['tracks'])

        logger.info("Full migration completed successfully.")
    except ProviderAuthError as e:
        logger.critical(f"Authentication failed: Check your credentials. {e}")
    except MusicImporterError as e:
        logger.error(f"Application error: {e}")
    except KeyboardInterrupt:
        logger.info("Process interrupted by user. Cleaning up...")
    except Exception as e:
        # exc_info=True sends the full traceback to the log file
        logger.critical(f"Unexpected system crash: {e}", exc_info=True)


if __name__ == "__main__":
    main()

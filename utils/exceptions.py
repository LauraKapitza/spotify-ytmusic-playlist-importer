class MusicImporterError(Exception):
    """Base class for all exceptions in this app."""
    pass


class ProviderAuthError(MusicImporterError):
    """Raised when authentication with a music platform fails."""
    pass


class ProviderApiError(MusicImporterError):
    """Raised when an API call fails (e.g., network issues, rate limits)."""
    pass

import logging
import sys


class Logger:
    def __init__(self, name="importer", log_file="debug.log"):
        """
        Initializes the logging system.
        :param name: The name of the logger (appears in the log output).
        :param log_file: The name of the file where logs will be saved.
        """

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Check if the logger already has handlers to prevent duplicate logs
        # if the class is instantiated more than once in the same session.
        if not self.logger.handlers:

            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'  # Year-Month-Day Hour:Minute:Second
            )

            # --- CONSOLE HANDLER ---
            console_handler = logging.StreamHandler(sys.stdout)
            # Console Handler is set to INFO to not display debug logs in the terminal
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # --- FILE HANDLER ---
            file_handler = logging.FileHandler(log_file)
            # File Handler is set to DEBUG so every detail is captured in the file.
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        """
        Returns the configured logger instance to be used by other classes.
        """
        return self.logger

"""Custom Logger"""
import logging
from .custom_formatters import ColoredFormatter
from .custom_formatters import FileFormatter
from .custom_formatters import JSONFormatter

class CustomLogger(logging.Logger):
    """Custom Logger class"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    MESSAGE = 25
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    logging.addLevelName(MESSAGE, "MESSAGE")

    def __init__(self, name, level=logging.DEBUG, parent_logger_name=None):
        super().__init__(name, level)

        if parent_logger_name:
            self.parent = logging.getLogger(parent_logger_name)
            self.propagate = True

        self.level = level
        self.setup_logger()

    def setup_logger(self):
        """Configure logger with handlers"""
        self.file_handler = logging.FileHandler('all.log')
        self.json_handler = logging.FileHandler('all.json.log')
        self.stream_handler = logging.StreamHandler()

        self.stream_handler.setLevel(self.MESSAGE)

        self.file_formatter = FileFormatter()
        self.json_formatter = JSONFormatter()
        self.stream_formatter = ColoredFormatter()

        self.file_handler.setFormatter(self.file_formatter)
        self.json_handler.setFormatter(self.json_formatter)
        self.stream_handler.setFormatter(self.stream_formatter)

        self.custom_logger_handlers = [
            self.file_handler,
            self.json_handler,
            self.stream_handler
        ]

        for handler in self.custom_logger_handlers:
            self.addHandler(handler)

    def message(self, message, *args, **kwargs):
        """message handler for custom log level"""
        self.log(self.MESSAGE, message, *args, **kwargs)

    def add_third_party_logger(self, logger):
        """"Add Third Party Logger"""
        logger.setLevel(self.level)
        logger.parent = self
        logger.propagate = False

        logger.handlers = []
        for handler in self.custom_logger_handlers:
            logger.addHandler(handler)

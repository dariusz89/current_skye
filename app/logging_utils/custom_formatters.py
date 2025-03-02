"""Custom formatters"""
import logging
import json
import traceback

class JSONFormatter(logging.Formatter):
    """Convert the entire record dictionary to JSON"""
    def format(self, record):
        log_data = {
            "name": record.name,
            "msg": record.msg,
            "args": record.args,
            "levelname": record.levelname,
            "levelno": record.levelno,
            "pathname": record.pathname,
            "filename": record.filename,
            "module": record.module,
            "exc_info": record.exc_info,
            "exc_text": record.exc_text,
            "stack_info": record.stack_info,
            "lineno": record.lineno,
            "funcName": record.funcName,
            "created": record.created,
            "msecs": record.msecs,
            "relativeCreated": record.relativeCreated,
            "thread": record.thread,
            "threadName": record.threadName,
            "processName": record.processName,
            "process": record.process,
            "message": record.getMessage(),
            "asctime": self.formatTime(record, '%Y-%m-%d %H:%M:%S')
        }

        exc_info = log_data.get("exc_info")
        if exc_info:
            exc_type, exc_value, exc_traceback = exc_info
            log_data["exc_info"] = {
                'type': str(exc_type),
                "message": str(exc_value),
                "traceback": traceback.format_tb(exc_traceback)
            }

        log_data = json.dumps(log_data)

        return log_data

class FileFormatter(logging.Formatter):
    """Convert the entire record dictionary to JSON"""
    def format(self, record):
        log_parts = {
            'asctime': self.formatTime(record, '%Y-%m-%d %H:%M:%S'),
            'msecs': int(record.msecs),
            'levelname': record.levelname,
            'name': record.name,
            'processName': record.processName,
            'funcName': record.funcName,
            'lineno': record.lineno,
            'message': record.getMessage(),
            "exc_info": record.exc_info
        }

        exc_info = log_parts.get("exc_info")
        if exc_info:
            exc_type, exc_value, _ = exc_info
            log_parts["exc_info"] = f"\n{exc_type}, {exc_value}\n{traceback.format_exc()}"

        log_message = (
            "{asctime}.{msecs:03d} - "
            "{levelname} - "
            "{name} - "
            "{processName} - "
            "{funcName}:{lineno} - "
            "{message}"
        ).format_map(log_parts)

        if log_parts['exc_info'] is not None:
            log_message = f"{log_message}{log_parts['exc_info']}"

        return log_message

class ColoredFormatter(logging.Formatter):
    """Colored Formatter class"""
    COLOR_CODES = {
        'RESET': '\033[0m',
        'BLACK': '\033[0;2;30m',
        'RED': '\033[0;1;31m',
        'GREEN': '\033[0;1;32m',
        'YELLOW': '\033[0;1;33m',
        'BLUE': '\033[0;1;34m',
        'MAGENTA': '\033[0;1;35m',
        'CYAN': '\033[0;1;36m',
        'WHITE': '\033[0;2;37m',
    }

    LOG_LEVEL_COLORS = {
        logging.DEBUG: COLOR_CODES['CYAN'],
        logging.INFO: COLOR_CODES['BLACK'],
        logging.WARNING: COLOR_CODES['YELLOW'],
        logging.ERROR: COLOR_CODES['RED'],
        logging.CRITICAL: COLOR_CODES['MAGENTA'],
        25: COLOR_CODES['GREEN']  # MESSAGE level
    }

    ALL_COLORS = {
        'BLACK': COLOR_CODES['BLACK'],
        'RESET': COLOR_CODES['RESET'],
        'BLUE': COLOR_CODES['BLUE']
    }

    def apply_color(self, color, text):
        """Apply color to given text"""
        return f"{color}{text}{self.ALL_COLORS['RESET']}"

    def format_time(self, record):
        """Colorized asctime with msecs"""
        time_components = [
            self.formatTime(record, '%Y-%m-%d %H:%M:%S'),
            f"{int(record.msecs):03d}"
        ]

        return ".".join(time_components)

    def format_levelname(self, record):
        """Colorized levelno"""
        level_color = self.LOG_LEVEL_COLORS.get(record.levelno, self.ALL_COLORS['RESET'])
        levelname_components = [
            self.apply_color(self.ALL_COLORS["BLACK"], "["),
            self.apply_color(level_color, record.levelname),
            self.apply_color(self.ALL_COLORS["BLACK"], "]")
        ]

        return "".join(levelname_components)

    def format_name(self, record):
        """Colorized name"""
        return self.apply_color(self.ALL_COLORS["BLUE"], record.name)

    def format_function(self, record):
        """Colorized func with lineno"""
        function_components = [
            record.funcName,
            str(record.lineno)
        ]
        formatted_function = ":".join(function_components)

        return self.apply_color(self.ALL_COLORS["BLACK"], formatted_function)

    def format_exception(self, record):
        """Colorized exc_info with traceback"""
        exc_info = record.exc_info
        if (exc_info and exc_info is not None):
            level_color = self.LOG_LEVEL_COLORS.get(record.levelno, self.ALL_COLORS['RESET'])
            exc_type, exc_value, _ = exc_info
            exception_components = [
                self.apply_color(level_color, f"\n{exc_type} \"{exc_value}\""),
                self.apply_color(self.ALL_COLORS["BLACK"], traceback.format_exc())
            ]

            return '\n'.join(exception_components)

        return None

    def format(self, record):
        log_parts = {
            'time': self.format_time(record),
            'levelname': self.format_levelname(record),
            'name': self.format_name(record),
            'function': self.format_function(record),
            'message': record.getMessage(),
            "exception": self.format_exception(record)
        }

        log_message = (
            "{time} {levelname} {name} - "
            "{function} - {message}"
        ).format_map(log_parts)

        if log_parts['exception'] is not None:
            log_message = f"{log_message}{log_parts['exception']}"

        return log_message

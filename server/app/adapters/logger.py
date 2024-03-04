"""Logger adapters for external libraries """
import logging

class PythonSocketIOLoggerAdapter(logging.LoggerAdapter):
    """Adapter for extending default looger"""
    def __init__(self, logger, prefix):
        super(PythonSocketIOLoggerAdapter, self).__init__(logger, {})
        self.prefix = prefix
        self.level = logging.getLevelName(self.getEffectiveLevel())

    def process(self, msg, kwargs):
        return f'{self.level}:\t\x1b[2;36;30m{self.prefix}\033[0m {msg}', kwargs

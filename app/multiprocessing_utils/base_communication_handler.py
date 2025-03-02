"""a"""
import threading
from logging_utils import CustomLogger

class BaseCommunicationHandler:
    """a"""
    def __init__(self, commands_interpreter_callback):
        """a"""
        self.logger = CustomLogger(
            "multiprocessing_utils.BaseCommunicationHandler",
            parent_logger_name="App"
        )
        self._commands_interpreter_callback = commands_interpreter_callback
        self._stop_command_thread_event = threading.Event()
        self._command_thread = threading.Thread(
            target=self.wait_for_command
        )

    def start_command_thread(self):
        """a"""
        self._command_thread.start()

    def stop_command_thread(self):
        """a"""
        self._stop_command_thread_event.set()

    def command_interpreter(self, **kwargs):
        """a"""
        self._commands_interpreter_callback(**kwargs)

    def send_command(self, command, data=None):
        """a"""
        if data is not None:
            command_data = (command, data)
        else:
            command_data = (command,)

        self._extend_send_command(*command_data)

    def wait_for_command(self):
        """a """
        while not self._stop_command_thread_event.is_set():
            if self._stop_command_thread_event.is_set():
                break

            message = self._extend_wait_for_command()
            if message is not None:
                command = message["command"]
                data = message["data"]
                self.command_interpreter(command=command, data=data)

    def _extend_send_command(self, *command_data):
        """a"""
        raise NotImplementedError("_extend_send_command method must be implemented in subclasses")

    def _extend_wait_for_command(self):
        """a"""
        raise NotImplementedError("_extend_wait_for_command method must be implemented in subclasses")

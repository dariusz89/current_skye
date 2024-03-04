"""
Module: parent_process_communication_handler.py
"""
import threading
from logging_utils import CustomLogger

class ParentProcessCommunicationHandler:
    """
    Handles communication between a parent process
    and a child process using threading and an IPC manager.
    """
    def __init__(
            self,
            ipc_manager,
            commands_interpreter_callback
        ):
        """
        Initializes an instance of the class.
        """
        self.logger = CustomLogger("multiprocessing_utils.ParentProcessCommunicationHandler", parent_logger_name="App")
        self._ipc_manager = ipc_manager
        self._commands_interpreter_callback = commands_interpreter_callback
        self._stop_command_thread_event = threading.Event()
        self._command_thread = threading.Thread(
            target=self.wait_for_command
        )

    def start_command_thread(self):
        """
        Starts the command thread.
        """
        self.logger.debug("start_command_thread")
        self._command_thread.start()

    def stop_command_thread(self):
        """
        Stops the command thread.
        """
        self.logger.debug("stop_command_thread")
        self._stop_command_thread_event.set()
        self._command_thread.join()

    def send_command(self, command, data=None):
        """
        Sends a command to the child process.
        """
        self.logger.debug("send_command")
        if data is not None:
            command_data = (command, data)
        else:
            command_data = (command,)

        self._ipc_manager.send_command_to_child(*command_data)
        self._ipc_manager.trigger_child_command_event()

    def wait_for_command(self):
        """
        Waits for incoming commands from the child process and interprets them.
        """
        self.logger.debug("START - Parent process: wait_for_command")

        while not self._stop_command_thread_event.is_set():
            self.logger.info("Parent process: wait_for_command")
            self._ipc_manager.wait_for_master_command_event()
            message = self._ipc_manager.receive_command_from_child()

            if message is not None:
                command = message["command"]
                data = message["data"]
                self.command_interpreter(command=command, data=data)

        self.logger.debug("STOP - Parent process: wait_for_command")

    def command_interpreter(self, **kwargs):
        """
        Interprets the received command and data.
        """
        self.logger.debug("command_interpreter")
        self._commands_interpreter_callback(**kwargs)

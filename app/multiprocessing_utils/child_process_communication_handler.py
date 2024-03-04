"""
Module: child_process_communication_handler.py
"""
from logging_utils import CustomLogger

class ChildProcessCommunicationHandler:
    """
    Handles communication between a child process and a parent process using an IPC manager.
    """
    def __init__(
            self,
            ipc_manager,
            commands_interpreter_callback
        ):
        """
        Initializes an instance of the class.
        """
        self.logger = CustomLogger("multiprocessing_utils.ChildProcessCommunicationHandler", parent_logger_name="App")
        self.ipc_manager = ipc_manager
        self.commands_interpreter_callback = commands_interpreter_callback

        self.logger.debug("ChildProcessCommunicationHandler initialized")

    def send_command(self, command, data=None):
        """
        Sends a command to the parent process.
        """
        self.logger.info("send_command")
        if data is not None:
            command_data = (command, data)
        else:
            command_data = (command,)

        self.ipc_manager.send_command_to_master(*command_data)
        self.ipc_manager.trigger_master_command_event()

    def wait_for_command(self):
        """
        Waits for incoming commands from the parent process and interprets them.
        """
        self.logger.debug("START - Child process: wait_for_command")

        while True:
            self.logger.info("Child process: wait for command loop")
            self.ipc_manager.wait_for_child_command_event()

            message = self.ipc_manager.receive_command_from_master()
            if message is None:
                continue

            command = message["command"]
            if command == "stop_command_loop":
                break

            data = message["data"]
            self.command_interpreter(command=command, data=data)

        self.logger.debug("STOP - Child process: wait_for_command")

    def command_interpreter(self, **kwargs):
        """
        Interprets the received command and data.
        """
        self.logger.info("command_interpreter")
        self.commands_interpreter_callback(**kwargs)

"""a"""
from logging_utils import CustomLogger

class ProcessGhi():
    """a"""
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.communication_handler = None
        self.logger = CustomLogger("processes.ProcessGhi", parent_logger_name="processes.ProcessDef")

    def set_communication_handler(self, communication_handler):
        """Set the communication handler after initialization."""
        self.communication_handler = communication_handler

    def run_wait_loop(self):
        """a"""
        self.communication_handler.start_command_thread()

    def commands_interpreter_callback(self, **kwargs):
        """a"""
        command = kwargs.get("command", None)
        data = kwargs.get("data", None)

        if command == 'message':
            self.cmd_message(data)
        elif command =='stop_command_loop':
            self.communication_handler.send_command("child_finish")
            self.communication_handler.stop_command_thread()

    def cmd_message(self, data):
        """a"""
        self.logger.message("New message from parent: " + str(data))
        self.communication_handler.send_command("message", data)

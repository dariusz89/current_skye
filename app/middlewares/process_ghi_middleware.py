"""a"""
from logging_utils import CustomLogger
from multiprocessing_utils import BaseProcess

class ProcessGhiMiddleware(BaseProcess):
    """a"""
    def __init__(self, process_class, start_method="spawn"):
        super().__init__(
            process_class,
            "run_wait_loop",
            self.command_interpreter,
            process_class.__name__,
            args=(),
            start_method=start_method
        )
        self.logger = CustomLogger(
            "middlewares.ProcessGhiMiddleware",
            parent_logger_name="processes.ProcessDef"
        )

    def command_interpreter(self, **kwargs):
        """a"""
        command = kwargs.get("command", None)
        data = kwargs.get("data", None)
        if command == "message":
            self.logger.message("New message from child: %s", data)
        elif command == "child_finish":
            self.stop_process()

    def cmd_start(self):
        """a"""
        self.start_process()

    def cmd_stop(self):
        """a"""
        self.parent_communication_handler.send_command("stop_command_loop")

    def cmd_message(self, data):
        """a"""
        self.parent_communication_handler.send_command("message", data)

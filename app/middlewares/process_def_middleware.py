"""a"""
from logging_utils import CustomLogger
from multiprocessing_utils import BaseProcess
from my_processes import ProcessGhi
from .process_ghi_middleware import ProcessGhiMiddleware

class ProcessDefMiddleware(BaseProcess):
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
            "middlewares.ProcessDefMiddleware",
            parent_logger_name="App"
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

    def cmd_run_process(self):
        """test_process_def()"""
        # Initialize new process
        process_ghi = ProcessGhiMiddleware(ProcessGhi)
        # Start process
        process_ghi.cmd_start()
        # ----------------------------------------
        import time
        self.logger.info("Loop started for 1 seconds")
        duration_ms = 3000
        start_time = time.time() * 1000
        while (time.time() * 1000) - start_time < duration_ms:
            # Send command
            process_ghi.cmd_message("Hello from Test")

            time.sleep(1)
        self.logger.info("Loop finished after 1 seconds")
        # ----------------------------------------
        # Stop process
        process_ghi.cmd_stop()
        self.logger.critical("process_ghi() - done")

    def cmd_message(self, data):
        """a"""
        self.parent_communication_handler.send_command("message", data)

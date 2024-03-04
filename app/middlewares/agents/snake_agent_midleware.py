"""
Module: snake_agent_midleware.py
"""
from logging_utils import CustomLogger
from agents import SnakeAgent
from multiprocessing_utils import BaseProcess

class SnakeAgentMiddleware(BaseProcess):
    """Middleware class for running an SnakeAgent process."""
    def __init__(
            self,
            start_method="spawn"
        ):
        super().__init__(
            SnakeAgent,
            "run_wait_loop",
            self.command_interpreter,
            args=(),
            start_method=start_method
        )
        self.logger = CustomLogger("middlewares.SnakeAgentMiddleware", parent_logger_name="App")
        self.logger.debug("SnakeAgentMiddleware initialized")

    def start(self):
        """Starts the SnakeAgent process."""
        self.logger.info("start")
        self.start_process()

    def stop(self):
        """Stops the SnakeAgent process."""
        self.logger.info("stop")
        self.stop_process()

    def cmd_message(self, data):
        """Sends a command to the SnakeAgent process to pass a message."""
        self.logger.info("cmd_message")
        self.communication_handler.send_command("message", data)

    def cmd_run_client(self, data):
        """Sends a command to the SnakeAgent process to run socketio client."""
        self.logger.info("cmd_run_client")
        self.communication_handler.send_command("run_client", data)

    def command_interpreter(self, **kwargs):
        """Callback function for interpreting commands received from the SnakeAgent process."""
        command = kwargs.get("command", None)
        data = kwargs.get("data", None)
        if command == "message":
            self.logger.message("New message from child: %s", data)

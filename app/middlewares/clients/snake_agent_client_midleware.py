"""
Module: snake_agent_client_midleware.py
"""
from logging_utils import CustomLogger
from clients import SnakeAgentClient
from multiprocessing_utils import BaseProcess

class SnakeAgentClientMiddleware(BaseProcess):
    """Middleware class for running an SnakeAgentClient process."""
    def __init__(
            self,
            server_url,
            namespace,
            token,
            transport,
            start_method="spawn"
        ):
        super().__init__(
            SnakeAgentClient,
            "run_wait_loop",
            self.command_interpreter,
            args=(server_url, namespace, token, transport),
            start_method=start_method
        )
        self.logger = CustomLogger("middlewares.SnakeAgentClientMiddleware", parent_logger_name="App")
        self.logger.debug("SnakeAgentClientMiddleware initialized")

    def start(self):
        """Starts the SnakeAgentClient process."""
        self.logger.info("start")
        self.start_process()

    def stop(self):
        """Stops the SnakeAgentClient process."""
        self.logger.info("stop")
        self.stop_process()

    def cmd_emit_welcome(self):
        """Sends a command to the SnakeAgentClient process to emit a welcome message."""
        self.logger.info("cmd_emit_welcome")
        self.communication_handler.send_command("emit_welcome", "Gówniarzu jebany zajebany!")

    def cmd_disconnect(self):
        """Sends a command to the SnakeAgentClient process to disconnect and stops the process."""
        self.logger.info("cmd_disconnect")
        self.communication_handler.send_command("disconnect")

    def cmd_message(self, data):
        """Sends a command to the SnakeAgentClient process to pass a message."""
        self.logger.info("cmd_message")
        self.communication_handler.send_command("message", data)

    def command_interpreter(self, **kwargs):
        """Callback function for interpreting commands
        received from the SnakeAgentClient process."""
        command = kwargs.get("command", None)
        data = kwargs.get("data", None)
        if command == "message":
            self.logger.info("New message from child: %s",data)

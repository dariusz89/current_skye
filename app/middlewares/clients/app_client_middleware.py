"""
Module: app_client_middleware.py
"""
from logging_utils import CustomLogger
from clients import AppClient
from multiprocessing_utils import BaseProcess

class AppClientMiddleware(BaseProcess):
    """
    Middleware class for running an AppClient process.
    """
    def __init__(
            self,
            server_url,
            namespace,
            token,
            transport,
            start_method="spawn"
        ):
        """
        Initializes an instance of the AppClientMiddleware class.
        """
        super().__init__(
            AppClient,
            "run_wait_loop",
            self.command_interpreter,
            args=(server_url, namespace, token, transport),
            start_method=start_method
        )
        self.logger = CustomLogger("middlewares.AppClientMiddleware", parent_logger_name="App")
        self.logger.debug("AppClientMiddleware initialized")

    def start(self):
        """
        Starts the AppClient process.
        """
        self.logger.info("start")
        self.start_process()

    def stop(self):
        """
        Stops the AppClient process.
        """
        self.logger.info("stop")
        self.stop_process()

    def cmd_emit_welcome(self):
        """
        Sends a command to the AppClient process to emit a welcome message.
        """
        self.logger.info("cmd_emit_welcome")
        self.communication_handler.send_command("emit_welcome", "Jasiu Stasiu!")

    def cmd_disconnect(self):
        """
        Sends a command to the AppClient process to disconnect and stops the process.
        """
        self.logger.info("cmd_disconnect")
        self.communication_handler.send_command("disconnect")

    def cmd_message(self, data):
        """
        Sends a command to the AppClient process to pass a message.
        """
        self.logger.info("cmd_message")
        self.communication_handler.send_command("message", data)

    def command_interpreter(self, **kwargs):
        """
        Callback function for interpreting commands received from the AppClient process.
        """
        command = kwargs.get("command", None)
        data = kwargs.get("data", None)
        if command == "message":
            self.logger.message("New message from child: %s", data)

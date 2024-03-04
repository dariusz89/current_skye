"""
Module: snake_agent_client.py
"""
from logging_utils import CustomLogger
from .base_client import BaseClient

class SnakeAgentClient(BaseClient):
    """
    App socketio client.
    """
    def __init__(
            self,
            ipc,
            server_url,
            namespace,
            token,
            transport
        ):
        """
        Initializes the SnakeAgentClient.
        """
        super().__init__(ipc, server_url, namespace, token, transport)
        self.logger = CustomLogger("clients.SnakeAgentClient", parent_logger_name="App")
        self.logger.add_third_party_logger(self.sio.logger)
        self.logger.debug("AppClient initialized")

    def commands_interpreter_callback(self, **kwargs):
        """
        Callback function for interpreting commands.
        """
        command = kwargs.get("command", None)
        data = kwargs.get("data", None)
        super().commands_interpreter_callback(command=command)
        if command == 'emit_welcome':
            self.welcome(data)
            self.logger.info("emit_welcome command was executed")

    def callbacks(self):
        """
        Event handlers declarations.
        """
        super().callbacks()
        self.sio.on(
            event="welcome",
            handler=self.on_welcome,
            namespace=self.namespace
        )
        self.sio.on(
            event="test_environment",
            handler=self.on_test_environment,
            namespace=self.namespace
        )

    def on_welcome(self, data):
        """
        On 'welcome' event handler.
        """
        self.logger.info("on_welcome")
        self.communication_handler.send_command("message", data)

    def on_test_environment(self, data):
        """
        On 'test_environment' event handler.
        """
        self.logger.info("on_test_environment")
        self.communication_handler.send_command("message", data)

    def welcome(self, data):
        """
        Emits a 'welcome' event.
        """
        try:
            self.sio.emit(event="welcome", data = data, namespace = self.namespace)
        except self.exception.BadNamespaceError as e:
            self.logger.warning("SocketIO Bad Namespace Error: %s", str(e), exc_info=True)

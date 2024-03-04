"""
Module: base_client.py
"""
import threading
import socketio
from logging_utils import CustomLogger
from multiprocessing_utils import ChildProcessCommunicationHandler as CommunicationHandler

class BaseClient():
    """
    Base socket.io client for handling communication with a server.
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
        Initializes an instance of the BaseClient class.
        """
        self.logger = CustomLogger("clients.BaseClient", parent_logger_name="App")
        self.server_url = server_url
        self.namespace = namespace
        self.token = token
        self.transport = transport
        self.sio = socketio.Client(logger=True)
        self.logger.add_third_party_logger(self.sio.logger)

        self.wait_thread = threading.Thread(
            target=self.sio.wait
        )
        self.communication_handler = CommunicationHandler(
            ipc,
            self.commands_interpreter_callback
        )
        self.exception = socketio.exceptions
        self.logger.debug("BaseClient initialized")

    def commands_interpreter_callback(self, **kwargs):
        """
        Callback function for interpreting commands received from the parent process.
        """
        command = kwargs.get("command", None)
        if command == 'disconnect':
            self.close()
            self.logger.info("disconnect command was executed")

    def run_wait_loop(self):
        """
        Runs the Socket.IO client and keeps it alive by waiting for commands and incomming events.
        """
        self.run()
        self.communication_handler.wait_for_command()
        self.wait_thread.start()

    def run(self):
        """
        Starts the Socket.IO client, connects to the server, and sets up event handlers.
        """
        self.callbacks()
        try:
            self.sio.connect(
                url=self.server_url,
                namespaces=[self.namespace],
                auth={"token":self.token},
                transports=[self.transport]
            )
        except socketio.exceptions.ConnectionError as e:
            self.logger.error("SocketIO Connection Error: %s", str(e), exc_info=True)

    def callbacks(self):
        """
        Declares event handlers for 'connect' and 'disconnect' events.
        """
        self.sio.on(
            event="connect",
            handler=self.on_connect,
            namespace=self.namespace
        )
        self.sio.on(
            event="disconnect",
            handler=self.on_disconnect,
            namespace=self.namespace
        )

    def on_connect(self):
        """
        Event handler for the 'connect' event.
        """
        self.logger.info("on_connect")
        self.communication_handler.send_command("message", "Base client is connected")

    def on_disconnect(self):
        """
        Event handler for the 'disconnect' event.
        """
        self.logger.info("on_disconnect")
        self.communication_handler.send_command("message", "Base client has been disconnected")

    def close(self):
        """
        Disconnects the Socket.IO client from the server.
        """
        self.logger.info("close")
        if self.sio.connected:
            self.sio.disconnect()

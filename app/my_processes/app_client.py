"""a"""
import threading
import socketio
from logging_utils import CustomLogger

class AppClient():
    """a"""
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.communication_handler = None
        self.logger = CustomLogger("processes.AppClient", parent_logger_name="App")
        self.sio = socketio.Client(logger=True)
        self.logger.add_third_party_logger(self.sio.logger)
        self.server_url = "ws://127.0.0.1:5000"
        self.namespace = "/snake"
        self.token = "snake"
        self.transport = "websocket"
        self.socket_io_wait_thread = None

    def set_communication_handler(self, communication_handler):
        """Set the communication handler after initialization."""
        self.communication_handler = communication_handler

    def run_wait_loop(self):
        """a"""
        self.runSocketIOClient()
        self.communication_handler.start_command_thread()

    def commands_interpreter_callback(self, **kwargs):
        """a"""
        command = kwargs.get("command", None)
        data = kwargs.get("data", None)

        if command == 'message':
            self.cmd_message(data)
        elif command =='stop_command_loop':
            self.closeSocketIOClient()
            self.communication_handler.send_command("child_finish")
            self.communication_handler.stop_command_thread()

    def cmd_message(self, data):
        """a"""
        self.logger.message("New message from parent: " + str(data))
        self.communication_handler.send_command("message", data)

    def runSocketIOClient(self):
        """
        Starts the Socket.IO client, connects to the server, and sets up event handlers.
        """
        self.wait_thread = threading.Thread(
            target=self.sio.wait
        )
        self.wait_thread.start()
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

    def closeSocketIOClient(self):
        self.sio.shutdown()
        self.wait_thread.join()
        self.logger.info("close")

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
        self.communication_handler.send_command("message", "App client is connected")

    def on_disconnect(self):
        """
        Event handler for the 'disconnect' event.
        """
        self.logger.info("on_disconnect")
        self.communication_handler.send_command("message", "App client has been disconnected")

    

            
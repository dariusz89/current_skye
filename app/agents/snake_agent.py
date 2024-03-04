"""
Module: snake_agent.py
"""
import time

from logging_utils import CustomLogger
from multiprocessing_utils import ChildProcessCommunicationHandler as CommunicationHandler
from middlewares.clients import SnakeAgentClientMiddleware

class SnakeAgent():
    """App socketio client."""
    def __init__(
            self,
            ipc
        ):
        self.logger = CustomLogger("agents.SnakeAgent", parent_logger_name="App")
        self.communication_handler = CommunicationHandler(
            ipc,
            self.commands_interpreter_callback
        )
        self.logger.debug("SnakeAgent initialized")

    def commands_interpreter_callback(self, **kwargs):
        """Callback function for interpreting commands."""
        command = kwargs.get("command", None)
        data = kwargs.get("data", None)

        if command == 'message':
            self.cmd_message(data)
            self.logger.info("message command was executed")
        elif command == 'run_client':
            self.cmd_run_client(data)
            self.logger.info("message command was executed")

    def run_wait_loop(self):
        """Waiting for commands."""
        self.communication_handler.wait_for_command()

    def cmd_message(self, data):
        """Sends a command to the AppClient process to pass a message"""
        self.logger.info("cmd_message")
        self.logger.message("New message from parent: " + str(data))
        self.communication_handler.send_command("message", data)

    def cmd_run_client(self, data):
        """Run socketio client"""
        self.logger.info("cmd_message")
        self.logger.message("New message from parent: " + str(data))

        # Initialize new process
        snake_agent_client = SnakeAgentClientMiddleware(
            data['server_url'],
            data['namespace'],
            data['token'],
            data['transport']
        )

        # Start process
        snake_agent_client.start()

        # ----------------------------------------
        self.logger.info("Loop started for 5 seconds")
        duration_ms = 5000
        start_time = time.time() * 1000
        while (time.time() * 1000) - start_time < duration_ms:
            snake_agent_client.cmd_emit_welcome()
            data = "Snake agent emitted welcome event to /snake namespace"
            self.communication_handler.send_command("message", data)
            time.sleep(1)
        self.logger.info("Loop finished after 5 seconds")
        # ----------------------------------------

        # Send command
        snake_agent_client.cmd_disconnect()

        # Stop process
        snake_agent_client.stop()

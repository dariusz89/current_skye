"""Skye app"""
import time
from middlewares.clients import AppClientMiddleware
from middlewares.agents import SnakeAgentMiddleware
from logging_utils import CustomLogger

def main(server_url, namespace, transport):
    """The main function"""
    logger = CustomLogger("App", CustomLogger.DEBUG)
    token = "skye"

    # Initialize new process
    app_client = AppClientMiddleware(server_url, namespace, token, transport)

    # Start process
    app_client.start()

    # ----------------------------------------
    snake_agent = SnakeAgentMiddleware()
    snake_agent.start()
    data = {
        "server_url": "ws://127.0.0.1:5000",
        "namespace": "/snake",
        "token": "snake",
        "transport": "websocket"
    }
    snake_agent.cmd_run_client(data)
    # ----------------------------------------
    logger.info("Loop started for 60 seconds")
    duration_ms = 10000
    start_time = time.time() * 1000
    while (time.time() * 1000) - start_time < duration_ms:
        # Send command
        app_client.cmd_emit_welcome()
        snake_agent.cmd_message("Hello from App, snakeAgent")
        time.sleep(1)  # Sleep for 1 second
    logger.info("Loop finished after 60 seconds")

    # Send command
    app_client.cmd_disconnect()

    # ----------------------------------------
    snake_agent.stop()
    # ----------------------------------------

    # Stop process
    app_client.stop()

if __name__ == '__main__':
    # Websocket server connection information
    SERVER_URL = "ws://127.0.0.1:5000"
    NAMESPACE = "/skye"
    TRANSPORT = "websocket"
    main(SERVER_URL, NAMESPACE, TRANSPORT)

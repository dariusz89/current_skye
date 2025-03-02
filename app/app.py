"""Test.py"""
import time

from my_processes import AppClient
from middlewares import AppClientMiddleware

from logging_utils import CustomLogger

def main():
    """main()"""
    # Initialize new process
    appClient = AppClientMiddleware(AppClient)
    # Start process
    appClient.cmd_start()
    # ----------------------------------------
    # Run child process
    duration_ms = 10000
    start_time = time.time() * 1000
    while (time.time() * 1000) - start_time < duration_ms:
        # Send command
        appClient.cmd_message("Hello from AppClient")
        # Run child process
        appClient.cmd_run_process()
        time.sleep(1)
    # ----------------------------------------
    # Stop process
    appClient.cmd_stop()

logger = CustomLogger("App", CustomLogger.INFO)
if __name__ == '__main__':
    main()
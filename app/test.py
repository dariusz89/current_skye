"""Test.py"""
import time

from my_processes import ProcessDef
from middlewares import ProcessDefMiddleware

from logging_utils import CustomLogger

def test_process_def():
    """test_process_def()"""
    # Initialize new process
    process_def = ProcessDefMiddleware(ProcessDef)
    # Start process
    process_def.cmd_start()
    # ----------------------------------------
    # Run child process
    process_def.cmd_run_process()
    logger.info("Loop started for 1 seconds")
    duration_ms = 2000
    start_time = time.time() * 1000
    while (time.time() * 1000) - start_time < duration_ms:
        # Send command
        process_def.cmd_message("Hello from Test")
        # Run child process
        process_def.cmd_run_process()
        time.sleep(1)
    logger.info("Loop finished after 1 seconds")
    # ----------------------------------------
    # Stop process
    process_def.cmd_stop()

def main():
    """main()"""
    # test_process_def()
    # x = 5
    # while x > 0:
    #     x = x - 1
    #     test_process_def()
    # logger.critical("test_process_def() done")

logger = CustomLogger("Test", CustomLogger.INFO)
if __name__ == '__main__':
    main()
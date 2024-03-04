"""
Module: inter_process_communication_manager.py
"""
import multiprocessing
from logging_utils import CustomLogger

class InterProcessCommunicationManager:
    """
    Manages inter-process communication between a parent and a child process.
    """
    def __init__(self, timeout):
        """
        Initializes an instance of the InterProcessCommunicationManager.
        """
        self.logger = CustomLogger("multiprocessing_utils.InterProcessCommunicationManager", parent_logger_name="App")
        self.timeout = timeout

        self.to_child_command_queue = multiprocessing.Queue()
        self.child_command_event = multiprocessing.Event()

        self.to_master_command_queue = multiprocessing.Queue()
        self.master_command_event = multiprocessing.Event()

        self.logger.debug("IPCManager initialized")

    def send_command_to_child(self, command, data=None):
        """
        Sends a command to the child process.
        """
        self.logger.debug("send_command_to_child")
        message = {'command': command, 'data': data}
        self.to_child_command_queue.put(message)

    def send_command_to_master(self, command, data=None):
        """
        Sends a command to the parent process.
        """
        self.logger.debug("send_command_to_master")
        message = {'command': command, 'data': data}
        self.to_master_command_queue.put(message)

    def receive_command_from_master(self):
        """
        Receives a command from the parent process.
        """
        self.logger.debug("receive_command_from_master")
        data = None

        if self.child_command_event.is_set():
            try:
                self.logger.info("Child Command event is set")
                data = self.to_child_command_queue.get(timeout=self.timeout)
            except multiprocessing.TimeoutError:
                self.logger.warning(
                    "Timeout occurred while waiting for a command from the parent process"
                )

            self.child_command_event.clear()
        else:
            self.logger.info("Child Command event is not set")

        return data

    def receive_command_from_child(self):
        """
        Receives a command from the child process.
        """
        self.logger.debug("receive_command_from_child")
        data = None

        if self.master_command_event.is_set():
            try:
                self.logger.info("Master Command event is set")
                data = self.to_master_command_queue.get(timeout=self.timeout)
            except multiprocessing.TimeoutError:
                self.logger.warning(
                    "Timeout occurred while waiting for a command from the child process"
                )

            self.master_command_event.clear()
        else:
            self.logger.info("Master Command event is not set")

        return data

    def trigger_child_command_event(self):
        """
        Triggers the event signaling the availability of commands for the child process.
        """
        self.logger.debug("trigger_child_command_event")
        self.child_command_event.set()

    def trigger_master_command_event(self):
        """
        Triggers the event signaling the availability of commands for the parent process.
        """
        self.logger.debug("trigger_master_command_event")
        self.master_command_event.set()

    def wait_for_child_command_event(self):
        """
        Waits for the event signaling the availability of commands for the child process.
        """
        self.logger.debug("wait_for_child_command_event")

        try:
            if not self.child_command_event.is_set():
                self.logger.info("Child Command event is not set")
                self.child_command_event.wait(timeout=self.timeout)
        except multiprocessing.TimeoutError:
            self.logger.warning("Timeout occurred while waiting for the child command event")

    def wait_for_master_command_event(self):
        """
        Waits for the event signaling the availability of commands for the parent process.
        """
        self.logger.debug("wait_for_master_command_event")

        try:
            if not self.master_command_event.is_set():
                self.logger.info("Master Command event is not set")
                self.master_command_event.wait(timeout=self.timeout)
        except multiprocessing.TimeoutError:
            self.logger.warning("Timeout occurred while waiting for the master command event")

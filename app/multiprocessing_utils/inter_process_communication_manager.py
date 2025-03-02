"""a"""
import multiprocessing
import multiprocessing.queues
from logging_utils import CustomLogger

class InterProcessCommunicationManager:
    """a"""
    def __init__(self, timeout):
        """a"""
        self.logger = CustomLogger(
            "multiprocessing_utils.InterProcessCommunicationManager",
            parent_logger_name="App"
        )
        self.timeout = timeout
        self.to_child_command_queue = multiprocessing.Manager().Queue()
        self.child_command_event = multiprocessing.Event()
        self.to_master_command_queue = multiprocessing.Manager().Queue()
        self.master_command_event = multiprocessing.Event()

    def send_command_to_child(self, command, data=None):
        """a"""
        message = {'command': command, 'data': data}
        self.to_child_command_queue.put(message)

    def send_command_to_master(self, command, data=None):
        """a"""
        message = {'command': command, 'data': data}
        self.to_master_command_queue.put(message)

    def receive_command_from_master(self):
        """a"""
        data = None

        if self.child_command_event.is_set():
            self.child_command_event.clear()
            try:
                data = self.to_child_command_queue.get(timeout=self.timeout)
            except multiprocessing.queues.Empty:
                pass
            

        return data

    def receive_command_from_child(self):
        """a"""
        data = None

        if self.master_command_event.is_set():
            self.master_command_event.clear()
            try:
                data = self.to_master_command_queue.get(timeout=self.timeout)
            except multiprocessing.queues.Empty:
                pass
            

        return data

    def trigger_child_command_event(self):
        """a"""
        self.child_command_event.set()

    def trigger_master_command_event(self):
        """a"""
        self.master_command_event.set()

    def wait_for_child_command_event(self):
        """a"""
        if not self.child_command_event.is_set():
            self.child_command_event.wait(timeout=self.timeout)

    def wait_for_master_command_event(self):
        """a"""
        if not self.master_command_event.is_set():
            self.master_command_event.wait(timeout=self.timeout)

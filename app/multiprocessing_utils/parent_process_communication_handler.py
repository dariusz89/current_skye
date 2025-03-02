"""a"""
from logging_utils import CustomLogger
from .base_communication_handler import BaseCommunicationHandler

class ParentProcessCommunicationHandler(BaseCommunicationHandler):
    """a"""
    def __init__(self, ipc_manager, commands_interpreter_callback):
        """a"""
        super().__init__(
            commands_interpreter_callback=commands_interpreter_callback
        )
        self.logger = CustomLogger(
            "multiprocessing_utils.ParentProcessCommunicationHandler",
            parent_logger_name="App"
        )
        self._ipc_manager = ipc_manager

    def _extend_send_command(self, *command_data):
        """a"""
        self._ipc_manager.send_command_to_child(*command_data)
        self._ipc_manager.trigger_child_command_event()

    def _extend_wait_for_command(self):
        """a"""
        self._ipc_manager.wait_for_master_command_event()
        return self._ipc_manager.receive_command_from_child()

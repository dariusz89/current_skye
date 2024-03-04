"""
Module: base_process.py
"""
import multiprocessing
from logging_utils import CustomLogger
from .inter_process_communication_manager import InterProcessCommunicationManager
from .parent_process_communication_handler import ParentProcessCommunicationHandler

class BaseProcess:
    """
    Represents a base class for creating child processes with communication capabilities.
    """
    def __init__(
            self,
            clazz,
            method_name,
            commands_interpreter,
            args=(),
            start_method=multiprocessing.get_start_method()
        ):
        """
        Initializes an instance of the BaseProcess class.
        """
        self.logger = CustomLogger("multiprocessing_utils.BaseProcess", parent_logger_name="App")
        self._validate_class(clazz)
        self._validate_method(clazz, method_name)

        self._clazz = clazz
        self._method_name = method_name

        self._ipc_manager = InterProcessCommunicationManager(timeout=10)
        self._args = (self._ipc_manager,) + args
        self._start_method = start_method
        self._process = None

        self.pid = None
        self.communication_handler = ParentProcessCommunicationHandler(
            self._ipc_manager,
            commands_interpreter
        )

        self.logger.debug("ParentProcess initialized")

    def _validate_class(self, clazz):
        """
        Validates if the provided class is a type or a callable object.
        """
        self.logger.debug("_validate_class")
        if not (isinstance(clazz, type) or callable(clazz)):
            self.logger.error("%s is not a type or a callable class", clazz)
            raise TypeError(f"{clazz} is not a type or a callable class")

    def _validate_method(self, clazz, method_name):
        """
        Validates if the provided class has a callable method with the specified name.
        """
        self.logger.debug("_validate_method")
        if not hasattr(clazz, method_name) or not callable(getattr(clazz, method_name)):
            self.logger.error(
                "%s does not have a callable method named %s",
                clazz.__name__,
                method_name
            )
            raise AttributeError(
                f"{clazz.__name__} does not have a callable method named {method_name}"
            )

    def _call_method(self, instance):
        """
        Calls the specified method on the provided instance.
        """
        self.logger.debug("_call_method")
        getattr(instance, self._method_name)()

    def _fork_process(self):
        """
        Prepares and returns a multiprocessing Process instance using the 'fork' start method.
        """
        self.logger.debug("_fork_process")
        obj = self._clazz(*self._args)
        return multiprocessing.Process(target=self._call_method, args=(obj,))

    def _spawn_process(self):
        """
        Prepares and returns a multiprocessing Process instance using the 'spawn' start method.
        """
        self.logger.debug("_spawn_process")
        return multiprocessing.Process(target=self._prepare_spawn_process)

    def _prepare_spawn_process(self):
        """
        Prepares the child process for 'spawn' start method 
        by instantiating the class and calling the method.
        """
        self.logger.debug("_prepare_spawn_process")
        obj = self._clazz(*self._args)
        self._call_method(obj)

    def start_process(self):
        """
        Starts the child process and its command thread.
        """
        self.logger.debug("Start method: %s", self._start_method)

        if self._start_method == 'spawn':
            self._process = self._spawn_process()
        elif self._start_method == 'fork':
            self._process = self._fork_process()
        else:
            raise ValueError(f"Unsupported start method: {self._start_method}")

        self._process.start()
        self.pid = self._process.pid
        self.logger.info("Child Process PID: %s", self.pid)

        self.communication_handler.start_command_thread()

    def stop_process(self):
        """
        Stops the child process by sending a stop command and joining the process.
        """
        self.communication_handler.send_command("stop_command_loop")
        self.logger.debug("stop_command_loop")
        self.communication_handler.stop_command_thread()
        self.logger.debug("stop_process")
        self._process.join()

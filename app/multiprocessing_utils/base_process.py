"""a"""
import multiprocessing
from logging_utils import CustomLogger
from .inter_process_communication_manager import InterProcessCommunicationManager
from .parent_process_communication_handler import ParentProcessCommunicationHandler
from .child_process_communication_handler import ChildProcessCommunicationHandler

class BaseProcess:
    """a"""
    def __init__(
            self,
            clazz,
            method_name,
            commands_interpreter,
            process_name,
            args=None,
            kwargs=None,
            start_method=multiprocessing.get_start_method()
        ):
        """a"""
        self.process_name = process_name
        self.logger = CustomLogger("multiprocessing_utils.BaseProcess", parent_logger_name="App")
        self._validate_class(clazz)
        self._validate_method(clazz, method_name)
        self._validate_method(clazz, 'commands_interpreter_callback')

        self._clazz = clazz
        self._method_name = method_name

        self._ipc_manager = InterProcessCommunicationManager(timeout=10)
        self.parent_communication_handler = ParentProcessCommunicationHandler(
            self._ipc_manager,
            commands_interpreter
        )
        self.child_communication_handler = None

        self._args = args if args is not None else ()
        self._kwargs = kwargs if kwargs is not None else {}
        self._start_method = start_method
        self._process = None

        self.pid = None

    def _validate_class(self, clazz):
        """a"""
        if not (isinstance(clazz, type) or callable(clazz)):
            raise TypeError(f"{clazz} is not a type or a callable class")

    def _validate_method(self, clazz, method_name):
        """a"""
        if not hasattr(clazz, method_name) or not callable(getattr(clazz, method_name)):
            raise AttributeError(
                f"{clazz.__name__} does not have a callable method named {method_name}"
            )

    def _initialize_child_communication_handler(self, instance):
        """Initialize the child communication handler with the instance's callback."""
        commands_interpreter_callback = getattr(instance, 'commands_interpreter_callback')
        self.child_communication_handler = ChildProcessCommunicationHandler(
            self._ipc_manager,
            commands_interpreter_callback
        )
        instance.set_communication_handler(self.child_communication_handler)

    def _call_method(self, instance):
        """a"""
        getattr(instance, self._method_name)()

    def _fork_process(self):
        """a"""
        instance = self._clazz(*self._args, **self._kwargs)
        self._initialize_child_communication_handler(instance)

        return multiprocessing.Process(
            target=self._call_method,
            name=self.process_name,
            args=(instance,)
        )

    def _spawn_process(self):
        """a"""
        return multiprocessing.Process(
            target=self._prepare_spawn_process, 
            name=self.process_name
        )

    def _prepare_spawn_process(self):
        """a"""
        instance = self._clazz(*self._args, **self._kwargs)
        self._initialize_child_communication_handler(instance)
        self._call_method(instance)

    def start_process(self):
        """a"""
        if self._start_method == 'spawn':
            self._process = self._spawn_process()
        elif self._start_method == 'fork':
            self._process = self._fork_process()
        else:
            raise ValueError(f"Unsupported start method: {self._start_method}")

        self._process.start()
        self.pid = self._process.pid
        self.parent_communication_handler.start_command_thread()

    def stop_process(self):
        """a"""
        self.parent_communication_handler.stop_command_thread()
        self._process.join()

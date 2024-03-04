"""Socket.IO Server"""
import socketio
from .adapters.logger import PythonSocketIOLoggerAdapter
from .events import Home
from .events import Snake
from .events import Skye

def prepare_app(socketio_server, development_mode):
    """Prepare application"""
    socketio_server.logger = PythonSocketIOLoggerAdapter(
        logger = socketio_server.logger,
        prefix = 'SOCKET.IO [server]'
    )
    socketio_server.eio.logger = PythonSocketIOLoggerAdapter(
        logger = socketio_server.eio.logger,
        prefix = 'ENGINE.IO [server]'
    )

    socketio_server.register_namespace(
        namespace_handler=Skye('/skye')
    )
    socketio_server.register_namespace(
        namespace_handler=Home('/home')
    )
    socketio_server.register_namespace(
        namespace_handler=Snake('/snake')
    )

    if development_mode:
        # development only
        static_files = {
            '/': "./public/home.html",
            '/snake': "./public/snake.html",
            '/static': "./public/static",
        }
        return socketio.ASGIApp(
            socketio_server=socketio_server,
            static_files=static_files
        )
    else:
        return socketio.ASGIApp(
        socketio_server=socketio_server
    )

def create_app(development_mode=False):
    """App factory"""
    sio = socketio.AsyncServer(
        async_mode = "asgi",
        logger = development_mode,
        engineio_logger = development_mode
    )

    return prepare_app(sio, development_mode)

app = create_app(development_mode=True)

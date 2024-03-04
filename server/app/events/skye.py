"""Events handlers for "/skye" namespace"""
from .. import socketio

class Skye(socketio.AsyncNamespace):
    """Class-Based Namespace for "/skye" namespace"""
    async def on_connect(self, sid, environ, data):
        """On 'connect' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: environemnt ->", environ)
        print("SERVER: client ->", sid)
        print("SERVER: data ->", data)
        print("SERVER: event[connect]", sid)

    async def on_disconnect(self, sid):
        """On 'disconnect' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: event[disconnect] ->", sid)

    async def on_welcome(self, sid, data):
        """On 'welcome' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: data ->", data)
        print("SERVER: event[welcome] ->", sid)
        await self.emit(
            event = "welcome",
            data = data,
            namespace=self.namespace
        )

    async def on_done(self, sid):
        """Disconnect on done"""
        await self.disconnect(sid=sid, namespace=self.namespace)

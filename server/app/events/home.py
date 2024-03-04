"""Events handlers for "/home" namespace"""
from .. import socketio

class Home(socketio.AsyncNamespace):
    """Class-Based Namespace for "/home" namespace"""
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

    async def on_start_agent(self, sid):
        """On 'start_agent' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: event[Start agent] ->", sid)
        print("=====")
        print("SERVER: Starting agent ->", sid)
        print("=====")

    async def on_agent_is_up(self, sid):
        """On 'agent_is_up' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: event[agent_is_up] ->", sid)
        await self.emit(
            event='my_event',
            namespace=self.namespace
        )

    async def on_hello_from_agent(self, sid, data):
        """On 'hello_from_agent' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: data ->", data)
        print("SERVER: event[hello_from_agent] ->", sid)
        await self.emit(
            event='hello_from_agent',
            data=data,
            to=data["to"],
            namespace=self.namespace
        )

    async def on_hello_from_browser(self, sid, data):
        """On 'hello_from_browser' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: data ->", data)
        print("SERVER: event[hello_from_browser] ->", sid)
        data = {"by" : sid, "data": data["message"]}
        await self.emit(
            event='hello_from_browser',
            data=data,
            namespace=self.namespace
        )

    async def on_agent_done(self, sid):
        """On 'agent_done' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: event[agent_done] ->", sid)
        await self.emit(
            event = 'end_connection',
            to = sid,
            namespace=self.namespace
        )

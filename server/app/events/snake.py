"""Events handlers for "/snake" namespace"""
from .. import socketio

class Snake(socketio.AsyncNamespace):
    """Class-Based Namespace for "/snake" namespace"""
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

    async def on_game_options(self, sid):
        """On 'game_options' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: event[game_options] ->", sid)

        return {
            'dimensions' : {
                'x': 10,
                'y': 10
            },
            'food' : {
                'location' : {
                    'x': 3,
                    'y': 3
                }
            },
            'snake' : {
                'body' : [
                    {'x': 4, 'y': 4},
                    {'x': 5, 'y': 4},
                    {'x': 6, 'y': 4}
                ],
                'movement' : {
                    'top': True,
                    'bottom': True,
                    'left': True,
                    'right': False
                },
                'direction' : {
                    'top': False,
                    'bottom': False,
                    'left': True,
                    'right': False
                },
                'farsight' : 1
            }
        }

    async def on_start_training(self, sid):
        """On 'start_training' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: event[start_training] ->", sid)

    async def on_test_environment(self, sid):
        """On 'test_environment' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: event[test_environment] ->", sid)
        data = {
            "sid": sid,
            "namespace": self.namespace,
            "event": "test_environment"
        }
        await self.emit(
            event = "test_environment",
            data = data,
            namespace="/skye"
        )

    async def on_client_is_up(self, sid):
        """On 'agent_is_up' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: event[start_training] ->", sid)

    async def on_start_training_game(self, sid, data):
        """On 'start_game' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: data ->", data)
        print("SERVER: event[environment_data] ->", sid)
        await self.emit(
            event = "start_training_game",
            data = data,
            to = data["to"]
        )

    async def on_environment_data(self, sid, data):
        """On 'environment_data' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: data ->", data)
        print("SERVER: event[environment_data] ->", sid)

    async def on_environment_info(self, sid, data):
        """On 'environment_info' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: data ->", data)
        print("SERVER: event[environment_info] ->", sid)


    async def on_request_for_observation(self, sid, data):
        """On 'request_for_observation' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: data ->", data)
        print("SERVER: event[request_for_observation] ->", sid)
        await self.emit(
            event = "request_for_observation",
            data = data,
            to = data["to"]
        )

    async def on_request_for_info(self, sid, data):
        """On 'request_for_info' event handler"""
        print("SERVER: namespace ->", self.namespace)
        print("SERVER: client ->", sid)
        print("SERVER: data ->", data)
        print("SERVER: event[request_for_info] ->", sid)
        await self.emit(
            event = "request_for_info",
            data = data,
            to = data["to"]
        )

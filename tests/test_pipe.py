import unittest
import vodka
import vodka.load_entrypoints
import vodka.app
import vodka.instance
import vodka.data.renderers
import vodka.data.data_types
import vodka.storage
import vodka.log
import conftest
import time
import json

import xbahn.message
import xbahn.connection.link
from xbahn.connection import listen

@vodka.app.register('test_app')
class DummyApp(vodka.app.Application):
    @vodka.data.renderers.RPC(errors=True)
    def view(self, data, *args, **kwargs):
        data.extend(vodka.storage.get("xbahn_server.test"))

vodka.log.set_loggers(vodka.log.default_config(name="xbahn"))

CONFIG = {

    "apps": {
        "test_app" : { "enabled" : True }
    },

    "data": [
        {
            "type" : "xbahn_server.test",
            "handlers" : [
                {
                    "type" : "store",
                    "container" : "list",
                    "limit" : 10
                }
            ]
        }
    ],

    "plugins" : [
        {
            "type" : "xbahn",
            "name" : "xbahn_server",
            "connections" : [
                {
                    "name" : "main",
                    "connect" : conftest.URL_CONNECT
                }
            ]
        }
    ]
}

class TestCase(unittest.TestCase):
    """
    Test the vodka-xbahn implementation
    """

    def test_pipe(self):
        conn = listen(conftest.URL_LISTEN)
        link = xbahn.connection.link.Link(send=conn, receive=conn)

        vodka.data.data_types.instantiate_from_config(CONFIG.get("data"))
        plugin=vodka.plugin.get_instance(CONFIG["plugins"][0])
        vodka.instance.instantiate(CONFIG)
        vodka.start(thread_workers=[plugin])

        link.main.send("test", xbahn.message.Message("first"))
        link.main.send("test", xbahn.message.Message("second"))

        time.sleep(1.0)

        print(vodka.storage.storage)

        self.assertEqual(json.loads(vodka.instance.get_instance("test_app").view()), {"meta":{}, "data":["first","second"]})

        conn.destroy()
        plugin.disconnect()


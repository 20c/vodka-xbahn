import vodka
import vodka.app
import vodka.data.renderers
import vodka.storage

@vodka.app.register('test_app')
class MyApplication(vodka.app.WebApplication):

    @vodka.data.renderers.RPC(errors=True)
    def index(self, data, *args, **kwargs):
        data.extend(vodka.storage.get("xbahn_server.test"))

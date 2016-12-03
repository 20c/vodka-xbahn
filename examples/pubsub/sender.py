import xbahn.connection
import xbahn.connection.link
import xbahn.message

import time

if __name__ == "__main__":

    # connect to api server using zmq REQ sockect over TCP (default)
    connection = xbahn.connection.connect("zmq://0.0.0.0:7061/pub/test")
    link = xbahn.connection.link.Link(send=connection, receive=connection)

    # print whatever message we get back from the other end
    def handle_response(message=None, wire=None, event_origin=None):
        print(message.data)
    #link.on("receive", handle_response)

    # send a message to the other side and wait for response (using the main wire)
    while True:
        link.main.send("test", xbahn.message.Message([{"ts":time.time()}]))
        print("Sent message", time.time())
        time.sleep(1.0)

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import base64
import sys
from twisted.python import log
from twisted.internet import reactor

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            encoded_string = "test msg every 20ms"
            self.sendMessage(encoded_string.encode('utf8'))
            self.factory.reactor.callLater(0.2, hello)

        # start sending messages every 20ms ..
        # hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
        else:
            print("Text message received: {}".format(payload.decode('utf8')))

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:50007")
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    # note to self: if using putChild, the child must be bytes...

    reactor.listenTCP(50007, factory)
    reactor.run()
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import base64
import sys
from twisted.python import log
from twisted.internet import reactor
import json
import state
from state import *

board = Board({
    (0,0): Piece(ANT, 0),
    (-1,0): Piece(BEETLE, 1),
    (1,0): Piece(SPIDER, 0),
    (-1,1): Piece(GRASSHOPPER, 1),
    (2,1): Piece(QUEEN, 0),
})
board.next_player=0


# board.positions[0,0] = Piece object in that position


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        """
		def hello():
            encoded_string = "test msg every 20ms"
            self.sendMessage(encoded_string.encode('utf8'))
            self.factory.reactor.callLater(0.2, hello)

        # start sending messages every 20ms ..
        hello()
		"""

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
        else:
            print("Text message received: {}".format(payload.decode('utf8')))
            j = json.loads(payload.decode('utf8'))
        
        if j['action'] == "getBoardPieces":
            #boardPieces_lp = input list of board pieces as per python code (i.e. list of PIECE objects)
            #boardPieces_ld = converted list to be transformed into the json object (i.e. list of DICT objects)
            boardPieces_lp = list(board.my_pieces())
            boardPieces_lp.extend(list(board.opponent_pieces())) # board.my_pieces() returns an array (in python it is a GENERATOR, but we here convert it to a LIST) with positions which are tuples (x,y)
            boardPieces_ld = []
            for POS in boardPieces_lp:
                thisPiece = json.loads('{}') # creates a DICT object that can be turned into json
                thisPiece['player'] = board.positions[POS].player
                thisPiece['insect'] = board.positions[POS].insect
                thisPiece['col'] = POS[0]
                thisPiece['row'] = POS[1]
                boardPieces_ld.append(thisPiece)
        
            print('')
            print('Hardcoded board on server side:')
            print(json.dumps(boardPieces_ld))
            print('')

            jsonObj = json.loads('{}') # DICT object
            jsonObj['boardPieces'] = boardPieces_ld
            jsonObj['action'] = 'setBoardPieces'
            jsonData = json.dumps(jsonObj)
            self.sendMessage(jsonData.encode('utf8'), isBinary)
            return
            
            """
            data structure example from server to client:
            {
                "action":"setBoardPieces
                boardPieces":[
                    {"insect":"S","player":0,"row":0,"col":1},
                    {"insect":"A","player":0,"row":0,"col":0},
                    {"insect":"Q","player":0,"row":1,"col":2},
                    {"insect":"B","player":1,"row":0,"col":-1},
                    {"insect":"G","player":1,"row":1,"col":-1}
                ]
            }
            """


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
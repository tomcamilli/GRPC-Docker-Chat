
from concurrent import futures
import logging

import grpc
import chat_pb2
import chat_pb2_grpc

serverTxt = ""
serverMsgCount = 0

class Chatter(chat_pb2_grpc.ChatterServicer):

    def JoinServer(self, request, context):
        global serverMsgCount
        print("%s joined." % request.name)
        return chat_pb2.ServerReply(message='%s has joined the server.' % request.name)

    def LeaveServer(self, request, context):
        global serverMsgCount
        print("%s left." % request.name)
        return chat_pb2.ServerReply(message='%s has left the server.' % request.name)

    def SendText(self, request, context): 
        global serverTxt
        global serverMsgCount

        serverMsgCount += 1
        serverTxt = request.text
        return chat_pb2.ReceivingText(message='%s' % serverTxt)

    def GetText(self, request, context):
        global serverTxt
        global serverMsgCount
        return chat_pb2.GetTextReply(message='%s' % serverTxt,num=serverMsgCount)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatterServicer_to_server(Chatter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

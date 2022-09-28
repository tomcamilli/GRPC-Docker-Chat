from __future__ import print_function

import logging

import grpc
import time
import threading
import chat_pb2
import chat_pb2_grpc

shutdown = False
workerShutdown = False
msgCount = 0
txt = ""
stub = None

def textFromOthers(name):
    global shutdown
    global workerShutdown
    global stub
    global txt
    global msgCount

    while shutdown == False:
        if stub != None:
            response = stub.GetText(chat_pb2.GetTextRequest())
            if response.num > msgCount and response.message != "":
                  print("\n%s\n[%s] " % (response.message, name), end="")
                  txt = response.message
                  msgCount = response.num
        time.sleep(0.02)

    workerShutdown = True

def run(): 
    with grpc.insecure_channel('localhost:50051') as channel:
        global stub
        global shutdown
        global workerShutdown
        global msgCount
        global txt

        stub = chat_pb2_grpc.ChatterStub(channel)
        
        # Get name of new client
        clientName = input("Enter name: ")
        response = stub.JoinServer(chat_pb2.ServerRequest(name=clientName))

        # Send message telling clients that a new client has joined
        stub.SendText(chat_pb2.SendingText(text='%s' % response.message))

        # Welcome new client to the chat
        print("Welcome to the chat! Enter 'q' to quit.")


        # Start thread for receiving messages from other clients
        textThread = threading.Thread(target=textFromOthers,args=(clientName,))
        textThread.start()

        # Wait for keyboard input
        while shutdown == False: 
            txt = input()
            if txt == "q":
                response = stub.LeaveServer(chat_pb2.ServerRequest(name=clientName))
                stub.SendText(chat_pb2.SendingText(text='%s' % response.message))
                shutdown = True
            else:
                textToSend = '[%s] %s' % (clientName,txt)
                stub.SendText(chat_pb2.SendingText(text=textToSend))
            time.sleep(0.02)

        # Wait until the thread has concluded
        while workerShutdown == False:
            time.sleep(0.02)

        textThread.join()

if __name__ == '__main__':
    logging.basicConfig()
    run()

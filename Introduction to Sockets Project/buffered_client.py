# Mike Brandin CPSC 3600-Section 91005 9/18/2021
# Assignment 2 - Introduction to Sockets in Python

# TODO: add any import statements required
from socket import *
from struct import *

class BufferedTCPClient:

    def __init__(self, server_host='localhost', server_port=36001, buffer_size=1024):
        self.buffer_size = buffer_size

        # TODO: Create a socket and establish a TCP connection with server 
        self.tcp_client_socket = socket(AF_INET , SOCK_STREAM)
        self.tcp_client_socket.connect((server_host, server_port))

    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should accept a message
    # from the user, which is packed according to the format specified for this assignment and then sent into the socket.
    # TODO: * Send a message to the server containing the message passed in to the function. 
    #           * Remember to pack it using the format defined in the instructions. 
    def send_message(self, message):
        print("CLIENT: Attempting to send a message...")
        format_string = "!I" + str(len(message)) + "s"      # create the format string and pack [bitlength][message] and send
        packed_message = pack(format_string, len(message.encode()), message.encode())
        self.tcp_client_socket.send(packed_message)
  
    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should wait to receive a 
    # message from the socket, which is then returned to the user. It should return two values: the message received and whether or not it was received 
    # successfully. In the event that it was not received successfully, return an empty string for the message.
    # TODO: * Return the *string* sent back by the server. This should be the same string you sent, except that first 10 characters will have been removed
    #           * Be sure to set the bufsize parameter to self.buffer_size when calling the socket's receive function
    #           * Remember that we're sending packed messages back and forth, for the format defined in the assignment instructions. You'll have to unpack
    #             the message and return just the string. Don't return the raw response from the server.
    #       * Handle any errors associated with the server disconnecting
    def receive_message(self):
        print("CLIENT: Attempting to receive a message...")
        
        FIXED_HEADER_LENGTH = 4
        try:
            data = self.tcp_client_socket.recv(FIXED_HEADER_LENGTH)     # retrieve length from header
        except ConnectionResetError as e:
            return "", False
        length = unpack('!I', data)[0]
        payload_buffer = b""    
        while len(payload_buffer) < length:     # for the message length     
            buffer_size = min(self.buffer_size, length - len(payload_buffer))
            data = self.tcp_client_socket.recv(buffer_size) # reconstructe message from reading in buffer
            if not data:    # if connection closes prematurely
                return "", False
            payload_buffer += data
            
        payload = payload_buffer.decode()   # decode and return payload and true if connection is live
        return payload, True

    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should close your socket.
    # TODO: Close your socket
    def shutdown(self):
        print("Client: Attempting to shut down...")
        self.tcp_client_socket.close() # close client socket

if __name__ == "__main__":
    l = BufferedTCPClient(server_host="localhost", server_port=36001)
    
    l.send_message("Four score and seven years ago")
    l.send_message("testing for failure")
    
    response = l.receive_message()
    response2 = l.receive_message()

    l.shutdown()
    print(response)
    print(response2)

# Mike Brandin CPSC 3600-Section 91005 9/18/2021
# Assignment 2 - Introduction to Sockets in Python

# TODO: Include any necessary import statements
from socket import *
from struct import *


class BufferedTCPEchoServer(object):
    def __init__(self, host = '', port = 36001, buffer_size = 1024):
        # Save the buffer size to a variable. You'll need this later
        self.buffer_size = buffer_size
        # This variable is used to tell the server when it should shut down. Our implementation of this server is centered
        # around one or more while loops that keeps the server listening for new connection requests and new messages from
        # a connected client. This should continue forever, or until this self.keep_running is set to False. My testing
        # code will use self.keep_running to shutdown the server for one test case 
        self.keep_running = True

        # TODO: Create and bind the server socket
        self.tcp_server_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_server_socket.bind(('', port))

    # This function starts the server listening for new connections and new messages. It initiates the core loop of our 
    # server, where we loop continuously listening for a new connection, or if we are already connected, listening for a new 
    # message. I recommend breaking the functionality up into helper functions
    # Remember that this server can only talk to one connected client at a time. We'll implement a server that
    # can connect to multiple clients at once in a future project.
    # TODO: * Listen for new connections
    #       * Accept new connections
    #       * Receive messages from the connected client until it disconnects. 
    #           * Be sure to set the bufsize parameter to self.buffer_size when calling the socket's receive function
    #       * When a message is received, remove the first ten characters and then send it back to the client. 
    #           * You can use the slice operator to remove the first 10 characters: shorter_string = my_string_variable[10:] 
    #           * You will need to package the message using the format discussed in the assignment instructions
    #       * On disconnect, attempt to accept a new connection
    #       * This process should continue until self.keep_running is set to False. (The program doesn't need immediately close when the value changes)
    #       * Shutdown the server's socket before exiting the program

    def start(self):
        while self.keep_running:            # while the server is running
            print('SERVER: listening...')
            self.tcp_server_socket.listen(1)    # listen for new connections
        
            print('The server is ready to receive')
            count = 0
            payload = {}                            # store payloads and corresponding dictionary entry index
            new_connection, addr = self.tcp_server_socket.accept()  # accept connection
            pending_messages = True                         
            while pending_messages:                # while there are new messages from the client
                FIXED_HEADER_LENGTH = 4

                incoming_message = new_connection.recv(FIXED_HEADER_LENGTH)       
                if not incoming_message:          # if there are no more incoming messages break from while loop
                    pending_messages = False
                    break
                length = unpack('!I', incoming_message)[0]  # store length of message from header

                payload_buffer = b""
                while len(payload_buffer) < length:         # for the message length
                    buffer_size = min(self.buffer_size, length - len(payload_buffer))
                    try:
                        data = new_connection.recv(buffer_size)     # recieve new data to add to buffer
                    except ConnectionResetError as e:
                        pass
                    if not data:    # if connection closes
                        self.keep_running = False
                        break
                    payload_buffer += data
                    
                payload[count] = payload_buffer.decode()    # store payload and splice off first 10 characters        
                payload[count] = payload[count][10:]
                payload[count] = pack('!I' + str(len(payload[count])) + 's', len(payload[count].encode()), payload[count].encode())     # pack and send
                try:
                    new_connection.send(payload[count])
                except ConnectionResetError as e:
                    pass
                count = count + 1
            new_connection.close() # close the connection

    # This method is called by the autograder when it is ready to shut down your program. You should clean up your server socket
    # here. Note that all other sockets opened by the server also need to be closed once you are done with them. You should be closing
    # the individual client sockets generated by socket.accept() inside of your start() function 
    # TODO: Clean up your server socket
    def shutdown(self):
        print("SERVER: shutting down...")
        self.tcp_server_socket.close() # close server socket

if __name__ == "__main__":
    BufferedTCPEchoServer(host='', port=36001, buffer_size=1024).start()
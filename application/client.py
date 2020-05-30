"""
Description:
    Class used to create and connect client to the server with a IP address and port.
    The client can receive and send messages from the server.

Packages:
    - pickle
    - socket
"""

__author__ = ("Manitas Bahri")
__version__ = "1.0"
__date__ = "2020/05"

import pickle
import socket


class Client:
    """
    Create client to chat.

    Args:
        - user_name (str) : The name of the user.
        - address_ip (str) : The address IP where the server is launched.
        - port (str) : The port where the server is launched.
        - password (str) : The password used to access to server.
    """
    def __init__(self, user_name, address_ip, port, password):
        self.user_name = user_name
        self.host = address_ip
        self.port = port
        self.password = password
        
        # Dictionary contain user data.
        self.data_user = {"User_Name":self.user_name,
                          "User_Password":self.password,
                          "Online_User":[]}

        # Define variables.
        self.is_connected = False
        self.is_stopped = False
        self.new_msg = False
        self.updt_user = False

    def create_connection(self):
        """
        Create a connection with a server. 
        Send the data from the client to the server and check if the connection is accepted before accessing it
        """
        try:
            # Turns the port into an integer.
            self.port = int(self.port)
            
            # The privileged port are between 1024 and 60000.
            if  self.port < 1024 or self.port > 60000:
                raise ValueError("The port is not between 1024 and 60000.")

            # Create the connection with the server
            self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_connection.connect((self.host, self.port))

            # Send data user to the server.
            self.server_connection.send(pickle.dumps(self.data_user))

            # Receive and decrypt the server authorization message.
            msg_connection = self.server_connection.recv(1024)
            msg_connection = pickle.loads(msg_connection)

            # The connection with the server is authorized.
            if msg_connection[0] == "server connection accepted":
                self.msg_report = ["Connection with the server.", "Connection au serveur."]
                self.data_server = msg_connection[1]
                self.is_connected = True
                self.updt_user = True

            # The connection with the server is refused.
            # Name already exists.
            if msg_connection[0] == "server connection refused" and msg_connection[1] == "user name":
                self.msg_report = ["The user name already exists. Please try again.",
                                   "Cet identifiant existe déjà. Veuillez réessayer."]

            # Password incorrect.
            elif msg_connection[0] == "server connection refused" and msg_connection[1] == "password":
                self.msg_report = ["The password does not match. Please try again.",
                                   "Le mot de passe ne correspond pas. Veuillez réessayer."]

        # The port is not an integer.
        except ValueError as ve:
            self.msg_report = [f"The server could not be launched. Please check the port.\nError : {ve}",
                               f"Le serveur n'a pas pu être lancé. Veuillez vérifier le port.\nErreur : {ve}"]

        # Incorrect address IP or Port.
        except socket.error as e:
            self.msg_report = [f"There is no server which correspond with these informations. Please check the IP address and port.\nError : {e}",
                               f"Aucun serveur ne correspond à ces informations. Veuillez vérifier l'adresse IP et le port.\nErreur : {e}"]

    def receive_message(self):
        """Receive messages and data from the server."""
        try:
            if self.is_connected:
                # Receive the messages.
                self.message_recv = self.server_connection.recv(1024)
                
                # Check if the message is not null.
                if self.message_recv != b"":

                    # Decrypt the messages.
                    self.message_recv = pickle.loads(self.message_recv)

                    # Server request to update the online users list.
                    if self.message_recv[0] == "Update User":
                        self.updt_user = True
                        self.data_user["Online_User"] = self.message_recv[1]

                    # Server request to exit the server.
                    elif self.message_recv[0] == "Exit Server":
                        self.new_msg = True
                        self.message_recv[0] = ["System", "Système"]
                        
                        self.is_stopped = True
                        self.is_connected = False

                    else:
                        self.new_msg = True

        # Avoid an error when shutting down the server.
        except ConnectionAbortedError as e:
            print(e)

    def send_message(self, message:str):
        """
        Encode and send a message to the server.
        
        Arg:
            - message (str): Message to send to the server.
        """
        msg_send = message.encode()
        self.server_connection.send(msg_send)

    def close(self):
        """Close the connection with the server."""
        try:
            self.server_connection.send(b"Close Client Connection")

        # Avoid an error when shutting down the server.
        except ConnectionAbortedError:
            pass

        # The connection is closed.
        self.is_connected = False

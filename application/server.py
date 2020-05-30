"""
Description:
    Class used to launch and manage server on a specific IP address and port. The server can be protected with a password.
    The server receives all messages from the clients and resends them to the other clients.

Packages:
    - pickle
    - select
    - socket
"""

__author__ = ("Manitas Bahri")
__version__ = "1.0"
__date__ = "2020/05"

import pickle
import select
import socket


class Server:
    """
    Create chat server.

    Args:
        - server_name (str) : The name of server.
        - user_name (str) : The name of the server owner.
        - address_ip (str) : The address IP used to launch the server.
        - port (str) : The port where the server will be created.
        - password (str) : The server can be password protected to prevent intrusion.
    """
    def __init__(self, server_name, user_name, address_ip, port, password):
        self.server_name = server_name
        self.owner_name = user_name
        self.host = address_ip
        self.port = port
        self.password = password

        # Create dictionary containing data of online users.
        self.data_online_client = {"User_Name":[], "Address":[]}

        # Define variables.
        self.is_launched = False
        self.updt_user = False
        self.new_msg = False

    def create_connection(self):
        """Create the server connection according to the IP address and the port."""
        try:
            # Turns the port into an integer.
            self.port = int(self.port)
            
            # The privileged port are between 1024 and 60000.
            if  self.port < 1024 or self.port > 60000:
                raise ValueError("The port is not between 1024 and 60000.")

            # Create server connection.
            self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_connection.bind((self.host, self.port))
            self.server_connection.listen(1)
            
            # Informs the user of the server launch.
            self.msg_report = [f"The server has been launched on the port {self.port}.",
                               f"Le serveur a été lancé sur le port {self.port}."]
            self.is_launched = True
            self.updt_user = True
        
        # Reports an error to the user when launching the server.
        except ValueError as ve:
            self.msg_report = [f"The server could not be launched. Please check the port.\nError : {ve}",
                               f"Le serveur n'a pas pu être lancé. Veuillez vérifier le port.\nErreur : {ve}"]
        
        except socket.error as e:
            self.msg_report = [f"The server could not be launched. Please check the IP address and port.\nError : {e}",
                               f"Le serveur n'a pas pu être lancé. Veuillez vérifier l'adresse IP et le port.\nErreur : {e}"]

    def main(self):
        """
        Starts the server on the server connection.
        Then accept new clients and manage the reception and sending of messages to other clients.
        """
        if self.is_launched:
            try:
                # Get the list of clients waiting to access the server.
                waiting_clients, __, __ = select.select([self.server_connection], [], [], 0.05)

                for client in waiting_clients:
                    # Accepts all clients in the server.
                    client_connection, __ = client.accept()

                    # The client send his data contain name and password.
                    data_user = client_connection.recv(1024)
                    data_user = pickle.loads(data_user)

                    # Check if the user can access the server.
                    permission = self.check_data_user(data_user["User_Password"], data_user["User_Name"])

                    if permission == True:
                        # Send permission to access the server and the welcome message.
                        msg_connection = ["server connection accepted", [self.server_name, self.owner_name]]
                        client_connection.send(pickle.dumps(msg_connection))

                        # Add the client to the online users dictionnary.
                        self.data_online_client["User_Name"].append(data_user["User_Name"])
                        self.data_online_client["Address"].append(client_connection)

                        # Request to update the display of online users.
                        self.updt_user = True

                        # Send to client the new list of online users.
                        updt_online_user = ["Update User", self.data_online_client["User_Name"]]

                        for client in self.data_online_client["Address"]:
                            client.send(pickle.dumps(updt_online_user))

                    else:
                        # Send a message to the client indicating why they are not allowed to access the server. 
                        msg_connection = ["server connection refused", permission]
                        client_connection.send(pickle.dumps(msg_connection))

                        # Close the connection with this client.
                        client_connection.close()
                
                # Get the list of clients who sent a unread message.
                readable_clients, __, __ = select.select(self.data_online_client["Address"],
                    [], [], 0.05)

            # Avoid an error if there are no client.
            except select.error:
                pass
        
            else:
                for client in readable_clients:
                    # Get the ID of the client who sent the message.
                    for user in self.data_online_client["Address"]:
                        if user == client:
                            id_client = self.data_online_client["Address"].index(user)

                    try:
                        # Receive and decrypt the message.
                        msg_recv = client.recv(1024)
                        msg_recv = msg_recv.decode()

                        # Create a list containing the author and message.
                        self.data_msg_send = [self.data_online_client["User_Name"][id_client], msg_recv]
                        
                        # Check if the client want close the connection with the server.
                        if msg_recv == "Close Client Connection":
                            name = self.data_online_client["User_Name"][id_client]
                            self.data_msg_send[1] = [f"{name} exit the server.", f"{name} quitte le serveur."]
                            self.close_user(client, id_client)

                        # Send the client's message to the other clients.
                        self.data_msg_send = pickle.dumps(self.data_msg_send)
                        for connection in self.data_online_client["Address"]:
                            if connection != client:
                                connection.send(self.data_msg_send)

                        # Informs for new message.
                        self.new_msg = True

                    # Avoids an error when a client is excluded and there is no other client remaining in the server.
                    except OSError:
                        pass

    def send_message(self, message:str):
        """
        Send a message to clients.
        
        Arg:
            - message (str): Message to send to clients.
        """
        msg_send = pickle.dumps([self.owner_name, message])

        for client in self.data_online_client["Address"]:
            client.send(msg_send)

    def check_data_user(self, user_password:str , user_name:str):
        """
        Check data entered by user before accept the client connection.
        
        Args:
            user_password (str): The password entered by the client.
            user_name (str): The name of the client.
        """
        same_name = False
        
        # Lowercase the name of the user.
        user_name = user_name.lower()

        # Lowercase all name in the list.
        online_user = [name.lower() for name in self.data_online_client["User_Name"]] 
        
        # Make sure the name is different from the other clients' names.
        try:
            online_user.index(user_name)

        except ValueError:
            same_name = False
        
        else:
            same_name = True
        
        # Check that the name is different from that of the owner.
        if user_name == self.owner_name.lower():
            same_name = True        

        # If the name doesn't already exist and the password is correct, then the connection is accepted.
        if user_password == self.password and not same_name:
            return True

        # The connection with the server is refused.
        # Name already exists.
        elif same_name:
            return "user name"        

        # Password incorrect.
        elif user_password != self.password:
            return "password"

    def delete_user(self, user_name:str):
        """
        Ban a user from the server.

        Arg:
            - user_name (str): The name of the user to ban.
        """
        # Get the ID of the user to ban.
        id_user = self.data_online_client["User_Name"].index(user_name)

        # Get his address.
        user_address = self.data_online_client["Address"][id_user]
        
        # Send a message to the user to inform them of their ban.
        msg_exit = pickle.dumps(["Exit Server", ["You have been kicked out by a moderator.", "Vous avez été exclu du serveur."]])
        user_address.send(msg_exit)

        # Close the client connection.
        user_address.close()
        
        # Delete user from online user dictionnary.
        for key in self.data_online_client:
            del self.data_online_client[key][id_user]
        
        # Update online users in the server.
        self.updt_user = True
        updt_online_user = ["Update User", self.data_online_client["User_Name"]]
        
        # Send the new online users list to all clients. 
        for client in self.data_online_client["Address"]:
            client.send(pickle.dumps(updt_online_user))

    def close_user(self, client, id_client):
        """
        Uses to close the client connection.
        
        Args:
            - client : The client that will be closed.
            - id_client : The ID corresponding to the client.
        """
        # Close the client connection.
        client.close()

        # Delete user from online user dictionnary.
        for key in self.data_online_client:
            del self.data_online_client[key][id_client]
        
        # Update online users in the server.
        self.updt_user = True
        updt_online_user = ["Update User", self.data_online_client["User_Name"]]
        
        # Send the new online users list to all clients. 
        for client in self.data_online_client["Address"]:
            client.send(pickle.dumps(updt_online_user))

    def close_server(self):
        """Close the server connection."""
        for client in self.data_online_client["Address"]:
            # Send a message to all clients to inform them of server shutdown.
            exit_msg = ["Exit Server", ["The server has been closed.", "Le serveur a été fermé."]]
            client.send(pickle.dumps(exit_msg))

            # Close the client connection.
            client.close()
        
        # The server is no longer launched.
        self.is_launched = False

        # Close the server connection.
        self.server_connection.close()

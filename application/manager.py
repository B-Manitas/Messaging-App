"""
Descrition:
    Online Chat is an application, made in Python 3, used to send messages. You can choose to create or connect to a server.
    The server can be launched in an IP address and a port of your choice and secure it with a password.

    This application is structured to 4 scripts. This script file is used to link the graphical user interface 
    with the file that manages the server or clients.

    The application is developped with Python 3 and Windows 10. The GUI is create with Tkinter.

Packages:
    - threading
    - tkinter
    - ttkthemes
    - pickle

Script File:
    - features : Creation of widgets classes used in the graphical user interface.
    - server : Launch and Manage server.
    - client : Create and connect a client to server.
"""

__author__ = ("Manitas Bahri")
__version__ = "1.0"
__date__ = "2020/05"

try:
    # Import modules
    from threading import Thread 
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import messagebox
    from ttkthemes import ThemedStyle
    import pickle
    import sys

    # Import other python scripts.
    import features as ft
    from server import Server
    from client import Client

# Prevents errors when importing modules.
except ImportError as e:
    print(e)
    messagebox.showerror(title="Online Chat", 
                         message=f"Please run the following command to install the missing libraries 'pip install -r requirements.txt'. Error: {e}")
    sys.exit()


class MainController(tk.Tk):
    """
    It is the main window of the application, it plays the role of manager.
    All page of the application are displayed in this window.
    It links the interface with the server or client script.
    """
    def __init__(self):
        super().__init__()
        # List containing the data entered by the user to create or connect to server.
        self.data_server = []
        self.data_client = []

        # Define variables
        self.current_page = None
        self.server = None
        self.client = None
        self.stop = False

        # Set the color themes of the application.
        self.current_color = 0

        # Set the default application language.
        self.languages = ["English", "Français"]
        self.current_language = 0

        # Define font family of the application.
        self.ft_title = ("Courier 18 underline")
        self.ft_subtitle = ("Courier 14 underline")
        self.ft_footer = ("Courier 10")

        # Defines the main container for the application.
        self.container = tk.Frame(self)
        self.container.pack(fill="both")

        # Add an icon to the application.
        try:
            self.iconbitmap("application/icon/icon_app.ico")

        # Avoid an error if the icon has not been found.
        except tk.TclError:
            pass

        # Configure main parameters of the application.
        self.title("Online Chat")
        self.geometry("790x600")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
        # First display the home menu page.
        self.show_frame(HomeMenu)

    def show_frame(self, frame_page):
        """
        Display a new page in the window.
        
        Arg:
            - frame_page (tk.Frame): The frame containing the page you want to display.
        """
        # Update the application theme.
        self.value_combobox = ["Light Mode", "Dark Mode"]
        self.name_theme = ["arc", "black"][self.current_color]
        self.bg_color = ["#F5F6F7", "#424242"][self.current_color]
        self.canvas_color = ["#FFFFFF", "#626262"][self.current_color]
        self.msg_other_color = ["#FFFDCD", "#D1D6DA"][self.current_color]
        self.font_color = ["#5C616C", "#A6A6A6"][self.current_color]
        self.msg_font_color = ["#000000", "#000000"][self.current_color]
        self.border_color = ["#DDE3E9", "#2A2A2A"][self.current_color]
        
        # Define the style.
        self.style = ThemedStyle()
        self.style.set_theme(self.name_theme)
        self.style.configure("TLabel", foreground=self.font_color)
        self.style.configure("TButton", font=("Courier 11 bold"), foreground=self.font_color)
        self.style.configure("TNotebook", font=("Courier 9"), foreground=self.font_color)
        self.style.configure("TScrollbar", bg=self.bg_color)
        self.style.configure("TSeparator", bg=self.font_color)
        
        self.config(bg=self.bg_color)

        # If a page is alredy displayed, it is destroyed.
        if self.current_page:
            self.current_page.destroy()

        # Change the current page and display the page.
        self.current_page = frame_page(self)
        self.current_page.pack(expand=True, fill="both", anchor="center")

    def create_server(self):
        """Create a new server."""
        self.server = Server(*self.data_server)
        
        # Create the server connection and report the connection status to inform the user.
        self.server.create_connection()
        self.msg_report = self.server.msg_report[self.current_language]

        # If the server is correctly launched, change the page of the application.
        if self.server.is_launched:
            self.after(200, lambda: self.show_frame(ServerMenu))

        # Else reset variable.
        else:
            self.server = None
            self.data_server = []

    def create_client(self):
        """Create a new instance of a user."""
        self.client = Client(*self.data_client)

        # Create connection and connect the client to server. And, informs him of the connection status.
        self.client.create_connection()
        self.msg_report = self.client.msg_report[self.current_language]

        # If the server is correctly launched, change the page of the application.
        if self.client.is_connected:
            self.after(200, lambda: self.show_frame(ClientMenu))

        # Else reset variable.
        else:
            self.client = None
            self.data_client = []

    def go_home(self):
        """Close the connection with server and return to home menu."""
        # Close the connection.
        if self.on_closing(False):
            self.stop = False

            # Change the current page of the application.
            self.show_frame(HomeMenu)

    def on_closing(self, quit=True):
        """
        Close the open instances (server or client) then, the application.
        
        Arg:
            - quit (bool): If true destroy and close the application.
        """
        try:
            exit = True

            # If a server exist.
            if self.server:
                exit = messagebox.askyesno(["Online Chat", "Quitter le serveur"][self.current_language], 
                                              ["Are you sure you want to stop and exit the server?", 
                                               "Voulez-vous vraiment arrêter et quitter le serveur ?"][self.current_language])

                # Close the connection.
                if exit:
                    self.server.close_server()
                    self.data_server = []
                    self.server = None

            # If a client exist.
            elif self.client:
                exit = messagebox.askyesno(["Online Chat", "Quitter le serveur"][self.current_language], 
                                              ["Are you sure you want to quit the server ?", 
                                               "Voulez-vous vraiment quitter le serveur ?"][self.current_language])

                # Close the connection.
                if exit:
                    self.client.close()
                    self.data_client = []
                    self.client = None

            # Close the application.
            if exit and quit:
                self.stop = True
                self.quit()
                return True

            elif exit and not quit:
                self.stop = True
                return True

        # Forces the application to stop.
        except Exception as e:
            print(e)
            messagebox.showerror("Online Chat", e)
            sys.exit()


class HomeMenu(tk.Frame):
    """
    This frame is the application's home menu.

    Args:
        - controller : The main controller of the application where the frame will be displayed.
    """
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        # Set the value of current language.
        self.lg = self.controller.current_language

        # Config the theme.
        self.bg_color = self.controller.bg_color
        self.border_color = self.controller.border_color
        self.canvas_color = self.controller.canvas_color
        self.font_color = self.controller.font_color
        self.config(bg=self.bg_color)

        # Change the window title with the server name.
        self.controller.title("Online Chat : Home Menu")

        # Create and positioning widget in the frame.
        # Title Frame.
        frm_title = tk.Frame(self, bg=self.bg_color)
        frm_title.pack(fill="both")

        # Theme Drop Down
        self.select_thm = ttk.Combobox(frm_title, values=self.controller.value_combobox, state="readonly",
                                      font=self.controller.ft_footer)
        self.select_thm.current(self.controller.current_color)
        self.select_thm.bind("<<ComboboxSelected>>", self.select_theme)
        self.select_thm.pack(pady=5, padx=10, anchor="ne")

        # Language Drop-Down.
        self.select_lg = ttk.Combobox(frm_title, values=self.controller.languages, state="readonly",
                                      font=self.controller.ft_footer)
        self.select_lg.current(self.lg)
        self.select_lg.bind("<<ComboboxSelected>>", self.select_language)
        self.select_lg.pack(pady=5, padx=10, anchor="ne")
        
        # Title Label.
        ttk.Label(frm_title, text=["Welcome to your Online\nMessage Box", "Bienvenue sur votre\nBoite de Messagerie"][self.lg], 
                  font=self.controller.ft_title, justify="center").pack(pady=30)
        
        # Frame where the input fields will be placed.
        frm_input_fields = tk.Frame(self, bg=self.bg_color)
        frm_input_fields.pack(pady=10)
        
        # Server Part.
        # Frame for the server input fields.
        frm_server = tk.Frame(frm_input_fields, bg=self.bg_color)
        frm_server.pack(side="left", anchor="nw", padx=15)
        
        ttk.Label(frm_server, text=["Server", "Serveur"][self.lg], font=self.controller.ft_subtitle).grid(column=0, row=0, sticky="w")

        # List containing data of all entries for the server input fields.
        server_entries = [[frm_server, ["Server Name", "Nom du Serveur"][self.lg], "server_name"],
                         [frm_server, ["User Name", "Nom d'Utilisateur"][self.lg], "server_user_name"],
                         [frm_server, ["Address IP", "Adresse IP"][self.lg], "server_address_ip"],
                         [frm_server, "Port", "server_port"],
                         [frm_server, ["Password", "Mot de Passe"][self.lg], "server_password", True]]

        # Creation and positioning of all server_entries entries.
        [self.create_entry(*server_entries[i]).grid(row=i+1, column=0, pady=5) for i in range(len(server_entries))]

        # Create a button to launch the server.
        btn_launch_server = ttk.Button(frm_server, text=["Launch Server", "Démarrer le serveur"][self.lg], command=self.launch_server)
        btn_launch_server.grid(row=6, column=0, sticky="wens", pady=5)

        # Client Part.
        # Frame for the client input fields.
        frm_client = tk.Frame(frm_input_fields, bg=self.bg_color)
        frm_client.pack(side="right", anchor="nw", padx=15)

        ttk.Label(frm_client, text="Client", font=self.controller.ft_subtitle).grid(column=0, row=0, sticky="w")

        # List containing data of all entries for the client input fields.
        client_entries = [[frm_client, ["User Name", "Nom d'Utilisateur"][self.lg], "user_name"],
                         [frm_client, ["Address IP", "Adresse IP"][self.lg], "client_address_ip"],
                         [frm_client, "Port", "client_port"],
                         [frm_client, ["Password", "Mot de Passe"][self.lg], "client_password", True]]

        # Creation and positioning of all client_entries entries.
        [self.create_entry(*client_entries[i]).grid(row=i+1, column=0, pady=5) for i in range(len(client_entries))]

        # Create a button to connect the client to a server.
        btn_connect_client = ttk.Button(frm_client, text=["Search Server", "Rechercher un serveur"][self.lg], command=self.connect_client)
        btn_connect_client.grid(row=5, column=0, sticky="wens", pady=5)

        # Create text where all error will be print here to inform the user.
        self.bbl_report = ft.BubbleMessage(self, ["Message Box", "Messagerie"][self.lg], ["No Message...", "Pas de message..."][self.lg], 
                                           msg_width=82, fg=self.font_color, bg=self.canvas_color)
        self.bbl_report.config(relief="flat", highlightbackground=self.border_color, highlightthickness=1)
        self.bbl_report.pack(fill="both", padx=35)

    def create_entry(self, frm_parent, text, name_obj, password=False):
        """
        Create a frame containing an entry and its associated label.

        Args :
            - frm_parent (Frame): The parent of this frame.
            - text (str): The text label associated with the entry.
            - name_obj (str): Name used to call the entry and get the value.

        Returns the frame containing the label and the entry.
        """
        # Create widgets.
        frame = tk.Frame(frm_parent, bg=self.bg_color)
        ttk.Label(frame, text=f"{text} :", font=self.controller.ft_footer, width=19).grid(column=0, row=1, sticky=tk.W, pady=10)
        entry = ttk.Entry(frame, name=name_obj, font=("Courier 11 bold"))
        entry.grid(column=1, row=1, sticky=tk.W+tk.E)

        # Change the text's displaying to not see the password entered by user. 
        if password == True:
            entry.config(show="*")

        # Create a self variable, to get the value later.
        setattr(self, name_obj, entry)
        return frame

    def launch_server(self):
        """Used to obtain the values of the entries and to ask the manager to create a new server."""        
        # Define the name of server input field.
        server_entries= ["server_name","server_user_name", 
                              "server_address_ip", "server_port", "server_password"]

        # Get the value of all the entries in the server input field.
        for i in range(len(server_entries)):
            entry = getattr(self, server_entries[i])
            self.controller.data_server.append(entry.get())

        # Check if the server entries are empty.
        try:
            self.controller.data_server.index("")

        # If not empty launch the server.
        except ValueError:
            # The names must contain less than 20 characters.
            if len(self.server_name.get()) > 20:
                self.bbl_report.modify(["System", "Système"][self.lg],
                                       ["The server name must contain less than 20 characters. Please try again.", 
                                        "Le nom doit contenir moins de 20 caractères. Veuillez réessayer."][self.lg])
                self.controller.data_server.clear()

            elif len(self.server_user_name.get()) > 20:
                self.bbl_report.modify(["System", "Système"][self.lg], 
                                       ["The server name must contain less than 20 characters. Please try again.", 
                                        "Le nom doit contenir moins de 20 caractères. Veuillez réessayer."][self.lg])
                self.controller.data_server.clear()

            # Launch the server.
            else:
                try:
                    self.controller.create_server()
                    self.bbl_report.modify(["System", "Système"][self.lg], self.controller.msg_report)
                
                # Prevents to error during the server execution.
                except Exception as e:
                    print(e)
                    messagebox.showerror(title="Online Chat", message=e)
                    sys.exit()

        # If entry an entry is empty, print an error message and delete data_server list.
        else:
            self.controller.data_server.clear()
            self.bbl_report.modify(["Error Syntax", "Erreur de Syntaxe"][self.lg], 
                                   ["Please complete all entries in the server input field.", 
                                    "Veuillez remplir tous les champs de saisie du serveur."][self.lg])

    def connect_client(self):
        """Used to obtain the values of the entries and to ask the manager to connect the client to the server."""
        # Define the name of client input field.
        client_entries = ["user_name","client_address_ip", "client_port", "client_password"]

        # Get the value of all the entries in the server input field.
        for i in range(len(client_entries)):
            entry = getattr(self, client_entries[i])
            self.controller.data_client.append(entry.get())

        # Check if the client entries are empty.
        try:
            self.controller.data_client.index("")

        # If not empty connect the client to server.
        except ValueError:
            # The name must contain less than 20 characters.
            if len(self.user_name.get()) > 20:
                self.bbl_report.modify(["System", "Système"][self.lg],
                                       ["The name must contain less than 20 characters. Please try again.",
                                        "Le nom doit contenir moins de 20 caractères. Veuillez réessayer."][self.lg])
                self.controller.data_client.clear()

            # Forbidden name.
            elif self.user_name.get() in ("Update User", "Exit Server", "System", "Système"):
                self.bbl_report.modify(["System", "Système"][self.lg],
                                       ["Please change the username",
                                        "Veuillez changer le nom d'utilisateur"][self.lg])
                self.controller.data_client.clear()

            else:
                try:
                    self.controller.create_client()
                    self.bbl_report.modify(["System", "Système"][self.lg], self.controller.msg_report)

                # Prevents to error during the server execution.
                except Exception as e:
                    print(e)
                    messagebox.showerror(title="Online Chat", message=e)
                    sys.exit()

        # If entry an entry is empty, print an error message and delete data_client list.
        else:            
            self.controller.data_client.clear()
            self.bbl_report.modify(["Error Syntax", "Erreur de Syntaxe"][self.lg], 
                                   ["Please complete all entries in the client input field.", 
                                   "Veuillez remplir tous les champs de saisie du client."][self.lg])

    def select_language(self, event):
        """Get the language select by the user and change all the texts."""
        # Get the language select.
        self.controller.current_language = self.controller.languages.index(self.select_lg.get())

        # Reload the application.
        self.controller.show_frame(HomeMenu)

    def select_theme(self, event):
        """Get the theme select by the user and change the theme of the application."""
        # Get the theme select.
        self.controller.current_color = self.controller.value_combobox.index(self.select_thm.get())

        # Reload the application.
        self.controller.show_frame(HomeMenu)


class ServerMenu(tk.Frame):
    """
    This frame is the application's server menu.

    Args:
        - controller : The main controller of the application where the frame will be displayed.
    """
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        # Set the value of current language.
        self.lg = self.controller.current_language

        # Config the theme colors.
        self.bg_color = self.controller.bg_color
        self.border_color = self.controller.border_color
        self.font_color = self.controller.font_color
        self.msg_font_color = self.controller.msg_font_color
        self.msg_other_color = self.controller.msg_other_color
        self.canvas_color = self.controller.canvas_color
        self.config(bg=self.bg_color)

        # Change the window title with the server name.
        self.controller.title("Online Chat : " + self.controller.data_server[0])

        # Creates and positioning widgets in the frame.
        # The title label.
        ttk.Label(self, text=["Welcome to Message", "Bienvenue sur la Messagerie"][self.lg], font=self.controller.ft_title).pack(pady=10)
        
        # Message Box Part.
        # Create the message box where the messages will be displayed.
        self.frm_scroll_msg = ft.ScrollableFrameMessage(self, c_width=400, c_height=500, highlightbackground=self.border_color,
                                                        highlightthickness=1, bg=self.canvas_color)
        self.frm_scroll_msg.pack(side="left", fill="y", padx=10, pady=10)
        
        # Create a new frame for the widgets to the right of the message box.
        self.frm_right = tk.Frame(self, bg=self.bg_color)
        self.frm_right.pack(side="left", fill="y", padx=10, pady=10)

        # Notebook Part.
        # Create a notebook.
        notebook = ttk.Notebook(self.frm_right)
        notebook.pack()

        # Create tab of notebook.
        tab_server_info = tk.Frame(notebook, bg=self.bg_color)
        tab_on_user = tk.Frame(notebook, bg=self.bg_color)

        # Add tab to notebook.
        notebook.add(tab_server_info, text=["Server Management", "Gestion du Serveur"][self.lg])        
        notebook.add(tab_on_user, text=["Online Users", "Utilisateurs Connectés"][self.lg])

        # Information Tab.
        # Create a scrollable frame where server information will be displayed.
        self.frm_info = ft.ScrollableFrame(tab_server_info, c_width=300, c_height=325, bg=self.canvas_color)
        self.frm_info.pack()

        # Define server information text. 
        txt_server_name = self.controller.server.server_name[:25] or (self.controller.server.server_name[25:] and "...")
        txt_address_ip = [f"Address IP : {self.controller.server.host}", f"Adresse IP : {self.controller.server.host}"][self.lg]
        txt_port = f"Port : {self.controller.server.port}"

        # Create a frame that encompasses all the labels information.
        frm_label = tk.Frame(self.frm_info.frm_scrollable, bg=self.bg_color)
        frm_label.pack(fill="x", padx=2, pady=2)

        # Create label for each server information.
        tk.Label(frm_label, text=txt_server_name, bg=self.bg_color, font=("Courier 11 underline"), fg=self.font_color).pack(fill="x", padx=2, pady=2)
        tk.Label(frm_label, text=txt_address_ip, bg=self.bg_color, font=("Courier 11"), fg=self.font_color, anchor="w", width=20).pack(fill="x", padx=2, pady=2)
        tk.Label(frm_label, text=txt_port, bg=self.bg_color, font=("Courier 11"), fg=self.font_color, anchor="w", width=20).pack(fill="x", padx=2, pady=2)

        ttk.Separator(self.frm_info.frm_scrollable, orient="horizontal").pack(fill="x", padx=2, pady=4)

        # Create a frame for the password part.
        frm_password = tk.Frame(self.frm_info.frm_scrollable, bg=self.bg_color)
        frm_password.pack(fill="x", padx=2, pady=2)

        # Subtitle.
        tk.Label(frm_password, text=["New Password", "Nouveau Mot de Passe"][self.lg], bg=self.bg_color, font=("Courier 11"), fg=self.font_color).pack()

        # Create a text to inform the user to modifing password.
        self.lbl_new_pass = tk.Label(frm_password, text="...", bg=self.bg_color, fg=self.font_color, font=("Courier 9"), width=50, anchor="w")
        self.lbl_new_pass.pack(side="bottom", anchor="w")

        # Create an entry where the user enters the new password.
        self.etr_new_password = ttk.Entry(frm_password, font=("Courier 11"), show="*")
        self.etr_new_password.pack(side="left")

        # Create a button to change the password.
        ttk.Button(frm_password, text=["Submit", "Modifier"][self.lg], command=self.change_password).pack(side="left")

        ttk.Separator(self.frm_info.frm_scrollable, orient="horizontal").pack(fill="x", padx=2, pady=4) 

        # Create a frame for the delete user part.
        frm_dlt_user = tk.Frame(self.frm_info.frm_scrollable, bg=self.bg_color)
        frm_dlt_user.pack(fill="x", padx=2, pady=2)

        # Subtitle.
        tk.Label(frm_dlt_user, text=["Ban User", "Exclure un Utilisateur"][self.lg], bg=self.bg_color, font=("Courier 11"), fg=self.font_color).pack()

        # Create a text to inform the user to modifing password.
        self.lbl_dlt_user = tk.Label(frm_dlt_user, text="...", bg=self.bg_color, fg=self.font_color, font=("Courier 9"), width=50, anchor="w")
        self.lbl_dlt_user.pack(side="bottom", anchor="w")

        # Create an entry where the user enters the name of the user who wants to ban.
        self.etr_dlt_user = ttk.Entry(frm_dlt_user, font=("Courier 11"))
        self.etr_dlt_user.pack(side="left")

        # Create a button to ban user.
        ttk.Button(frm_dlt_user, text=["Submit", "Exclure"][self.lg], command=self.delete_user).pack(side="left")

        # Online User Tab.
        # Create a scrollable frame where online users will be displayed.
        self.frm_on_user = ft.ScrollableFrameOnUser(tab_on_user, c_width=300, c_height=325, bg=self.canvas_color)
        self.frm_on_user.pack()

        # Create a button to return to home page.
        ttk.Button(self.frm_right, text=["Return to home page", "Retourner à la page d'accueil"][self.lg],
                   command=self.controller.go_home).pack(fill="x", pady=15)

        # Text Box Part.
        # Create a frame for text box and the scrollbar associated.
        frm_txtbox = tk.Frame(self.frm_right, bg=self.bg_color)
        frm_txtbox.pack(fill="both")

        # Create vertical scrollbar attached to text box.
        vbar_txtbox = ttk.Scrollbar(frm_txtbox)
        vbar_txtbox.pack(side="right", fill="y")
        
        # Create Text box.
        self.txtbox = tk.Text(frm_txtbox, height=4, width=1, font=("Courier 11"), relief="flat", 
                              highlightbackground=self.border_color, highlightthickness=1, 
                              bg=self.canvas_color, wrap="word", yscrollcommand=vbar_txtbox.set)
        vbar_txtbox.config(command=self.txtbox.yview)
        self.txtbox.pack(expand=True, fill="x")
        
        # Create a button to send a message.
        ttk.Button(frm_txtbox, text=["Send", "Envoyer"][self.lg], command=self.send_message).pack(side="bottom", anchor="e", pady=3)

        # Create a thread in parallel to the menu creation.  
        trd_main = Thread(target=self.main)
        trd_main.start()

    def main(self):
        """Main method used to update client connections, displaying online users and receive messages."""
        try:
            while not self.controller.stop:
                # Accept client in server. Then, manage the reception and the messages sending to other clients.
                self.controller.server.main()

                # Manage the display of online users in the server.
                # Check if a user update request has been asked.
                if self.controller.server.updt_user:
                    # Delete all widgets in the "Online User Tab".
                    for user in self.frm_on_user.frm_scrollable.winfo_children():
                        user.destroy()

                    # Add a widget for the name of the server owner.
                    self.frm_on_user.display_user(self.controller.data_server[1], self.bg_color, self.font_color, "moderator")

                    # Create new widget for each online user.
                    for online_user in range(len(self.controller.server.data_online_client["User_Name"])):
                        self.frm_on_user.display_user(self.controller.server.data_online_client["User_Name"][online_user], 
                                                    self.bg_color, self.font_color)
                    
                    # The user's update request is complete.
                    self.controller.server.updt_user = False

                # Manage the display of received messages.
                # Check for new message.
                if self.controller.server.new_msg:
                    # Decrypt the message.
                    msg_rcv = pickle.loads(self.controller.server.data_msg_send)

                    # Translation for the message.
                    # Check if the message is a simple str or if it contains a list of multiple translations.
                    if isinstance(msg_rcv[0], list):
                        msg_rcv[0] = msg_rcv[0][self.lg]

                    if isinstance(msg_rcv[1], list):
                        msg_rcv[1] = msg_rcv[1][self.lg]

                    # Create new widget fot the message.
                    self.frm_scroll_msg.display_message(msg_rcv[0], msg_rcv[1], self.msg_other_color, self.border_color, self.msg_font_color)

                    # The message is displayed.
                    self.controller.server.new_msg = False

        # Avoid an error when the user return to home because the loop has been stopped.
        except AttributeError:
            pass

    def send_message(self):
        """Manage the sending and displaying of the message."""

        # Get the sent message to display.
        msg_send = self.txtbox.get("1.0", "end")

        # Check if the message is blank.
        if msg_send != "\n":
            # Send the message. 
            self.controller.server.send_message(msg_send)

            # Display the message.
            self.after(20, self.frm_scroll_msg.display_message(self.controller.data_server[1], msg_send, self.bg_color, self.border_color, self.font_color))

        # Cleans up the user text box.
        self.txtbox.delete("1.0", "end")

    def change_password(self):
        """Change the server password."""
        # Get the new password entered by the user.
        new_password = self.etr_new_password.get()

        # The password can't be null.
        if len(new_password) > 0:
            self.controller.server.password = new_password
        
            # Clean up the entry.
            self.etr_new_password.delete(0, "end")
            # Informs the user than the password has been correctly changed.
            self.lbl_new_pass["text"] = ["The password has been changed.", "Le mots de passe a été changer."][self.lg]
        
        else:
            self.lbl_new_pass["text"] = ["The password can't be null.", "Le mots de passe ne peut pas être vide."][self.lg]

    def delete_user(self):
        """Ban user from the server."""
        try:
            # Get the name of user who will be banned.
            self.controller.server.delete_user(self.etr_dlt_user.get())
            # Clean up the entry.
            self.etr_dlt_user.delete(0, "end")
            # Informs the user than the user has been correctly banned.
            self.lbl_dlt_user["text"] = ["The user has been banned.", "L'utilisateur a été exclu."][self.lg]

        # Informs the user if no user with this name has been found on the server.
        except ValueError:
            self.lbl_dlt_user["text"] = ["No user with this name was found.", 
                                         "Aucun utilisateur n'a été trouvé."][self.lg]


class ClientMenu(tk.Frame):
    """
    This frame is the application's client menu.

    Args:
        - controller : The main controller of the application where the frame will be displayed.
    """
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        # Set the value of current language.
        self.lg = self.controller.current_language

        # Config the theme colors.
        self.bg_color = self.controller.bg_color
        self.border_color = self.controller.border_color
        self.font_color = self.controller.font_color
        self.msg_font_color = self.controller.msg_font_color
        self.msg_other_color = self.controller.msg_other_color
        self.canvas_color = self.controller.canvas_color
        self.config(bg=self.bg_color)

        # Change the window title with the server name.
        self.controller.title("Online Chat : " + self.controller.client.data_server[0])

        # Creates and positioning widgets in the frame.
        # The title label.
        ttk.Label(self, text=["Welcome to Message", "Bienvenue sur la Messagerie"][self.lg], font=self.controller.ft_title).pack(pady=10)
        
        # Message Box Part.
        # Create the message box where the messages will be displayed.
        self.frm_scroll_msg = ft.ScrollableFrameMessage(self, c_width=400, c_height=500, highlightbackground=self.border_color,
                                                        highlightthickness=1, bg=self.canvas_color)
        self.frm_scroll_msg.pack(side="left", fill="y", padx=10, pady=10)
        
        # Create a new frame for the widgets to the right of the message box.
        frm_right = tk.Frame(self, bg=self.bg_color)
        frm_right.pack(side="left", fill="y", padx=10)

        # Online User Part.
        # Subtitle.
        ttk.Label(frm_right, text=["Online Users", "Utilisateurs Connectés"][self.lg], font=("Courier 14")).pack(side="top", anchor="w", pady=5)
        
        # Create a scrollable frame where online users will be displayed.
        self.frm_on_user = ft.ScrollableFrameOnUser(frm_right, c_width=300, c_height=350, highlightbackground=self.border_color, 
                                                    highlightthickness=1, bg=self.canvas_color)
        self.frm_on_user.pack()
        
        # Create a button to return to home page.
        ttk.Button(frm_right, text=["Return to home page", "Retourner à la page d'accueil"][self.lg], width=14,
                   command=self.controller.go_home).pack(fill="x", pady=15)

        # Text Box Part.
        # Create a frame for text box and the scrollbar associated.
        frm_txtbox = tk.Frame(frm_right, bg=self.bg_color)
        frm_txtbox.pack(fill="both")

        # Create vertical scrollbar attached to text box.
        vbar_txtbox = ttk.Scrollbar(frm_txtbox)
        vbar_txtbox.pack(side="right", fill="y")

        # Create Text box.
        self.txtbox = tk.Text(frm_txtbox, height=3, width=1, font=("Courier 11"), relief="flat",
                              highlightbackground=self.border_color, highlightthickness=1, bg=self.canvas_color,
                              wrap="word", yscrollcommand=vbar_txtbox.set)
        vbar_txtbox.config(command=self.txtbox.yview)
        self.txtbox.pack(expand=True, fill="x")

        # Create a button to send a message.
        self.btn_send = ttk.Button(frm_txtbox, text=["Send", "Envoyer"][self.lg], command=self.send_message)
        self.btn_send.pack(side="bottom", anchor="e", pady=3)
        
        # Create a thread in parallel to the menu creation.
        trd_main = Thread(target=self.main)
        trd_main.start()

    def main(self):
        """Main method used to update receive messages and displaying online users."""
        try:
            while not self.controller.stop:
                # Manage the display of online users in the server.
                # Check if a user update request has been asked.
                if self.controller.client.updt_user:
                    # Delete all widgets in the "Online User Tab".
                    for user in self.frm_on_user.frm_scrollable.winfo_children():
                        user.destroy()

                    # Add a widget for the name of the server owner.
                    self.frm_on_user.display_user(self.controller.client.data_server[1], self.bg_color, self.font_color, "moderator")

                    # Create new widget for each online user.
                    for online_user in range(len(self.controller.client.data_user["Online_User"])):
                        self.frm_on_user.display_user(self.controller.client.data_user["Online_User"][online_user], self.bg_color, self.font_color)

                    # The user's update request is complete.
                    self.controller.client.updt_user = False

                # Manage the display of received messages.
                # Receive messages sent by the server.
                self.controller.client.receive_message()

                # Check for new message.
                if self.controller.client.new_msg:
                    # Get the message
                    msg_rcv = self.controller.client.message_recv

                    # Translation for the message.
                    # Check if the message is a simple str or if it contains a list of multiple translations.
                    if isinstance(msg_rcv[0], list):
                        msg_rcv[0] = msg_rcv[0][self.lg]

                    if isinstance(msg_rcv[1], list):
                        msg_rcv[1] = msg_rcv[1][self.lg]

                    # Create new widget fot the message.
                    self.frm_scroll_msg.display_message(msg_rcv[0], msg_rcv[1], self.msg_other_color, self.border_color, self.msg_font_color)
                    # The message is displayed.
                    self.controller.client.new_msg = False

                # Stop the main controller if the client is disconnected.
                if self.controller.client.is_stopped:
                    self.controller.stop = True

                    # Go to Home Menu when the client is not connected.
                    self.btn_send.configure(text=["Back to Home Menu", "Retourner au Menu"], command=self.controller.go_home, width=19)

        # Avoid an error when the user return to home because the loop has been stopped.
        except AttributeError:
            pass

    def send_message(self):
        """Manage the sending and displaying of the message."""

        # Get the sent message to display.
        msg_send = self.txtbox.get("1.0", "end")

        # Check if the message is blank.
        if msg_send != "\n":
            # Send the message.
            self.controller.client.send_message(msg_send)

            # Display the message.
            self.frm_scroll_msg.display_message(self.controller.data_client[0], msg_send, self.bg_color, self.border_color, self.font_color)

        # Cleans up the user text box
        self.txtbox.delete("1.0", "end")


if __name__ == "__main__":
    try:
        application = MainController()
        application.mainloop()

    # Prevents to error when the script execution.
    except Exception as e:
        print(e)
        messagebox.showerror(title="Online Chat", message=e)
        sys.exit()

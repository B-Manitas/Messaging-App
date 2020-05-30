"""
This script file contains all the widgets classes needed for the GUI of the messaging application.
The widgets are created with Tkinter and Python 3.

Packages:
    - datetime
    - textwrap
    - tkinter
    - ttkthemes
"""

__author__ = ("Manitas Bahri")
__version__ = "1.0"
__date__ = "2020/05"

from datetime import datetime
import textwrap
import tkinter as tk
import tkinter.ttk as ttk


class BubbleMessage(tk.Frame):
    """
    Create a frame that can contain an editable message. 
    
    Args:
        - parent: The parent of this frame.
        - title (str): The title of the message.
        - message (str): The message sent by the client.
        - fg: The color font.
        - bg: The background color of the bubble message.
        - msg_width (int): The length of message in a line.
    """
    def __init__(self, parent, title:str, message:str, fg, bg, msg_width:int=45):
        super().__init__(parent)
        self.title = title
        self.message = message
        self.bg_color = bg
        self.fg_color = fg
        self.msg_width = msg_width

        # Config the background color.
        self.config(bg=self.bg_color)

        # Format the title text.
        txt_title = "%s, %s" % (self.title, datetime.now().strftime("%H:%M"))

        # Create labels in the bubble message.
        self.lbl_title = tk.Label(self, text=txt_title, font=("Courier 9 bold"), fg=self.fg_color, bg=self.bg_color)
        self.lbl_msg = tk.Label(self, text=textwrap.fill(message, self.msg_width), font=("Courier 10"), fg=self.fg_color, justify="left", bg=self.bg_color)

        self.lbl_title.pack(anchor="w")
        self.lbl_msg.pack(anchor="w")

    def modify(self, title:str, message:str):
        """
        Edit the title and message of the frame.
        
        Args:
            - title (str): New title of the frame.
            - message (str): New message of the frame.
        """
        # Format the title text.
        txt_title = "%s, %s" % (title, datetime.now().strftime("%H:%M"))
        
        # Modify the title.
        self.lbl_title.config(text=txt_title)
        
        # Modify the message.
        self.lbl_msg.config(text=textwrap.fill(textwrap.dedent(message), self.msg_width))


class TextButton(tk.Label):
    """
    Button widget with a label appearance.
    
    Args:
        - parent : The parent of the text button.
        - hover_color : Text color when the mouse is over the label.
        - command : Function to call when the mouse presses the label.
    """
    def __init__(self, parent, hover_color, command=None, **kw):
        super().__init__(parent, **kw)
        self.hover_color = hover_color
        self.command = command
        
        # Get the default text color.
        self.default_color = self["fg"]

        # Call on_pressed method when user pressed the text button widget.
        self.bind("<Button-1>", self.on_pressed, add="+")

        # When the mouse is over and leave the text button widget.
        self.bind("<Enter>", self.on_enter, add="+")        
        self.bind("<Leave>", self.on_leave)

    def on_pressed(self, event):
        """Call function when mouse is pressing the text button widget."""
        self.command()

    def on_enter(self, event):
        """Change the text color when mouse is over the text button widget."""
        self["fg"] = self.hover_color
    
    def on_leave(self, event):
        """Change the text color to default color when mouse is not over the text button widget."""
        self["fg"] = self.default_color


class ScrollableFrameMessage(tk.Frame):
    """
    Create a scrollable frame for displaying messages.

    Args:
        - parent: The parent of this frame.
        - c_width (int): The canvas width of the frame.
        - c_height (int): The canvas height of the frame.
        - bg: The background color of the frame.
        - msg_width (int): The length of message in a line.
    """
    def __init__(self, parent, c_width:int, c_height:int, bg, msg_width:int=48, **kw):
        super().__init__(parent, bg=bg, **kw)
        self.c_width = c_width
        self.c_height = c_height
        self.background = bg
        self.msg_width = msg_width

        # Define variables.
        self.frm_options = None
        self.current_event = None

        # Create canvas contain the scrollbar frame.
        self.canvas = tk.Canvas(self, highlightbackground=self.background, highlightthickness=1, bg=self.background, width=self.c_width, height=self.c_height)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create vertical scrollbar associated to canvas.
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure the scrollbar to the canvas.
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        # The main scrollable frame contain all messages.
        self.frm_scrollable = tk.Frame(self.canvas, bg=self.background)
        
        # Update the value of scrollregion.
        self.frm_scrollable.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        
        # When mouse is over the frame, the user can scroll it with the mouse wheel.
        self.frm_scrollable.bind("<Enter>", self.bound_mousewheel)
        self.frm_scrollable.bind("<Leave>", self.unbound_mousewheel)

        # Create a window at the top of the canvas where the messages will appear.
        self.canvas.create_window(0, 0, window=self.frm_scrollable, anchor=("nw"), width=self.c_width)        
        
    def bound_mousewheel(self, event):
        """
        When the mouse is over frame, 
        call "scrollbar_bottom" method to use the scrolling with the mouse wheel.
        """
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    
    def unbound_mousewheel(self, event):
        """When the mouse is not on the frame, scrolling with the mouse is not activated."""
        self.canvas.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        """Method used to scroll with mouse wheel."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def display_message(self, user_name:str, message:str, bg_color, bd_color, font_color):
        """
        Create a new bubble message in the message box.

        Args:
            - user_name (str): The name of the user who has sent this message.
            - message (str): The message that will be displayed in this bubble message.
            - bg_color : The background color of the bubble message.
            - bd_color : The border color of the bubble message.
            - font_color : The font color in the bubble message.
        """

        # Format the information text.
        txt_info = "%s, %s" % (user_name, datetime.now().strftime("%H:%M"))
        
        # Frame containing the title and message.
        bubble_frame = tk.Frame(self.frm_scrollable, bg=bg_color, highlightbackground=bd_color, highlightthickness=1)
        bubble_frame.pack(fill="x", expand=True, padx=5, pady=5)

        # Create labels in the bubble message.
        tk.Label(bubble_frame, text=txt_info, font=("Courier 9 bold"), bg=bg_color, fg=font_color).pack(anchor="w")
        lbl_msg = tk.Label(bubble_frame, text=textwrap.fill(message, self.msg_width), font=("Courier 10"), bg=bg_color, justify="left", fg=font_color)
        lbl_msg.pack(anchor="w")

        # Call message_option method if the user clicks on the text message or on the frame.
        lbl_msg.bind("<Button-1>", lambda event:self.message_option(event, font_color))
        bubble_frame.bind("<Button-1>", lambda event:self.message_option(event, font_color))
        
        # Move the scrollbar to bottom of frame.
        self.after(30, lambda: self.canvas.yview_moveto(1))

    def message_option(self, event, font_color):
        """
        When the user clicks on the bubble message, 
        a new frame appears with option to delete it.

        Arg:
            - font_color: The font color.
        """        
        def delete_message():
            """Function used to delete the message from the message box."""
            frm_bubble.destroy()
            self.frm_options.destroy()

        # Check the type of event.widget so that the message bubble frame is used as the parent. 
        if event.widget.winfo_class() == "Frame":
            frm_bubble = event.widget
        
        elif event.widget.winfo_class() == "Label":
            frm_bubble = event.widget.master

        # Check if the bubble message does not already have the frm_options.
        if self.current_event != event.widget:
            
            # If the frm_options already exists, then it destroys it.
            if self.frm_options:
                self.frm_options.destroy()
            
            # Create the frm_options.
            self.frm_options = tk.Frame(frm_bubble, bg=frm_bubble["bg"], highlightbackground="#F5F6F7", highlightthickness=1)
            self.frm_options.pack(fill="x")
            
            # Create text button to delete the current message.
            TextButton(self.frm_options, hover_color="#FFBEBE", text="Delete this message.", 
                                        command=delete_message, font=("Courier 9 bold"), bg=frm_bubble["bg"], fg=font_color).pack(side="left")
            
            # Change the bubble message that has the frm_options.
            self.current_event = event.widget
        
        # If the bubble message already has the frm_options, it destroys it. 
        else:
            self.frm_options.destroy()
            self.frm_options = None
            self.current_event = None    


class ScrollableFrameOnUser(tk.Frame):
    """
    Create a scrollable frame for displaying the online users.

    Args:
        - parent: The parent of this frame.
        - c_width (int): The width of the frame.
        - c_height (int): The height of the frame.
        - bg: The background color of the frame.
    """
    def __init__(self, parent, c_width:int, c_height:int, bg="white", **kw):
        super().__init__(parent, bg=bg, **kw)
        self.c_width = c_width
        self.c_height = c_height
        self.background = bg

        # Define variables.
        self.frm_options = None
        self.current_event = None

        # Create canvas contain the scrollbar frame.
        self.canvas = tk.Canvas(self, highlightbackground=self.background, highlightthickness=1, bg=self.background, width=self.c_width, height=self.c_height)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create vertical scrollbar associated to canvas.
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure the scrollbar to the canvas.
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        # The main scrollable frame contain all messages.
        self.frm_scrollable = tk.Frame(self.canvas, bg=self.background)
        
        # Update the value of scrollregion.
        self.frm_scrollable.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        
        # When mouse is over the frame, the user can scroll it with the mouse wheel.
        self.frm_scrollable.bind("<Enter>", self.bound_mousewheel)
        self.frm_scrollable.bind("<Leave>", self.unbound_mousewheel)

        # Create a window at the top of the canvas where the messages will appear.
        self.canvas.create_window(0, 0, window=self.frm_scrollable, anchor=("nw"), width=self.c_width)   
        
    def bound_mousewheel(self, event):
        """
        When the mouse is over frame, 
        call "scrollbar_bottom" method to use the scrolling with the mouse wheel.
        """
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    
    def unbound_mousewheel(self, event):
        """When the mouse is not on the frame, scrolling with the mouse is not activated."""
        self.canvas.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        """Method used to scroll with mouse wheel."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def display_user(self, user_name:str, bg_color, font_color, user_status="client"):
        """
        Create a new bubble message in the online user frame.
        
        Args:
            - user_name (str): The name of the user.
            - bg_color: The background color of the bubble message.
            - font_color: The font color.
            - user_status (str): The status of the user (moderator or client).
        """
        bubble_user = tk.Text(self.frm_scrollable, font=("Courier 11"), bg=bg_color, fg=font_color, relief="flat", height=1)

        # Crown icon next
        try:
            if user_status == "moderator":
                self.crown_img = tk.PhotoImage(file="application/icon/crown.png")
                bubble_user.image_create("end", image=self.crown_img)
            
            else:
                self.client_img = tk.PhotoImage(file="application/icon/client.png")
                bubble_user.image_create("end", image=self.client_img)

        except tk.TclError:
            pass

        # Insert the name of user.
        bubble_user.insert("end", " " + user_name)

        # Disables the text to not modify it.
        bubble_user.config(state="disabled")
        bubble_user.pack(fill="x", expand=True, padx=5, pady=5)
        
        # Move the scrollbar to bottom of frame.
        self.after(30, lambda: self.canvas.yview_moveto(1))


class ScrollableFrame(tk.Frame):
    """
    Create a scrollable frame.

    Args:
        - parent: The parent of this frame.
        - c_width (int): The canvas width of the frame.
        - c_height (int): The canvas height of the frame.
        - bg (str): The background color of the frame.
    """
    def __init__(self, parent, c_width:int, c_height:int, bg:str="white", **kw):
        super().__init__(parent, bg=bg, **kw)
        self.c_width = c_width
        self.c_height = c_height
        self.background = bg

        # Define variables.
        self.frm_options = None
        self.current_event = None

        # Create canvas contain the scrollbar frame.
        self.canvas = tk.Canvas(self, highlightbackground=self.background, highlightthickness=1, bg=self.background, width=self.c_width, height=self.c_height)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create vertical scrollbar associated to canvas.
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure the scrollbar to the canvas.
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        # The main scrollable frame contain all messages.
        self.frm_scrollable = tk.Frame(self.canvas, bg=self.background)
        
        # Update the value of scrollregion.
        self.frm_scrollable.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        
        # When mouse is over the frame, the user can scroll it with the mouse wheel.
        self.frm_scrollable.bind("<Enter>", self.bound_mousewheel)
        self.frm_scrollable.bind("<Leave>", self.unbound_mousewheel)

        # Create a window at the top of the canvas where the messages will appear.
        self.canvas.create_window(0, 0, window=self.frm_scrollable, anchor=("nw"), width=self.c_width)   
        
    def bound_mousewheel(self, event):
        """
        When the mouse is over frame, 
        call "scrollbar_bottom" method to use the scrolling with the mouse wheel.
        """
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    
    def unbound_mousewheel(self, event):
        """When the mouse is not on the frame, scrolling with the mouse is not activated."""
        self.canvas.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        """Method used to scroll with mouse wheel."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

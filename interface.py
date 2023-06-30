"""
The primary GUI interface for the ConneXion tool.

Includes a home screen with two buttons to search for and conenct
with LinkedIn profiles. The buttons create new windows that include
user settings and filters to be used in the program. 

Author: Ethan Baker
"""
import os
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
import pickle
import consts as c
import search_tool.search_for_profiles as search_for_profiles
from connection_automator.bot_controller import BotController

class Interface:
    """
    A controller for the overall ConneXion Application.

    Manages all of the buttons and entry fields for the application.
    Contains methods to create GUI windows and to initiate the 
    execution of the search and connect features.
    """

    def __init__(self):
        """
        Initializes the home window of the ConneXion app.
        """
        self.root = tk.Tk()
        self.root.title("ConneXion for LinkedIn")
        self.root.geometry("350x250")  # Set initial window size
        self.root.resizable(False, False)  # Disable window resizing
        
        blank = tk.Label(self.root)
        blank.pack()

        # Insert image for logo
        logo = Image.open(c.PATH_TO_LOGO)
        logo = logo.resize((250, 110), Image.ANTIALIAS)
        self.tk_logo = ImageTk.PhotoImage(logo)
        image_label = tk.Label(self.root, image=self.tk_logo)
        image_label.pack_propagate(0)  # Disable label resizing
        image_label.pack()
        
        self.search_button = tk.Button(self.root, text="Search for Profiles", 
                                       command=self.open_search_page, width=20)
        self.search_button.pack(pady=10)
        
        self.connect_button = tk.Button(self.root, text="Automate Connections",
                                        command=self.open_connect_page,
                                        width=20)
        self.connect_button.pack(pady=0)

        self.search_message = ""
        self.connect_message = ""

        
    def open_search_page(self):
        """
        Creates a new GUI window that includes entry boxes for filters
        and user preferences for the profile search feature. Also includes
        a search button which initiates the backend of the search program.
        """
        try:
            with open ("search_tool/data/saved_search_inputs.pkl", 'rb') as file:
                saved_settings = pickle.load(file)
        except:
            pass

        # Function to open the Profile Search page
        search_page = tk.Toplevel(self.root)
        search_page.title("Search for Profiles")
        search_page.geometry("300x510")  # Set window size
        search_page.resizable(False, False)  # Disable window resizing

        # Create Filters frame
        filters_frame = tk.LabelFrame(search_page, text="Filters")
        filters_frame.pack(pady=10)

        # Create location entry field
        location_label = tk.Label(filters_frame, 
                                  text="Locations (Comma Separated):")
        location_label.pack(pady=5)
        location_entry = tk.Entry(filters_frame)
        location_entry.pack()
        try:
            location_entry.insert(0, saved_settings[0])
        except:
            pass

        # Create position entry field
        position_label = tk.Label(filters_frame, 
                                  text="Positions (Comma Separated):")
        position_label.pack(pady=5)
        position_entry = tk.Entry(filters_frame)
        position_entry.pack()
        try:
            position_entry.insert(0, saved_settings[1])
        except:
            pass

        # Create years of experience and operator entry fields
        exp_label = tk.Label(filters_frame, text="Years of Experience:")
        exp_label.pack(pady=5)

        exp_frame = tk.Frame(filters_frame)
        exp_frame.pack(pady=5)

        operator_var = tk.StringVar()
        operator_dropdown = ttk.OptionMenu(exp_frame, 
                                           operator_var, '', '>', '<', "=")
        operator_dropdown.pack(side=tk.LEFT, padx=5)
        try:
            operator_var.set(saved_settings[2])
        except:
            pass

        experience_entry = tk.Entry(exp_frame, width=13)
        experience_entry.pack(side=tk.LEFT, padx=5)
        try:
            experience_entry.insert(0, saved_settings[3])
        except:
            pass

        # Create Advanced Configuration frame
        adv_config_frame = tk.LabelFrame(search_page, text="Advanced")
        adv_config_frame.pack(pady=10)

        # Create output location field
        output_label = tk.Label(adv_config_frame, text="Output Location:")
        output_label.pack(pady=5)
        output_entry = tk.Entry(adv_config_frame)
        output_entry.pack()
        try:
            output_entry.insert(0, saved_settings[4])
        except:
            pass

        # Create API key entry field
        api_label = tk.Label(adv_config_frame, text="Custom Search API Key:")
        api_label.pack(pady=5)
        api_entry = tk.Entry(adv_config_frame)
        api_entry.pack()
        try:
            api_entry.insert(0, saved_settings[5])
        except:
            pass

        # Create Repeat Queries checkbox
        repeat_var = tk.IntVar()
        repeat_check = tk.Checkbutton(adv_config_frame, 
                                      text="Repeat Queries", 
                                      variable=repeat_var)
        repeat_check.pack(pady=5)
        try:
            repeat_var.set(saved_settings[6])
        except:
            pass

        # Create message label
        self.search_msg_label = tk.Label(search_page, text="",)
        self.search_msg_label.pack(pady=5)

        # Create Search button
        search_button = tk.Button(search_page, text="Search", width=20,
                command=lambda: self.from_search_gui(position_entry.get(),
                                                    location_entry.get(),
                                                    operator_var.get(),
                                                    experience_entry.get(),
                                                    output_entry.get(),
                                                    api_entry.get(),
                                                    repeat_var.get()))
        search_button.pack(pady=10)

    def open_connect_page(self):
        """
        Creates a new GUI window that includes entry boxes for login information
        and user preferences for the connection request feature. Also includes
        a connect button which initiates the backend of the connect program.
        """
        try:
            saved_inputs = "connection_automator/data/saved_connect_inputs.pkl"
            with open (saved_inputs, 'rb') as file:
                saved_settings = pickle.load(file)
        except:
            pass
        # Function to open the Connection Automator page
        connect_page = tk.Toplevel(self.root)
        connect_page.title("Automate Connections")
        connect_page.geometry("300x610")  # Set window size
        connect_page.resizable(False, False) 

        # Set LinkedIn frame
        linkedin_frame = tk.LabelFrame(connect_page, text="LinkedIn")
        linkedin_frame.pack(pady=10)

        # LinkedIn username and password labels and entry boxes
        user_label = tk.Label(linkedin_frame, text="LinkedIn Username:")
        user_label.pack(pady=5)
        user_entry = tk.Entry(linkedin_frame)
        user_entry.pack(padx=6)
        try:
            user_entry.insert(0, saved_settings[0])
        except:
            pass

        password_label = tk.Label(linkedin_frame, text="LinkedIn Password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(linkedin_frame, show="*")
        password_entry.pack(padx=6, pady=5)

        # Set filters frame
        filters_frame = tk.LabelFrame(connect_page, text="Filters")
        filters_frame.pack(pady=10)

        # Connection message label and entry box
        con_msg_label = tk.Label(filters_frame, text="Connection Message:")
        con_msg_label.pack(pady=5)
        con_msg_entry= tk.Entry(filters_frame)
        con_msg_entry.pack(pady=5)
        try:
            con_msg_entry.insert(0, saved_settings[1])
        except:
            pass

        # Number of requests to send label entry box
        num_req_label = tk.Label(filters_frame, 
                                 text="Number of requests to send:")
        num_req_label.pack(pady=5)
        num_req_entry = tk.Entry(filters_frame)
        num_req_entry.pack()
        try:
            num_req_entry.insert(0, saved_settings[2])
        except:
            pass

        # Minimum connection count label and entry box
        min_label = tk.Label(filters_frame, 
                             text="Minimum connections count:")
        min_label.pack(pady=5)
        min_entry = tk.Entry(filters_frame)
        min_entry.pack(padx=6, pady=5)
        try:
            min_entry.insert(0, saved_settings[3])
        except:
            pass

        # Set advanced frame
        adv_frame = tk.LabelFrame(connect_page, text="Advanced")
        adv_frame.pack(pady=10)

        # Excel file path label and entry box
        exl_label = tk.Label(adv_frame, text="Excel file path:")
        exl_label.pack(pady=5)
        exl_entry = tk.Entry(adv_frame)
        exl_entry.pack(pady=5)
        try:
            exl_entry.insert(0, saved_settings[4])
        except:
            pass

        # Set message label
        self.connect_msg_label = tk.Label(connect_page, text="")
        self.connect_msg_label.pack(pady=5)

        # Set Connect button
        search_button = tk.Button(connect_page, text="Connect", width=20,
                    command=lambda: self.from_connect_gui(user_entry.get(),
                                                        password_entry.get(),
                                                        con_msg_entry.get(),
                                                        num_req_entry.get(),
                                                        min_entry.get(),
                                                        exl_entry.get()))
        search_button.pack(pady=10)


    def display_search_message(self):
        """
        Changes the search message label to display a message to the user.

        The text of the message depends on what the value of self.search_message
        is when it is called. It is used to display error messages and let
        the user know if the search methods were successful.
        """
        self.search_msg_label.config(text=self.search_message, 
                                     wraplength=300, height=1)
        self.search_msg_label.update()

    def display_connect_message(self):
        """
        Changes the connect message label to display a message to the user.

        The text of the message depends on what the value of self.connect_message
        is when it is called. It is used to display error messages and let
        the user know if the connect methods were successful.
        """
        self.connect_msg_label.config(text=self.connect_message, 
                                      wraplength=300, height=1)
        self.connect_msg_label.update()


    def from_search_gui(self, positions, locations, 
                        exp_op, exp_num, output, api_key, repeat):
        """
        Converts the users' GUI input for the profile search tool to create
        input constants which are used throughout the program to customize results.
        Uses save_search_settings to save the user's input for the next time.

        Parameter positions: The positions to search for.
        Precondition: positions is a String.

        Parameter locations: The locations to search for. 
        Precondition: locations is a String.

        Parameter exp_op: The operator for years of experience.
        Precondition: exp_op is ">", "<", or "=".

        Parameter exp_num: The number for years of experience.
        Precondition: exp_num is a String.

        Parameter output: The location of the output excel file.
        Precondition: output is a String.

        Parameter api_key: The Custom Search API key.
        Precondition: api_key is a String.

        Parameter repeat: If the user would like to repeat queries or not.
        Precondition: repeat is 0 or 1.
        """
        self.save_search_settings(positions, locations, 
                                  exp_op, exp_num, output, api_key, repeat)
        search = True
        try:
            if locations !="":
                c.LOCATIONS = locations.split(', ')
            else: 
                search = False
                self.search_message = "Locations must not be blank."
                self.display_search_message()
                raise ValueError
            
            if positions != "":
                c.POSITIONS = positions.split(', ')
            else: 
                search = False
                self.search_message = "Positions must not be blank."
                self.display_search_message()
                raise ValueError

            if exp_op in [">", "<", "="]:
                c.EXPERIENCE_OPERATOR = exp_op
            else: 
                search = False
                self.search_message = "YoE dropdown must not be blank."
                self.display_search_message()
                raise ValueError

            if exp_num.isnumeric() and 0 <= int(exp_num) <= 30:
                c.EXPERIENCE_YEARS = exp_num
            else:
                search = False
                self.search_message = "YoE must be between 0 and 30."
                self.display_search_message()
                raise ValueError

            isdir = os.path.isdir(os.path.dirname(output))
            access = os.access(os.path.dirname(output), os.W_OK)
            end = output[-4:] == 'xlsx'
            if isdir and access and end:
                c.EXCEL_FILE_LOCATION = output
            else:
                search = False
                self.search_message = "Invalid output location."
                self.display_search_message()
                raise ValueError

            if api_key != "":
                c.API_KEY = api_key
            else: 
                search = False
                self.search_message = "API Key must not be blank."
                self.display_search_message()
                raise ValueError

            if repeat==0: c.REPEAT_QUERIES = False
            else: c.REPEAT_QUERIES = True

            if search:
                self.search_message="Searching..."
                self.display_search_message()
                self.search_message = search_for_profiles.execute_search()
                self.display_search_message()

        except ValueError:
            pass

    def from_connect_gui(self, user, password, msg, num, min, excel_path):
        """
        Converts the users' GUI input for the connection request tool to create
        input constants which are used throughout the program to customize results.
        Uses save_connect_settings to save the user's input for the next time.

        Parameter user: The user's LinkedIn username.
        Precondition: user is a String.

        Parameter password: The user's LinkedIn password.
        Precondition: password is a String.

        Parameter msg: The custom message the user wants to send with the request.
        Precondition: msg is a String.

        Parameter num: The number of connection requests to send 
        from the user's account.
        Precondition: num is a String.

        Parameter min: The minimum number of connections a profile
        must have to connect.
        Precondition: min is a String.

        Parameter excel_path: The filepath of the excel file that 
        contains urls of profiles.
        Precondition: excel_path is a String.
        """
        self.save_connect_settings(user, msg, num, min, excel_path)
        connect = True
        try:
            if user !="":
                c.USERNAME = user
            else: 
                connect = False
                self.connect_message = "Username must not be blank."
                self.display_connect_message()
                raise ValueError
            
            if password != "":
                c.PASSWORD = password
            else: 
                connect = False
                self.connect_message = "Password must not be blank."
                self.display_connect_message()
                raise ValueError
            
            if len(msg) <= 300:
                c.MESSAGE = msg
            else:
                connect = False
                self.connect_message = "Message must be less than 300 chars."
                self.display_connect_message()
                raise ValueError

            if num.isnumeric() and 1 <= int(num) <= 50:
                c.NUM_REQUESTS = int(num)
            else: 
                connect = False
                self.connect_message = "Num requests must be between 1 and 50."
                self.display_connect_message()
                raise ValueError

            if min.isnumeric() and 0<= int(min) <= 500:
                c.MINIMUM_CONNECTION_COUNT = int(min)
            else: 
                connect = False
                self.connect_message = "Min connections must be between 0 and 500."
                self.display_connect_message()
                raise ValueError

            end = excel_path[-4:] == 'xlsx'
            if os.path.exists(excel_path) and end:
                c.EXCEL_INPUT_LOCATION = excel_path
            else:
                connect = False
                self.connect_message = "Invalid Excel file location."
                self.display_connect_message()
                raise ValueError
            
            if connect:
                self.connect_message = "Connecting: Do not close window!"
                self.display_connect_message()
                controller = BotController()
                self.connect_message = controller.run()
                self.display_connect_message()

        except ValueError:
            pass

    def save_search_settings(self, positions, locations, exp_op, 
                                    exp_num, output, api_key, repeat):
        """
        Saves user input settings on Search button press.
         
        Converts input into a list and saves it as a .pkl file. The .pkl 
        file is used upon initialization of the Search for Profiles window
        to set the user's last used settings. 

        Parameter positions: The positions to search for.
        Precondition: positions is a String.

        Parameter locations: The locations to search for. 
        Precondition: locations is a String.

        Parameter exp_op: The operator for years of experience.
        Precondition: exp_op is ">", "<", or "=".

        Parameter exp_num: The number for years of experience.
        Precondition: exp_num is a String.

        Parameter output: The location of the output excel file.
        Precondition: output is a String.

        Parameter api_key: The Custom Search API key.
        Precondition: api_key is a String.

        Parameter repeat: If the user would like to repeat queries or not.
        Precondition: repeat is 0 or 1.
        """
        settings = [locations, positions, exp_op, exp_num, output, api_key, repeat]
        with open ("search_tool/data/saved_search_inputs.pkl", 'wb') as file:
            pickle.dump(settings, file)

    def save_connect_settings(self, user, msg, num, min, excel_path):
        """
        Saves user input settings on Connect button press.
        
        Converts input into a list and saves it as a .pkl file. The .pkl file
        is used upon the initialization of the Connection Automator window
        to set the use's last used settings

        Parameter user: The user's LinkedIn username.
        Precondition: user is a String.

        Parameter msg: The custom message the user wants to send with the request.
        Precondition: msg is a String.

        Parameter num: The number of connection requests to 
        send from the user's account.
        Precondition: num is a String.

        Parameter min: The minimum number of connections a 
        profile must have to connect.
        Precondition: min is a String.

        Parameter excel_path: The filepath of the excel file 
        that contains urls of profiles.
        Precondition: excel_path is a String.
        """
        settings = [user,msg,num,min,excel_path]
        with open ("connection_automator/data/saved_connect_inputs.pkl", 
                   'wb') as file:
            pickle.dump(settings, file)

    def run(self):
        """
        Launches the GUI application.
        """
        self.root.mainloop()
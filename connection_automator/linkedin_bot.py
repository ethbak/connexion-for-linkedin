"""
The LinkedIn Bot module of the LinkedIn Connection Automation Bot.

This module handles the setup and interaction of the Selenium 
Webdriver for the bot. It includes the class LinkedinBot, which 
includes methods which interact with data from the website. 
This module works in conjunction with the Bot Controller module
to use Selenium to automatically connect with LinkedIn Profiles.

Author: Ethan Baker
"""
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import consts as c

class LinkedinBot():
    """
    Encapsulates the functionality related to interacting with
    LinkedIn using Selenium.
    """

    def __init__(self):
        """
        Initializes the Linkedin Bot.
        """
        self.user = c.USERNAME
        self.password = c.PASSWORD
        self.num_requests = c.NUM_REQUESTS
        self.min_connections = c.MINIMUM_CONNECTION_COUNT
        self.excel = c.EXCEL_INPUT_LOCATION
        self.message = c.MESSAGE
        options = Options()
        user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                      " AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/114.0.5735.133 Safari/537.36")
        
        options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome(options=options)
    
    def login(self):
        """
        Logs into LinkedIn using the provided username and password.

        Returns: True if the login is successful, False otherwise.
        """
        # Enter username and password into fields
        self.driver.get("https://linkedin.com/login")
        username_field = self.driver.find_element("id", "username")
        username_field.send_keys(self.user)
        password_field = self.driver.find_element("id", "password")
        password_field.send_keys(self.password)

        # Randomize wait to avoid being flagged
        time.sleep(random.uniform(3,5))

        # Submit
        password_field.send_keys(Keys.ENTER)

        # Check success
        time.sleep(random.uniform(3,5))
        if self.driver.current_url == "https://www.linkedin.com/feed/":
            return True
        else:
            time.sleep(30)
        return False

    def send_connection_request(self, message):
        """
        Sends a connection request to a LinkedIn profile.

        Returns: True if connection request was successful, False otherwise.

        Parameter message: The connection message being sent.
        Precondition: message must be a String where len(message) <= 300.
        """
        try:
            connect_button = self.driver.find_element("xpath", 
                ( "(//button[contains(@aria-label,"
                " 'Invite') and contains(@class, "
                "'pvs-profile-actions__action')])"))
            connect_button.click()
            time.sleep(random.uniform(3,5))

            add_note_button = self.driver.find_element("xpath", 
                                        "//button[@aria-label='Add a note']")
            add_note_button.click()
            time.sleep(random.uniform(3,5))

            message_entry = self.driver.find_element("xpath", 
                                        "//textarea[@name='message']")
            message_entry.send_keys(message)
            time.sleep(random.uniform(3,5))

            send_button = self.driver.find_element("xpath", 
                                    "//button[@aria-label='Send now']")
            send_button.click()
            time.sleep(random.uniform(3,5))

            self.driver.find_element('xpath', 
                ("//button[contains(@aria-label, 'Pending') and contains(@class,"
                 " 'pvs-profile-actions__action') and .//span[contains(@class, "
                 "'artdeco-button__text') and text()='Pending']]"))
            return True
        
        except NoSuchElementException:
            return False
        
    def more_then_connect(self, message):
        """
        Sends a conenction request to a LinkedIn profile when the blue
        connection button isn't visible.

        Returns: True if the connection request was successful, False otherwise.

        Parameter message: The connection message being sent.
        Precondition: message must be a String where len(message) <= 300.
        """
        try:
            more_button = self.driver.find_element("xpath", 
                ("(//button[contains(@class, 'artdeco-dropdown__trigger') "
                 "and contains(@class, 'artdeco-dropdown__trigger--placement-"
                 "bottom') and contains(@class, 'ember-view') and contains(@class,"
                 " 'pvs-profile-actions__action') and contains(@class, "
                 "'artdeco-button') and contains(@class, "
                 "'artdeco-button--secondary') and contains(@class, "
                 "'artdeco-button--muted') and contains(@class,"
                 " 'artdeco-button--2') and @aria-label='More actions'])[2]"))
            more_button.click()
            self.driver.execute_script("window.scrollBy(0, 300)")
            time.sleep(random.uniform(3,5))

            connect_button = self.driver.find_element("xpath", 
                    ("(//div[contains(@aria-label, 'Invite') and "
                     "contains(@aria-label, 'to connect')])"))
            self.driver.execute_script("arguments[0].click();", connect_button)
            time.sleep(random.uniform(3,5))

            add_note_button = self.driver.find_element("xpath", 
                "//button[@aria-label='Add a note']")
            add_note_button.click()
            time.sleep(random.uniform(3,5))

            message_entry = self.driver.find_element("xpath", 
                "//textarea[@name='message']")
            message_entry.send_keys(message)
            time.sleep(random.uniform(3,5))

            send_button = self.driver.find_element("xpath", 
                "//button[@aria-label='Send now']")
            send_button.click()
            time.sleep(random.uniform(3,5))

            self.driver.find_element('xpath', 
                ("//div[contains(@aria-label, 'Pending') and "
                 "contains(@class, 'artdeco-dropdown__item')]"))
            return True
        
        except WebDriverException:
            return False
        
    def accept_request(self):
        """
        Accepts any incoming connection requests from users being checked.

        Returns: True if the connection request was successful, False otherwise.
        """
        try:
            accept_button = self.driver.find_element("xpath", 
                ("//button[contains(@aria-label, 'Accept') and "
                 "contains(@class, 'pvs-profile-actions__action')]"))
            accept_button.click()
            time.sleep(random.uniform(3,5))

            self.driver.find_element("xpath", 
                ("//button[contains(@aria-label, 'Message') and "
                 "contains(@class, 'artdeco-button--primary')]"))
            return True
        
        except NoSuchElementException:
            return False
        
    def extract_connection_count(self):
        """
        Extracts the connection count from the LinkedIn Profile page.

        If the connection count isn't visable, it returns the follower count instead.

        Returns: An Integer between 0 and 500 representing the 
        number of connections that the profile has.
        """
        time.sleep(random.uniform(3,5))
        try:
            connection_count = self.driver.find_element("xpath",
                '(//span[@class="t-bold"])[1]')
            number = connection_count.text.replace(",", "")
            if number.isnumeric():
                return int(number)
            elif connection_count.text == "500+":
                return 500
            else:
                return 0
        except NoSuchElementException:
            return 0

    def has_connect_button(self):
        """
        Checks if LinkedIn gives the user the option to connect with the current profile.

        Returns: True if the profile has the conenct button, False otherwise.
        """
        try:
            connect = self.driver.find_element("xpath", 
                "(//span[@class='artdeco-button__text'])[6]")
            connect_following = self.driver.find_element("xpath", 
                "(//span[@class='artdeco-button__text'])[8]")
            if connect.text == "Connect" or connect_following.text=="Connect":
                return True
            else:
                return False
        except NoSuchElementException:
            return False
        
    def has_accept_button(self):
        """
        Checks if the user can accept an invite from the current profile.

        Returns True if the profile has an accept button, False otherwise.
        """
        try:
            accept = self.driver.find_element("xpath", 
                "(//span[@class='artdeco-button__text'])[6]")
            if accept.text == "Accept":
                return True
            else:
                return False
        except NoSuchElementException:
            return False
    
    def has_hidden_connect_button(self):
        """
        Checks if the user can send a request after clicking more.

        Returns True if the profile has a hidden connect button, False otherwise.
        """
        try:
            self.driver.find_element("xpath", 
                ("(//div[contains(@class, 'artdeco-dropdown__item') and "
                 "contains(@class, 'artdeco-dropdown__item--is-dropdown')"
                 " and contains(@class, 'ember-view') and contains(@class,"
                 " 'full-width') and contains(@class, 'display-flex') and"
                 " contains(@class, 'align-items-center')]/"
                 "span[text()='Connect'])[1]"))
            return True
        except NoSuchElementException:
            return False
    
    def write_message(self):
        """
        Extracts the first name from the LinkedIn profile page,
        then assembles the personalized message to send. Allows the 
        user the put [FULL NAME] and [FIRST NAME] in their message to instruct the 
        program to automatically insert the profile's name.

        Returns: A String representing the personalized connection message.
        """
        full_name = self.driver.find_element("xpath", 
            ('(//h1[@class="text-heading-xlarge inline t-24'
             ' v-align-middle break-words"])[1]')).text
        name_list = full_name.split(" ")
        first = name_list[0]
        if first.lower() not in ['dr.', 'mr.' 'mrs.', 
                                 'ms.', 'dr', 'mr', 'mrs' 'ms']:
            first_name = name_list[0]
        else: 
            first_name = name_list[1]

        msg = c.MESSAGE.replace('[FULL NAME]', full_name)
        msg =msg.replace('[FIRST NAME]', first_name)
        return msg
        
    def check_weekly_limit(self):
        """
        Checks if the weekly request limit has been reached.

        Returns: True if the request limit has been reached, False otherwise.
        """
        try:
            self.driver.find_element("xpath", 
                ("//h2[@class='ip-fuse-limit-alert__header t-20 t-black ph4' "
                 "and @id='ip-fuse-limit-alert__header' and text()='You’ve "
                 "reached the weekly invitation limit']"))
            return True
        except NoSuchElementException:
            return False
        
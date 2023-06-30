"""
The Bot Controller module of the LinkedIn Connection Automation Bot.

This module coordinates the overall execution of the LinkedIn Bot's Tasks.
"""
import time
import random
import pandas as pd
from selenium.common.exceptions import WebDriverException
from connection_automator.linkedin_bot import LinkedinBot
import consts as c

class BotController():
    """
    This class coordinates the overall execution of the LinkedIn bot.
    """

    def __init__(self):
        """
        Initializes the bot controller.
        """
        self.min_connections = c.MINIMUM_CONNECTION_COUNT
        self.num_requests = c.NUM_REQUESTS
        self.excel = c.EXCEL_INPUT_LOCATION
        self.used_profiles = []
        self.num_sent = 0
        self.df = pd.read_excel(self.excel)

    def run(self):
        """
        Executes the LinkedIn bot, performing login, reading URLs,
        and sending connection requests.

        Returns: A success message, or any error messages the program encounters.
        """
        try:
            # Create LinkedIn Bot
            bot = LinkedinBot()
            # Login
            if not bot.login():
                return "Could not login. Possible Captcha."

            # Send request
            i = 0
            error = ""
            while self.num_sent < self.num_requests:
                # Go to profile
                url = self.df['Link'][i]
                bot.driver.get(url)
                self.used_profiles.append(url)
                time.sleep(random.uniform(3,5))
                # Assess connection conditions and send
                try:
                    if bot.extract_connection_count() >= self.min_connections:
                        if bot.has_connect_button():
                            message = bot.write_message()
                            if bot.send_connection_request(message):
                                self.num_sent+=1
                        elif bot.has_hidden_connect_button():
                            message = bot.write_message()
                            if bot.more_then_connect(message):
                                self.num_sent+=1
                        elif bot.has_accept_button():
                            bot.accept_request()
                    
                    # Check if limit has been triggered
                    if bot.check_weekly_limit():
                        error = "Weekly limit reached. " + self.num_sent + " sent."
                        break
                except:
                    pass
                i+=1
                if i < self.num_requests:
                    time.sleep(random.uniform(3,5))

            bot.driver.quit()

            # Remove used profiles from dataframe
            self.df = self.df[~self.df['Link'].isin(self.used_profiles)]

            # Save to excel
            self.df.to_excel(self.excel, index=False)

            if error != "":
                return error
            return "Completed: " + str(self.num_sent) + " sent."

        except WebDriverException:
            self.df = self.df[~self.df['Link'].isin(self.used_profiles)]
            self.df.to_excel(self.excel, index=False)
            return "WebDriverException Error"
        except KeyboardInterrupt:
            self.df = self.df[~self.df['Link'].isin(self.used_profiles)]
            self.df.to_excel(self.excel, index=False)
            return "Program stopped by the user."
        except:
            self.df = self.df[~self.df['Link'].isin(self.used_profiles)]
            self.df.to_excel(self.excel, index=False)
            return "Unexpected error."
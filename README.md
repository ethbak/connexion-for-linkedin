![connexion_banner](https://github.com/ethbak/connexion-for-linkedin/assets/136761692/be87064a-181f-42f3-be6b-21a6c352df5a)

<div align="center">

![Static Badge](https://img.shields.io/badge/Author-Ethan_Baker-green)
![Static Badge](https://img.shields.io/badge/GitHub-ethbak-orange?link=https%3A%2F%2Fgithub.com%2Fethbak)
![Static Badge](https://img.shields.io/badge/LinkedIn-ethbak-blue?link=https%3A%2F%2Flinkedin.com%2Fin%2Fethbak)
![Static Badge](https://img.shields.io/badge/Website-ebaker.us-red?link=http%3A%2F%2Febaker.us)
![Static Badge](https://img.shields.io/badge/License-Apache%202.0-purple?link=https%3A%2F%2Fwww.apache.org%2Flicenses%2FLICENSE-2.0)

</div>

# ❓ What is ConneXion?

ConneXion is a Python tool that serves as a free alternative to LinkedIn Sales Navigator. It enables users to search for and automatically connect with new LinkedIn profiles based on their preferences. Initially developed for Price Financial Management, a Financial Advising firm looking to expand their online presence and find client leads via LinkedIn, ConneXion can be used by any professional looking to expand their LinkedIn network efficiently. With ConneXion, you can find relevant professionals easily, personalize connection requests, and establish valuable connections effortlessly.

# 🎥 Videos
### [Search Demo](https://youtu.be/bCwgYY1-Xi4)
### [Connect Demo](https://youtu.be/rrk3BKkUm2E)

# 💡 Features
### Profile Search Tool
Utilizes the Google Custom Search JSON API to allow users to find LinkedIn profiles based on Position, Location, and Experience preferences. The tool outputs profile data to an Excel file that can be used with the Connection Automation Tool or be saved for further analysis by the user. With a Google API key, the user can generate up to 1,000 free results per day.
### Connection Automation Tool
Allows the user to automate sending LinkedIn connection requests via Selenium. The tool parses through an Excel file of LinkedIn profile URLs and sends each one a connection request, if possible. The user can specify how many requests to send and can customize the connection request message to their preferences, including the option to dynamically insert the receiving profile’s name. Utilizing this tool allows users to easily grow their LinkedIn connection network.

# 📀 Technologies

![Static Badge](https://img.shields.io/badge/PYTHON-blue?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/PANDAS-purple?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/TKINTER-gold?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/SELENIUM-green?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/JSON-orange?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/CUSTOM%20SEARCH%20API-red?style=for-the-badge)

# 🚫 Limitations

### Google API Requests
Google limits its free Custom Search API requests to 100 per day, resulting in a maximum of 1000 new profile results. Extra requests can be purchased for $5 per 1000 [here](https://developers.google.com/custom-search/v1/overview).

### LinkedIn TOS
As per LinkedIn’s [Terms of Service](https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin?lang=en#:~:text=In%20order%20to%20protect%20our,automate%20activity%20on%20LinkedIn's%20website), the use of third party automated tools is prohibited. Therefore, users of the Connection Automation Tool must operate at their own risk. If LinkedIn detects extended automated activity, they can temporarily deactivate or ban users’ accounts. The bot takes precautions the limit this possibility, including randomized delays between activity, but it still is important to use the tool responsibly. It is recommended to only send ~30 requests at a time, once per day. If an account is temporarily disabled, it is recommended to stop using the tool for an extended period of time to avoid a permanent ban.

### Login Captchas
A common precaution against unnatural activity on LinkedIn are login captchas. LinkedIn may make users fill out a captcha after logging in if they detect too many logins in a short period of time. To combat this, the bot stops for a short period of time on the Captcha screen to allow the user to manually solve it. This allows the program to work efficiently until the next time it has to log the user in.

### Connection Limits
LinkedIn imposes a series of [limits](https://www.linkedin.com/help/linkedin/answer/a551012/types-of-restrictions-for-sending-invitations?lang=en) on the number of connections you can have and send. To stay within the limits, do not exceed the following:
- 100 connection requests per week
- 3,000 active connection requests
- 30,000 connections overall

# 🛠️ Installation

### From Source Code
Prerequisites:
1. Install [Python / Anaconda](https://docs.anaconda.com/free/anaconda/install/index.html).
2. Download [Google Chrome](https://www.google.com/chrome/).

Steps:
1. Download source code from the [repository](https://github.com/ethbak/connexion-for-linkedin).
2. Open your computer's terminal and navigate to the application's folder.
3. Run the following command to install the application's dependencies:
   ```console
   pip install pillow numpy pandas selenium requests
   ```
4. Start the application by running the following command:
   ```console
   python main.py
   ```
### From Release
1. TODO

# 👥 Usage

### Profile Search Tool
The Profile Search Tool can be accessed by starting the application and clicking the "Search for Profiles" button. This reveals a window containing filters and user preferences for the tool. Below is an overview of the different fields and their capabilities.
- Locations (Comma Separated):
  - Allows the user to search for profiles based on a list of locations. Users should input a comma-separated list of locations for best results. Must not be blank.
- Positions (Comma Separated):
   - Allows the user to search for profiles that work in a variety of positions. Users should input a comma-separated list of positions for best results. Must not be blank.
- Experience Dropdown:
   - A dropdown list containing the options ">", "<", and "=", where ">" represents greater than, "<" represents less than, and "=" represents equal to. Works in conjunction with the experience entry field to allow the user to search for profiles with a range of experience levels.
- Experience Entry Field:
  - Allows the user to enter their desired number of years of experience to allow them to search for profiles of all experience levels. Must be an integer between 0 and 30.
- Output Location:
   - The location of the output Excel file. Must end with .xlsx and represent a valid file path. Existing Excel files will be added to, not overridden. New Excel files can also be created as long as the path is valid.
- Custom Search API Key:
   - The user's Google Custom Search JSON API key. Must be a valid key. User's can create an API key [here](https://developers.google.com/custom-search/v1/overview).
- Repeat Queries Box:
   - When checked, previously searched terms will be searched again, it is recommended to check this if significant time has passed since last searching. When unchecked, previously searched terms are skipped.

### Connection Automation Tool
The Connection Automation Tool can be accessed by starting the application and clicking the "Automate Connections" button. This reveals a window containing filters and user preferences for the tool. Below is an overview of the different fields and their capabilities.
- LinkedIn Username:
   - The email or phone number associated with the user's LinkedIn account. Must be a valid LinkedIn username. Users that do not have a LinkedIn account can sign up [here](https://www.linkedin.com/signup) 
- LinkedIn Password:
   - The password associated with the user's LinkedIn account. Paired with the username, the password must represent a valid LinkedIn login. 
- Connection Message:
   - The message that is sent to profiles when completing connection requests. User's can write [FIRST NAME] and [FULL NAME] to instruct the user to dynamically insert profile name information into the message. Must be less than 300 characters, but it is recommended to stay below 250 characters when using the dynamic name operators as longer LinkedIn profile names can cause issues.
- Number of requests to send:
   - The number of outgoing connection requests to send. Must be an integer between 1 and 50, but it is recommended to limit the number of requests to less than 30 per day.
- Minimum connections count:
   - The minimum number of connections a LinkedIn profile must have to be sent a connection request. This allows users to filter out inactive LinkedIn accounts if needed. Must be an integer between 0 and 500. 
- Excel file path:
   - The location of the Excel file containing the list of all of the LinkedIn URLs to attempt to connect with. URLs must be listed under a column named "Links". It is recommended to use the same excel path for the Search Tool output and the Connection Automation Tool input. Must represent a valid file path to a .xlsx file fitting the description above.

# 🏎️ Performance

### Profile Search Tool

Retrieves `1000` new profiles in under `60` seconds.

### Connection Automation Tool

Completes `30` connection requests in under `18` minutes.

# 🧪 Running Tests
To run tests for ConneXion, navigate to the `test.py` file in the project directory, which contains all of the application’s test cases. Files related to testing are stored in the `tests` folder. Some test cases, especially those relating to the linkedin connection bot, will fail due to the dynamic and unpredictable nature of LinkedIn profiles. Many of the test cases are resource intensive, i.e. they use Google API requests or they heighten the risk of LinkedIn restrictions by repeatedly logging in the user. Therefore, it is advisable to only test a few methods at a time.

# 👨‍💻 Contributors

### [Ethan Baker](http://ebaker.us)

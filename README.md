![connexion_banner](https://github.com/ethbak/connexion-for-linkedin/assets/136761692/be87064a-181f-42f3-be6b-21a6c352df5a)

<div align="center">

![Static Badge](https://img.shields.io/badge/Author-Ethan_Baker-green)
![Static Badge](https://img.shields.io/badge/GitHub-ethbak-orange?link=https%3A%2F%2Fgithub.com%2Fethbak)
![Static Badge](https://img.shields.io/badge/LinkedIn-ethbak-blue?link=https%3A%2F%2Flinkedin.com%2Fin%2Fethbak)
![Static Badge](https://img.shields.io/badge/Website-ebaker.com-red?link=https%3A%2F%2Febaker.com)
![Static Badge](https://img.shields.io/badge/License-Apache%202.0-purple?link=https%3A%2F%2Fwww.apache.org%2Flicenses%2FLICENSE-2.0)

</div>

# ❓ What is Connexion?

Connexion is a Python tool that serves as a free alternative to LinkedIn Sales Navigator. It enables users to search for and automatically connect with new LinkedIn profiles based on their preferences. Initially developed for Price Financial Management, a Financial Advising firm looking expand their online presence and find client leads via LinkedIn, Connexion can be used by any professional looking to expand their LinkedIn network efficiently. With Connexion, you can find relevant professionals easily, personalize connection requests, and establish valuable connections effortlessly.

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

### From Release

# 👥 Usage

### Profile Search Tool

### Connection Automation Tool

# 🏎️ Performance

### Profile Search Tool

### Connection Automation Tool

# 🧪 Running Tests
To run tests for Connexion, navigate to the `test.py` file in the project directory, which contains all of the application’s test cases. Files related to testing are stored in the `tests` folder. Some test cases, especially those relating to the linkedin connection bot, will fail due to the dynamic and unpredictable nature of LinkedIn profiles. Many of the test cases are resource intensive, ie. they use Google API requests or they heighten the risk of LinkedIn restrictions by repeatedly logging in the user. Therefore, it is advisable to only test a few methods at a time.

# 👨‍💻 Contributors

### [Ethan Baker](https://ebaker.com)

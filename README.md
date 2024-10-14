README

X.com Post Tracker Discord Bot

This is a Python Discord bot that tracks new posts from a specified account on X.com and sends them to a specified Discord channel. The bot checks for new posts every 30 minutes.

Requirements

Python 3.9 or higher
Discord.py library
Requests library
A X.com API key
A Discord bot token
Installation

Clone the repository: git clone https://github.com/<your-github-QuothingRaven>/x-post-tracker-bot.git
Install the required libraries: pip install discord.py requests
Create a new file named .env in the project folder and add your X.com API key, X.com API secret, Discord bot token, X.com account name, and Discord channel ID:

Copy code

X_API_KEY=your_x_api_key
X_API_SECRET=your_x_api_secret
DISCORD_TOKEN=your_discord_bot_token
X_ACCOUNT=your_x_account_name
DISCORD_CHANNEL_ID=your_discord_channel_id
Run the bot: python bot.py
Usage

Invite the bot to your Discord server: https://discord.com/oauth2/authorize?client_id=<bot-client-id>&scope=bot
Once the bot is invited, run the bot using python bot.py
The bot will check for new posts from the specified X.com account every 30 minutes and send them to the specified Discord channel.
Contributing

Feel free to contribute to this project by submitting bug fixes, adding features, or improving the code structure. Please create a pull request with a clear description of the changes you've made.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Author

QuothingRaven - ravenmarketing@protonmail.com

I hope this helps! Let me know if you have any questions or need further assistance.

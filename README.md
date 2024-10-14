Discord Bot for Multiple Account Post Embeds

This bot fetches the latest posts from multiple accounts and embeds them into specified Discord channels at regular intervals. It uses the Discord API and an external API (e.g., X.com) to retrieve posts.

Features

	•	Monitors multiple accounts for new posts.
	•	Sends the latest posts to one or more Discord channels associated with each account.
	•	Fetches posts every 10 minutes (can be adjusted).
	•	Handles errors during API requests and logs them.

Prerequisites

	•	Python 3.8 or higher
	•	A Discord bot with Message Content Intent enabled
	•	External API keys for fetching posts from accounts (in this example, X.com)

Setup Instructions

1. Clone the repository

git clone https://github.com/your-repo/discord-bot-multi-account.git
cd discord-bot-multi-account

2. Install the required dependencies

Ensure you have pip installed, then run:

pip install -r requirements.txt

3. Create a .env file

Create a .env file in the root directory of the project (next to your Python scripts). See the Environment Variables section for the required keys.

4. Enable Intent Permissions in the Discord Developer Portal

	•	Go to the Discord Developer Portal.
	•	Select your bot.
	•	Under the Bot tab, scroll to Privileged Gateway Intents.
	•	Enable Message Content Intent.

5. Run the bot

Run the following command to start your bot:

python bot.py

Environment Variables

You’ll need to provide several environment variables in your .env file to configure the bot. Here’s a breakdown:

Required Variables:

Variable Name	Description
X_API_KEY	The API key for the external service (e.g., X.com) to fetch posts
X_API_SECRET	The API secret for authentication with the external service
DISCORD_TOKEN	The token for your Discord bot
X_ACCOUNTS	Comma-separated list of account usernames to monitor for posts
DISCORD_CHANNEL_IDS	Comma-separated list of Discord channel IDs to send posts to

Example .env file:

# API Keys and Secrets
X_API_KEY=your_x_api_key_here
X_API_SECRET=your_x_api_secret_here

# Discord Bot Token
DISCORD_TOKEN=your_discord_bot_token_here

# Account Usernames to Monitor
X_ACCOUNTS=account_1,account_2

# Channel IDs where posts will be sent
# For each account, you can specify the channels in the bot's code

Modifying Fetch Interval

The bot fetches new posts every 10 minutes by default. If you’d like to change the fetch interval, adjust the asyncio.sleep(10 * 60) line in the fetch_new_posts function in the bot.py file. This value is the delay between each fetch cycle, measured in seconds (e.g., 10 minutes = 600 seconds).

Example Code Customization

Mapping Channels to Accounts

If you need to send posts from different accounts to different channels, edit the account_channel_map dictionary in bot.py:

account_channel_map = {
    "account_1": [123456789012345678, 987654321098765432],  # Channels for account_1
    "account_2": [123456789012345678],                     # Channels for account_2
    # Add more accounts and channels as needed
}

Logging and Error Handling

The bot currently prints any errors that occur when fetching posts. You can customize this behavior by modifying the print statements in the fetch_new_posts function.

Troubleshooting

	1.	Bot is not sending messages to the channel:
	•	Ensure the bot has permission to send messages in the specified channel.
	•	Verify that the bot is properly connected and authenticated with the correct token.
	2.	API Requests Fail:
	•	Check the API key and secret in your .env file.
	•	Make sure the external service (e.g., X.com) is accessible and not experiencing downtime.
	3.	Message Content Warning:
	•	Ensure that Message Content Intent is enabled both in the bot’s code and in the Discord Developer Portal.
	4.	Bot Crashes:
	•	Review the error logs printed to the console. If necessary, add more specific error handling or logging in the fetch_new_posts function.
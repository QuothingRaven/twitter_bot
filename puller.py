import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Enable message content intent

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def fetch_new_posts(self):
        while True:
            for account, channel_ids in account_channel_map.items():
                try:
                    # Fetch the latest post for each account
                    response = requests.get(f'https://x.com/v1/users/{account}/posts', headers=headers)
                    response.raise_for_status()  # Check for HTTP errors
                    post = response.json()['data'][0]
                    post_text = post['text']

                    # Send the post to all associated channels
                    for channel_id in channel_ids:
                        channel = self.get_channel(channel_id)
                        if channel:
                            await channel.send(f'New post from {account}: {post_text}')
                except Exception as e:
                    print(f"Failed to fetch new post for {account}: {e}")

            await asyncio.sleep(10 * 60)  # Check every 10 minutes

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')
        await self.fetch_new_posts()

bot = MyBot()

# Load API credentials from environment variables
x_api_key = os.getenv("X_API_KEY")
x_api_secret = os.getenv("X_API_SECRET")
discord_token = os.getenv("DISCORD_TOKEN")

# List of accounts to monitor
x_accounts = os.getenv("X_ACCOUNTS").split(',')

# Mapping of accounts to channel IDs
account_channel_map = {
    "account_1": [123456789012345678, 987654321098765432],  # Channels for account_1
    "account_2": [123456789012345678],                     # Channels for account_2
    # Add more accounts and channels here
}

headers = {
    'Authorization': f'Bearer {x_api_key}',
    'Content-Type': 'application/json',
}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

bot.run(discord_token)
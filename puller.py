import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import asyncio
from discord import Channel

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

x_api_key = os.getenv("X_API_KEY")
x_api_secret = os.getenv("X_API_SECRET")
discord_token = os.getenv("DISCORD_TOKEN")
x_account = os.getenv("X_ACCOUNT")
discord_channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))

headers = {
    'Authorization': f'Bearer {x_api_key}',
    'Content-Type': 'application/json',
}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!'):
        return

    if message.author.name.lower() == x_account:
        response = requests.get(f'https://x.com/v1/users/{x_account}/posts', headers=headers)
        post = response.json()['data'][0]
        post_text = post['text']
        await message.channel.send(f'{post_text}')

async def fetch_new_posts(self):
    while True:
        await self.schedule_post_check(30 * 60)  # Check for new posts every 30 minutes

async def schedule_post_check(self, delay):
    await self.loop.call_later(delay, self.fetch_new_posts)

@bot.event
async def on_ready():
    await self.fetch_new_posts()

bot.run(discord_token)

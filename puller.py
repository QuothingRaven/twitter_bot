import discord
from discord.ext import commands, tasks
import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

# Discord bot token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# X (formerly Twitter) API credentials
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')

# X account to monitor
X_ACCOUNT = os.getenv('X_ACCOUNT')

# Discord channel ID to post X posts
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# Set up Discord bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Enable if using discord.py v2.0+
bot = commands.Bot(command_prefix='!', intents=intents)

# Set up X (formerly Twitter) API client
auth = tweepy.OAuthHandler(X_API_KEY, X_API_SECRET)
auth.set_access_token(X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    check_posts.start()

@tasks.loop(minutes=5)  # Check for new posts every 5 minutes
async def check_posts():
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        try:
            tweets = api.user_timeline(screen_name=X_ACCOUNT, count=5, tweet_mode="extended")
            
            for tweet in reversed(tweets):
                # Check if the tweet is new
                if tweet.created_at.replace(tzinfo=timezone.utc) > bot.last_checked:
                    embed = discord.Embed(description=tweet.full_text, color=0x1DA1F2)
                    embed.set_author(name=f"{tweet.user.name} (@{tweet.user.screen_name})", icon_url=tweet.user.profile_image_url)
                    embed.set_footer(text=f"X • {tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # If the tweet has media, add it to the embed
                    if 'media' in tweet.entities:
                        embed.set_image(url=tweet.entities['media'][0]['media_url_https'])
                    
                    await channel.send(embed=embed)
            
            if tweets:
                bot.last_checked = tweets[0].created_at.replace(tzinfo=timezone.utc)
        except tweepy.TweepError as e:
            print(f"Tweepy Error: {e}")
            print(f"Error code: {e.api_code if hasattr(e, 'api_code') else 'N/A'}")
            print(f"Error message: {e.response.text if hasattr(e, 'response') else str(e)}")
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            print(f"Error type: {type(e)}")
            print(f"Error details: {str(e)}")

@check_posts.before_loop
async def before_check_posts():
    await bot.wait_until_ready()
    bot.last_checked = datetime.now(timezone.utc)

bot.run(DISCORD_TOKEN)

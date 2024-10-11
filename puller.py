import discord
from discord.ext import commands, tasks
import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord bot token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Twitter API credentials
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Twitter account to monitor
TWITTER_ACCOUNT = os.getenv('TWITTER_ACCOUNT')

# Discord channel ID to post tweets
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# Set up Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Set up Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    check_tweets.start()

@tasks.loop(minutes=5)  # Check for new tweets every 5 minutes
async def check_tweets():
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        tweets = api.user_timeline(screen_name=TWITTER_ACCOUNT, count=5, tweet_mode="extended")
        for tweet in reversed(tweets):
            # Check if the tweet is new (you may want to implement a more robust check)
            if tweet.created_at > bot.last_checked:
                embed = discord.Embed(description=tweet.full_text, color=0x1DA1F2)
                embed.set_author(name=f"{tweet.user.name} (@{tweet.user.screen_name})", icon_url=tweet.user.profile_image_url)
                embed.set_footer(text=f"Twitter • {tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # If the tweet has media, add it to the embed
                if 'media' in tweet.entities:
                    embed.set_image(url=tweet.entities['media'][0]['media_url_https'])
                
                await channel.send(embed=embed)
        
        bot.last_checked = tweets[0].created_at if tweets else bot.last_checked

@check_tweets.before_loop
async def before_check_tweets():
    await bot.wait_until_ready()
    bot.last_checked = discord.utils.utcnow()

bot.run(DISCORD_TOKEN)

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

# X.com API credentials
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')

# X.com account to monitor
X_ACCOUNT = os.getenv('X_ACCOUNT')

# Discord channel ID to post X.com posts
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# Set up Discord bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Set up X.com API client
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
            posts = api.user_timeline(screen_name=X_ACCOUNT, count=5, tweet_mode='extended')

            for post in reversed(posts):
                # Check if the post is new
                if post.created_at.replace(tzinfo=timezone.utc) > bot.last_checked:
                    embed = discord.Embed(description=post.full_text, color=0x1DA1F2)
                    embed.set_author(name=f'{post.user.name} (@{post.user.screen_name})', icon_url=post.user.profile_image_url)
                    embed.set_footer(text=f'X.com • {post.created_at.strftime("%Y-%m-%d %H:%M:%S")}')

                    if 'media' in post.entities:
                        embed.set_image(url=post.entities['media'][0]['media_url_https'])

                    await channel.send(embed=embed)

            if posts:
                bot.last_checked = posts[0].created_at.replace(tzinfo=timezone.utc)

        except tweepy.TweepError as e:
            print(f'Tweepy Error: {e}')
            print(f'Error code: {e.api_code if hasattr(e, "api_code") else "N/A"}')
            print(f'Error message: {e.response.text if hasattr(e, "response") else str(e)}')
        except Exception as e:
            print(f'Error fetching posts: {e}')
            print(f'Error type: {type(e)}')
            print(f'Error details: {str(e)}')

@check_posts.before_loop
async def before_check_posts():
    await bot.wait_until_ready()
    bot.last_checked = datetime.now(timezone.utc)

bot.run(DISCORD_TOKEN)

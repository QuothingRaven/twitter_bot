# Discord Twitter Bot

## Description
This Discord bot automatically fetches tweets from specified Twitter accounts and posts them as embeds in designated Discord channels. It's designed to keep your Discord community updated with the latest tweets from chosen Twitter accounts without leaving Discord.

## Features
- Fetches tweets from specified Twitter accounts at regular intervals
- Embeds tweets in Discord channels, including text content, author information, and media
- Configurable through environment variables
- Open-source and customizable

## Installation

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token
- Twitter Developer Account with API credentials

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/discord-twitter-bot.git
   cd discord-twitter-bot
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your credentials:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   TWITTER_API_KEY=your_

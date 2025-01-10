# version for windows exe, use config parser to parse ini instead of a json

import discord
from discord.ext import tasks, commands
import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

BOT_TOKEN = config['MAIN']['BOT_TOKEN']

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

target_channel_id = config['MAIN']['target_channel_id']
posted_urls_file = 'posted_urls.json'

def load_posted_urls():
    if os.path.exists(posted_urls_file):
        with open(posted_urls_file, 'r') as f:
            return set(json.load(f))
    else:
        return set()

def save_posted_urls(urls):
    with open(posted_urls_file, 'w') as f:
        json.dump(list(urls), f)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("bot is ready! 👍")
    fetch_releases.start()

@tasks.loop(minutes=5)
async def fetch_releases():
    channel = bot.get_channel(target_channel_id)
    if not channel:
        print("ERROR: target channel not found.")
        return

    url = "https://www.reddit.com/r/VinylReleases/new.json"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.1"} # one of the most common user agents

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # raise an exception for error HTTP status
        data = response.json()
        posts = data['data']['children']

        posted_urls = load_posted_urls()

        for post in posts:
            post_data = post['data']
            title = post_data.get('title', 'Unknown Title').lower()
            flair = post_data.get('link_flair_text', '')
            store_url = post_data.get('url', 'No URL')

            if flair in ["REPRESS", "NEW RELEASE"] and store_url not in posted_urls: # you can add or remove flairs to be pinged for those aswell
                artists_to_ping = [artist.lower() for artist in config.get("MAIN", "artists").split(",")]
                
                user_id = config["MAIN"]["user_id"]
                for artist in artists_to_ping:
                    if artist in title.lower():
                        await channel.send(f"<@{user_id}> New release: {title}\n{store_url}") # replace with your user ID or role ID
                        posted_urls.add(store_url)
                        break

        save_posted_urls(posted_urls)

    except Exception as e:
        print(f"Error fetching or sending data: {e}")

bot.run(BOT_TOKEN)

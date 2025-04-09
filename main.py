import discord
from discord.ext import tasks, commands
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)  # no / commands but it doesnt work w/o it for some reason

BOT_TOKEN = os.getenv('BOT_TOKEN')
target_channel_id = int(os.getenv('TARGET_CHANNEL_ID'))
posted_urls_file = 'posted_urls.json'
USER_ID = int(os.getenv('USER_ID'))
ARTISTS_TO_PING = os.getenv('ARTISTS_TO_PING').split(',')

def load_posted_urls():
    if os.path.exists(posted_urls_file):
        with open(posted_urls_file, 'r') as f:
            return set(json.load(f))
    return set()

def save_posted_urls(urls):
    with open(posted_urls_file, 'w') as f:
        json.dump(list(urls), f)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("🤖 ready to fetch releases 🤖")
    fetch_releases.start()

@tasks.loop(minutes=5)
async def fetch_releases():
    channel = bot.get_channel(target_channel_id)
    if not channel:
        print("ERROR: target channel not found.")
        return

    url = "https://www.reddit.com/r/VinylReleases/new.json"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3"} # common user agent

    try:
        response = requests.get(url, headers=headers, timeout=10) # dont quit progra if it timesout
        response.raise_for_status()
        data = response.json()
        posts = data['data']['children']
        posted_urls = load_posted_urls()

        for post in posts:
            post_data = post['data']
            title = post_data.get('title', 'Unknown Title').lower()
            flair = post_data.get('link_flair_text', '')
            store_url = post_data.get('url', 'No URL')

            if flair in ["REPRESS", "NEW RELEASE"] and store_url not in posted_urls:
                for artist in ARTISTS_TO_PING:
                    if artist.lower() in title:
                        await channel.send(f"<@{USER_ID}> New release: {title}\n{store_url}")
                        posted_urls.add(store_url)
                        break

        save_posted_urls(posted_urls)

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
    except Exception as e:
        print(f"Unexpected error: {e}")

bot.run(BOT_TOKEN)

import discord
from discord.ext import tasks, commands
import requests
import json
import os
import ssl
import python-dotenv

BOT_TOKEN = '1234567890asdfghjkl'  # Replace with your actual token

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

target_channel_id = 12345678900987654321 # replace with ur real channel id
posted_urls_file = 'posted_urls.json'
USER_ID = 123456 # User ID to ping
ARTISTS_TO_PING = ["replace", "with", "artists", "to", "be", "pinged", "for"]

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
    print("🤖 ready to fetch releases 🤖")
    fetch_releases.start()

@tasks.loop(minutes=5)
async def fetch_releases():
    channel = bot.get_channel(target_channel_id)
    if not channel:
        print("ERROR: target channel not found.")
        return

    url = "https://www.reddit.com/r/VinylReleases/new.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" #common useragent
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        posts = data['data']['children']

        posted_urls = load_posted_urls()

        for post in posts:
            post_data = post['data']
            title = post_data.get('title', 'Unknown Title').lower()
            flair = post_data.get('link_flair_text', '')
            store_url = post_data.get('url', 'No URL')

            if flair in ["REPRESS", "NEW RELEASE"] and store_url not in posted_urls: #you can change these to what they have on the reddit
                for artist in ARTISTS_TO_PING:
                    if artist in title.lower():
                        await channel.send(f"<@{USER_ID}> New release: {title}\n{store_url}") #change the message if u want
                        posted_urls.add(store_url)
                        break

        save_posted_urls(posted_urls)
#stuff below is to not quit if max timeouts or retries are reached
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
    except Exception as e:
        print(f"Unexpected error: {e}")

bot.run(BOT_TOKEN)

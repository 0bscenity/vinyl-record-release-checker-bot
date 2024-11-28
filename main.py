import discord
from discord.ext import tasks, commands
import requests

BOT_TOKEN = 'REPLACE W/ UR TOKEN' #token

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

target_channel_id = None

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print("Bot is ready to fetch releases.")

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$start_release'):
        global target_channel_id
        target_channel_id = message.channel.id
        await message.channel.send("Release tracking started in this channel.")
        fetch_releases.start()

@tasks.loop(minutes=5)
async def fetch_releases():
    """
    Fetch and post releases every 5 minutes if a target channel is set.
    """
    global target_channel_id
    if not target_channel_id:
        return

    url = "https://www.reddit.com/r/VinylReleases/new.json"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.3"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        posts = data['data']['children']

        posted_urls = set()

        for post in posts:
            post_data = post['data']
            store_url = post_data.get('url', 'No URL')

            if store_url not in posted_urls:
                title = post_data['title']
                flair = post_data.get('link_flair_text', '')

                if flair in ["REPRESS", "NEW RELEASE", "RESTOCK"]:
                    artist = title.split(" - ")[0] if " - " in title else title.split("-")[0]
                    artist = artist.strip()

                    message_text = f"@{artist} - {store_url}"

                    channel = client.get_channel(target_channel_id)
                    if channel:
                        await channel.send(message_text)

            posted_urls.add(store_url)
    except Exception as e:
        print(f"Error fetching or sending data: {e}")


client.run(BOT_TOKEN)

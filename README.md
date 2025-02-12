# vinyl-record-release-checker-bot
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
discord bot for new vinyl releases by scraping https://www.reddit.com/r/VinylReleases/new.json

# How do I use this?
---

## Windows 8/10/11
- If you know how to edit python files you can simply follow the instructions meant for linux, but instead of running the nohup command you can just doubleclick main.py
- If you do not know what you are doing with python, there is a precompiled exe for you to run in releases.
- Download latest release (you should download the release meant for you're cpu architecture. If you don't know what you have, just try `x86_64`
- Extract files
- Go to the extracted directory
- Go to https://discord.com/developers/applications/ and click new application and name it whatever you want
- Go to "Bot" in the side menu
- Click "Reset Token"
- Copy the new token (DO NOT LOSE IT OR YOU WILL HAVE TO RESET IT AGAIN)
- Replace `123CHANGEME123`  in `config.ini` with your new token (you MUST keep the `'` around the token)
- Right click the channel where you want the bot to run in, and click `Copy Channnel ID`
- Replace `CHANGEME2CHANNEL` in `config.ini` with your channel id
- replace `artist1, artist2, artist3` in `config.ini` with the artists you want to be pinged for. you MUST include a comma in between artists
- Copy your user id ([click here if you dont know how](https://support.playhive.com/discord-user-id/)) and replace `1234567890` with your user id in `config.ini`
- Run main.exe
- If you followed the instructions correctly, the bot should be running
---

## Python file (Linux/BSD(?)/Mac OS (w/ homebrew))
- Go to releases and download the latest Linux release
- Extract files
- Go to the extracted directory
- Go to https://discord.com/developers/applications/ and click new application and name it whatever u want
- Go to "Bot" in the side menu
- Click "Reset Token"
- Copy the new token (DO NOT LOSE IT OR U WILL HAVE TO RESET IT AGAIN)
- Go into config.json and put in your token with your token
- Right click the channel where you want the bot to run in, and right click "Copy Channnel ID". Paste the channel ID in the spot for it in config.json
- Copy your user id ([click here if you dont know how](https://support.playhive.com/discord-user-id/)) and paste it in the correct spot in config.json
  In config, replace `"artist1", "artist2", "artist3"` with the artists you want to be pinged for. **YOU MUST KEEP THE COMMAS AND QUOTATION MARKS**
- Run `pip install -r requirements.txt`
- If on linux and you want it to continue running after you close the terminal window, install python and run `nohup python main.py &`
- If you want it to stop you can simply double click main.py
- if on windows install python and double click main.py

there are other things you can configure. they have a comment next to them in the code

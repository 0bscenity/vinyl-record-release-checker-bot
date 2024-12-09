# vinyl-release-checker-bot
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
discord bot for new vinyl releases by scraping https://www.reddit.com/r/VinylReleases/new.json


# How do I use this?
---

** INSTRUCTIONS NOT FINISHED YET**
- Click the green "Code" button at the top right and click download zip
- Extract files
- Go to the extracted directory
- Go to https://discord.com/developers/applications/ and click new application and name it whatever u want
- Go to "Bot" in the side menu
- Click "Reset Token"
- Copy the new token (DO NOT LOSE IT OR U WILL HAVE TO RESET IT AGAIN)
- Go into main.py and edit line 6 with your token
- Right click the channel where you want the bot to run in, and right click "Copy Channnel ID". Paste the channel ID in line 14
- Copy your user id ([click here if you dont know how](https://support.playhive.com/discord-user-id/)) and paste it in line 63
- Replace ```"replace", "with", "real", "artists"``` with the artists you want to be pinged for

- 
- Run ```pip install -r requirements.txt```
- if on linux run ```nohup python main.py```

there are other things you can configure. they have a comment next to them in the code

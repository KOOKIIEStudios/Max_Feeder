"""This bot periodically checks a RSS Feed for updates

This bot will keep track of the latest posts of the
Orange Mushroom Blog, and post to Dicord whenever there
is a new post.
"""

import os  # Standard Library
import json
from datetime import datetime, timdelta
import discord  # Required Modules
from discord.ext import commands, tasks

import feeder  # User-defined Modules


# Load config
with open(os.path.dirname(os.path.abspath(__file__)) + '/config.json', 'r') as f:
	config = json.load(f)

# Creating an instance of the bot client
bot = commands.Bot("!")  # commands not used currently; open for future extension

@tasks.loop(hours=12)
async def check_for_new(ctx):
    # Checks for new posts every 12 hours
	# Logic goes here

@bot.event
async def on_ready():
	print("Bot has successfully started!")
	await check_for_new.start()

def main():
	print("Loading bot...")
	# bot.run(config['BOT_TOKEN'])
	if not feeder.fetch_latest_post():  # terminate bot if feeder does not return a String
		raise SystemExit("There seems to be something wrong with the feed parser! TERMINATING...")


if __name__ == '__main__':
	main()

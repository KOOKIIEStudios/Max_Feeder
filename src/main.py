"""This bot periodically checks a RSS Feed for updates

@author KOOKIIE
This bot will keep track of the latest posts of the
Orange Mushroom's Blog, and post to Dicord whenever there
is a new post.
"""

import os  # Standard Library
import json
import discord  # Required Modules
from discord.ext import commands, tasks

import feeder  # User-defined Modules


# Load config
JSON_PATH = os.path.dirname(os.path.abspath(__file__)) + "/config.json"  # Constant
with open(JSON_PATH, 'r') as f:
	config = json.load(f)

# Creating an instance of the bot client
bot = commands.Bot("!")  # commands not used currently; open for future extension

@tasks.loop(hours=config['DELAY'])
async def check_for_new():
	"""Checks for new posts every 12 hours"""
	latest_post = feeder.fetch_latest_post()
	# If there is a new post
	if int(latest_post.get('id')) > config['LAST_POST']:
		print(f"New post found! Title: {latest_post.get('title')}")
		# Update stored ID for last fetched post 
		temp = config
		temp['LAST_POST'] = latest_post.get('id')
		with open(JSON_PATH, 'w') as f:
			json.dump(temp, f)

		# Send link of post as message body to the kms-updates channel in Azure
		channel = bot.get_channel(config['CHANNEL_ID'])
		await channel.send(latest_post.get('link'))
		print(f"Link sent to Discord channel {config['CHANNEL_ID'}: {latest_post.get('link')}")  # for debug
	else:
		print(f"No new post on Orange Mushroom's Blog. Will try again in {config['DELAY']}hours time.")

@bot.event
async def on_ready():
	print("Bot has successfully started!")
	await check_for_new.start()

def main():
	print("Loading bot...")
	if not feeder.fetch_latest_post():  # terminate bot if feeder does not return a String
		raise SystemExit("There seems to be something wrong with the feed parser! TERMINATING...")
	bot.run(config['BOT_TOKEN'])


if __name__ == '__main__':
	main()

"""Allows Max_Feeder to automatically answer dev details

@author KOOKIIE
Allows the bot to reply in Discord, when users ask questions about the devs.
(Simple prototype)
"""
import re  # Built-in Modules
from discord.ext import commands  # External Modules

import constants  # User-defined Modules


class Dev(commands.Cog, name='dev'):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		# Sends dev details
		if message.author.bot:
			return  # Catch any bot messages, and short-circuit
		name = message.author.name
		contents = message.content
		channel = message.channel

		output = is_a_dev(contents, name)
		if output:  # If not empty
			await channel.send(output)


def setup(bot):  # discord.py construct
	bot.add_cog(Dev(bot))


def is_a_dev(contents, name):
	# Check against all known devs, and for all possible bot names
	for dev in constants.DEVS.keys():
		for bot_name in constants.BOT_NAMES:
			is_dev = re.search(f"{bot_name}.*[Ww]ho.*{dev}", contents)
			if is_dev:
				dev_value = constants.DEVS.get(dev)
				output = f"Hi {name}, {dev_value.get('Name')}'s Profile is as follows:\n"
				output += "\n".join(f"**{k}**: {v}" for (k, v) in dev_value.items())
				return output
	return ""

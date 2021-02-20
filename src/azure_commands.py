"""Azure-related commands

@author KOOKIIE
These are commands specific to Azure, and can be turned on or off
via in-Discord commands
"""

import discord  # Required Modules
from discord.ext import commands

import constants  # User-defined Modules


class AzureCommands(commands.Cog, name='AzureCommands'):
	def __init__(self, bot):
		self.bot = bot

	# Technically possible to group all of them into 1 single handler
	# and perform pattern matching inside the handler
	# instead of using 6 identical commands.
	# But that might be over-engineering.
	# Information commands - outputs string constants to Discord
	@commands.command(aliases=constants.COMMANDS.get('warp').get('aliases'))
	async def warp(self, ctx):
		if not await is_help(ctx, "warp"):
			await ctx.send(constants.WARP_FORMAT)

	@commands.command(aliases=constants.COMMANDS.get('playable').get('aliases'))
	async def playable(self, ctx):
		if not await is_help(ctx, "playable"):
			await ctx.send(constants.PLAYABLE)

	@commands.command(aliases=constants.COMMANDS.get('locale').get('aliases'))
	async def locale(self, ctx):
		if not await is_help(ctx, "locale"):
			await ctx.send(constants.LOCALE)

	@commands.command(aliases=constants.COMMANDS.get('register').get('aliases'))
	async def register(self, ctx):
		if not await is_help(ctx, "register"):
			await ctx.send(constants.REGISTER)

	@commands.command(aliases=constants.COMMANDS.get('versions').get('aliases'))
	async def versions(self, ctx):
		if not await is_help(ctx, "versions"):
			await ctx.send(constants.VERSIONS)

	@commands.command(aliases=constants.COMMANDS.get('wiki').get('aliases'))
	async def wiki(self, ctx):
		if not await is_help(ctx, "wiki"):
			await ctx.send(constants.WIKI)

	@commands.command(aliases=constants.COMMANDS.get('classes').get('aliases'))
	async def hero(self, ctx):
		if not await is_help(ctx, "classes"):
			await ctx.send(constants.CLASSES)

	# Other commands
	@commands.command(name="say")
	async def say(self, ctx):
		"""Redirects messages to a desired channel"""
		if await is_help(ctx, "say"):
			return  # Short-circuit if it's just a 'help'

		# process message contents
		args = ctx.message.content.split(" ")
		if len(args) < 3:  # sanity check
			await ctx.send("Please provide all necessary arguments! `$say <channel> <message>`")
			return
		channel_name = args[1]
		msg = args[2:]

		# map channel name/alias to ID
		channel_id = 0
		for chnl in constants.channels.values():
			names = chnl.get('aliases')
			if channel_name in names:
				channel_id = chnl.get('channel_ID')
				break
		if channel_id == 0:
			await ctx.send("Invalid channel name!")
			return

		# direct message to the appropriate channel
		channel = self.bot.get_channel(channel_id)
		await channel.send(" ".join(msg))


def setup(bot):  # discord.py construct
	bot.add_cog(AzureCommands(bot))


async def is_help(ctx, command):
	"""Show help messages for commands

	Used in every command.
	First checks if there is only 1 (no more/less) argument following 
	the command. Then checks if 2nd word in message is `help`.
	If so, output (to Discord) the description and aliases for the 
	command being queried, and return whether the above action was taken.
	e.g. `$warp help`

	Args:
		ctx: Message context (discord.py construct)
		command: String, representing the command being queried

	Returns:
		True, if 2nd word is `help`
		False, if 2nd word is not `help`, or if the number of arguments
			is more/less than 1
	"""
	args = ctx.message.content.split(" ")
	if len(args) != 2:  # Note: args includes the command itself!
		return False
	elif args[1] == "help":
		output = "**Description:** " + constants.COMMANDS.get(command).get('description')
		if constants.COMMANDS.get(command).get('aliases') is not None:
			output += "\n**Aliases:** " + ", ".join(constants.COMMANDS.get(command).get('aliases'))
		await ctx.send(output)
		return True

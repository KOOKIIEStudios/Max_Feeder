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

	@commands.command(name="say")
	async def say(self, ctx):
		if await is_help(ctx, "say"):
			return  # Short-circuit if it's just a 'help'
		args = ctx.message.content.split(" ")
		if len(args) < 3:  # sanity check
			await ctx.send("Please provide all necessary arguments! `$say <channel> <message>`")
			return
		channel_name = args[1]
		msg = args[2:]

		channel_id = 0
		for chnl in constants.channels.values():
			names = chnl.get('aliases')
			if channel_name in names:
				channel_id = chnl.get('channel_ID')
				break
		if channel_id == 0:
			await ctx.send("Invalid channel name!")
			return

		channel = self.bot.get_channel(channel_id)
		await channel.send(" ".join(msg))


def setup(bot):
	bot.add_cog(AzureCommands(bot))


async def is_help(ctx, command):
	args = ctx.message.content.split(" ")
	if len(args) < 2:
		return False
	elif args[1] == "help":
		output = "**Description:** " + constants.COMMANDS.get(command).get('description')
		if constants.COMMANDS.get(command).get('aliases') is not None:
			output += "\n**Aliases:** " + ", ".join(constants.COMMANDS.get(command).get('aliases'))
		await ctx.send(output)
		return True

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
		if not is_help(ctx, "warp"):
			await ctx.send(constants.WARP_FORMAT)

	@commands.command(aliases=constants.COMMANDS.get('playable').get('aliases'))
	async def playable(self, ctx):
		if not is_help(ctx, "playable"):
			await ctx.send(constants.PLAYABLE)

	@commands.command(aliases=constants.COMMANDS.get('locale').get('aliases'))
	async def locale(self, ctx):
		if not is_help(ctx, "locale"):
			await ctx.send(constants.LOCALE)

	@commands.command(aliases=constants.COMMANDS.get('register').get('aliases'))
	async def register(self, ctx):
		if not is_help(ctx, "register"):
			await ctx.send(constants.REGISTER)

	@commands.command(aliases=constants.COMMANDS.get('versions').get('aliases'))
	async def versions(self, ctx):
		if not is_help(ctx, "versions"):
			await ctx.send(constants.VERSIONS)

	@commands.command(aliases=constants.COMMANDS.get('wiki').get('aliases'))
	async def wiki(self, ctx):
		if not is_help(ctx, "wiki"):
			await ctx.send(constants.WIKI)




def setup(bot):
	bot.add_cog(AzureCommands(bot))


def is_help(ctx, command):
	args = ctx.message.content.split(" ")
	if args[1] == "help":
		await ctx.send(constants.COMMANDS.get(command).get('description'))
		return True
	return False

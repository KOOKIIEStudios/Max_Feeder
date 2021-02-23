"""This bot periodically checks a RSS Feed for updates

@author KOOKIIE
This bot will keep track of the latest posts of the
Orange Mushroom's Blog, and post to Discord whenever there
is a new post.
"""

import os  # Standard Libraries
import json
from datetime import date
import discord  # Required Modules
from discord.ext import commands, tasks

import feeder  # User-defined Modules
import constants
import azure_commands

# Load config
print("Loading Max_Feeder bot...")
JSON_PATH = os.path.dirname(os.path.abspath(__file__)) + "/config.json"  # Constant
with open(JSON_PATH, 'r') as f:
	config = json.load(f)
print("  Config file loaded")

# Creating an instance of the bot client
intents = discord.Intents.default()  # Instantiate Intents object
intents.members = config['MEMBER_INTENT']  # This is required for roles to work
intents.typing = config['TYPING_INTENT']  # Set False to reduce spam
intents.presences = config['PRESENCE_INTENT']  # Set False to reduce spam
bot = commands.Bot(  # Instantiate Bot object with Intents
	command_prefix=config['COMMAND_PREFIX'],
	help_command=None,
	intents=intents,
)
print("  Intents and Privileges configured")
# Load commands
bot.load_extension("azure_commands")
print("  Extension: 'azure_commands' loaded")
bot.load_extension("dev")
print("  Extension: 'dev' loaded")


@tasks.loop(hours=config['DELAY'])
async def check_for_new():
	"""Checks for new posts every 12 hours"""
	latest_post = feeder.fetch_latest_post()

	year = int(latest_post.get('link')[27:31].strip("0"))  # Extract date from the link
	month = int(latest_post.get('link')[32:34].strip("0"))
	day = int(latest_post.get('link')[35:37].strip("0"))
	current_post_date = date(year, month, day)

	last_post_date = date(config['YEAR'], config['MONTH'], config['DAY'])  # Fetch last known post date
	# If there is a new post
	if current_post_date > last_post_date:
		print(f"New post found! Title: {latest_post.get('title')}")
		# Update stored date for last fetched post
		temp = config
		temp['YEAR'] = year
		temp['MONTH'] = month
		temp['DAY'] = day
		with open(JSON_PATH, 'w') as file:
			json.dump(temp, file, indent=4)

		# Send link of post as message body to the kms-updates channel in Azure
		channel = bot.get_channel(config['CHANNEL_ID'])
		await channel.send(latest_post.get('link'))
		print(f"Link sent to Discord channel {config['CHANNEL_ID']}: {latest_post.get('link')}")  # for debug
	else:
		print(f"No new post on Orange Mushroom's Blog. Will try again in {config['DELAY']}hours time.")


@bot.event
async def on_ready():
	print("Bot has successfully started!\n")
	await check_for_new.start()
	print(f"RSS feed parse service started! (Runs every {config['DELAY']} hours)")
	# Monolith architecture: check_for_new added here
	# Optional to refactor out to a Cog


@bot.event
async def on_member_join(member):
	"""
	When a member joins assign them a role from config.json

	Uses Role ID instead of names because SoulGirlJP uses Korean characters
	in the role names, which may or may not cause encoding-related issues.
	"""
	print(f"{member} has joined the discord server!")
	if config['ADD_ROLE']:  # Turn on or off in config.json
		try:
			role = discord.utils.get(member.guild.roles, id=config['PLAYER'])
			await member.add_roles(role)
			print(f"  Role 'Player' added for for {member}.")
		except Exception as e:
			print(f"Error encountered while attempting to assign role:\n  {e}")


@bot.command(name='togglecommands', pass_context=True)
@commands.has_any_role(*constants.STAFF.values())
async def toggle_commands(ctx):
	"""Toggles Azure-related commands on/off"""
	if await azure_commands.is_help(ctx, "togglecommands"):
		return

	commands_cog = bot.get_cog('AzureCommands')  # Returns None if not loaded
	try:
		if commands_cog:
			bot.unload_extension("azure_commands")
			print("Commands turned off")
			await ctx.send("Commands turned off")
		else:
			bot.load_extension("azure_commands")
			print("Commands turned on")
			await ctx.send("Commands turned on")
	except Exception as e:
		print(f"Error encountered while attempting to load/unload extensions:\n  {e}")
		await ctx.send("An error has occurred. Please check the logs.")


@bot.command(name='toggledev', pass_context=True)
@commands.has_any_role(*constants.STAFF.values())
async def toggle_dev(ctx):
	"""Toggles pattern matching on/off"""
	# Short-circuit if fetching help:
	if await azure_commands.is_help(ctx, "toggledev"):
		return

	dev_cog = bot.get_cog('dev')  # Returns None if not loaded
	try:
		if dev_cog:
			bot.unload_extension("dev")
			print("Pattern matching turned off")
			await ctx.send("Pattern matching turned off")
		else:
			bot.load_extension("dev")
			print("Pattern matching turned on")
			await ctx.send("Pattern matching turned on")
	except Exception as e:
		print(f"Error encountered while attempting to load/unload extensions:\n  {e}")
		await ctx.send("An error has occurred. Please check the logs.")


def append_command_toggle(ctx, output):
	"""Appends staff-only commands

	Used by list_commands()

	Args:
		ctx: Message context (discord.py construct)
		output: String, representing the output in list_commands,
			that is to be mutated by append_command_toggle()
	"""
	for role in ctx.author.roles:
		if role.id in constants.STAFF.values():
			output += "\ntogglecommands\ntoggledev\nreload"
	return output


@bot.command(name='commands', pass_context=True)
async def list_commands(ctx):
	"""Returns list of available commands, if enabled"""
	commands_cog = bot.get_cog('AzureCommands')  # Returns None if not loaded
	output = "**Commands:**\n----------\n"
	if commands_cog:  # If Azure-specific commands enabled
		cmd_list = [command.name for command in commands_cog.get_commands()]
		output += "\n".join(cmd_list)
		output = append_command_toggle(ctx, output)
		await ctx.send(output)
	else:
		# Display remaining commands that are accessible
		output = append_command_toggle(ctx, output)
		output += "\nCommands are not currently enabled."
		await ctx.send(output)


@bot.command(name='reload', pass_context=True)
@commands.has_any_role(*constants.STAFF.values())
async def reload_cogs(ctx):
	"""
	Command for reloading azure-related commands
	"""
	if await azure_commands.is_help(ctx, "reload"):
		return
	try:
		bot.reload_extension('azure_commands')
		bot.reload_extension('dev')
		print("Successfully reloaded commands!")
		await ctx.send("Successfully reloaded commands!")
	except Exception as e:
		print(f"Error occurred while reloading commands: \n {e}")
		await ctx.send("Error occurred while reloading commands. Check logs for details.")


@bot.command(name='credits', pass_context=True)
async def credit(ctx):
	# Included Brandon as per his request
	output = """**A *KOOKIIE Studios* Production**
	Inspired by: *Lapis* by Brandon (GitHub: Bratah123)
	KOOKIIE Studios: https://github.com/KOOKIIEStudios
	Team SPIRIT: https://github.com/TEAM-SPIRIT-Productions
	Lapis: https://github.com/TEAM-SPIRIT-Productions/Lapis/"""
	await ctx.send(output)


@bot.command(name='botversion', pass_context=True)
async def version(ctx):
	output = """This bot is running: **Max_Feeder v1.4.0**
	Find the source code here: https://github.com/KOOKIIEStudios/Max_Feeder"""
	await ctx.send(output)


def main():
	print("  Running self-checks...")
	if not feeder.fetch_latest_post():  # terminate bot if feeder does not return a String
		raise SystemExit("There seems to be something wrong with the feed parser! TERMINATING...")
	print("  Self-checks passed! RSS feed parse is working correctly.")
	bot.run(config['BOT_TOKEN'])


if __name__ == '__main__':
	main()

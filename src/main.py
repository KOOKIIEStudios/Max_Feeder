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
print("Config file loaded")

# Creating an instance of the bot client
intents = discord.Intents.default()  # Set intents
intents.members = config['MEMBER_INTENT']  # This is required for roles to work
intents.typing = config['TYPING_INTENT']  # Set False to reduce spam
intents.presences = config['PRESENCE_INTENT']  # Set False to reduce spam
bot = commands.Bot(
	command_prefix=config['COMMAND_PREFIX'],
	help_command=None,
	intents=intents,
)
print("Intents and Privileges configured")
# Load commands
bot.load_extension("azure_commands")
print("Extension: 'azure_commands' loaded")
COMMANDS_ON = True  # Global variable to track status


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
	print("Bot has successfully started!")
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
		print(f"Attempting to add role for {member}.")
		try:
			role = discord.utils.get(member.guild.roles, id=config['PLAYER'])
			await member.add_roles(role)
		except Exception as e:
			print(f"Error encountered while attempting to assign role:\n  {e}")


@bot.command(name='commandsoff', pass_context=True)
@commands.has_any_role(*constants.STAFF.values())
async def turn_commands_off(ctx):
	"""Allows turning Azure-related commands off"""
	global COMMANDS_ON
	if await azure_commands.is_help(ctx, "commandsoff"):
		return
	try:
		bot.unload_extension("azure_commands")
		COMMANDS_ON = False
		print("Commands turned off")
		await ctx.send("Commands turned off")
	except commands.ExtensionNotLoaded:
		print(f"Commands are already off!")
		await ctx.send("Commands are already off!")
	except Exception as e:
		print(f"Error encountered while attempting to unload extensions:\n  {e}")
		await ctx.send("An error has occurred. Please check the logs.")


@bot.command(name='commandson', pass_context=True)
@commands.has_any_role(*constants.STAFF.values())
async def turn_commands_on(ctx):
	"""Allows turning Azure-related commands off"""
	global COMMANDS_ON
	if await azure_commands.is_help(ctx, "commandson"):
		return
	try:
		bot.load_extension("azure_commands")
		COMMANDS_ON = True
		print("Commands turned on")
		await ctx.send("Commands turned on")
	except commands.ExtensionAlreadyLoaded:
		print(f"Commands are already on!")
		await ctx.send("Commands are already on!")
	except Exception as e:
		print(f"Error encountered while attempting to load extensions:\n  {e}")
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
			output += "\ncommandson\ncommandsoff\nreload"
	return output


@bot.command(name='commands', pass_context=True)
async def list_commands(ctx):
	"""Returns list of available commands, if enabled"""
	global COMMANDS_ON
	output = "**Commands:**\n----------\n"
	if COMMANDS_ON:  # If Azure-specific commands enabled
		user_cog = bot.get_cog('AzureCommands')
		cmd_list = [command.name for command in user_cog.get_commands()]
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


@bot.command(name='version', pass_context=True)
async def version(ctx):
	output = """This bot is running: **Max_Feeder v1.4.0**
	Find the source code here: https://github.com/KOOKIIEStudios/Max_Feeder"""
	await ctx.send(output)


def main():
	print("Running self-checks...")
	if not feeder.fetch_latest_post():  # terminate bot if feeder does not return a String
		raise SystemExit("There seems to be something wrong with the feed parser! TERMINATING...")
	print("Self-checks passed! RSS feed parse is working correctly.")
	bot.run(config['BOT_TOKEN'])


if __name__ == '__main__':
	main()

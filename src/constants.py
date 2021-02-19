"""Constants used by Azure-related commands

@author KOOKIIE
"""

# Int Constants
AZURE_VERSION = "343"

# ------------------------------------------------------------------------------
# String Constants
# Implicit concat used where f-strings are needed
WARP_FORMAT = """The format for warp command in-game is `@warp <map ID>`
E.g. `@warp 100000000` warps you to Henesys"""

PLAYABLE = (
	f"Please note that the v{AZURE_VERSION} test server is the developers' test"
	" bench.\nIt is intended for developers to perform simple unit tests, and is"
	" NOT for players to play.\nThe game is still early in development "
	"(i.e. written from scratch), and is in no way ready for play.\n"
	"Kindly refer to #faq , if you have any questions."
)

LOCALE = """1. Search for "region" in **Start**, and select **Region Settings**
2. In the left sidebar, select **Additional date, time & regional settings**
3. Select **Change date, time or number formats**
4. Under the **Administrative** tab, select **Change system locale...**
5. Set it to **Korean**, with the Beta UTF-8 option **OFF**
For step-by-step screenshots, refer to: <https://discord.com/channels/608382980183949439/793183592066449420/793185534658871376>"""

REGISTER = (
	f"The v{AZURE_VERSION} test bench is set to **auto-register**.\n"
	"A new account will be added when you first log into game.\n"
	"\n"
	"For the open source v316 project, refer to: "
	"<https://github.com/SoulGirlJP/AzureV316/wiki/FAQ#q-how-do-i-add-new-accounts>"
)

VERSIONS = (
	"There are 2 different versions of Azure!\n"
	"**v316** is an open source project forked from an early build of "
	"Azure v316. This is the version you should use if you want to make your "
	"own server.\n**v{AZURE_VERSION}** is the official hosted version that is "
	"currently in development.\nSee: "
	"<https://discord.com/channels/608382980183949439/793183592066449420/793184319916736513>"
)

WIKI = """Azure v316 Open Source Wiki: <https://github.com/SoulGirlJP/AzureV316/wiki>
Azure v316 Open Source Set-up Guide: <https://github.com/SoulGirlJP/AzureV316/wiki/Setup>
Azure v316 Open Source FAQ: <https://github.com/SoulGirlJP/AzureV316/wiki/FAQ>"""

# ------------------------------------------------------------------------------
# Command alias & description
# Note: This project uses single-quotes for key-value pairs
COMMANDS = {
	'warp': {
		'aliases': ["format"],
		'description': "Explains how the `@warp` command in-game works.",
	},
	'playable': {
		'aliases': ["isitplayable", "play", "status"],
		'description': f"Explains whether Azure v{AZURE_VERSION}",
	},
	'locale': {
		'aliases': ["korean"],
		'description': "Explains how to change locale to Korean.",
	},
	'register': {
		'aliases': ["autoreg", "autoregister"],
		'description': "Explains how to register an account.",
	},
	'versions': {
		'aliases': ["version"],
		'description': "Explains why there are 2 different Azure versions.",
	},
	'wiki': {
		'aliases': ["setup", "faq", "316", "v316"],
		'description': "Provides v316 wiki links.",
	},
	'commandsoff': {
		'description': "Turns Azure-related commands off.",
	},
	'commandson': {
		'description': "Turns Azure-related commands on.",
	},
	'reload': {
		'description': "Reloads Azure-related commands.",
	},
}

# Staff Roles
STAFF = {
	"owner": 608387039624298528,
	"dev": 608511788165890050,
	"brandon": 696547808689389579,
	"skynet": 610818770327437323,
	"gm": 609955277122306051,
	"discord_mod": 608497409315700750,
}

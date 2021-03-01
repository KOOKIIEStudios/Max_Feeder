# Max_Feeder
A Discord Bot that makes a post whenever there is a new post on Orange Mushroom Blog.
Max_Feeder works by scraping/processing the RSS feed for Max's blog.  
A launcher script (`start.bat`) has been provided in the root of the repository.  
You may run this batch file to start the bot after configuring `src/config.json`.  

## Technical Details
|  | Target Minimum | Target Maximum |
|---|---|---|
| Python | 3.6.12 | 3.6.12 |

NOTE: Please do **not** use Python versions older than 3.6 because:
1. f-strings are used - *requires 3.6 or newer*

## How to Use
*This assumes you already have a bot added to the Azure server*

 1. Install Python 3.6
    - Remember to add it to PATH
 2. Clone the repo
    - Or, download a [release](https://github.com/KOOKIIEStudios/Max_Feeder/releases)
 3. Setup your virtual environment
    - You will need to generate your `VENV` prior to use. Refer to [Lazuli's Wiki](https://github.com/TEAM-SPIRIT-Productions/Lazuli/wiki/Technical-Details#step-1-generate-the-virtual-environment) for details on how to do so manually
      - A `requirements.txt` file has been generated for this repo, for your convenience
    - You may run [setup.bat](https://github.com/KOOKIIEStudios/Max_Feeder/blob/main/setup.bat) to generate it automatically instead.
 4. Configure the `src/config.json` file
    - Replace `INSERT_YOUR_BOT_TOKEN` in the file with your bot token
 5. Run `start.bat`

## About v1.2.0
This update brings various new Azure-focused features.  
You may download releases older than this version if you would like to use the initial RSS feeder-only bot.

## About v2.0.1
[CVE-2021-21330 - GitHub Advisory Database](https://github.com/advisories/GHSA-v6wp-4m6f-gcjg)  
Following the release of the advisory (see above), we have updated dependencies to include the security patch(es).  

*Note: `aiohttp` is a library used by `discord.py`, which is the basis for most Python-based bots for Discord, including `Max_Feeder`*.  
### To grab the updates
1. Perform `git pull`
2. Grab the new dependencies  
    - For Global Environment:  
      - `pip install -r requirements.txt`  
    - For Virtual Environment:  
      - `venv/scripts/activate`  
      - `pip install -r requirements.txt`  

### Disclaimer:
*Max_Feeder is an open-source project aimed at the Discord server of a particular MapleStory server emulation project ([AzureMSv316](https://github.com/SoulGirlJP/AzureV316)). Max_Feeder is non-monetised, provided as is, and is unaffiliated with NEXON. Every effort has been taken to ensure correctness and reliability at the time of release. We will not be liable for any special, direct, indirect, or consequential damages or any damages whatsoever resulting from loss of use, data or profits, whether in an action if contract, negligence or other tortious action, arising out of or in connection with the use of Max_Feeder (in part or in whole).*

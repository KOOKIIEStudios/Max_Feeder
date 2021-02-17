# Max_Feeder
A Discord Bot that makes a post whenever there is a new post on Orange Mushroom Blog.  
A launcher script (`start.bat`) has been provided in the root of the repository.  
You may run this batch file to start the bot after configuring `src/config.json`.  

## Technical Details
|  | Target Minimum | Target Maximum |
|---|---|---|
| Python | 3.6.12 | 3.6.12 |

NOTE: Please do **not** use Python versions other than 3.6 because:
1. f-strings are used - *requires 3.6 or newer*
2. Discord.py library is used - *requires 3.6 or older*

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

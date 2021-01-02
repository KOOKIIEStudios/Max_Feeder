# Max_Feeder
A Discord Bot that makes a post whenever there is a new post on Orange Mushroom Blog.  
A launcher script (`start.bat`) has been provided in the root of the repository.  
You may run this batch file to start the bot after configuring `src/config.json`.  

You will need to generate your `VENV` prior to use. Refer to [Lazuli's Wiki](https://github.com/TEAM-SPIRIT-Productions/Lazuli/wiki/Technical-Details#step-1-generate-the-virtual-environment) for details on how to do so.  

## Technical Details
|  | Target Minimum | Target Maximum |
|---|---|---|
| Python | 3.6.12 | 3.6.12 |

NOTE: Please do **not** use Python versions other than 3.6 because:
1. f-strings are used - *requires 3.6 or newer*
2. Discord.py library is used - *requires 3.6 or older*
# umc-web-scraper
Processing the Unfortunate Maps Catalogue.

*Quick disclaimer: I'm still a beginner with this stuff. Python probably isn't the best language for this but its all I know.*


## How to use
There are 2 main options for using the code: run the Python code on your own computer (you will need to install the relevant modules) or use repl.it to run the code.

1. Request an API key from me via discord (iamflowting#1569). This will come in the form of a .json file for you to download. You must have a key to access the Google Sheets API. Save this json file in the same directory as the python file and rename it to client_secret.json.
2. Open the main.py code in your Python IDE and scroll to the very bottom of the code. You will need to edit the following lines:  
gsheets_name = "<*put name of the google sheets here*>"  
main(<*starting map id*>*, <*ending map id*>)  
These values are inclusive. i.e main(1,1000) will do maps 1 to 1000 including map 1 and map 1000.
3. Open the Google Sheets document you will be writing to. Go to add participants and add the API bot, umc-v1@unfortunate-maps-catalogue-api.iam.gserviceaccount.com, and give it the role of editor. 
4. Run the code in your IDE.

For repl.it users: Import the github page. Set the main language to Python and press Done. Delete the .replit file. Then just follow all of the steps 1 to 4 above.


Extra things to know:  
* Deprecated column contains: spawn points on old maps (nowadays spawn point information is stored in the .json file instead of the .png file), mars balls on old maps (not verified), possibly more that I haven't spotted. It seems the way the .json/.png files are coded were changed at some point. 
* If you want you can change time.sleep(x) depending on how good your computer/internet is. I personally run it at x = 1.5 (1.5 second wait between each map) however it should be fine to run it as low as x = 1. However I do not recommend ever going below 1s as the Google Sheets API does have a write limit of 100 write requests per 100 seconds per user.
* Test run using Spyder on my laptop on 09/01/21 (5s sleep): 2001-2101 took 1018.1s.
* Test run using repl.it on 09/01/21 (5s sleep): 2301-2800 took 2915.8s.


## To-do
* Can potato/ghost maps be automated? Might be on the json file.
* Automatically protect ranges of cells once they have been completed.
* Verify whether the current check for invalid maps is correct. It might also be possible to optimise the check.
* Implement a variant of the code that can be run on past spreadsheets without writing over any data (read what is currently in the tags section, then update it with the new prototype functionality and/or any other tag changes). 
* It should be possible to only use 1 write request per page by storing a huge list of all the row_inputs which would mean that the code doesn't run into the API write limit. This would likely also reduce computational time because there are less API requests.
* Improve commenting.
* Optimisations of code.
* Tests to find approximate running time across large batches of maps.
* Investigate the broken maps.


## Broken maps
These maps could not be processed by the code:  
- 666-669 (PNG files were in a different format)
- 729-735 (JSON files not found)
- 846 (PNG file not found)
- 998-1001 (JSON files broken)
- 1879 (JSON file broken) -> fixed manually
- 1965-1967 (PNG files broken)
- 2181 (JSON file broken)
- 2239 (PNG file broken)
- 2837-2839 (JSON files broken)
- 2848 (PNG file broken)
- 3218 (PNG file broken)
- 3541 (unregistered tile)
- 4016-4017, 4019, 4021 (JSON file broken, likely because of map name)
- 4543-4544 (PNG files broken)

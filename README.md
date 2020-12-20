# umc-web-scraper
Processing the Unfortunate Maps Catalogue.

*Quick disclaimer: I'm still a beginner with this stuff. Python probably isn't the best language for this but its all I know.*


## How to use
**2 main options currently: run the Python code on your own computer (you will need to install the relevant modules) or use repl.it to run the code. I'm looking into whether it would be worthwhile to create an executable but may take a bit of time.**

1. Request an API key from me via discord (iamflowting#1569). This will come in the form of a .json file for you to download. You must have a key to access the Google Sheets API. Save this json file in the same directory as the python file and rename it to client_secret.json.
2. Open the code in your Python IDE and scroll to the very bottom of the code. You will need to edit the following lines:  
gsheets_name = "<*put name of the google sheets here*>"  
main(<*starting map id*>*, <*ending map id*>)  
These values are inclusive. i.e main(1,1000) will do maps 1 to 1000 including map 1 and map 1000.
3. Open the Google Sheets document you will be writing to. Go to add participants and add the API bot, umc-v1@unfortunate-maps-catalogue-api.iam.gserviceaccount.com, and give it the role of editor. Make sure that in your Google Sheets you have 10 pages per sheet and that the name matches the one you entered in the python code. Each of your pages must have at least 35 columns (up to AI) or you will run into an error in your code.
4. Run the code in your IDE.

For repl.it users: Import the github page. Set the main language to Python then press Done. Delete the .replit file and rename the python file to main.py. Then follow all of the steps 1 to 4 above.


Extra things to know:  
* Deprecated column contains: spawn points on old maps (nowadays spawn point information is stored in the .json file instead of the .png file), mars balls on old maps (not verified), possibly more that I haven't spotted. It seems the way the .json/.png files are coded were changed at some point. (possibly potatoes as well?)
* If you want you can change time.sleep(x) depending on how good your computer/internet is. I personally run it at x = 1.5 (1.5 second wait between each map) however it should be fine to run it as low as x = 1. However I do not recommend ever going below 1s as the Google Sheets API does have a write limit of 100 write requests per 100 seconds per user.


## To-do
* Add functionality that checks whether a cell that is about to be updated is already filled and raise exception if so.
* Improve commenting.
* Optimisations of code.
* It should be possible to only use 1 write request per page by storing a huge list of all the row_inputs which would mean that the code doesn't run into the API write limit. This would likely also reduce computational time because there are less API requests.
* Update README and properly do the How to use section (update screenshots as well).
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

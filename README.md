# umc-web-scraper
Processing the Unfortunate Maps Catalogue.

*Quick disclaimer: I'm still a beginner with this stuff. Python probably isn't the best language for this but its all I know.*


## How to use (needs to be revised)
**2 main options currently: create a Python environment on your device or use repl.it to run the code. I'm looking into whether its worthwhile to create an executable.**

**If you are using repl.it the steps are as follows: Create a new repl and set the main language to Python. Add the python and json files to the main directory. Rename the python file to main.py and the json file to client_secret.json. Follow step 6 below and edit the relevant lines of code. Now just run and it should hopefully work automatically.**

1. Request an API key from me via discord (iamflowting#1569). This will come in the form of a .json file for you to download. You must have a key to access the Google Sheets API.
4. Download the umc_web_scraper.py file from github and save it to your computer. I would suggest making a new folder in your documents folder. In this folder you should save the .py file and the .json API key I sent to you in step 1. You must rename the .json file to "client_secret.json". For example:
![Step 3](https://i.imgur.com/X7czSSB.png)
6. Hopefully you have the code open now. Scroll to the very bottom of the code. You will need to edit the following lines:  
gsheets_name = "<*put name of the google sheets here*>"  
main(<*starting map id*>*, <*ending map id*>)  
![Step 5](https://i.imgur.com/Azmvl6O.png)
7. Open the Google Sheets document you will be writing to. Go to add participants and add the API bot, umc-v1@unfortunate-maps-catalogue-api.iam.gserviceaccount.com, and give it the role of editor. Make sure that in your Google Sheets you have 10 pages per sheet and that the name matches the one you entered in the python code. Each of your pages must have at least 35 columns (up to AI) or you will run into an error in your code.

Extra things to know:  
* Deprecated column contains: spawn points on old maps (nowadays spawn point information is stored in the .json file instead of the .png file), mars balls on old maps (not verified), possibly more that I haven't spotted. It seems the way the .json/.png files are coded were changed at some point.
* If you want you can change time.sleep(x) depending on how good your computer/internet is. I personally run it at x = 3 (3 second wait between each map) however it should be fine to run it as low as x = 1. However I do not recommend ever going below 1s as the Google Sheets API does have a write limit of 100 write requests per 100 seconds per user.

Images last updated: 01/10/20 (prior to some important v1.1 changes)

## Notes
Test 1 (v1): Maps 1-200 (wait time = 3s)  
Total time: 1006.9392986297607s

Test 2 (v1.1): To-do  
Total time: 

## To-do
* Add functionality that checks whether a cell that is about to be updated is already filled and raise exception if so.
* Improve commenting.
* Move redundant code to a new section or just move it to a new file entirely (web scraping stuff is useful, but its irrelevant now that I can access the json/png files).
* User interface?
* Optimisations of code.
* It should be possible to only use 1 write request per page by storing a huge list of all the row_inputs which would mean that the code doesn't run into the API write limit. This would likely also reduce computational time because there are less API requests.
* Update Python and check if code works on 3.8.5.
* Update README and properly do the How to use section (update screenshots as well).

## References
* https://realpython.com/beautiful-soup-web-scraper-python/#part-2-scrape-html-content-from-a-page 
* https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html  
* https://gspread.readthedocs.io/en/latest/api.html

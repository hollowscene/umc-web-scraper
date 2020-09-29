# umc-web-scraper
Processing the Unfortunate Maps Catalogue.

How to Use (im still working on this):  
1. Request an API key from me via discord (iamflowting#1569). This will come in the form of a .json file for you to download. You must have a key to access the Google Sheets API.  
2. If you don't already have Python download it from https://www.python.org/downloads/. I am running my code on the latest version of Python, I cannot guarantee it works on older versions.  
3. Download the .py file from github and save it to your computer. I would suggest making a new folder in your documents folder. In this folder you should save the .py file and the .json API key I sent to you in step 1. Rename the .json file to "client_secret.json". This is mandatory.  
4. Open your python file in any python ide of choice. If you do not know what a python ide is you should look up Python IDLE in your programs or just contact me for help. (to add screenshots)  
5. You should have the code open in front of you. If not contact me for help. First thing is you will need to change the name of the sheet that you are writing to. Idk what line this is... I'll add a screenshot later/find the exact line but basically the code accesses your google sheets by its name.
6. You will need to add the api bot as a editor participant. just go to add participants and enter this email: <to be added>
7. Scroll down in the code till you reach the bottom. There will be a line that says "# main(1, 200)". What this means is that it will automatically process all the maps between map id 1 and 200 including 1 and 200. Replace the numbers with new values and then go to file > run if you are in Python IDLE. Note that you must stay in the range of 1-1000. If you do things write you should basically just be doing 1-1000, 1001-2000, 2001-3000 e.t.c. You will overwrite data if you do not stay within the bounds (but i would like to prevent this in the future)

Things to take note of:  
please have empty Google Sheets prepared beforehand. There should be 10 pages per sheet and each page will hold 100 entries.





Test 1: Maps 1-200 on an empty sheet on my laptop (wait time between maps = 3s)  
Total time: 17m

Test 2: Maps 1-200 again. Same parameters. Added the new Deprecated column and also using timer inside of python code  
Total time: 1006.9392986297607s

Currently averaging about 3s to process each map and then there is a further wait between each map that can be adjusted.

Note that Google Sheets API has a limit of 100 write requests per 100 seconds per user and 500 write requests per 100 seconds.  
Please do not increase the rate beyond this limit.


<i>Quick Note: the "Deprecated" column is for old spawn points and I would also guess old mars balls.  
In current maps spawn points and mars ball data are stored in the json files  
In past maps the json files did not contain any information about spawn points or mars ball and instead the data was stored in the png files</i>



This code sucks, plenty of optimisations for someone better at coding.


This will download json/png files to whereever the code is (these are very small files dont worry).  
But just remember to clear them whenever you need to. Feel free to delete these files after they have been processed.   
Maybe in the future I will add functionality that automatically clears it although probably less likely for errors if just delete them manually.


Contact me via discord for a key if you would like to help process. (once I add that functionality)



<b>To-do</b>  
Add functionality that checks whether a cell that is about to be updated is already filled and raise exception if so.  
Proper commenting  
Move redundant code to a new section or just move it to a new file entirely (web scraping stuff is useful, but its irrelevant now that I can access the json/png files)  
Make it easier for other people to download the code and use a private API key that I provide  
Create user interface  
Automate CTF/NF/Mars Ball tags (will not always be right but it'll catch like 99% of cases)  (not necessary)  
Automatically tag invalid maps as "INVALID". Can do this by using the webscraper. Look for the name of the map in the html soup and if its not there then you can assign tags = "INVALID" 
Make tags into a list. tags = ["INVALID"]. When writing to google sheets write ", ".join(tags). This is just futureproofing. 



<b>References</b>  
Most code is sourced from  
https://realpython.com/beautiful-soup-web-scraper-python/#part-2-scrape-html-content-from-a-page  
Additional sources  
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html  
https://stackoverflow.com/questions/38709324/unexpected-credentials-type-none-expected-service-account-with-oauth2  
https://stackoverflow.com/questions/49258566/gspread-authentication-throwing-insufficient-permission  
https://gspread.readthedocs.io/en/latest/api.html

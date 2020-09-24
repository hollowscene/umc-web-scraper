# umc-web-scraper
Processing the Unfortunate Maps Catalogue.


Test 1: Maps 1-200 on an empty sheet on my laptop (wait time between maps = 3s)
Total time: 17m

Currently averaging about 3s to process each map and then there is a further wait between each map that can be adjusted.

Note that Google Sheets API has a limit of 100 write requests per 100 seconds per user and 500 write requests per 100 seconds.
Please do not increase the rate beyond this limit.




This code sucks, plenty of optimisations for someone better at coding.


This will download json/png files to whereever the code is (these are very small files dont worry).
But just remember to clear them whenever you need to. Feel free to delete these files after they have been processed. 
Maybe in the future I will add functionality that automatically clears it although probably less likely for errors if just delete them manually



Contact me via discord for a key if you would like to help process. (once I add that functionality)



To-do
Add functionality that checks whether a cell that is about to be updated is already filled and raise exception if so.
Proper commenting
Move redundant code to a new section or just move it to a new file entirely (web scraping stuff is useful, but its irrelevant now that I can access the json/png files)
Make it easier for other people to download the code and use a private API key that I provide


References
Most code is sourced from
https://realpython.com/beautiful-soup-web-scraper-python/#part-2-scrape-html-content-from-a-page

Additional sources
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
https://stackoverflow.com/questions/38709324/unexpected-credentials-type-none-expected-service-account-with-oauth2
https://stackoverflow.com/questions/49258566/gspread-authentication-throwing-insufficient-permission
https://gspread.readthedocs.io/en/latest/api.html

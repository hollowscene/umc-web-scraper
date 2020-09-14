# -*- coding: utf-8 -*-
"""
Unfortunate Maps Catalogue Webscraper.

@author: iamflowting
@created-on: 12/09/20
@last-updated: 14/09/20

Most code is sourced from
https://realpython.com/beautiful-soup-web-scraper-python/#part-2-scrape-html-content-from-a-page

Additional sources
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
https://stackoverflow.com/questions/38709324/unexpected-credentials-type-none-expected-service-account-with-oauth2
https://stackoverflow.com/questions/49258566/gspread-authentication-throwing-insufficient-permission
https://gspread.readthedocs.io/en/latest/api.html


TO-DO
Add functionality that checks whether a cell that is about to be updated is
already filled and raise exception if so. PNG/JSON parser.
"""


import requests
from bs4 import BeautifulSoup
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# %%

import json
import PIL

# test_url = "http://unfortunate-maps.jukejuice.com/show/75634"

json_file_path = "C:\\Users\\andre\\Desktop\\test.json"
png_file_path = "C:\\Users\\andre\\Desktop\\test.png"


"""
JSON file contains gameMode, name, author, portal connections, gates,
switches, mars ball spawns and spawn points.

PNG file contains all tile placements.
"""


def parse_json(json_file_path):
    """Read JSON file and return relevant data.

    To-do.
    """
    with open(json_file_path) as f:
        json_data = json.load(f)
    return json_data


def parse_png(png_file_path):
    """Read PNG file and return relevant data.

    While this works it requires the png file to be downloaded.
    """
    map_image = PIL.Image.open(png_file_path, mode="r").convert("RGB")
    width, height = map_image.size

    map_pixel_data = map_image.getdata()
    pixel_list = []

    tile_dict = {(120, 120, 120): 0,    # wall
                 (64, 128, 80): 1,      # wall tl
                 (64, 80, 128): 2,      # wall tr
                 (128, 112, 64): 3,     # wall bl
                 (128, 64, 112): 4,     # wall br
                 (212, 212, 212): 5,    # tile (spawns/mars ball)
                 (0, 0, 0): 6,          # background
                 (55, 55, 55): 7,       # spike
                 (0, 255, 0): 8,        # powerup
                 (202, 192, 0): 9,      # portal
                 (32, 32, 32): 10,      # gravity well
                 (128, 128, 0): 11,     # yellow flag
                 (255, 0, 0): 12,       # red flag
                 (0, 0, 255): 13,       # blue flag
                 (185, 0, 0): 14,       # red endzone
                 (25, 0, 148): 15,      # blue endzone
                 (255, 255, 0): 16,     # boost
                 (255, 115, 115): 17,   # red boost
                 (115, 115, 255): 18,   # blue boost
                 (220, 220, 186): 19,   # yellow team tile
                 (220, 186, 186): 20,   # red team tile
                 (187, 184, 221): 21,   # blue team tile
                 (185, 122, 87): 22,    # button
                 (0, 117, 0): 23,       # gate (grey/green/red/blue)
                 (255, 128, 0): 24      # bomb
                 }

    for pixel_data in map_pixel_data:
        try:
            pixel_list.append(tile_dict[pixel_data])
        except KeyError:
            raise Exception("Unregistered tile.")

    return width, height, pixel_list


def download_json(soup):
    """Download json file from link in html soup.

    The HTML code that contains the dl link will look like this:
    <a href="json_dl_link" download="map_name" class="btn btn-primary">json</a>

    TO DO
    """
    json_file_path = None
    return json_file_path


def download_png(soup):
    """Download png file from link in html soup.

    The HTML code that contains the dl link will look like this:
    <a href="png_dl_link" download="map_name" class="btn btn-primary">png</a>

    TO DO
    """
    png_file_path = None
    return png_file_path


# %%


def umc_web_scraper(map_id):
    """Get static copy of HTML from given url and returns it as HTML soup."""
    url = f"http://unfortunate-maps.jukejuice.com/show/{map_id}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def parse_map_name(soup):
    """Return map name from HTML soup.

    This function is unnecessary if you just extract the name from json file.
    """
    try:
        map_name = soup.find_all("h2", class_="searchable")
    except:
        raise Exception("Could not find map name. Invalid map?")
    return map_name


def parse_map_author(soup):
    """Return map author from HTML soup.

    This function is unnecessary if you just extract the author from json file.
    """
    try:
        map_author = soup.find_all("a", class_="searchable")
    except:
        raise Exception("Could not find author. Invalid map?")
    return map_author


def html_text_parser(html_text):
    """Remove HTML fluff.

    e.g [<h2 class="searchable" style="">test</h2>] -> test.
    Note that this only works for a single HTML code.
    """
    for unparsed_html in html_text:
        return unparsed_html.text.strip()


# %%

def access_gsheets_api(index):
    """Access Google Sheets document."""
    # create client to interact with Google Drive API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
    client = gspread.authorize(creds)

    # find workbook by name and open the required sheet
    sheet = client.open("Tagpro Unfortunate Maps Catalogue Parser Test").get_worksheet(index)

    return sheet


def gsheets_input(map_id, map_name, map_author, sheet):
    """Update values of the Google Sheets."""
    row = ((map_id - 1) % 100) + 2
    sheet.update(f"B{row}", str(map_id).zfill(5))
    if map_name is None:
        # invalid map
        sheet.update_cell(row, 1, "INVALID")
    else:
        # map name
        sheet.update_cell(row, 3, map_name)
        # put author here
        sheet.update_cell(row, 4, map_author)

    """
    sheet.update_cell(row, 7, width)
    sheet.update_cell(row, 8, height)

    for i in range(9, 34):
        sheet.update_cell(row, i, tile_counts[i])
    """


def gsheets_header_row(sheet):
    """Initialise sheet with a header row."""
    header_row = ["Reserved by", "ID", "Name", "Author", "Tags", "Notes",
                  "Width", "Height", "Wall", "Wall TL", "Wall TR", "Wall BL",
                  "Wall BR", "Tile", "Background", "Spike", "Powerup",
                  "Portal", "Gravity Well", "Mars Ball", "Yellow Flag",
                  "Red Flag", "Blue Flag", "Red Spawn Tile", "Blue Spawn Tile",
                  "Red Endzone", "Blue Endzone", "Boost", "Red Team Boost",
                  "Blue Team Boost", "Yellow Speed Tile", "Red Speed Tile",
                  "Blue Speed Tile", "Button", "Gate Off", "Gate On",
                  "Gate Red", "Gate Blue", "Bomb"]

    sheet.insert_row(header_row, index=1, value_input_option="RAW")


# %%

def main(start, end):
    """Iterate through urls from start to end (inclusive)."""
    for map_id in range(start, end + 1):
        soup = umc_web_scraper(map_id)

        map_name = html_text_parser(parse_map_name(soup))
        map_author = html_text_parser(parse_map_author(soup))

        if map_author == "Anonymous":
            # could just leave it as anonymous if you want
            map_author = ""

        index = (((map_id % 10000) % 1000) - 1) // 100
        x = str(map_id).zfill(5)
        if map_author is None:
            print(f"{x}: Invalid map.")
        elif map_author == "":
            print(f"{x}: Processed {map_name} on sheet {index}.")
        else:
            print(f"{x}: Processed {map_name} by {map_author} on sheet {index}.")

        # only open a new sheet if you need to
        if map_id == start:
            sheet = access_gsheets_api(index)
            gsheets_header_row(sheet)
            previous_index = index
        elif previous_index != index:
            # open a new sheet and generate a header row
            # note that this DOES NOT create a new sheet
            sheet = access_gsheets_api(index)
            gsheets_header_row(sheet)

        gsheets_input(map_id, map_name, map_author, sheet)

        previous_index = index

        # limit speed. 1/second = 60/minute = 3600/hour
        # probably wouldn't suggest any less than 1 second sleep
        time.sleep(5)


# %%

"""
1-100 refers to sheet 1
101-200 refers to sheet 2
201-300 refers to sheet 3
e.t.c
1001-1100 loops back to sheet 1 on the same Google Sheets

Only use in the range xx001 to xy000 to prevent writing over your data.

Please use empty sheets.
The code will automatically add a header row.
"""

if __name__ == "__main__":
    # main(1, 200)
    pass

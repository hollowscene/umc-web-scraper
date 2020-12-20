# -*- coding: utf-8 -*-
"""
Unfortunate Maps Catalogue Webscraper v1.4.3.

@author: iamflowting
@created-on: 12/09/20
@last-updated: 20/12/20
"""


import requests
from bs4 import BeautifulSoup
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import collections
import os


# %% JSON/PNG Files

import json
# import PIL
from PIL import Image

"""
JSON file contains gameMode, name, author, portal connections, gates,
switches, mars ball spawns and spawn points.

PNG file contains all tile placements.

test url: http://unfortunate-maps.jukejuice.com/show/75634

"""


def parse_json(json_file_path):
    """Read JSON file and return relevant data.

    gamemode: "normal", "gravity" or "gravityCTF" (?)
    map_name
    map_author
    marsballs

    """
    gamemode = "normal"
    marsballs = 0

    with open(json_file_path) as f:
        json_data = json.load(f)

        try:
            gamemode = json_data["info"]["gameMode"]
        except KeyError:
            pass

        map_name = json_data["info"]["name"]
        map_author = json_data["info"]["author"]

        try:
            marsballs = len(json_data["marsballs"])
        except KeyError:
            pass

    return gamemode, map_name, map_author, marsballs


def parse_png(png_file_path):
    """Read PNG file and return relevant data.

    width
    height
    pixel_list: png file converted to a dictionary for every pixel
    """
    map_image = Image.open(png_file_path, mode="r").convert("RGB")
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
                 (255, 128, 0): 24,     # bomb
                 (155, 0, 0): 25,       # invalid tile
                 (0, 0, 155): 25,       # invalid tile
                 (179, 179, 179): 25,   # invalid tile found on 661
                 (180, 180, 180): 25,   # invalid tile found on 661
                 (255, 255, 255): 25    # invalid tile found on 661
                 }

    for pixel_data in map_pixel_data:
        try:
            pixel_list.append(tile_dict[pixel_data])
        except KeyError:
            raise Exception("Unregistered tile.")

    return width, height, pixel_list


def download_json(map_id):
    """Download map's json file to map_id.json."""
    json_link = f"http://unfortunate-maps.jukejuice.com/download?mapname={map_id}&type=json&mapid={map_id}"
    with open(f"{map_id}.json", "wb") as f:
        response = requests.get(json_link)
        f.write(response.content)

    return f"{map_id}.json"


def download_png(map_id):
    """Download map's png file to map_id.png."""
    png_link = f"http://unfortunate-maps.jukejuice.com/download?mapname={map_id}&type=png&mapid={map_id}"
    with open(f"{map_id}.png", "wb") as f:
        response = requests.get(png_link)
        f.write(response.content)

    return f"{map_id}.png"


# %% HTML Web Scraper


def umc_web_scraper(map_id):
    """Get static copy of HTML from given url and returns it as HTML soup."""
    url = f"http://unfortunate-maps.jukejuice.com/show/{map_id}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def parse_map_name(soup):
    """Find and returns map name from HTML soup.

    Note: map name can also be retrieved from json file.

    """
    try:
        map_name = soup.find_all("h2", class_="searchable")
    except:
        print("Could not find map name. Invalid map?")
        map_name = None
    return map_name


def parse_map_author(soup):
    """Find and returns map author from HTML soup.

    Note: map author can also be retrieved from json file.

    """
    try:
        map_author = soup.find_all("a", class_="searchable")
    except:
        print("Could not find author. Invalid map?")
        map_author = None
    return map_author


def html_text_parser(html_text):
    """Remove HTML fluff from a line of HTML code.

    e.g [<h2 class="searchable" style="">test</h2>] -> test.

    """
    for unparsed_html in html_text:
        return unparsed_html.text.strip()


# %% Google Sheets API

def access_gsheets_api(index):
    """Access Google Sheets document via Google Drive API."""
    # create client to interact with Google Drive API
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "client_secret.json", scope)
    client = gspread.authorize(creds)

    # find workbook by name and open the required sheet
    sheet = client.open(gsheets_name).get_worksheet(index)

    return sheet


def gsheets_input(map_data, sheet):
    """Update values of the Google Sheets.

    Updates row by row using data obtained from the png/json files.

    """
    map_id, map_name, tags, width, height, tile_data, marsballs = map_data
    row = ((map_id - 1) % 100) + 2

    # this adds about a second extra per map
    if len(parse_map_name(umc_web_scraper(map_id))) == 0:
        tags = ["INVALID"]

    row_inputs = [[None,
                   str(map_id).zfill(5),
                   map_name,
                   ", ".join(tags),
                   None, 
                   None,
                   None,
                   None,
                   None,
                   None,
                   None,
                   width,
                   height,
                   tile_data[0],
                   tile_data[1],
                   tile_data[2],
                   tile_data[3],
                   tile_data[4],
                   tile_data[5],
                   tile_data[6],
                   tile_data[7],
                   tile_data[8],
                   tile_data[9],
                   tile_data[10],
                   tile_data[11],
                   tile_data[12],
                   tile_data[13],
                   tile_data[14],
                   tile_data[15],
                   tile_data[16],
                   tile_data[17],
                   tile_data[18],
                   tile_data[19],
                   tile_data[20],
                   tile_data[21],
                   tile_data[22],
                   tile_data[23],
                   tile_data[24],
                   marsballs,
                   tile_data[25]]]

    sheet.update(f"A{row}:AN{row}", row_inputs)


def gsheets_header_row(sheet):
    """Initialise sheet with a header row."""
    header_row = [["Reserved by",
                   "Map ID",
                   "Map Name",
                   "Tags",
                   "Notes (Optional)",
                   None,
                   None,
                   None,
                   None,
                   None,
                   None,
                   "Width",
                   "Height",
                   "Wall",
                   "Wall TL",
                   "Wall TR",
                   "Wall BL",
                   "Wall BR",
                   "Tile",
                   "Background",
                   "Spike",
                   "Powerup",
                   "Portal",
                   "Gravity Well",
                   "Yellow Flag",
                   "Red Flag",
                   "Blue Flag",
                   "Red Endzone",
                   "Blue Endzone",
                   "Boost",
                   "Red Team Boost",
                   "Blue Team Boost",
                   "Yellow Speed Tile",
                   "Red Speed Tile",
                   "Blue Speed Tile",
                   "Button",
                   "Gate",
                   "Bomb",
                   "Mars Ball",
                   "Deprecated"
                   ]]

    # check if there is already a header row
    if sheet.acell("AN1").value == "?":
        pass
    else:
        sheet.update("A1:AN1", header_row)


# %% Main

def main(start, end):
    """Iterate through urls from start to end (inclusive).

    Download json/png files and parse the data from them. Then accesses gsheets
    API and writes relevant data to the sheet.

    """
    for map_id in range(start, end + 1):
        start_time = time.time()
        # soup = umc_web_scraper(map_id)

        # map_name = html_text_parser(parse_map_name(soup))
        # map_author = html_text_parser(parse_map_author(soup))

        json_data = parse_json(download_json(map_id))
        png_data = parse_png(download_png(map_id))

        gamemode, map_name, map_author, marsballs = json_data
        width, height, pixel_list = png_data

        tile_data = collections.Counter(pixel_list)

        tags = []
        if gamemode == "gravity":
            tags.append("Gravity")
        elif gamemode == "gravityCTF":
            tags.append("Gravity")

        if map_id % 1000 == 0:
          index = 9
        else:
          index = (((map_id % 10000) % 1000) - 1) // 100

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

        input_data = [map_id, map_name, tags, width, height,
                      tile_data, marsballs]
        gsheets_input(input_data, sheet)

        x = str(map_id).zfill(5)
        print(f"{x}: Processed {map_name} on sheet {index}.")
        print(f"{time.time() - start_time}s")

        previous_index = index

        # automatically deletes json/png file
        os.remove(f"{map_id}.json")
        os.remove(f"{map_id}.png")

        # wait time after each map is processed
        time.sleep(limit_speed)


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
    # limit speed. 1/second = 60/minute = 3600/hour
    # note that google sheets limits to 100 write requests per 100 seconds
    # wouldn't suggest any less than 1 second sleep
    # default speed: 1.5s
    limit_speed = 1.5

    # put name of sheet here
    gsheets_name = "Unfortunate Maps <insert map range>"

    start_total_time = time.time()

    print("Started Processing")

    # put range of map ids you wish to process here (start to end inclusive)
    # please only put ranges within 1-1000, 1001-2000, 2001-3000 e.t.c
    # i.e 200-500 is okay but 980-1100 is not okay.
    main("start", "end")

    print("Completed Processing")
    print(f"Total processing time: {time.time() - start_total_time}s")

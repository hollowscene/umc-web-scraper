# -*- coding: utf-8 -*-
"""
Unfortunate Maps Catalogue Webscraper - Google Sheets API Functions.

@author: iamflowting
@created-on: 25/12/20
@last-updated: 25/12/20
"""


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import webscraping_functions as wf


# %% Google Sheets API

def access_gsheets_api(gsheets_name, index):
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
    if len(wf.parse_map_name(wf.umc_web_scraper(map_id))) == 0:
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

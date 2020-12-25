# -*- coding: utf-8 -*-
"""
Unfortunate Maps Catalogue Webscraper - Webscraping Functions.

@author: iamflowting
@created-on: 24/12/20
@last-updated: 25/12/20
"""


import requests
from bs4 import BeautifulSoup
import json
from PIL import Image


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


def scrape_lists(soup):
    # look for drop down menu
    # can ignore remix since remix is literally just if they have the same name
    # prototype look through for the most recent version/map id
    versions = []
    remixes = []
    try:
        lists = soup.find_all("ul", class_="dropdown-menu")
    except:
        raise Exception("Could not find any dropdown menus in html soup.")
    if len(lists) == 6:
        # 5th item is versions, 6th item is remixes
        versions = lists[4]
        remixes = lists[5]
    elif len(lists) == 3:
        # this occurs when there is an invalid map ("Oops, something went wrong" error page)
        pass
    else:
        print(len(lists))
        raise Exception("Not 3 or 6 dropdown menus found.")
    return versions, remixes


def html_text_parser(html_text):
    """Remove HTML fluff from a line of HTML code.

    e.g [<h2 class="searchable" style="">test</h2>] -> test.

    """
    for unparsed_html in html_text:
        return unparsed_html.text.strip()


# %% JSON/PNG Files

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


# %% Testing

if __name__ == "__main__":
    map_id = 1000
    versions, remixes = scrape_lists(umc_web_scraper(map_id))

    print(versions)

    latest_version = map_id
    if versions:
        latest_version = versions.find("a")
        if latest_version is not None:
            latest_version = latest_version["href"][6:]

    print(latest_version)

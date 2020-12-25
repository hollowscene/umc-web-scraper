# -*- coding: utf-8 -*-
"""
Unfortunate Maps Catalogue Webscraper v1.5.0.

@author: iamflowting
@created-on: 12/09/20
@last-updated: 25/12/20
"""


import time
import collections
import os
import webscraping_functions as wf
import google_sheets_functions as gsf


# %% Main

def main(start, end):
    """Iterate through urls from start to end (inclusive).

    Download json/png files and parse the data from them. Then accesses gsheets
    API and writes relevant data to the sheet.

    """
    for map_id in range(start, end + 1):
        start_time = time.time()
        soup = wf.umc_web_scraper(map_id)
        versions, remixes = wf.scrape_lists(soup)
        latest_version = map_id
        if versions:
            latest_version = versions.find("a")
            if latest_version is None:
                latest_version = map_id
            else:
                latest_version = latest_version["href"][6:]
        else:
            latest_version = map_id

        # map_name = html_text_parser(parse_map_name(soup))
        # map_author = html_text_parser(parse_map_author(soup))

        json_data = wf.parse_json(wf.download_json(map_id))
        png_data = wf.parse_png(wf.download_png(map_id))

        gamemode, map_name, map_author, marsballs = json_data
        width, height, pixel_list = png_data

        tile_data = collections.Counter(pixel_list)

        tags = []
        if map_id != latest_version:
            tags.append(f"Prototype ({latest_version})")
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
            sheet = gsf.access_gsheets_api(gsheets_name, index)
            gsf.gsheets_header_row(sheet)
            previous_index = index
        elif previous_index != index:
            # open a new sheet and generate a header row
            # note that this DOES NOT create a new sheet
            sheet = gsf.access_gsheets_api(gsheets_name, index)
            gsf.gsheets_header_row(sheet)

        input_data = [map_id, map_name, tags, width, height,
                      tile_data, marsballs]
        gsf.gsheets_input(input_data, sheet)

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
    gsheets_name = "umc-testing"

    start_total_time = time.time()

    print("Started Processing")

    # put range of map ids you wish to process here (start to end inclusive)
    # please only put ranges within 1-1000, 1001-2000, 2001-3000 e.t.c
    # i.e 200-500 is okay but 980-1100 is not okay.
    main(60001, 60200)

    print("Completed Processing")
    print(f"Total processing time: {time.time() - start_total_time}s")
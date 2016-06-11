""" Downloads images from zen masters(?) from a site with a bit of obfuscated
code hiding it's art, also apparently built in dreamweaver. """

from tools import REQUESTS_HEADER, get_url_filename, make_output_folder
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import requests
import re
import os

page = "http://zenpaintings.com/"

# Gather all the pages of the artists
pattern = r'stm_aix\("p2i\d+","p1i0",\[0,".*","","",-1,-1,0,"(.*)"\],120,\d+\);'
menu_javascript = BeautifulSoup(requests.get(page + "js/menu.js", headers=REQUESTS_HEADER).text, 'lxml')
artist_links = re.findall(pattern, menu_javascript.text)

# Scrape through every page
for artist_link in artist_links:
    artist_name = get_url_filename(artist_link).replace(".htm", "").split("artist-")[1]
    soup = BeautifulSoup(requests.get(artist_link, headers=REQUESTS_HEADER).text, 'lxml')
    images = [page + img['src'] for img in soup.find_all('img')]

    for image in images:
        path = os.path.join(make_output_folder(artist_name), get_url_filename(image))

        if not os.path.exists(path):
            try:
                urllib.request.urlretrieve(image, path)
                print("Downloaded {0}.".format(image))

            except urllib.error.HTTPError as e:
                # File doesn't exist, no need to handle really
                if e.errno == 404:
                    pass


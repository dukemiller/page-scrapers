""" Downloads the original gallery images from studioralu.com.
"""

from tools import REQUESTS_HEADER, get_content_type, make_folder
from urllib.request import urlretrieve
from collections import namedtuple
from bs4 import BeautifulSoup
import requests
import os

download_dir = make_folder(r'E:\Output\Scrapers\studioralu')
gallery_image = namedtuple('gallery_image', "link name ext")
page = r'http://www.studioralu.com/'

soup = BeautifulSoup(requests.get(page, headers=REQUESTS_HEADER).text, 'lxml')
images = (gallery_image(img['data-src'], img['alt'], get_content_type(img['data-src']))
          for img in soup.find_all('img'))

for image in images:
    full_path = os.path.join(download_dir, image.name + '.' + image.ext)
    if not os.path.exists(full_path):
        print("Downloading {0} ...".format(image.name))
        urlretrieve(image.link, full_path)
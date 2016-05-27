""" Downloads every original sized image in the gallery. """

from tools import REQUESTS_HEADER, get_content_subtype, make_output_folder
from urllib.request import urlretrieve
from collections import namedtuple
from bs4 import BeautifulSoup
import requests
import os

page = r'http://www.studioralu.com/'
download_dir = make_output_folder()
GalleryImage = namedtuple('gallery_image', "link name ext")

soup = BeautifulSoup(requests.get(page, headers=REQUESTS_HEADER).text, 'lxml')
images = (GalleryImage(img['data-src'], img['alt'], get_content_subtype(img['data-src']))
          for img in soup.find_all('img'))

for image in images:
    full_path = os.path.join(download_dir, image.name + '.' + image.ext)
    if not os.path.exists(full_path):
        print("Downloading {0} ...".format(image.name))
        urlretrieve(image.link, full_path)

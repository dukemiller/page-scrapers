""" Downloads every song for a video game soundtrack.
"""

from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from tools import REQUESTS_HEADER, make_output_folder, get_url_filename
import requests
import os

page = r'http://downloads.khinsider.com/game-soundtracks/album/fire-emblem-awakening'

soup = BeautifulSoup(requests.get(page, headers=REQUESTS_HEADER).text, 'lxml')
name = soup.find('div', {'id': 'EchoTopic'}).find_all('p')[1].find_all('b')[0].text
table = soup.find('table', {'cellpadding': '3'}).find_all('tr')[1:]
links = [row.td.a['href'] for row in table]
folder = make_output_folder(name)

for link in links:
    soup = BeautifulSoup(requests.get(link, headers=REQUESTS_HEADER).text, 'lxml')
    file = soup.find('div', {'id': 'EchoTopic'}).find_all('p')[3].a['href']
    file_path = os.path.join(folder, get_url_filename(file))
    if not os.path.exists(file_path):
        urlretrieve(file, file_path)
        print('Downloaded {0}.'.format(file))

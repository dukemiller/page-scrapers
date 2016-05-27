from bs4 import BeautifulSoup
import requests
import os
from tools import make_output_folder, REQUESTS_HEADER
from urllib.request import urlretrieve

page = 'http://anime.thehylia.com/soundtracks/album/rokka-no-yuusha-ed2-single-dance-in-the-fake'

soup = BeautifulSoup(requests.get(page, headers=REQUESTS_HEADER).text, 'lxml')
name = soup.find('table', {'class': 'blog'}).find('p', {'align': 'left'}).b.text
links = [x.a['href'] for x in soup.find('table', {'width': '95%'}).find_all('td')[0::2]]
path = make_output_folder(name)

for link in links:
    soup = BeautifulSoup(requests.get(link, headers=REQUESTS_HEADER).text,'lxml')
    name = soup.find('table', {'class': 'blog'}).find_all('b')[2].text
    file = soup.find('table', {'class': 'blog'}).find_all('b')[4].a['href']
    extension = file.split('.')[-1]
    file_path = os.path.join(path, "{0}.{1}".format(name, extension))
    if not os.path.exists(file_path):
        urlretrieve(file, file_path)
        print('downloaded %s' % file)

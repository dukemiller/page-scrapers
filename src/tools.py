import os
from urllib.request import urlopen

REQUESTS_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'}


def make_folder(path: str) -> str:
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_content_subtype(url: str) -> str:
    """ Returns the second part of content-type in the content header,
     e.g. 'Content-Type: image/{jpeg}' """

    return urlopen(url).info().get_content_subtype()


def get_extension_from_url(url: str) -> str:
    """ Returns the extension of a url,
    e.g. 'http://google.com/image{.jpg}' """

    return '.' + url.split('.')[-1]


def get_filename(url: str) -> str:
    """ Returns the filename from a url if there are no slashes in the name,
    e.g. 'http://google.com/{file.png}' """
    return url.split('/')[-1]

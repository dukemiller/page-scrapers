import os
import inspect
from urllib.request import urlopen

REQUESTS_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'}
OUTPUT_FOLDER = r'E:\Output\scrapers'


def make_folder(path: str) -> str:
    r""" Creates a path arbitrarily deep if not exists and returns that path.
        e.g. C:\ exists so C:\{The\New\Path} is created, and the whole path is returned. """

    if not os.path.exists(path):
        os.makedirs(path)
    return path


def make_output_folder(*args: str) -> str:
    """ Create a folder in the output folder with the name of the of the calling script
     with any extra parameters after.
     e.g. called from flickr.py, the folder will be {C:\...\...\OUTPUT_FOLDER\flickr},
          any arguments would be appended as folders afterwards """

    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    delimiter = '/' if filename.count("/") > 0 else '\\'
    name = filename.split(delimiter)[-1].split('.py')[0]

    path = os.path.join(OUTPUT_FOLDER, name, *args)

    return make_folder(path)


def get_content_subtype(url: str) -> str:
    """ Returns the second part of content-type in the content header.
     e.g. 'Content-Type: image/{jpeg}' """

    return urlopen(url).info().get_content_subtype()


def get_extension_from_url(url: str) -> str:
    """ Returns the extension of a url.
    e.g. 'http://google.com/image{.jpg}' """

    return '.' + url.split('.')[-1]


def get_url_filename(url: str) -> str:
    """ Returns the filename from a url if there are no slashes in the name.
    e.g. 'http://google.com/{file.png}' """

    return url.split('/')[-1]


def get_filename(path: str) -> str:
    """ Returns the path filename. """

    delimiter = '/' if path.count("/") > 0 else '\\'
    return path.split(delimiter)[-1]


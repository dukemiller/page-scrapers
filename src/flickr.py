""" Downloads all images from one person on flickr at high quality.

Note: This is generally less of a scraper than what would usually be, but I do
sort of take advantage of flickr's API for how it handles requests and gives
authentication to viewers on a page through temporary keys so I would still
call it a scraper """

from tools import REQUESTS_HEADER, make_output_folder, get_extension_from_url
from urllib.request import urlretrieve
from collections import namedtuple
from typing import Iterable, List
import requests
import json
import os

FlickrImage = namedtuple('flickr', 'id link')
Credentials = namedtuple('credentials', 'user_id req_id api_key')


# Unused
def get_url_from_flickr_image_page(flickr_image_page_url: str) -> str:
    html = requests.get(flickr_image_page_url, headers=REQUESTS_HEADER).text

    # Find the javascript function
    left = html.find("modelExport: {") + 13
    right = html[left:].find('"}]},') + left
    function = html[left:right]

    # Find the key value
    left = function.rfind('"displayUrl":"')
    right = function[left:].find('","') + left
    json_value = json.loads("{" + function[left:right + 1] + "}")['displayUrl']

    # Join together with cdn page
    url = "https://c8.staticflickr.com/2/" + '/'.join(json_value.split('/')[3:])

    return url


def get_user_credentials(flickr_user_url: str) -> Credentials:
    """ Parses the page for the plain text displayed credentials
    for accessing the API. """

    html = requests.get(flickr_user_url, headers=REQUESTS_HEADER).text

    left = html.find('params: {"nsid":"')
    right = html[left:].find('","') + left
    user_id = html[left + 17:right]

    left = html.find('root.YUI_config.flickr.request.id = "')
    right = html[left:].find('";') + left
    req_id = html[left + 37:right]

    left = html.find('root.YUI_config.flickr.api.site_key = "')
    right = html[left:].find('";') + left
    api_key = html[left + 39:right]

    return Credentials(user_id, req_id, api_key)


def create_api_request_url(page: int, credentials: Credentials) -> str:
    return "https://api.flickr.com/services/rest?per_page=50" \
           "&page={0}" \
           "&extras=can_addmeta%2Ccan_comment%2Ccan_download%2Ccan_share%2Ccontact%2Ccount_comments%2Ccount_faves%2Ccount_views%2Cdate_taken%2Cdate_upload%2Cdescription%2Cicon_urls_deep%2Cisfavorite%2Cispro%2Clicense%2Cmedia%2Cneeds_interstitial%2Cowner_name%2Cowner_datecreate%2Cpath_alias%2Crealname%2Crotation%2Csafety_level%2Csecret_k%2Csecret_h%2Curl_c%2Curl_f%2Curl_h%2Curl_k%2Curl_l%2Curl_m%2Curl_n%2Curl_o%2Curl_q%2Curl_s%2Curl_sq%2Curl_t%2Curl_z%2Cvisibility%2Cvisibility_source%2Co_dims%2Cis_marketplace_printable%2Cis_marketplace_licensable%2Cpubliceditability" \
           "&get_user_info=1" \
           "&jump_to=" \
           "&user_id={1}" \
           "&view_as=use_pref" \
           "&sort=use_pref" \
           "&viewerNSID=" \
           "&method=flickr.people.getPhotos" \
           "&csrf=" \
           "&api_key={2}" \
           "&format=json" \
           "&hermes=1" \
           "&hermesClient=1" \
           "&reqId={3}" \
           "&nojsoncallback=1".format(page, credentials.user_id, credentials.api_key, credentials.req_id)


def get_images_from_page(page: int, credentials: Credentials) -> List[FlickrImage]:
    """ Retrieves images with high quality urls only from the current page in the API. """

    url = create_api_request_url(page, credentials)
    request = requests.get(url).json()['photos']['photo']
    response = [FlickrImage(link['id'], link['url_h_cdn']) for link in request
                if 'url_h_cdn' in link.keys()]
    return response


def get_all_images_from_user(credentials: Credentials) -> Iterable[List[FlickrImage]]:
    page = 1
    previous, current = None, get_images_from_page(page, credentials)

    while previous != current:
        yield current
        page += 1
        previous, current = current, get_images_from_page(page, credentials)


def download_image(download_dir: str, image: FlickrImage) -> None:
    full_path = os.path.join(download_dir, image.id + get_extension_from_url(image.link))
    if not os.path.exists(full_path):
        print("Downloading {0} ...".format(image.id))
        urlretrieve(image.link, full_path)
    else:
        print("Already have {0}.".format(image.id))


def main():
    download_dir = make_output_folder('megane_wakui')
    profile_page = "https://www.flickr.com/photos/megane_wakui/"
    credentials = get_user_credentials(profile_page)

    for image_collection in get_all_images_from_user(credentials):
        for image in image_collection:
            download_image(download_dir, image)


if __name__ == '__main__':
    main()

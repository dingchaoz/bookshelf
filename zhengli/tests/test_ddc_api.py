from os.path import abspath, dirname, join

import PIL
import pytest
from PIL import Image

from zhengli.core.title_of_book_api import (extract_IBSN_from_api_return,
                                            find_closest_image,
                                            get_bookimages_url, get_ddc_api,
                                            get_hashdiff_image, get_image_book,
                                            get_ISBN_from_title)

PAYLOAD_DIR = join(abspath(dirname(dirname(dirname((__file__))))),
                   "zhengli/data")
PAYLOAD_FILE = join(PAYLOAD_DIR, "wanted_shelf.png")


@pytest.mark.parametrize(
    'title, author, exp_ISBN', [pytest.param(
        'Silence', 'Shusaku Endo', (['9780720612868',
                                     '0720612861', '9780870115356',
                                     '0870115359'], ['Fiction']))])
def test_get_ISBN_from_title(title, author, exp_ISBN):
    response = get_ISBN_from_title(title)
    res_isbn = extract_IBSN_from_api_return(response, author)
    assert exp_ISBN == res_isbn


@pytest.mark.parametrize(
    'title,, author, exp_ddc', [pytest.param(
        'All the living', 'C. E. Morgan', 813.6
    )])
def test_ddc_api(title, author, exp_ddc):
    res_ddc = get_ddc_api(title=title, author_name=author)
    assert res_ddc == exp_ddc


@pytest.mark.parametrize(
    'image_url',
    [pytest.param('https://images.isbndb.com/covers/22/90/9780857072290.jpg')])
def test_open_image(image_url):
    img = get_image_book(image_url)
    assert isinstance(img, PIL.JpegImagePlugin.JpegImageFile)


@pytest.mark.parametrize(
    'image1_url,image2_path',
    [pytest.param('https://images.isbndb.com/covers/22/90/9780857072290.jpg',
                  PAYLOAD_FILE)])
def test_hashdiff_image(image1_url, image2_path):
    img1 = get_image_book(image1_url)
    img2 = Image.open(image2_path)
    assert 41 == get_hashdiff_image(img1, img2)


@pytest.mark.parametrize(
    'title,image2_path',
    [pytest.param("Silence",
                  PAYLOAD_FILE)])
def test_find_closest_image(title, image2_path):
    response = get_ISBN_from_title(title)
    image_urls = get_bookimages_url(response)
    book_shelf = Image.open(image2_path)
    most_likely_author = find_closest_image(image_urls, book_shelf)
    assert 'Becca Fitzpatrick' == most_likely_author

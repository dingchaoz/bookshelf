import os
from os.path import abspath, dirname, join

import cv2
import pytest

from zhengli.core.detect_books_from_shelf import (find_rectangles,
                                                  get_book_lines,
                                                  make_crops_from_rect)
from zhengli.core.image_title_author_scrape import detect_text
from zhengli.core.main import get_rect_from_img, get_text_from_rect, main
from zhengli.core.spell_check import correct_text

PAYLOAD_DIR = join(abspath(dirname(dirname(dirname((__file__))))),
                   "zhengli/data")
IMAGE_FILE = join(PAYLOAD_DIR, "IMG_20190904_155939359.jpg")

@pytest.mark.parametrize(
    'num_books', [pytest.param(8)])
def test_main(num_books):
    result = main()
    assert len(result) == num_books
    assert isinstance(result, list)

@pytest.mark.parametrize(
    'IMAGE_FILE,num_books', [pytest.param(IMAGE_FILE, 8)])
def test_get_storage_books(IMAGE_FILE, num_books):
    rectangles, img = get_rect_from_img(IMAGE_FILE)
    storage_book = get_text_from_rect(rectangles, img)
    assert len(storage_book) == num_books

@pytest.mark.parametrize(
    'img_path,num_books', [pytest.param(IMAGE_FILE, 9)])
def test_book_img(img_path, num_books):
    img = cv2.imread(img_path)
    booklines = get_book_lines(img, debug=False)
    rectangles = find_rectangles(booklines)
    books_img = []
    for x in rectangles:
        books_img.append(make_crops_from_rect(img, x))

    assert len(books_img) == num_books

    storage_book = {}
    for order, book in enumerate(books_img):

        filename = join(PAYLOAD_DIR, "{}_ind.png".format(os.getpid()))
        cv2.imwrite(filename, book)
        text = detect_text(filename)
        if text:
            storage_book.setdefault(order, text)
    assert len(storage_book) == 8


@pytest.mark.parametrize(
    'raw_input,corrected_input',
    [pytest.param
     (("whereis th elove hehad dated forImuch of thepast who "
       "couqdn'tread in sixtgrade and ins pired him"),
      "where is the love he had dated for much of the past who couldn't read in six grade and inspired him")])
def test_correct_text(raw_input, corrected_input):
    output = correct_text(raw_input)
    assert corrected_input == output

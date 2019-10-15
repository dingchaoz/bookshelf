import os
from os.path import abspath, dirname, join

import cv2

from zhengli.core.detect_books_from_shelf import (find_rectangles,
                                                  get_book_lines,
                                                  make_crops_from_rect)
from zhengli.core.image_title_author_scrape import detect_text
from zhengli.core.spell_check import correct_text
from zhengli.core.title_of_book_api import get_ddc_api

PAYLOAD_DIR = join(abspath(dirname(dirname(dirname((__file__))))),
                   "zhengli/data")
IMAGE_FILE = join(PAYLOAD_DIR, "IMG_20190904_155939359.jpg")


def get_rect_from_img(img_path):
    img = cv2.imread(img_path)
    booklines = get_book_lines(img, debug=False)
    rectangles = find_rectangles(booklines)
    return rectangles, img


def get_text_from_rect(rectangles, img):
    books_img = []
    for x in rectangles:
        books_img.append(make_crops_from_rect(img, x))

    storage_book = {}
    for order, book in enumerate(books_img):

        filename = join(PAYLOAD_DIR, "{}_ind.png".format(order))
        cv2.imwrite(filename, book)
        text = detect_text(filename)
        if text:
            corrected_text = text.split('\n')
            corrected_text = [correct_text(x) for x in corrected_text]
            storage_book.setdefault(order, corrected_text)

    return storage_book


def main():
    rectangles, img = get_rect_from_img(IMAGE_FILE)
    storage_book = get_text_from_rect(rectangles, img)
    print("detected texts from books are the following {}".format(storage_book))
    books_info = []
    for i, book in storage_book.items():
        ddc, dict_of_results = get_ddc_api(max(book, key=len))
        books_info.append((ddc, dict_of_results))
    print(books_info)
    return books_info


if __name__ == "__main__":
    main()

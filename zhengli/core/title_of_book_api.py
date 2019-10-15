import re
from collections import defaultdict
from io import BytesIO

import imagehash
import requests
from PIL import Image


def form_url(ISBN=None):
    """Formulate an url that will be sent to openlibrary.org/api'.

    Parameters
    ----------
    ISBN : string
        a string of book's ISBN.

    Returns
    -------
    string
        An url that will be sent to openlibrary/org/api.

    """
    url = 'https://openlibrary.org/api/books?bibkeys=ISBN:' + \
        ISBN + '&jscmd=data&format=json'

    return url


def form_url_title(title='here is where we meet'):
    """Formulate an url that will be sent to openlibrary.org/api'.

    Parameters
    ----------
    ISBN : string
        a string of book's ISBN.

    Returns
    -------
    string
        An url that will be sent to openlibrary/org/api.

    """
    title = "+".join(title.split())
    url = 'https://isbnsearch.org/search?s=' + \
        title

    return url


def get_ISBN_from_title(title):
    h = {'Authorization': '43360_fd60754106422e4ff2600025312a1118'}
    title = title.title()

    resp = requests.get("https://api2.isbndb.com/books/{"
                        + title + "}", headers=h)
    # print('Acquired following info about the book {}'.format(resp.))
    # print(resp.json())
    results = resp.json()['books']

    return results


def get_author_name(results):
    authors = []
    for x in results:
        try:
            if 'authors' in x.keys():
                authors.append(x['authors'])
        except Exception:
            return "Jane Doe"

    return authors


def get_bookimages_url(results):
    image_urls = []
    for x in results:
        try:
            if 'image' in x.keys() and 'authors' in x.keys():
                image_urls.append((x['image'], x['authors']))
        except Exception:
            pass

    return image_urls


def mode_authors(list_of_authors):
    author_count = defaultdict(int)
    for auth in list_of_authors:
        for x in auth:
            author_count[x] += 1

    return max(author_count, key=lambda key: author_count[key])


def extract_IBSN_from_api_return(results, author):
    # note that this gets the last ISBN in the list--there maybe multiple
    # copies
    # of the book--hopefully all additions have the same dewey decimal number
    ISBN = None
    right = []
    genre = None

    for x in results:
        # print(x.keys)
        try:
            if 'authors' in x.keys():
                if author in x['authors']:
                    # print(x)
                    right.append(x['isbn13'])
                    right.append(x['isbn'])

                    if 'subjects' in x.keys():
                        genre = x['subjects']

        except Exception:
            pass

    return right, genre


def get_response(url):
    response = requests.get(url)
    # print('Acquired following info about the book {}'.format(response.text))
    return response.text


def extract_ddc(text):
    try:
        dewey_pattern = re.compile(r'(\\d{3}/.\\d+?\/?d)')
        ddc = dewey_pattern.findall(text)[0]
        # print('Dewey decimal code of the book is {}'.format(ddc))
    except Exception:
        if 'fiction' in text:
            return 813.
        else:
            print("dewey_decimal_not_found")
            ddc = None

    return ddc


def check_genre_ddc(genre):
    for x in genre:
        # print(x)
        if x.lower() == 'fiction':
            return 813.6
        if x.lower() == 'nonfiction':
            return 810
        if x.lower() == 'journalism':
            return '070'

    return 000.0


def get_image_book(image_url):
    '''
    Open up an image by its url
    '''
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img


def get_hashdiff_image(img1, img2):
    '''
    Get the absolute differene bewteen hashed images
    '''
    hash = imagehash.average_hash(img1)
    otherhash = imagehash.average_hash(img2)
    return abs(hash - otherhash)


def find_closest_image(urls, book_shelf):
    most_likely_author = None
    min_diff = 1e6
    for url, author in urls:
        try:
            candidate_img = get_image_book(url)
            diff = get_hashdiff_image(candidate_img, book_shelf)
            if diff < min_diff:
                min_diff = diff
                most_likely_author = author
        except Exception:
            pass

    return most_likely_author


def get_ddc_api(ISBN=None, title=None, author_name=None):

    ddc = None

    if ISBN is not None:
        url = form_url(ISBN)
        response = get_response(url)
        ddc = extract_ddc(response)
        return ddc

    else:
        response = get_ISBN_from_title(title)
        if author_name is None:
            author_name = mode_authors(get_author_name(response))
            print(author_name)

        ISBN, genre = extract_IBSN_from_api_return(response, author_name)
        print(ISBN, genre)
        # print(ISBN)
        for x in ISBN:
            if not ddc:
                url = form_url(x)
                response = get_response(url)
                ddc = extract_ddc(response)
                if ddc is not None:
                    return ddc
                else:
                    pass
        if ddc is None and genre is not None:
            ddc = check_genre_ddc(genre)
            return ddc

    return ddc

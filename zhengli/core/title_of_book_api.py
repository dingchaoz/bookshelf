import re
from collections import defaultdict
from io import BytesIO

import cv2
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
    # url = 'https://openlibrary.org/api/books?bibkeys=ISBN:' + \
    #     ISBN + '&jscmd=data&format=json'

    url = 'http://classify.oclc.org/classify2/Classify?isbn=' + ISBN +\
        '&summary=true'

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
    print('calling api to get isbn')
    h = {'Authorization': '43360_fd60754106422e4ff2600025312a1118'}
    title = title.title()

    resp = requests.get("https://api2.isbndb.com/books/{"
                        + title + "}", headers=h)

    results = resp.json()['books']
    # print('Acquired following info about the book {}'.format(results))
    dict_results = order_results_into_dict(results)
    return dict_results


def order_results_into_dict(results):
    '''
    order the response from get_ISBN_from_title into a dictionary
    '''
    dict_of_results = dict(zip(range(len(results)), results))
    return dict_of_results


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


def extract_IBSN_from_api_return(results):
    # note that this gets the last ISBN in the list--there maybe multiple
    # copies
    # of the book--hopefully all additions have the same dewey decimal number
    ISBN = []
    genre = None

    # print(x.keys)
    if 'isbn13' in results.keys():
        ISBN.append(results['isbn13'])
    elif 'isbn' in results.keys():
        ISBN.append(results['isbn'])
    else:
        print('no isbn found')

    if 'subjects' in results.keys():
        genre = results['subjects']

    return ISBN[0], genre


def get_response(url):
    response = requests.get(url)
    # print('Acquired following info about the book {}'.format(response.text))
    return response.text


def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i + 1)


def extract_ddc(text):
    # try:
    #     dewey_pattern = re.compile(r'(\\d{3}/.\\d+?\/?d)')
    #     ddc = dewey_pattern.findall(text)[0]
    #     # print('Dewey decimal code of the book is {}'.format(ddc))
    # except Exception:
    #     if 'fiction' in text:
    #         return 813.
    #     else:
    #         print("dewey_decimal_not_found")
    #         ddc = None
    print('response from api call to get ddc is{}'.format(text))
    potential_ddcs = [text[i + 6:i + 11].strip()for i in findall('nsfa', text)]
    print('potential ddcs', potential_ddcs)
    if any([ddc[:3].isdigit() for ddc in potential_ddcs]):
        print('valid ddc')
        return next(ddc for ddc in potential_ddcs if ddc[:3].isdigit())
    elif any(['FIC' in ddc.strip() for ddc in potential_ddcs]):
        print('FIC found')
        return '813.0'
    else:
        return None


def check_genre_ddc(genre):
    for x in genre:
        # print(x)
        if x.lower() == 'fiction':
            return 813.6
        if x.lower() == 'nonfiction':
            return 810
        if x.lower() == 'journalism':
            return '070'
        if x.lower() == 'literacy':
            return 302

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


def extract_key_from_api(dict_of_results, key='image'):
    '''
    return list of image urls from books
    '''
    field_urls = {}
    for k, item in dict_of_results.items():
        try:
            field_urls[k] = item[key]
        except Exception:
            pass
    return field_urls


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min((distances[i1], distances[i1 + 1],
                             distances_[-1])))
        distances = distances_
    return distances[-1]


def load_publisher(list_path):
    with open(list_path, "r") as text_file:
        publisher_list = text_file.read().split(',')

    return publisher_list


def find_closest_image(response, spine_image):
    urls = extract_key_from_api(response, 'image')
    min_diff = 1e6
    closest_item_index = []
    for k, url in urls.items():
        try:
            candidate_img = get_image_book(url)
            diff = get_hashdiff_image(candidate_img, spine_image)
            if diff < min_diff:
                min_diff = diff
                closest_item_index.append(k)
        except Exception:
            pass

    return closest_item_index


def find_closest_titlestring(response, detected_text):
    titles = extract_key_from_api(response, 'title')
    min_diff = 1e6
    closest_item_index = []
    detected_title = max(detected_text, key=len)
    for k, url in titles.items():
        try:
            diff = levenshteinDistance(detected_title, url)
            if diff <= min_diff:
                min_diff = diff
                closest_item_index.append(k)
        except Exception:
            pass

    return closest_item_index


def get_potential_publisher(publisher_list, detected_text):
    print('checking if there is publisher in detected text')
    min_diff = 3
    potential_publisher = None
    for text in detected_text:
        for publisher in publisher_list:
            diff = levenshteinDistance(text, publisher)
            if diff <= min_diff:
                print('there is a pontential publisher{}'.format(publisher))
                min_diff = diff
                potential_publisher = publisher
    return potential_publisher


def find_closest_publisherstring(response, detected_text, publisher_list):
    publishers = extract_key_from_api(response, 'publisher')
    min_diff = 3
    closest_item_index = []
    detected_publisher = get_potential_publisher(publisher_list, detected_text)
    for k, url in publishers.items():
        try:
            diff = levenshteinDistance(detected_publisher, url)
            if diff <= min_diff:
                min_diff = diff
                closest_item_index.append(k)
        except Exception:
            pass

    return closest_item_index

# TODO


def get_best_match_response(response,
                            detected_text, publisher_list):
    spine_image = cv2.imread(detected_text[-1])
    image_closest_item_index = find_closest_image(response, spine_image)
    # closest_item = response[image_closest_item_index]
    string_closest_item_index = find_closest_titlestring(
        response, detected_text)
    publisherclosest_item_index = find_closest_publisherstring(response,
                                                               detected_text,
                                                               publisher_list)
    print(image_closest_item_index, string_closest_item_index,
          publisherclosest_item_index)
    lst = image_closest_item_index + \
        string_closest_item_index + publisherclosest_item_index
    best_match_index = max(set(lst), key=lst.count)
    best_match_response = response[best_match_index]
    print('best match book is{}'.format(best_match_response))
    return best_match_response


def get_ddc_from_isbn(isbn_string):
    url = form_url(isbn_string)
    response = get_response(url)
    ddc = extract_ddc(response)
    return ddc


def get_ddc_api(ISBN=None, title=None, author_name=None,
                detected_text=None, pub_list_path=None, image_id=None):
    print('calling api to get ddc ')
    ddc = None
    publisher_list = load_publisher(pub_list_path)

    if ISBN is not None:
        url = form_url(ISBN)
        response = get_response(url)
        ddc = extract_ddc(response)
        return ddc, eval(response)

    else:
        response = get_ISBN_from_title(title)

        best_match_response = get_best_match_response(response,
                                                      detected_text,
                                                      publisher_list)
        ISBN, genre = extract_IBSN_from_api_return(
            best_match_response)
        print(ISBN, genre)
        url = form_url(ISBN)
        response = get_response(url)
        ddc = extract_ddc(response)
        if ddc is None and genre is not None:
            print('ddc is none and genre is not none')
            ddc = check_genre_ddc(genre)

        print('ddc is {} and best match book is {}'.
              format(ddc, best_match_response))

    return ddc, best_match_response

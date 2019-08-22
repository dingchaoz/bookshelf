import re

import requests


def form_url(ISBN='9780980200447'):
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


def get_reponse(url):
    response = requests.get(url)
    print('Acquired following info about the book {}'.format(response.text))
    return response.text


def extract_ddc(text):
    dewey_pattern = re.compile(r'(\d{3}/.\d)')
    ddc = dewey_pattern.findall(text)[0]
    print('Dewey decimal code of the book is {}'.format(ddc))
    return ddc


def get_ddc_api(ISBN=None):
    url = form_url(ISBN)
    response = get_reponse(url)
    print(response)
    ddc = extract_ddc(response)
    return ddc

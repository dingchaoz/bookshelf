import re

import requests


def form_ddc_api_url(ISBN='9780980200447'):
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


def get_books_from_title(title):
    """returns list of books for any given book title.

    Parameters
    ----------
    title : string
        Title of book for which we need the ISBN .
    author : string
        author of the book for which we need the ISBN.

    Returns
    -------
    int
        returns the ISBN number of the matching book (actually returns the
        last entry in the json's ISBN number.)

    """

    h = {'Authorization': '43360_fd60754106422e4ff2600025312a1118'}
    title = title.title()
    # title = "%20".join( title.split() )
    resp = requests.get("https://api2.isbndb.com/books/{"
                        + title + "}", headers=h)

    results = resp.json()['books']

    return results


def extract_IBSN_from_api_return(results, author):
    # note that this gets the last ISBN in the list--there maybe multiple copies
    # of the book--hopefully all additions have the same dewey decimal number
    ISBN = None
    for x in results:
        # print(x)
        try:
            if 'authors' in x.keys() and author in x['authors']:
                ISBN = x['isbn13']
        except Exception:
            pass

    return ISBN


def get_reponse(url):
    response = requests.get(url)
    print('Acquired following info about the book {}'.format(response.text))
    return response.text


def extract_ddc(text):
    try:
        dewey_pattern = re.compile('(\\d{3}/.\\d)')
        ddc = dewey_pattern.findall(text)[0]
        print('Dewey decimal code of the book is {}'.format(ddc))
    except Exception:
        print("dewey_decimal_not_found")
        ddc = 000.0
    return ddc


def get_ddc_api(ISBN=None, title=None, author_name=None):
    if ISBN is not None:
        url = form_ddc_api_url(ISBN)
    else:
        response = get_books_from_title(title)
        ISBN = extract_IBSN_from_api_return(response, author_name)
        url = form_ddc_api_url(ISBN)

    response = get_reponse(url)
    ddc = extract_ddc(response)
    return ddc

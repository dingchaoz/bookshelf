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
<<<<<<< HEAD
    #title = "%20".join( title.split() )
    resp = requests.get("https://api2.isbndb.com/books/{" \
             +title +"}", headers=h)
    #print('Acquired following info about the book {}'.format(resp.))
    print(resp.json())
    results = resp.json()['books']

    # note that this gets the last ISBN in the list--there maybe multiple copies
    # of the book--hopefully all additions have the same dewey decimal number
    right = []
    ddc = []
=======
    # title = "%20".join( title.split() )
    resp = requests.get("https://api2.isbndb.com/books/{"
                        + title + "}", headers=h)

    results = resp.json()['books']

    return results


def extract_IBSN_from_api_return(results, author):
    # note that this gets the last ISBN in the list--there maybe multiple copies
    # of the book--hopefully all additions have the same dewey decimal number
    ISBN = None
>>>>>>> a11c9423f3991d6b717b1a975b0bd6ed48ad8c05
    for x in results:
        # print(x)
        try:
<<<<<<< HEAD
            if 'authors' in x.keys():
                if author in x['authors']:
                    right.append(x['isbn13'])
                    right.append(x['isbn'])
        except:
                pass
=======
            if 'authors' in x.keys() and author in x['authors']:
                ISBN = x['isbn13']
        except Exception:
            pass

    return ISBN
>>>>>>> a11c9423f3991d6b717b1a975b0bd6ed48ad8c05


#def get_isbn(text):

#def get_classifications():


def get_response(url):
    response = requests.get(url)
    print('Acquired following info about the book {}'.format(response.text))
    return response.text


def extract_ddc(text):
    try:
        dewey_pattern = re.compile(r'(\\d{3}/.\\d+?\/?d)')
        ddc = dewey_pattern.findall(text)[0]
        print('Dewey decimal code of the book is {}'.format(ddc))
<<<<<<< HEAD
    except:
        if 'fiction' in text:
            return 813.
        else:
            print("dewey_decimal_not_found")
            ddc = None
=======
    except Exception:
        print("dewey_decimal_not_found")
        ddc = 000.0
>>>>>>> a11c9423f3991d6b717b1a975b0bd6ed48ad8c05
    return ddc


def get_ddc_api(ISBN=None, title=None, author_name=None):
<<<<<<< HEAD
    ddc = None
    if ISBN is not None:
        url = form_url(ISBN)

    else:
        print("getting ISBN")
=======
    if ISBN is not None:
        url = form_ddc_api_url(ISBN)
    else:
        response = get_books_from_title(title)
        ISBN = extract_IBSN_from_api_return(response, author_name)
        url = form_ddc_api_url(ISBN)
>>>>>>> a11c9423f3991d6b717b1a975b0bd6ed48ad8c05

        ISBN = get_ISBN_from_title(title, author_name)
        #print(ISBN)
        for x in ISBN:
            if not ddc:
                url = form_url(x)
                response = get_response(url)
                ddc = extract_ddc(response)
                if ddc is not None:
                    return ddc
                else:
                    pass
    response = get_response(url)
    ddc = extract_ddc(response)
    print(ddc)
    return ddc

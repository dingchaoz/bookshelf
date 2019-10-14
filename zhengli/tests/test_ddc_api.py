import pytest

# from zhengli.core.dewey_decimal_api import get_ddc_api
<<<<<<< HEAD
from zhengli.core.title_of_book_api import get_ISBN_from_title, get_ddc_api
from zhengli.core.image_title_author_scrape import detect_text
# tests get_ddc_api with a given ISBN to return a given Dewey Decimal Number

@pytest.mark.parametrize(
    'ISBN,exp_ddc', [pytest.param(
        '9780980200447', '028/.9'
    )])
def test_ddc_api(ISBN, exp_ddc):
    res_ddc = get_ddc_api(ISBN)
    assert res_ddc == exp_ddc
=======
from zhengli.core.title_of_book_api import (extract_IBSN_from_api_return,
                                            get_books_from_title, get_ddc_api)
>>>>>>> a11c9423f3991d6b717b1a975b0bd6ed48ad8c05

# tests get_ISBN_from_title with a given book title and author, returns ISBN
@pytest.mark.parametrize(
    'title, author, exp_ISBN', [pytest.param(
        'Silence', 'Shusaku Endo', ['9780720612868', '9780870115356']
    )])
def test_get_ISBN_from_title(title, author, exp_ISBN):
    response = get_books_from_title(title)
    res_isbn = extract_IBSN_from_api_return(response, author)
    assert res_isbn in exp_ISBN

# tests get_ddc_api with given title and author to return Dewey Decimal Number
@pytest.mark.parametrize(
    'title,, author, exp_ddc', [pytest.param(
        'All the living', 'C. E. Morgan', '813/.6'
    )])
def test_ddc_api(title, author, exp_ddc):
    res_ddc = get_ddc_api(title=title, author_name=author)
    assert res_ddc == exp_ddc

#
'''
@pytest.mark.parametrize(
    'path, exp_text_len', [pytest.param(
        'john_cheever_shelf.png', 1
    )])
def test_detect_text(path, exp_text_len):
    res_text = detect_text(path)
    assert res_text > exp_text_len
    '''

import pytest

# from zhengli.core.dewey_decimal_api import get_ddc_api
from zhengli.core.title_of_book_api import (extract_IBSN_from_api_return,
                                            get_books_from_title, get_ddc_api)


@pytest.mark.parametrize(
    'title, author, exp_ISBN', [pytest.param(
        'Silence', 'Shusaku Endo', ['9780720612868', '9780870115356']
    )])
def test_get_ISBN_from_title(title, author, exp_ISBN):
    response = get_books_from_title(title)
    res_isbn = extract_IBSN_from_api_return(response, author)
    assert res_isbn in exp_ISBN


@pytest.mark.parametrize(
    'title,, author, exp_ddc', [pytest.param(
        'All the living', 'C. E. Morgan', '813/.6'
    )])
def test_ddc_api(title, author, exp_ddc):
    res_ddc = get_ddc_api(title=title, author_name=author)
    assert res_ddc == exp_ddc

import pytest

# from zhengli.core.dewey_decimal_api import get_ddc_api
from zhengli.core.title_of_book_api import get_ISBN_from_title, get_ddc_api

@pytest.mark.parametrize(
    'ISBN,exp_ddc', [pytest.param(
        '9780980200447', '028/.9'
    )])
def test_ddc_api(ISBN, exp_ddc):
    res_ddc = get_ddc_api(ISBN)
    assert res_ddc == exp_ddc


@pytest.mark.parametrize(
    'title, author, exp_ISBN', [pytest.param(
        'Silence', 'Shusaku Endo', ['9780720612868', '9780870115356']
    )])


def test_get_ISBN_from_title(title, author, exp_ISBN):
    res_isbn = get_ISBN_from_title(title, author)
    assert res_isbn in exp_ISBN


@pytest.mark.parametrize(
    'title,, author, exp_ddc', [pytest.param(
        'All the living', 'C. E. Morgan', '813/.6'
    )])
def test_ddc_api(title, author, exp_ddc):
    res_ddc = get_ddc_api(title=title, author_name=author)
    assert res_ddc == exp_ddc

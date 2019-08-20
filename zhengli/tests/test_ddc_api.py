import pytest

from zhengli.core.dewey_decimal_api import get_ddc_api


@pytest.mark.parametrize(
    'ISBN,exp_ddc', [pytest.param(
        '9780980200447', '028/.9'
    )])
def test_ddc_api(ISBN, exp_ddc):
    res_ddc = get_ddc_api(ISBN)
    assert res_ddc == exp_ddc

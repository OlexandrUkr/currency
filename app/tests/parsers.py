from unittest.mock import MagicMock

from currency.models import Rate
from currency.tasks import parse_privatbank, parse_monobank


def test_privatbank_parser(mocker):
    initial_count = Rate.objects.all().count()
    privat_data = [{"ccy":"EUR","base_ccy":"UAH","buy":"40.05630","sale":"41.74000"},  # noqa: E231
                   {"ccy":"USD","base_ccy":"UAH","buy":"36.46850","sale":"37.35317"}]  # noqa: E231
    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(
            json=lambda: privat_data
        )
    )

    parse_privatbank()
    assert Rate.objects.all().count() == initial_count + 2

    parse_privatbank()
    assert Rate.objects.all().count() == initial_count + 2

    assert request_get_mock.call_count == 2


def test_monobank_parser(mocker):
    initial_count = Rate.objects.count()
    monobank_data = [
        {"currencyCodeA":840,"currencyCodeB":980,"date":1682546474,  # noqa: E231
         "rateBuy":36.64,"rateCross":0,"rateSell":37.4405},  # noqa: E231
        {"currencyCodeA":978,"currencyCodeB":980,"date":1682606774,  # noqa: E231
         "rateBuy":40.30,"rateCross":0,"rateSell":41.4696},  # noqa: E231
        {"currencyCodeA":978,"currencyCodeB":840,"date":1682546474,  # noqa: E231
         "rateBuy":1.096,"rateCross":0,"rateSell":1.11},  # noqa: E231
        {"currencyCodeA":826,"currencyCodeB":980,"date":1682613397,  # noqa: E231
         "rateBuy":0,"rateCross":46.8522,"rateSell":0}  # noqa: E231
    ]
    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(
            json=lambda: monobank_data
        )
    )

    parse_monobank()
    assert Rate.objects.count() == initial_count + 2

    parse_monobank()
    assert Rate.objects.count() == initial_count + 2

    assert request_get_mock.call_count == 2

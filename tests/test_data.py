import pandas as pd

from blablatest.data import compute_pairwise_rates


def test_compute_pairwise_rates():
    rates = pd.Series([1.2, 0.8], index=['USD', 'GBP'], name='rate')
    result = compute_pairwise_rates(rates)

    expected = pd.DataFrame({
        'from_cur_code': ['USD', 'GBP'],
        'to_cur_code': ['GBP', 'USD'],
        'exchange_rate': [0.8 / 1.2, 1.2 / 0.8],
    }, index=[0, 1])
    pd.testing.assert_frame_equal(result, expected)

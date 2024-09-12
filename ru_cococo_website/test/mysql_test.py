from ru_cococo_website.App.database import TOTAL_BIGRAM_COUNT
from ru_cococo_website.Collocation.collocation import calculate_bigram_rates


def test_bigram_count():
    assert TOTAL_BIGRAM_COUNT > 0


def test_rates():
    assert calculate_bigram_rates(123, 1213001, 6)["TSCORE"] == 2.4147

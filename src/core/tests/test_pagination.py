from core.utilities import paginate


def test_paginate_numeric_string_out_of_range_clamps_to_last_page():
    items = list(range(30))
    page, _ = paginate("999", items, per_page=10)
    assert page.number == 3

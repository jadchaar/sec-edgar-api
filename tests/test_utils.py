from sec_edgar_api._utils import is_cik, merge_submission_dicts


def test_is_cik():
    assert not is_cik("AAPL")
    assert not is_cik("")
    assert not is_cik("0" * 11)

    assert is_cik("320193")
    assert is_cik("320193".zfill(10))


def test_merge_submission_dicts():
    d1 = {
        "foo": ["1", "2", "3"],
        "bar": ["a", "b", "c"],
    }
    d2 = {
        "foo": ["4", "5", "6"],
        "bar": ["d", "e", "f"],
    }
    to_merge = [d1, d2]
    merged = merge_submission_dicts(to_merge)

    assert merged["foo"] == d1["foo"] + d2["foo"]
    assert merged["bar"] == d1["bar"] + d2["bar"]
    assert len(merged.keys()) == 2

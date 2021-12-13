import datetime as dt
from pytest_experiments import common


def test_mark_utc():
    now = dt.datetime.utcnow()
    assert now.tzinfo is None
    utcnow = common.mark_utc(now)
    assert utcnow.tzinfo == dt.timezone.utc
    assert now.date() == utcnow.date()
    assert now.time() == utcnow.time()


def test_type_name_of():
    class SomeClass:
        pass

    obj = SomeClass()
    assert common.type_name_of(obj) == "SomeClass"


def test_any_are_none():
    assert common.any_are_none(None, 0.0)
    assert not common.any_are_none(False, 0)

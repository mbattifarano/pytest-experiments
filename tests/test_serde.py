import datetime as dt
import numpy as np
import json
from pytest_experiments import serde


def test_datetime_serde():
    now = dt.datetime.now()
    encoded = serde.datetime_encode(now)
    assert json.dumps(encoded)
    decoded = serde.datetime_decode(encoded)
    assert isinstance(decoded, dt.datetime)
    assert now == decoded


def test_numpy_array_serde():
    a = np.arange(12).reshape((3, 4))
    encoded = serde.numpy_encode(a)
    assert json.dumps(encoded)
    decoded = serde.numpy_decode(encoded)
    assert isinstance(decoded, type(a))
    assert np.allclose(a, decoded)

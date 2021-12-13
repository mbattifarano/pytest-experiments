import datetime as dt
import numpy as np
import json

from numpy.lib.arraysetops import isin
from pytest_experiments import json_tools


def test_serialize_deserialize():
    now = dt.datetime.utcnow()
    data = {
        "hello": "a_string",
        "world": now,
        "range": np.arange(5),
    }
    json_string = json_tools.json_serializer(data)
    naive_decode = json.loads(json_string)
    assert naive_decode == {
        "hello": "a_string",
        "world": {"__data__": now.isoformat(), "__typename__": "datetime"},
        "range": {"__data__": [0, 1, 2, 3, 4], "__typename__": "ndarray"},
    }
    custom_decode = json_tools.json_deserializer(json_string)
    print(custom_decode)
    assert data["hello"] == custom_decode["hello"]
    assert data["world"] == custom_decode["world"]
    assert isinstance(custom_decode["range"], np.ndarray)
    assert np.allclose(data["range"], custom_decode["range"])

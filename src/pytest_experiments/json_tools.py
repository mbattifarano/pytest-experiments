from typing import Any
import json
from .config import TYPE_KEY, DATA_KEY, SKIP_UNKNOWN_JSON_TYPES, TYPE_MAPPINGS
from .common import type_name_of, any_are_none


def json_serializer(obj: dict) -> str:
    """Serialize an object to a JSON string."""
    return TypeDispatchedJSONEncoder().encode(obj)


def json_deserializer(s: str) -> dict:
    """Deserialize an object from a JSON string."""
    return json.loads(s, object_hook=object_hook)


class TypeDispatchedJSONEncoder(json.JSONEncoder):
    def __init__(
        self, *, skip_unknown_types=SKIP_UNKNOWN_JSON_TYPES, **kwargs
    ):
        super().__init__(**kwargs)
        self._skip_unknown_types = skip_unknown_types

    def default(self, o: Any) -> Any:
        typename = type_name_of(o)
        encoder, _ = TYPE_MAPPINGS.get(typename, (None, None))
        if encoder is not None:
            return {TYPE_KEY: typename, DATA_KEY: encoder(o)}
        if self._skip_unknown_types:
            return None
        return super().default(o)


def object_hook(obj: dict) -> dict:
    """Deserializes custom json objects."""
    typename = obj.get(TYPE_KEY, None)
    if typename is None:
        return obj
    data = obj.get(DATA_KEY, None)
    _, decoder = TYPE_MAPPINGS.get(typename, (None, None))
    if not any_are_none(data, decoder):
        data = decoder(data)
    return data

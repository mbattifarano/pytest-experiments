"""JSON serializers and deserializers for common datatypes."""
import datetime as dt


def numpy_encode(obj):
    """Encode a numpy array."""
    return obj.tolist()


def numpy_decode(obj):
    """Decode a numpy array."""
    import numpy  # noqa
    return numpy.array(obj)


def datetime_encode(obj):
    """Encode a datetime."""
    return obj.isoformat()


def datetime_decode(obj):
    """Decode a datetime."""
    return dt.datetime.fromisoformat(obj)

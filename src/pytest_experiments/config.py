"""Package configuration."""
from . import serde

OUTCOMES_ATTR = "outcomes"
EXPERIMENT_TABLENAME = "experiments"
TYPE_KEY = "__typename__"
DATA_KEY = "__data__"
SKIP_UNKNOWN_JSON_TYPES = True
TYPE_MAPPINGS = {
    "ndarray": (serde.numpy_encode, serde.numpy_decode),
    "datetime": (serde.datetime_encode, serde.datetime_decode),
}

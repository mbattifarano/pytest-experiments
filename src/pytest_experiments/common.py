"""Package tools common across modules."""
import enum
import datetime as dt
from typing import Any, Dict, NamedTuple

try:
    from typing import Protocol
except:
    from typing_extensions import Protocol

import pytest


class PytestExperimentsError(Exception):
    """Base class for package exceptions."""


class DocumentedEnum(enum.Enum):
    """An enum base class than enables docstrings for members.

    See https://stackoverflow.com/a/50473952
    """

    def __new__(cls, value, doc=None):
        self = object.__new__(cls)
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self


class PytestReportPhase(DocumentedEnum):
    """An enum for pytest report phases.

    These are the possible values that `TestReport.when` may take.
    """

    setup = 1, "The report generated during test setup."
    call = 2, "The report generated during test exectuion."
    teardown = 3, "The report generated during test teardown."


class PytestOutcome(DocumentedEnum):
    """An enum for the pytest report outcomes.

    These are the possible values that `TestReport.outcome` may take.
    """

    passed = 1, "The phase succeeded."
    failed = 2, "The phase failed."
    skipped = 3, "The phase was skipped by pytest."


class ExperimentOutcome(DocumentedEnum):
    """An enum for the experiment outcome.

    pytest reports are generated for each phase: setup, call, teardown.
    The experiment outcome reflects a single outcome from the three phases.
    """

    passed = 1, "The test passed."
    failed = 2, "The test failed."
    skipped = 3, "The test was skipped by pytest."
    error = 4, "The test failed during setup."
    not_reported = 5, "The test outcome was not reported."


class ExperimentRecord(NamedTuple):
    name: str
    start_time: dt.datetime
    end_time: dt.datetime
    outcome: str
    parameters: Dict[str, Any]
    data: Dict[str, Any]

class Storage(Protocol):

    def record_experiment(self, record: ExperimentRecord):
        """ Record an experiment in the storage """
        raise NotImplementedError

def mark_utc(timestamp: dt.datetime) -> dt.datetime:
    """Mark a UTC timestamp with the UTC timezone.

    This function should only be used when `timestamp` is already in UTC, but
    not labeled as such.
    """
    return timestamp.replace(tzinfo=dt.timezone.utc)


def type_name_of(obj: Any) -> str:
    """Return the name of the input's type."""
    return type(obj).__name__


def any_are_none(*args):
    """Return True if any of args are None."""
    for arg in args:
        if arg is None:
            return True
    return False

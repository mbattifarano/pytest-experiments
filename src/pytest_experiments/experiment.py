import datetime as dt
import pytest
from .config import OUTCOMES_ATTR
from .common import (
    PytestExperimentsError, PytestOutcome, PytestReportPhase, ExperimentOutcome
)
from .store import StorageManager, ExperimentModel


class Experiment:
    def __init__(self, request: pytest.FixtureRequest) -> None:
        self.context = request
        self.store = StorageManager(experiments_db_uri(self.context))
        self.created_at = dt.datetime.utcnow()
        self.completed_at = None
        self.outcome = ExperimentOutcome.not_reported
        self.data = {}

    def record(self, **kwargs):
        """Record data about this experiment.

        As this data will be serialized as JSON, keys *must* be strings. This
        is enforced by the stricter requirement that keys be valid python
        identifiers.
        """
        self.data.update(**kwargs)

    @property
    def test_fn(self) -> pytest.Function:
        """The test function."""
        return self.context.node

    @property
    def name(self) -> str:
        """The full qualified name of the test."""
        return self.test_fn.nodeid

    @property
    def parameters(self) -> dict:
        """The input parameters of the test.

        This will contain the closure of inputs supplied to the test,
        some of which we do not care about.
        """
        return dict(
            filter(self._ignore_funcargs_items, self.test_fn.funcargs.items())
        )

    def _ignore_funcargs_items(self, item) -> bool:
        """Ignores some funcarg items that we do not care about."""
        _, v = item
        if v is self:
            return False
        if isinstance(v, pytest.FixtureRequest):
            return False
        return True

    def get_reports(self) -> dict:
        """Returns the reports dict if it exists.

        The reports dict is populated by our custom hook and is *only*
        available after the test has run.
        """
        reports = getattr(self.context.node, OUTCOMES_ATTR, None)
        if reports is None:
            raise ExperimentError(
                "Could not find a `reports` attribute. "
                "This method may only be called after the test has run."
            )
        return reports

    def post_process(self):
        """Inspect the context for test outcome.

        The method may only be run *after* the test has completed.
        """
        self.completed_at = dt.datetime.utcnow()
        self.outcome = to_experiment_outcome(self.get_reports())

    def to_model(self) -> ExperimentModel:
        """Render the experiment into its database model."""
        return ExperimentModel(
            name=self.name,
            start_time=self.created_at,
            end_time=self.completed_at,
            outcome=self.outcome.name,
            parameters=self.parameters,
            data=self.data,
        )

    def save(self):
        """Save this experiment to the database."""
        self.store.record_experiment(self.to_model())

    def finish(self):
        """Post process the experiment and save to the database."""
        self.post_process()
        self.save()


def experiments_db_uri(request: pytest.FixtureRequest) -> str:
    """Retrieve the URI of the database used to store experiment results."""
    return request.config.option.experiments_database_uri


def to_experiment_outcome(reports: dict) -> ExperimentOutcome:
    """Return an ExperimentOutcome from the pytest reports"""
    if reports[PytestReportPhase.setup] is PytestOutcome.failed:
        return ExperimentOutcome.error
    test_outcome = reports.get(PytestReportPhase.call)
    if test_outcome is None:
        return ExperimentOutcome.not_reported
    return ExperimentOutcome[test_outcome.name]


class ExperimentError(PytestExperimentsError):
    pass

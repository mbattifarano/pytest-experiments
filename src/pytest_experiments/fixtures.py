import pytest
from .experiment import Experiment
from .config import OUTCOMES_ATTR
from .common import PytestOutcome, PytestReportPhase


def pytest_addoption(parser):
    """Add our pytest cli options."""
    group = parser.getgroup("experiments")
    group.addoption(
        "--experiments-database",
        action="store",
        dest="experiments_database_uri",
        default="sqlite:///experiments.db",
        help='Set the value for the fixture "bar".',
    )


def pytest_configure(config):
    """Add the `experiment` marker."""
    config.addinivalue_line(
        "markers", "experiment: mark a test as an experiment"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # pylint: disable=unused-argument
    """Store test reports on the test object for later inspection.

    Modified from:
    https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
    """
    # execute all other hooks to obtain the report object
    result = yield
    outcomes = getattr(item, OUTCOMES_ATTR, {})
    report = result.get_result()
    outcomes[PytestReportPhase[report.when]] = PytestOutcome[report.outcome]
    setattr(item, OUTCOMES_ATTR, outcomes)


@pytest.fixture
def notebook(request):
    """A notebook for your experiments."""
    exp = Experiment(request)
    yield exp
    exp.finish()

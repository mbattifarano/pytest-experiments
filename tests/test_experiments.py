from pytest_experiments.store import StorageManager


def test_notebook_fixture(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        def test_db_uri(notebook):
            assert notebook.store.db_uri == "sqlite:///:memory:"
            assert notebook.data == {}
            assert notebook.outcome.name == "not_reported"
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest(
        "--experiments-database=sqlite:///:memory:", "-v"
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_db_uri PASSED*",
        ]
    )

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_help_message(testdir):
    """Ensure that our options appear in `pytest --help`"""
    result = testdir.runpytest(
        "--help",
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "experiments:",
            "*--experiments-database*",
        ]
    )

    assert result.ret == 0


def test_experiment_mark(testdir):
    """Ensure that pytest has picked up our marker"""
    result = testdir.runpytest("--markers")

    result.stdout.fnmatch_lines(
        ["@pytest.mark.experiment: mark a test as an experiment"]
    )

    assert result.ret == 0


def test_experiment_database(testdir):
    """Test that the notebook persists data in the database."""

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        def test_experiment_record(notebook):
            notebook.record(
                hello='world',
                number=5.0,
            )
            assert notebook.store.db_uri == "sqlite:///experiments.db"
            assert notebook.data == {'hello': 'world', 'number': 5.0}
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_experiment_record PASSED*",
        ]
    )

    # the database was created
    db_path = testdir.tmpdir / "experiments.db"
    assert db_path.exists() is True

    store = StorageManager(f"sqlite:///{db_path}")
    experiments = store.get_all_experiments()
    assert len(experiments) == 1
    exp = experiments[0]
    assert exp.name == "test_experiment_database.py::test_experiment_record"
    assert exp.data == {"hello": "world", "number": 5.0}
    assert exp.outcome == "passed"
    assert exp.parameters == {}

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_experiment_parameters(testdir):
    """Test that the notebook persists data in the database."""

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        import pytest

        @pytest.fixture
        def zero():
            return 0


        @pytest.mark.parametrize("a", [1, 2, 3])
        def test_experiment_store_parameters(notebook, zero, a):
            notebook.record(
                hello='world',
                number=5.0,
            )
            assert True
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.re_match_lines(
        [
            r".*::test_experiment_store_parameters\[1\] PASSED.*",
        ]
    )

    # the database was created
    db_path = testdir.tmpdir / "experiments.db"
    assert db_path.exists() is True

    store = StorageManager(f"sqlite:///{db_path}")
    experiments = store.get_all_experiments()
    assert len(experiments) == 3
    for i, exp in enumerate(experiments):
        a = i + 1
        assert exp.name == (
            "test_experiment_parameters.py"
            f"::test_experiment_store_parameters[{a}]"
        )
        assert exp.data == {"hello": "world", "number": 5.0}
        assert exp.outcome == "passed"
        assert exp.parameters == {"zero": 0, "a": a}

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

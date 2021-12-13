import pytest
from my_algorithm import my_implementation


@pytest.mark.experiment
@pytest.mark.parametrize("x", list(range(-4, 4)))
def test_my_algorithm(notebook, x):
    """Run numerical experiments of ``my_implementation`` against some input.

    ``my_implementation`` represents a numerical method we are developing. For
    the sake of example, it simply computes the square of the input.

    Here is what's happening line by line:

    ``@pytest.mark.experiment``
        [optional] `mark`_ this test as an
        experiment. This does nothing on its own, but will make it easy
        to separate our experiments from other tests.

    ``@pytest.mark.parametrize(...``
        Generate some input.
        ``pytest-experiments`` automatically records the input to the
        experiment function so it's best practice to use pytest `fixtures`_
        and `parameters`_ to set up the input data. The experiment will run
        once for each value we specify.

    ``def test_my_algorithm(notebook, x):``
        Define the experiment.
        Since we will use pytest to execute our experiments, we **must** prefix
        the experiment name with ``test_``. We also will need to bring in the
        ``notebook`` fixture, which does all of the heavy lifting behind the
        scenes. Lastly, ``x`` is the parameter we defined in the previous line.

    ``y = my_implementation(x)``
        We call our implementation on the input and store the result in a
        local variable ``y``.

    ``assert y >= 0``
        We know that regardless of what ``x`` is, ``y``
        should never be negative. If it is, our code is wrong and our
        experiment should fail. It is important to have some basic validity
        checks in our experiments.

    ``notebook.record(result=y)``
        Tell the notebook to record the value of ``y`` under the key "y". Note
        that the values **must** be JSON-serializable. See the documentation
        for details but as a rule of thumb, this includes most python built-in
        datatypes.


    .. _`fixtures`: https://docs.pytest.org/en/latest/explanation/fixtures.html
    .. _`parameters`: https://docs.pytest.org/en/6.2.x/parametrize.html#parametrize-basics  # noqa
    .. _`mark`: https://docs.pytest.org/en/6.2.x/example/markers.html
    """
    y = my_implementation(x)
    assert y >= 0
    notebook.record(y=y)

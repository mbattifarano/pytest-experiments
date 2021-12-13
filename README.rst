==================
pytest-experiments
==================

.. image:: https://img.shields.io/pypi/v/pytest-experiments.svg
    :target: https://pypi.org/project/pytest-experiments
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-experiments.svg
    :target: https://pypi.org/project/pytest-experiments
    :alt: Python versions

.. image:: https://app.travis-ci.com/mbattifarano/pytest-experiments.svg?branch=main
    :target: https://app.travis-ci.com/mbattifarano/pytest-experiments 
    :alt: See Build Status on travis

.. image:: https://readthedocs.org/projects/pytest-experiments/badge/?version=latest
    :target: https://pytest-experiments.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

A pytest plugin to help developers of research-oriented software projects keep track of the results of their numerical experiments.

----


What it does
------------

``pytest-experiments`` allows **research-oriented programmers** to easily
persist data about **numerical experiments** so that they can **track
metrics over time**.

1. Know **what** experiments you've run, **when** you ran them, its
   **inputs** and its **results** over time and project development.
2. **Review and compare** experiments over time to ensure that
   continued development is improving your results.


How it works
------------

An **experiment** is a python function that runs your method or algorithm
against some input and reports one or more metrics of interest. 

Experiments are basically `unit tests`_ of numerical methods. Like unit tests
we provide a function or method under test with some input and assert that its 
output conforms to some concrete expectations. Unlike unit tests, the method 
under test produces some metrics which we are interested in but for which
concrete expectations do not exist. We store these metrics, along with some
metadata in a database so that we can track our results over time.

We use ``pytest`` to collect and execute our experiments. This plugin offers
a ``notebook`` `fixture`_ to facilitate recording your experiments. Here is 
a very simple example experiment:

.. code-block:: python
    
    import pytest
    from my_numerical_method_package import (
        my_implementation,  # your numerical method
        result_is_valid,    # returns True iff the result is well-formed
        performance_metric, # the performance metric we care about
    )

    @pytest.mark.experiment  # [optional] mark this test as an experiment
    @pytest.mark.parameterize("x", [1, 2, 3])  # The inputs; we will run this experiment for x=1, x=2, and x=3
    def test_my_numerical_method(notebook, x):  # Request the notebook fixture
        result = my_implementation(x)
        assert result_is_valid(result)  # our concrete expectations about the result
        notebook.record(performance=performance_metric(result))  # record the performance

At the end of the test the notebook fixture will save experiment metadata, the
inputs, and whatever was passed to ``notebook.record`` to a database. By default,
this database will be a sqlite database called ``experiments.db``.

A machine learning example
^^^^^^^^^^^^^^^^^^^^^^^^^^

For example, suppose we are building a machine learning classifier. The method
under test would be our model, the input would be train and validation
datasets and any hyper-parameters of our methods. The model is initialized 
with the hyper-parameters, trained on the training data, and the output is the
predictions on the validation set. 

We want the model to return probabilities, so we have a concrete expectation
that the predictions should all be between 0 and 1. If any are not, our code 
is wrong and the experiment should fail.

However, we are not only interested in returning probabilities, we also want
our model to return good predictions (e.g. the predictions have high accuracy
and high fairness). We might have some conrete expectations about these metrics:
for example we may wish to reject any result that has metrics strictly worse
than some baseline, but it is not easy or meaningful to specify a criterion
based on the accuracy and fairness values for when we should stop developing
our model. In fact, the metrics collected during the experiment may inform
subsequent development.

See the ``demo`` directory for a detailed example-based walkthrough.


Installation
------------

You can install "pytest-experiments" via `pip`_ from `PyPI`_::

    $ pip install pytest-experiments


Contributing
------------

Contributions are very welcome. This project uses `poetry`_ for packaging.

To get set up simply clone the repo and run

::

    poetry install
    poetry run pre-commit install

The first command will install the package along with all development dependencies
in a virtual environment. The second command will install the pre-commit hook which
will automatically format source files with `black`_.


Tests can be run with ``pytest``

Please document any code added with docstrings. New modules can be auto-documented by 
running::

    sphinx-apidoc -e -o docs/source src/pytest_experiments

Documentation can be compiled (for example to html with ``make``)::

    cd docs/
    make html


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-experiments" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.


Acknowledgements
----------------

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/mbattifarano/pytest-experiments/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`black`: https://black.readthedocs.io/en/stable/
.. _`unit tests`: https://en.wikipedia.org/wiki/Unit_testing
.. _`fixture`: https://docs.pytest.org/en/latest/explanation/fixtures.html
.. _`poetry`: https://python-poetry.org/
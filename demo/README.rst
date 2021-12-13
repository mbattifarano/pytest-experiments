Basic Example
-------------

The code in this directory contains a very simple working example of the
features of ``pytest-experiments``.

To run this example:

1. Open terminal and change directory into the ``demo`` directory.
2. Ensure that ``pytest-experiments`` has been installed.
3. Run ``pytest`` at the command line.

After running ``pytest``, you should see some output to terminal that ends
with:

::

    test_algorithm.py ........                                              [100%]

    ============================== 8 passed in 0.25s ==============================

Even though we have only defined one experiment, the experiment is run once for *each*
value of the input, ``x``. Since we gave it 8 values, the experiment is run 8 times.

You should now see a file in this directory called ``experiments.db`` this is a sqlite
database containing the results of our experiments. It is automatically created and will
be automatically updated with new results. You can specify a different database with the
``--experiments-database`` option to pytest like so:

::

    pytest --experiments-database sqlite::///results.db

Let's take a look at the database. You may use any tool that interfaces with 
sqlite. In the database you will find a table called ``experiments`` with 8 rows:

+----+----------------------------+----------------------------+-----------------------------------------------+---------+------------+----------+
| id |         start_time         |          end_time          |                      name                     | outcome | parameters |   data   |
+====+============================+============================+===============================================+=========+============+==========+
| 1  | 2021-12-13 14:11:36.632226 | 2021-12-13 14:11:36.634156 | demo/test_algorithm.py::test_my_algorithm[-4] | passed  | {"x": -4}  | {"y": 0} |
+----+----------------------------+----------------------------+-----------------------------------------------+---------+------------+----------+
| 2  | 2021-12-13 14:11:36.652584 | 2021-12-13 14:11:36.654346 | demo/test_algorithm.py::test_my_algorithm[-3] | passed  | {"x": -3}  | {"y": 0} |
+----+----------------------------+----------------------------+-----------------------------------------------+---------+------------+----------+
| 3  | 2021-12-13 14:11:36.671212 | 2021-12-13 14:11:36.672924 | demo/test_algorithm.py::test_my_algorithm[-2] | passed  | {"x": -2}  | {"y": 0} |
+----+----------------------------+----------------------------+-----------------------------------------------+---------+------------+----------+
| 4  | 2021-12-13 14:11:36.690071 | 2021-12-13 14:11:36.692138 | demo/test_algorithm.py::test_my_algorithm[-1] | passed  | {"x": -1}  | {"y": 0} |
+----+----------------------------+----------------------------+-----------------------------------------------+---------+------------+----------+
| 5  | 2021-12-13 14:11:36.709403 | 2021-12-13 14:11:36.711488 | demo/test_algorithm.py::test_my_algorithm[0]  | passed  | {"x": 0}   | {"y": 0} |
+----+----------------------------+----------------------------+-----------------------------------------------+---------+------------+----------+
| 6  | 2021-12-13 14:11:36.727766 | 2021-12-13 14:11:36.729193 | demo/test_algorithm.py::test_my_algorithm[1]  | passed  | {"x": 1}   | {"y": 0} |
+----+----------------------------+----------------------------+-----------------------------------------------+---------+------------+----------+
| 7  | 2021-12-13 14:11:36.745785 | 2021-12-13 14:11:36.747479 | demo/test_algorithm.py::test_my_algorithm[2]  | passed  | {"x": 2}   | {"y": 0} |
+----+----------------------------+----------------------------+-----------------------------------------------+---------+------------+----------+
| 8  | 2021-12-13 14:11:36.764671 | 2021-12-13 14:11:36.766846 | demo/test_algorithm.py::test_my_algorithm[3]  | passed  | {"x": 3}   | {"y": 0} |
+----+----------------------------+----------------------------+-----------------------------------------------+---------+------------+----------+
| 9  | 2021-12-13 14:13:27.304881 | 2021-12-13 14:13:27.306669 | demo/test_algorithm.py::test_my_algorithm[-4] | passed  | {"x": -4}  | {"y": 0} |
+----+----------------------------+----------------------------+-----------------------------------------------+---------+------------+----------+

In order, the fields are:

id
    A unique id for the experiment run.

start_time, end_time
    The start and end time of the experiment as a UTC timestamp.

name
    The fully qualified name of the experiment including the file, the name of
    the test and the value of any parameters

outcome
    The outcome of the test, one of: passed, failed, skipped

parameters
    The value of the inputs to the experiment.

data
    The data recorded (via ``notebook.record``) during the experiment.

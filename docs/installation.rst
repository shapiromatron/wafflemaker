.. highlight:: shell

============
Installation
============

To install Wafflemaker, run this command in your terminal:

.. code-block:: console

    $ pip install wafflemaker

This is the preferred method to install Wafflemaker, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


========================
Development installation
========================

To install for development:

.. code-block:: console

    git clone https://github.com/shapiromatron/wafflemaker
    cd wafflemaker
    pip install -e .
    pip install -e .[test]

To run tests:

.. code-block:: console

    cd wafflemaker
    py.test

Image comparisons from matplotlib use the excellent `pytest-mpl`_ library. To
create new baseline images for comparison:

.. code-block:: console

    py.test --mpl-generate-path=tests/baseline

Please submit tests with new feature requests.

.. _`pytest-mpl`: https://pypi.python.org/pypi/pytest-mpl

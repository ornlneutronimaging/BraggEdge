Installation
============

Requirements
------------

- Python 3.11 or 3.12
- numpy >= 1.24
- pandas >= 2.0

Install from PyPI
-----------------

The easiest way to install neutronbraggedge is via pip:

.. code-block:: bash

    pip install neutronbraggedge

Install from Source
-------------------

To install from source for development:

.. code-block:: bash

    git clone https://github.com/ornlneutronimaging/BraggEdge.git
    cd BraggEdge
    pip install -e .

Using Pixi (Recommended for Development)
----------------------------------------

We use `Pixi <https://pixi.sh/>`_ for environment management:

.. code-block:: bash

    git clone https://github.com/ornlneutronimaging/BraggEdge.git
    cd BraggEdge
    pixi install
    pixi run test  # verify installation

Verify Installation
-------------------

After installation, verify it works:

.. code-block:: python

    >>> from neutronbraggedge.braggedge import BraggEdge
    >>> handler = BraggEdge(material='Fe', number_of_bragg_edges=4)
    >>> print(handler.bragg_edges['Fe'])
    [4.0537, 2.8664, 2.3404, 2.0269]

Installation
============

FreshForge ``0.1.0a5`` is available from PyPI as an alpha package:

.. code-block:: bash

   python -m pip install freshforge==0.1.0a5

For source-checkout development, use a repo-local virtual environment and an
editable install.

Linux and macOS
---------------

.. code-block:: bash

   python -m venv .venv
   . .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -e .[dev]

Windows PowerShell
------------------

.. code-block:: powershell

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -e .[dev]

Smoke Check
-----------

.. code-block:: bash

   freshforge --version
   freshforge info
   freshforge providers
   freshforge run --help

Alpha Boundary
--------------

FreshForge ``0.1.0a5`` validates, inspects, plans, and can run workflow specs
through provider-owned ``run_node(...)`` hooks with optional run namespaces,
compact run summaries, and generic run matrices. It does not install real
FEMIC, FHOPS, ws3, Modelwright, Nemora, GIS, optimization, or spreadsheet
runtimes.

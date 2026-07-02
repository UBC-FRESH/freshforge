Installation
============

FreshForge ``0.1.0a4`` is available as a GitHub prerelease artifact. It is not
yet published to PyPI. Install it from a local checkout or from a downloaded
wheel artifact.

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

FreshForge ``0.1.0a4`` validates, inspects, plans, and can run workflow specs
through provider-owned ``run_node(...)`` hooks with optional run namespaces,
compact run summaries, and generic run matrices. It does not install real
FEMIC, FHOPS, ws3, Modelwright, Nemora, GIS, optimization, or spreadsheet
runtimes.

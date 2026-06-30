Installation
============

FreshForge is not yet published to PyPI. Install it from a local checkout during
Phase 0 development.

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

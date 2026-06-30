Development Workflow
====================

FreshForge follows the UBC-FRESH phase/task/subtask workflow.

Local Checks
------------

.. code-block:: bash

   python -m ruff check .
   python -m pytest
   sphinx-build -b html docs _build/html -W
   python -m build
   twine check dist/*

Development Rules
-----------------

* Keep ``ROADMAP.md`` as the current plan and issue tracker map.
* Keep ``CHANGE_LOG.md`` as the append-only project narrative.
* Use ``planning/`` for focused design notes and decisions.
* Map one active roadmap phase to one GitHub parent issue and feature branch.
* Map roadmap tasks to child issues linked from the parent issue.
* Keep issue bodies, roadmap checklists, changelog entries, and PR descriptions
  synchronized.
* Keep private data, raw transcripts, generated local outputs, and
  machine-specific paths out of tracked files.

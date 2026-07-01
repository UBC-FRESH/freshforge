Release Checklist
=================

FreshForge ``0.1.0a2`` is released as a GitHub prerelease with checked package
artifacts. It is not published to PyPI.

Local Verification
------------------

Run the acceptance checks from a clean checkout:

.. code-block:: bash

   python -m pip install -e .[dev]
   python -m ruff check .
   python -m pytest
   sphinx-build -b html docs _build/html -W
   python -m build
   twine check dist/*

Inspect the release artifact contract:

* the source distribution includes tracked files under ``examples/``;
* the wheel metadata includes the ``freshforge.providers`` entry-point group;
* ``freshforge providers --json`` lists ``freshforge.example`` and
  ``freshforge.fixture``;
* ``freshforge plan examples/ecosystem_adapter_workflow.yaml --json`` resolves
  both providers.
* ``freshforge --version`` reports ``freshforge 0.1.0a2``.
* ``freshforge run --help`` is available.

Tag And Release
---------------

The release tag is ``v0.1.0a2`` and the GitHub release title is
``FreshForge 0.1.0a2``.

Closeout sequence:

1. Merge the Phase 9 pull request after CI passes.
2. Verify the Docs workflow deploys successfully on ``main``.
3. Verify the live docs root, examples page, and this release checklist page.
4. Create and push tag ``v0.1.0a2``.
5. Wait for the release-artifact workflow to pass for the tag.
6. Download or otherwise inspect the workflow-built artifacts.
7. Create the GitHub prerelease and attach the checked artifacts.

Deferred Publication
--------------------

PyPI publication is explicitly deferred. A future release phase should decide
whether to use trusted publishing, API-token publishing, or a separate manual
publication process.

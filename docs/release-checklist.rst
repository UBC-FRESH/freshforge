Release Checklist
=================

FreshForge ``0.1.0a5`` is released as the first PyPI alpha package and as a
GitHub prerelease with checked package artifacts.

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
* ``freshforge --version`` reports ``freshforge 0.1.0a5``.
* ``freshforge run --help`` is available.
* ``freshforge run`` supports ``--namespace`` and JSON summaries.
* ``freshforge matrix --help`` is available.
* ``freshforge matrix plan examples/run_matrix.yaml --json`` succeeds.

Tag And Release
---------------

The release tag is ``v0.1.0a5`` and the GitHub release title is
``FreshForge 0.1.0a5``.

Closeout sequence:

1. Merge the Phase 12 pull request after CI passes.
2. Verify the Docs workflow deploys successfully on ``main``.
3. Verify the live docs root, examples page, and this release checklist page.
4. Confirm the PyPI trusted publisher is configured for project
   ``freshforge`` with repository ``UBC-FRESH/freshforge``, workflow
   ``release.yml``, and environment ``pypi``.
5. Create and push tag ``v0.1.0a5``.
6. Wait for the release-artifact workflow to pass for the tag and publish to
   PyPI.
7. Download or otherwise inspect the workflow-built artifacts.
8. Create the GitHub prerelease and attach the checked artifacts.
9. Verify a clean PyPI install reports ``freshforge 0.1.0a5``.

PyPI Publication
----------------

PyPI publication uses GitHub trusted publishing through the release workflow's
``pypi`` environment. Do not push the release tag until the corresponding PyPI
publisher has been configured by a maintainer.

Governance
==========

FreshForge starts with the stricter FRESH agent and issue workflow used by recent
package projects.

Key Surfaces
------------

``AGENTS.md``
   Agent contract, repository rules, issue body standards, and verification
   expectations.

``ROADMAP.md``
   Current phase/task plan and issue tracker map.

``CHANGE_LOG.md``
   Append-only narrative of completed work.

``planning/``
   Focused design notes, research records, and durable decisions that are too
   detailed for the roadmap.

Issue Hierarchy
---------------

FreshForge uses at most three issue levels:

* phase parent issue;
* task child issue;
* optional implementation-subtask issue for large subtasks.

Lightweight implementation steps should stay as checklist items inside the child
issue body.

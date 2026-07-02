# Post-v0.1.0a5 Downstream Ergonomics Watchlist

FreshForge `v0.1.0a5` is the first PyPI alpha and already includes validation, inspection, planning,
serial local runs, run namespaces, compact summaries, and matrices.

The next FreshForge core phase should not add features speculatively. Modelwright and FABLE
Pyculator now have enough workflow machinery to expose real friction.

## Watchlist Sources

- Modelwright Phase 38: matrix generated-model evidence aggregation.
- FABLE Pyculator Phase 25: FABLE benchmark matrix evidence cookbook.
- FEMIC FreshForge compatibility and matrix/preflight workflow work.

## Possible Future Ergonomics

- Clearer matrix summary shapes if downstream packages need less parsing.
- Better CLI affordances for compact summary output.
- Small provider-result conventions if multiple domain packages converge on the same pattern.

## Boundaries

- No domain semantics in FreshForge core.
- No production scheduling, caching, checkpoints, retries, remotes, or parallel execution without a
  separately scoped phase.
- No Phase 13 child issues until concrete downstream evidence exists.

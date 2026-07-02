# Return Decision

Decision: EXPLORATORY_SUPERSEDED_BY_STEP09

Reason: sentence-embedding retrieval reached the Step 07 mixed-method 80% threshold, but Step 09 method-matched validation later failed.

Selected setting: `sentence-transformers/LaBSE` / `csls` / `kbh->nhg`.

Test chrF++: `64.434500`.

Required chrF++: `49.567925`.

Mixed-method ratio: `1.039939`.

Step 09 method-matched LaBSE+CSLS ratio: `0.567179`.

## Return Instruction

Do not merge this branch as top-tier translation evidence. Return to Step 07 only after a method-matched branch is selected on dev and evaluated on a fresh held-out test.

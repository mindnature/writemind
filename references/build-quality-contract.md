# Build Quality Contract

`build-skill` is part of the product, not a formatting utility. A generated Writer Advisor must not lose the evidence and coaching structure that made a heuristic useful.

For every included heuristic, preserve when available:

- decision_structure
- rule
- operational_actions
- diagnostic_questions
- boundary_conditions
- failure_signals
- writer_added_delta
- supporting Episodes / provenance
- composition audit
- lens eligibility

CI tests must fail if the builder regresses to emitting only a heuristic title and one-line rule.

Generated skills may add presentation text, but they must not silently invent diagnostic questions or revision actions that are absent from the heuristic data. If a useful coaching element exists only in a hand-written generated Skill, move it upstream into the heuristic JSON or another traceable source before relying on it.

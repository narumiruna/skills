# Architecture Assessment

Use these concepts to compare the current structure with a concrete alternative. They are evaluation tools, not a requirement to introduce more types or layers.

## Vocabulary

- **Module:** code that owns a coherent capability behind an interface. It may be a function, class, package, process, or vertical slice.
- **Interface:** everything a caller must know to use a module correctly: operations, inputs, invariants, sequencing, errors, side effects, configuration, and performance constraints.
- **Implementation:** behavior hidden behind the interface.
- **Depth:** useful behavior provided per unit of interface burden. A deep module hides meaningful policy behind a smaller stable interface; a shallow module exposes nearly as much complexity as it contains.
- **Seam:** a justified point where behavior or dependencies can vary without editing the caller.
- **Adapter:** an implementation that translates across a seam. An adapter should absorb a real integration difference rather than merely rename calls.
- **Ownership:** the one place responsible for a policy, invariant, state transition, or lifecycle.
- **Locality:** related knowledge, change, failure, and verification stay together.
- **Leverage:** one implementation or policy benefits multiple callers and tests through a stable interface.

## Candidate Tests

A strong candidate has direct evidence for several of these:

- One domain behavior requires coordinated edits across unrelated callers.
- Multiple callers repeat ordering, validation, recovery, or state-transition policy.
- State is written or invalidated by several modules without one lifecycle owner.
- A dependency's details leak through multiple interfaces.
- Tests must reproduce caller orchestration or reach past the intended interface.
- Recent changes repeatedly cross the same files or seams for one conceptual change.
- The proposed owner can enforce an invariant once and expose a smaller contract.

Apply the **deletion test** to current and proposed modules: if deletion merely copies or moves the same complexity into callers, the module provides little depth. A useful module makes deletion disperse policy, knowledge, or verification that was legitimately concentrated.

## Evidence and Ranking

For each candidate, capture:

1. source and test paths demonstrating the friction;
2. the present owner, callers, interface burden, and dependency direction;
3. the proposed owner and seam;
4. which caller knowledge or repeated coordination disappears;
5. behavior and contracts that must remain stable;
6. migration and rollback shape;
7. verification that would prove the improvement; and
8. confidence, including contrary evidence.

Rank candidates by expected locality and leverage, frequency of future change, migration risk, and confidence. Prefer a smaller high-confidence change over a broad redesign supported only by taste.

## Rejection Signals

Reject or downgrade a candidate when it:

- adds a pass-through interface, manager, facade, or wrapper without absorbing policy;
- introduces a seam for a hypothetical variation with no ownership, test, deployment, or integration need;
- replaces direct readable code with indirection while preserving the same caller burden;
- optimizes naming, folder symmetry, line count, or architectural fashion without runtime or change evidence;
- centralizes unrelated behavior into a large module with a wide interface;
- hides transactions, retries, authorization, latency, or failure semantics callers still need to reason about;
- conflicts with an ADR without new evidence that its trade-off has changed; or
- requires a broad migration before any independently verifiable benefit appears.

A proposed deep module is not automatically good. Verify that its interface is smaller in required caller knowledge, its ownership is coherent, dependencies still point in a sustainable direction, and tests exercise meaningful behavior through the same contract callers use.

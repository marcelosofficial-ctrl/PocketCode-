# CHECKPOINT — 2026-11-12

Unit 1 complete: grant-event envelope and relay contract.
Branch: pocketcode-ai-workflow-director-research-2026-10-28
Parent before unit: 1ec716a75ee6a05ebbe4d8f6a2eb570837ea4f13
New document: AI_COLLAB/GRANT_EVENT_ENVELOPE_AND_RELAY_CONTRACT_20261112.md
Scope: documentation/spec only; no application/test changes; P39 implementation/adapter gate remains CLOSED.
Contract version: grant-event-envelope/v1 (not a canonical LOOP/CASE/D ID).

Verified source defects:
- aggregate_version increments on equal progress without matching event/outbox.
- consumer trusts supplied first-delivery digest and does not validate complete authority/scope.
- grant-event delivery marker has no lease, relay fence or stale-ack protection.
- initial grant/event/outbox atomicity is only a synchronous in-memory model; no durable proof.
- P40 suite did not include parity/first-delivery-authentication/relay-fencing adversarial tests.

Contract decisions:
- Every semantic aggregate transition commits exactly one immutable event/outbox row with its version; no-op does not advance version.
- Canonical data bytes are hashed; producer authentication is separate; CloudEvents source+id is identity only.
- Business transition fence and relay fence are separate.
- At-least-once publication with immutable identity, ordered application, durable inbox and stale-ack rejection; no exactly-once claim.
- Database, transport, key system, signature algorithm and runtime remain unselected.

Research sources opened 2026-11-12: AWS transactional outbox, Debezium Outbox Event Router, CloudEvents core, NATS JetStream ack/consumer docs, RFC 8785 JCS, RFC 9421 HTTP Message Signatures. Pattern reuse only; no code/dependencies copied. See source register in the contract.

Housekeeping reconciled: INDEX now includes name collision, provider cache/context and Claude red-team documents; AI_LANES_AND_DISPATCH remains indexed once. P39 and P40 rows compacted. Name-clearance is a non-blocking open item; do not rename or publish PoCo before clearance. Official Catrobat/Poco-project sources support product/search collision; alleged trademark specifics remain unverified.

Prior P40 evidence remains: run #59 / 43126974602 SUCCESS, exact checkout 319cffef121e327331aeaff59522ae279b112ecc; full scripts 266/266; lane 4 BLOCKED. Model-only, not adapter/CASE acceptance. Latest relevant CI is the same run; docs-only commit has no CI trigger.

Next unit: opaque-origin execution message protocol. Then storage/artifact recovery contract, followed by state/NEXT_TASK/name-collision housekeeping. Tests NOT RUN in this unit. CASE-04 remains INCOMPLETE / timed_out.

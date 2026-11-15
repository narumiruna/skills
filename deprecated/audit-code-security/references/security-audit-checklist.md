# Security audit checklist

Use this as a prompt library, not a mechanical checklist. Select only categories connected to the reachable attack surface and requested scope. Absence of a finding in selected checks is not proof that the target is secure.

## Threat frame

- Name the protected assets and intended confidentiality, integrity, availability, authenticity, and tenant-isolation properties.
- State realistic attacker capabilities: anonymous, authenticated, privileged, same-tenant, cross-tenant, local process, compromised dependency, or control of an upstream response.
- Enumerate reachable entry points, including HTTP and RPC handlers, queues, webhooks, file imports, CLI arguments, environment and configuration, database records, browser messages, and dependency callbacks.
- Mark trust boundaries, privilege changes, parsers, authorization decisions, persistence, side effects, and outbound connections.
- Follow sensitive data flows through logs, errors, metrics, caches, queues, backups, exports, and deletion paths—not only the primary response.

## Evidence and reachability

For each candidate, trace the complete source-to-sink path:

1. What input, identity, state, package, or configuration can the attacker influence?
2. What parsing, canonicalization, validation, authorization, or escaping occurs, and in what order?
3. Can an equivalent encoding, alternate route, stale state, race, retry, or direct object reference bypass the guard?
4. Which sink or security decision is reached, under what attack prerequisites, and with what affected asset and impact?
5. Does a test, safe local reproduction, specification, or framework contract confirm the claim?

Apply confirmation criteria by alert type. For data-flow alerts, reject the alert as a false positive or report it as unverified when the source is not attacker-controlled, the sink is unreachable, a real guard blocks the path, or the claimed consequence does not follow. For dependency alerts, require the affected version and feature in a relevant runtime, build, CI, or release execution path. For secret alerts, determine whether credential-like material or sensitive data crosses its intended trust boundary without reproducing or using it. For configuration alerts, verify that the reported setting is actually executed or deployed. Do not require attacker-controlled input or runtime shipping when direct exposure or a build, CI, or release path is the security issue; do not dismiss a data-flow alert merely because a nearby layer appears to validate without checking actual ordering and equivalent routes.

## Identity, sessions, and authorization

- Authentication confusion across API keys, cookies, bearer tokens, proxies, callbacks, account linking, password reset, and multi-factor recovery
- Session fixation, replay, rotation, revocation, expiry, cookie attributes, CSRF, redirect handling, and state or nonce binding
- Function-level and object-level authorization on every route, job, export, websocket, and indirect lookup
- Tenant, owner, organization, role, and scope checks performed against authoritative current state rather than user-supplied identifiers or stale caches
- Default, error, retry, bulk, administrative, and migration paths that accidentally fail open or bypass policy

## Injection, parsing, and output boundaries

- SQL, query-language, template, HTML, header, log, terminal, shell, argument, expression, and command injection at the final sink
- Unsafe deserialization, schema confusion, polymorphic types, parser differentials, request smuggling, and unbounded recursive or compressed input
- Encoding and canonicalization order across Unicode, URL, path, hostname, delimiter, quoting, escaping, and double-decoding variants
- Untrusted content crossing into prompts, markup, browser DOM, terminals, generated code, or structured protocols without preserving provenance and framing
- Output encoding matched to the actual consumer rather than assumed safe from an earlier representation

## Files, processes, and network

- Absolute paths, `..`, symlink escape or swap, archive extraction, temporary files, permissions, ownership, and time-of-check/time-of-use races
- Process execution with structured arguments, controlled executable resolution, minimal environment inheritance, bounded output, timeout, cancellation, and child cleanup
- SSRF, open redirects, hostname and IP validation, alternate address forms, DNS rebinding, redirect revalidation, cloud metadata access, and egress policy
- Protocol downgrade, certificate validation, webhook authenticity, replay, message ordering, partial responses, retry classification, and idempotency

## Secrets, sensitive data, and cryptography

- Credentials or personal data in source, history, fixtures, build artifacts, command arguments, logs, traces, metrics, errors, URLs, caches, or exports
- Data minimization, retention, deletion, access logging, redaction, backup handling, and least-privilege access
- Standard cryptographic primitives and protocols used with suitable randomness, nonces, key separation, comparison, rotation, storage, and failure behavior
- Encryption that authenticates data and binds the necessary context; signatures or tokens that verify algorithm, issuer, audience, purpose, and expiry
- Secret scanners handled without reproducing secret values in commands, logs, captured output, or the final report

## Availability and abuse resistance

- Bounded request bodies, collections, recursion, regex work, decompression, parsing, fan-out, concurrency, queues, retries, and retained state
- Rate, quota, cost, and amplification controls applied to the correct actor, tenant, route, and expensive downstream operation
- Lock, transaction, cancellation, timeout, and cleanup behavior under partial failure or attacker-controlled ordering
- Duplicate submission, replay, race, inventory or balance invariants, workflow skipping, and abuse of valid functionality

## Dependencies, supply chain, configuration, and deployment

- Direct and transitive dependency findings verified against the resolved version, vulnerable feature, and relevant runtime, build, CI, or release execution path
- Lockfile integrity, source and registry provenance, install or build scripts, generated artifacts, update policy, and compromised maintainer risk where supported by evidence
- CI and release token permissions, untrusted pull-request execution, artifact provenance, cache poisoning, secret exposure, and deployment approval boundaries
- Debug or development modes, default credentials, permissive CORS, public binding, proxy trust, unsafe feature flags, exposed management endpoints, and weak production defaults
- Infrastructure and runtime controls that materially change exploitability; do not assume an undocumented external control exists

## Tool evidence

- Prefer repository-configured commands and already available scanners; do not install a preferred tool just to complete the checklist.
- Record what was actually scanned, relevant exclusions, tool and ruleset versions when available, network or registry freshness, and command failures.
- For SAST, inspect the reported source, sanitizers, control flow, and sink. For dependency tools, verify the resolved version, affected feature, and relevant runtime, build, CI, or release path. For secret tools, determine exposure without disclosing or using the value. For configuration tools, compare findings with the executed or deployed path rather than templates alone.
- Treat passing tools as evidence only for the rules, files, dependency data, and configuration they covered. Name meaningful gaps and unavailable checks.

## Classification check

Before reporting a confirmed finding, verify that the attack prerequisites are plausible, the affected assets and impact are concrete, file and line evidence identifies the path, remediation addresses the shared boundary, and confidence reflects any unverified premise. Put useful hardening ideas without a demonstrated violation under defense-in-depth rather than inflating the vulnerability list.

---
name: audit-code-security
description: Perform read-only security audits, vulnerability assessments, or threat-focused reviews of diffs, pull requests, code paths, or explicitly scoped repositories when security is the primary objective or acceptance criterion. Use review-code for ordinary review with baseline security coverage and harden-code-paths for fixing confirmed findings.
---

# Auditing Code Security

Treat audits, assessments, and diagnoses as read-only. An audit request does not authorize code changes, intrusive testing, credential use, or testing beyond the requested target.

## Scope and Threat Frame

1. Determine the exact target from the request and repository or pull-request context. For a branch or pull request, compare from the target branch's merge base rather than assuming a branch name. For a named code path, trace its directly relevant callers, data stores, and downstream sinks.
2. If no target is named, inspect `git status --short` and relevant staged, unstaged, and untracked changes. Ask for one target only when the current changes and request still do not identify a bounded scope. A repository-wide audit must be explicitly requested; never silently turn a focused request into an unbounded scan.
3. Infer the intended security properties from code, tests, documentation, deployment configuration, and surrounding contracts. Label material assumptions.
4. Identify the assets, attacker capabilities, entry points, trust boundaries, sensitive data flows, and security decisions reachable within scope.
5. Load [the security audit checklist](references/security-audit-checklist.md) and select only domains supported by that threat frame.

## Audit and Verify

1. Trace attacker-controlled identity and data from source to validation, normalization, authorization, storage, side effects, and final sink. Check both the permitted path and the nearest denied or malformed path.
2. Where reachable, assess authentication and session handling; authorization and tenant or object ownership; injection and unsafe parsing; file, process, and network boundaries; secrets and sensitive data; cryptographic use; resource exhaustion and abuse controls; dependencies and supply chain; and configuration or deployment exposure.
3. Prefer non-destructive SAST, dependency, secret, and configuration tools that the repository has already configured or the environment has already made available. Record the relevant command, version when available, target, and limitations. Do not install tools, modify lockfiles or configuration, or add generated scanner artifacts.
4. Treat scanner output as candidate evidence and apply alert-specific confirmation criteria. For data-flow alerts, confirm attacker influence, the full source-to-sink path, existing guards, and impact. For dependency alerts, confirm the affected version and feature in the relevant runtime, build, CI, or release path. For secret alerts, confirm that credential-like material or sensitive data crosses its intended trust boundary without reproducing or using it. For configuration alerts, compare the reported setting with the configuration actually executed or deployed. An alert without a relevant executed, deployed, or exposed path remains unverified.
5. Use only safe, bounded local checks to test a hypothesis. Do not probe external or live targets, run destructive or persistence-producing tests, use credentials, make purchases, or materially expand scope without exact authorization for the operation and target; stop and request that authorization when it is required. Prefer the minimum proof that establishes the issue without exposing secrets or weaponizing the result.
6. Stop after the requested surface, directly affected trust boundaries, focused tool evidence, and plausible high-impact paths have been examined. Record unavailable checks instead of substituting confidence.

## Findings

Lead with confirmed findings ordered by the repository scale:

- **Critical:** a reachable issue with severe compromise, broad unauthorized access, destructive impact, or secret exposure.
- **Major:** an exploitable security failure that should block release or merge but has narrower impact or stronger prerequisites.
- **Minor:** a real, bounded weakness with low impact that is still worth correcting.

For each finding, provide attack prerequisites, affected assets, file and line evidence, the source-to-sink or authorization path, impact, actionable remediation, and confidence. Keep scanner identifiers or standards mappings secondary to the concrete code evidence.

Separate defense-in-depth recommendations, unverified risks, unavailable checks, and uncovered scope from confirmed vulnerabilities. If no finding survives verification, say that no confirmed finding was found in the examined scope; do not claim the target is secure or the audit is complete.

## Confirmed-Finding Handoff

When the user also requests fixes, hand only confirmed findings to `harden-code-paths`. Preserve the original attack conditions in a failing regression check when practical, fix the shared trust boundary, and scan directly affected sibling paths for the same root cause. Then re-audit the fix diff and original attack path. Keep broader threat analysis and unverified alerts in this audit workflow rather than turning them into speculative code changes.

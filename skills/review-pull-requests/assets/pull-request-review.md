# Pull request review: {{ Repository }} #{{ Pull request number }}

## Goal

<!-- State why the pull request exists and what outcome it is meant to achieve. -->

## Bug reproduction (optional)

<!-- Include for bug fixes, even if reproduction could not run. Distinguish the PR's claims from direct observations. Use Reproduced, Not reproduced, or Not attempted for each revision. -->

- Environment: {{ Reproduction environment }}
- Commands and inputs: {{ Reproduction steps and fixtures }}
- Expected behavior: {{ Expected behavior }}
- Base: **{{ Base result }}** — {{ Base observation }}
- Head: **{{ Head result }}** — {{ Head observation }}
- Blocker: [Reproduction blocker]

## Root cause (optional)

<!-- Include when evidence supports a cause. Explain whether the change addresses the cause or only a symptom. Put uncertainty that affects the verdict under Risks or Open questions. -->

## Implementation approach (optional)

<!-- Include when the design or its tradeoffs help explain the change. -->

## Changes

<!-- Group changes by behavior or responsibility. Include relevant API, configuration, data, command, UI, documentation, generated-file, and dependency changes. -->

## Expected behavior (optional)

<!-- Include when a before-and-after comparison adds detail. Note what stays the same, including whether a refactor is intended to preserve behavior. -->

## Repository impact

<!-- Identify affected packages, callers, consumers, contracts, and workflows. Include release, deployment, operational, or maintenance effects when relevant. State explicitly if impact is limited. -->

## Findings

<!-- Repeat the block for each confirmed, independently actionable defect, highest severity first. Combine symptoms of one cause. If none exist, replace the block with "No confirmed findings." -->

### [{{ Severity }}] {{ Finding title }} — {{ File path }}:{{ Line number }}

- **Trigger:** {{ Input, state, or sequence that exposes the defect }}
- **Impact:** {{ Observable consequence and who or what is affected }}
- **Evidence:** {{ How the change causes or worsens the defect and why protections do not prevent it }}
- **Fix:** {{ Smallest practical fix }}

## Risks (optional)

<!-- Include only plausible, material concerns that are not yet confirmed. State why each matters, what evidence is missing, and how to verify it. -->

## Verification

- Base commit: `{{ Reviewed base commit }}`
- Head commit: `{{ Reviewed head commit }}`
- Merge base: `{{ Comparison merge base }}`

<!-- Distinguish CI results from commands you ran and their outcomes. Note useful test coverage, concrete gaps, and anything you did not inspect or run. -->

## What looks good (optional)

<!-- Include only unusually strong design, implementation, tests, or documentation. -->

## What looks bad (optional)

<!-- Include only evidence-backed limitations or tradeoffs that do not warrant a finding. Do not repeat Findings or Risks. -->

## Open questions (optional)

<!-- Include only merge-blocking questions that cannot be answered from the PR or repository. -->

## Verdict

**{{ Verdict label }}**

<!-- Explain the verdict in one or two sentences consistent with the findings, risks, and verification. -->

---
name: refine-uiux
description: Refine a specified existing web or app screen, flow, or terminal user interface (TUI) when the user wants to find and fix friction or compare ways to improve it. Walk through the main task, make small fixes backed by evidence, and show comparable previews when the user needs to choose an approach. Skip reviews that ask only for findings, requests to apply a known fix, and redesigns.
---

# Refine UI/UX

Improve the user's main task without redesigning the interface.

## Observe the Current Task

1. Use the requested interface or flow and its primary task.
   If the task is omitted, state what you assume the user is trying to do and proceed.
2. In a safe test environment, walk through the task from the same starting state using test data.
   For graphical interfaces, use desktop and mobile layouts where supported.
   For a TUI, use representative wide and narrow terminal sizes and exercise the relevant key sequences with a non-interactive test harness when available.
   Before editing, record the test data, screen sizes (columns × rows for a TUI), and baseline screenshots or terminal captures of the affected steps.
   If you cannot observe the task at all, report what blocked it and stop without editing.
3. Identify up to three problems, ordered by how much they interfere with the task.
   For each, name the step, describe what the user has to do or guess, and point to visible or interactive evidence.

## Decide Whether to Edit

- Recommend rather than implement changes when the cause is unclear or the fix requires a redesign, a change to the flow between screens, a permission change, or a change to how data is handled.
  If a layout or terminal size is unavailable, make a fix only if you can reproduce the problem and verify the fix without relying on it.
- Apply the smallest local fix directly when the cause and correction are clear, there is no meaningful choice, and the user did not ask for options.
- Present options when the user asks for them, viable approaches have meaningful tradeoffs, or you can recommend changes but cannot implement them.

## Present Options and Samples

1. Offer two or three distinct approaches to the same finding in a numbered list.
   For each, explain what changes, what gets easier for the user, and the main tradeoff.
   Recommend one and say why; if only one approach is viable, explain why instead of inventing alternatives.
2. When feasible, show comparable samples before asking for a choice.
   Use a standalone local preview or annotated mockup for a graphical interface, monospaced screen mockups for a TUI, or text examples when wording is the only difference.
   Keep the task step, sample data, and screen size the same across options.
   Label samples as proposals and keep them separate from product code and live actions.
3. Ask the user which option they want and wait before editing that finding.
   Keep options that exceed the current scope as recommendations unless the user explicitly authorizes the broader change.

## Make Small Fixes

- To address a selected finding, make the current state, next action, and consequences clear where the user needs them.
  Place warnings that affect a decision next to the relevant controls.
- Remove duplicate information or collapse secondary details by default only when doing so addresses a selected finding.
  Preserve distinct guidance and keep information needed for the task, a decision, or recovery easy to find.
- Reuse existing UI patterns and leave unrelated behavior and styling unchanged.
- If no finding qualifies for a fix now, report the findings or options and stop without editing product code.

## Verify and Report

1. Repeat the same task with the same test data, starting state, and available layouts or terminal sizes.
   Recheck each fix at the step where the problem occurred.
   Check keyboard operation, including focus order and visibility where applicable, and exercise affected error and empty states.
   For a TUI, check affected key bindings and look for clipped text or controls at the tested sizes.
   If a fix leaves the problem unresolved or introduces a regression, correct it within scope and recheck it, or undo only that fix and explain why.
2. Provide before-and-after screenshots or terminal captures at matching steps and sizes.
   If a capture or check is unavailable, report what is missing and why instead of implying it was verified.
3. Explain what the user now does or guesses less, which findings remain recommendations, and what you did not verify.
   Stop after reporting without expanding the scope.

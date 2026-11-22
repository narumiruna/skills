---
name: refine-uiux
description: Refine a specified existing web or app screen, flow, or terminal user interface (TUI) when the user wants to find and fix friction or compare ways to improve it. Walk through the main task, make small fixes backed by evidence, and show comparable previews when the user needs to choose an approach. Skip reviews that ask only for findings, requests to apply a known fix, and redesigns.
---

# Refine UI/UX

Improve the user's main task without redesigning the interface.

## Observe the Current Task

1. Identify the primary task for the requested interface or flow.
   If the user did not specify a task, state your assumption and proceed.
2. In a safe test environment, use test data and start each walkthrough from the same state.
   - For graphical interfaces, test desktop and mobile layouts where supported.
   - For a TUI, test representative wide and narrow terminal sizes.
     Use a non-interactive test harness to exercise relevant key sequences when one is available.
   - If you cannot observe the task at all, report the blocker and stop without editing.
   - Before editing, record the test data and screen sizes (columns × rows for a TUI).
     Capture the affected steps in screenshots or terminal output.
3. List up to three problems in order of impact on the task.
   For each, name the step, explain what the user has to do or guess, and cite what you saw or what happened during the interaction.

## Decide Whether to Edit

- If a layout or terminal size is unavailable, edit only if you can reproduce the problem and verify the fix without it.
- Recommend changes instead of implementing them if the cause is unclear or the fix requires a redesign or changes to navigation between screens, permissions, or data handling.
- Present options when the user asks for them, viable approaches involve meaningful tradeoffs, or you can recommend a change but cannot make it.
- Otherwise, apply the smallest local fix directly when the cause and correction are clear.

## Present Options and Samples

1. Give a numbered list of two or three distinct ways to address the same finding.
   For each, state the change, the user benefit, and the main tradeoff.
   Recommend one and explain why.
   If only one approach is viable, explain why rather than invent alternatives.
2. When feasible, show samples before asking the user to choose.
   - Use a standalone local preview or annotated mockup for a graphical interface, a monospaced mockup for a TUI, or text examples for wording-only changes.
   - Show the same task step, sample data, and screen size for each option.
   - Label samples as proposals and keep them separate from product code and live actions.
3. Ask the user to choose and wait for their answer before editing for that finding.
   Keep out-of-scope options as recommendations unless the user explicitly authorizes the broader change.

## Make Small Fixes

- If no finding qualifies for a fix now, report the findings or options and stop without editing product code.
- For selected findings, make the current state, next action, and consequences clear where the user needs them.
  Put warnings that affect a decision next to the relevant controls.
- Remove repeated information or collapse secondary details by default only if doing so addresses a selected finding.
  Preserve distinct guidance and keep information for the task, decisions, or recovery easy to find.
- Reuse existing UI patterns and leave unrelated behavior and styling unchanged.

## Verify and Report

1. Repeat the task with the same test data, starting state, and available layouts or terminal sizes.
   - Recheck each fix at the step where the problem occurred.
   - Test keyboard operation and any affected error or empty states.
     Check focus order and visibility where applicable.
   - For a TUI, check affected key bindings and look for clipped text or controls at the tested sizes.
   - If the problem persists or the fix introduces a regression, correct and recheck it within scope, or undo only that fix and explain why.
2. Report what the user now does or guesses less and which findings remain recommendations.
   Provide before-and-after screenshots or terminal captures at matching steps and sizes.
   List any unverified scenarios and explain why any capture or check was unavailable.
   Stop without expanding the scope.

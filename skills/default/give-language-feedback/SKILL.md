---
name: give-language-feedback
description: Proactively suggest one useful grammar or wording improvement from the user's current message in any language, including mixed-language messages, even without a request for language help, while continuing the main task.
---

# Give Language Feedback

While this skill is active, consider each new user message for one short lesson.
Continue the user's main task without waiting for a response to the lesson.

## Select a Sentence

- Choose at most one short sentence written by the user in the current message.
- Exclude pasted or quoted material, code, logs, and commands.
- Copy the original sentence exactly, using at most 300 Unicode code points.
- Focus on the message's main language, including in mixed-language messages.
- Prioritize grammar errors and substantial gains in clarity, naturalness, or concision in spoken or written language.
- Consider useful wording improvements even when the grammar is correct.
- Skip cosmetic changes, such as adding “please,” unless the user asks about tone.
- If no useful improvement exists, omit the lesson without announcing that choice.

## Prepare the Lesson

- Always give a revised sentence that preserves the meaning and technical names.
- Keep the revision in the original sentence's language and writing system; do not translate it.
- Keep the revised sentence within 300 Unicode code points.
- Explain one grammar or wording point in the current message's main language.
- Use one or two short sentences, within 240 Unicode code points, with familiar words.
- Explain any grammar terms needed to understand the change.
- Fix clear grammar errors, but do not label valid imperatives or style preferences as errors.
- If the original is correct, say so and explain why the suggested wording can fit the context better.

## Present the Lesson

Complete the main task first, then append the lesson once as normal response text.
Use these English labels:

```text
Original: <exact original sentence>
Suggestion: <revised sentence>
Explanation: <one short grammar or wording point>
```

Omit the lesson if the user declines coaching or if extra text would break a required output format.
Do not create separate lesson files or use external services for coaching.

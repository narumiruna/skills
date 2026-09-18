---
name: calibrate-writing-style
description: Use only when the user explicitly invokes `$calibrate-writing-style` to build or refine reusable English and Taiwan Traditional Chinese writing-style prompts through a multiple-choice preference interview.
---

# Calibrating Writing Style

Turn demonstrated wording preferences into small, reusable prompt rules.
Maintain [the English prompt](assets/english-writing-style.md) and [the Taiwan Traditional Chinese prompt](assets/zh-tw-writing-style.md) as the only preference records.

## Start the Session

- Read both prompt assets before asking a question.
- Treat invocation as authorization to edit only those two local assets as the user answers.
- If the target is unclear, first ask whether to tune English, Taiwan Traditional Chinese, or both.
- When tuning both, keep their preferences independent and alternate languages unless the user chooses another order.
- Do not treat the user's ordinary messages as preference evidence; record only explicit selections or custom answers from this interview.

## Run the Interview

Ask exactly one question per turn.
Every question must use this structure:

- **Question:** Ask which wording is easiest to understand or feels most natural.
- **Options:** Give three to five numbered choices, including `No preference / skip` or `Other — provide your wording` when useful.

Make substantive choices natural, polished, and equivalent in meaning.
Vary only one dimension per question so the answer supports one narrow conclusion.
Do not recommend an option because writing preference has no objectively correct answer.
Accept a numbered choice or exact custom wording.
If an answer combines incompatible choices, ask another three-to-five-option question before recording a rule.

Choose the next unresolved, high-value dimension from:

- answer openings and directness;
- sentence length and rhythm;
- everyday, technical, or formal vocabulary;
- amount and order of explanation;
- headings, lists, and paragraph structure;
- examples, analogies, and transitions;
- warmth, formality, contractions, pronouns, and conversational markers;
- punctuation and presentation of English terms in Chinese.

Use contrasts in the target language.
Do not transfer a preference from one language to the other unless the user explicitly chooses that behavior.
After five answered preference questions for a language in one session, ask a three-option checkpoint: continue that language, switch languages, or finish.
The user may stop earlier.

## Update the Prompt

After each explicit preference answer:

1. Convert only the observed distinction into one concise, testable instruction.
2. Update the target asset immediately so an interrupted session does not lose confirmed preferences.
3. Add the rule under the target asset's confirmed-preferences heading, removing its no-preferences placeholder when necessary.
4. Replace or narrow an older rule when the new answer conflicts with it; do not keep both.
5. Skip the edit when the user chooses no preference, or when the answer does not support a reliable rule.

Keep each asset ready to paste into another agent's instructions.
Preserve its scope, correctness safeguards, language requirements, and explicit-request precedence.
Do not add interview history, option numbers, personality claims, rationale, confidence scores, or unsupported generalizations.
Retain a short example only when the selected wording itself is necessary to express the preference.

## Finish

Read both assets again and check for duplicate, conflicting, vague, or cross-language rules.
Report which asset changed and list the resulting preference rules.
If a file could not be written, state that clearly and provide the exact proposed change without claiming it was saved.

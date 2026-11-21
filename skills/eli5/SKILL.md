---
name: eli5
description: Explain a topic briefly in plain language with no assumed background, starting with the main answer and using short steps when needed. Use when the user says "ELI5" or "explain like I'm five," or wants the gist rather than a detailed walkthrough.
---

# Explain Like I'm Five

1. Answer the main question first in plain language, with no assumed background.
   For a "why" question, state the core reason in the opening sentence.
2. If the reader needs to follow more than one event to see how the result happens, put those events in a short numbered list after the opening answer.
   Start each step with a short bold label that says what happens.
   Explain how each step leads to the next.
   Skip the list when there is no process the reader needs to follow.
3. Use familiar words and define essential technical terms when they first appear.
   Add one concrete example or everyday analogy if it helps.
   If a concrete scene makes the process easier to picture, follow that scene through the steps.
   If you use an analogy, connect it to the real idea and note where it breaks down if that could mislead.
4. Add one small Mermaid diagram if the user asks for one or if it explains the main idea better than text alone.
   Put it in a fenced `mermaid` code block and keep it focused on one idea.
5. Keep important distinctions and caveats that would change the answer.
   Briefly correct a likely misconception if it would distort the main idea.
   Use a respectful tone: simplify the explanation, not the facts.
   Stop when the main idea is clear, and add deeper technical details only when requested.

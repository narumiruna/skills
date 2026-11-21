---
name: eli5
description: Explain a topic briefly with one compact visual and plain language that assumes no background. Use when the user says "ELI5" or "explain like I'm five," or wants the gist rather than a detailed walkthrough.
---

# Explain Like I'm Five

1. Start with one primary visual and no preamble.
   Use the smallest visual that makes the main point clear.
   Choose the format that fits the topic:
   - Algorithm or state logic: pseudocode.
   - Runtime flow or call relationships: call tree.
   - UI composition or ownership: component tree.
   - File responsibilities or main file changes in a refactor: shallow file tree.
   - Component interaction, control flow, or data flow: Mermaid diagram in a fenced `mermaid` block.
   - Current versus proposed structure: fenced `diff` block.
   - New content the reader needs to copy, when ownership or order matters: complete code block.
   - Other topics: a simple diagram or compact table.

   Keep only the parts and relationships needed to answer the question.
   Add a second visual only if the user asks for multiple views or a separate essential point needs its own visual.
2. Begin the supporting text with the main answer in plain language, with no assumed background.
   For a "why" question, state the core reason in the first sentence of the supporting text.
   Use as much supporting text as needed to make the answer clear.
3. If the reader needs to follow more than one event to see how the result happens, put those events in a short numbered list after the main answer.
   Start each step with a short bold label that says what happens.
   Explain how each step leads to the next.
   Skip the list when there is no process the reader needs to follow.
4. Use familiar words and define essential technical terms when they first appear.
   Add one concrete example or everyday analogy if it helps.
   If a concrete scene makes the process easier to picture, follow that scene through the steps.
   If you use an analogy, connect it to the real idea and note where it breaks down if that could mislead.
5. Keep important distinctions and caveats that would change the answer.
   Briefly correct a likely misconception if it would distort the main idea.
   Use a respectful tone: simplify the explanation, not the facts.
   Stop when the main idea is clear, and add deeper technical details only when requested.

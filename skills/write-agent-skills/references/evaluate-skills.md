# Evaluate a skill

Check that the client can find the skill, that it loads on the right requests, and that its instructions improve the result.
Use the target client and model for behavior checks, and report what you could not observe.

## Check activation

1. Confirm the client lists the skill where it is installed or registered.
   Fix discovery before changing the description.
2. Start with a realistic request that needs the skill and a near miss that shares its vocabulary but needs something else.
   Include an indirect request that describes a goal without naming the skill.
3. Run each prompt in a fresh session without explicitly invoking the skill.
   Inspect the client trace for a load of `SKILL.md` or the equivalent activation event; a good answer alone does not show that the skill loaded.
4. Revise the description around the missing or overly broad intent, not the exact words of one failed prompt.
   Recheck both positive and negative requests.

For a more systematic optimization, use roughly 20 balanced positive and negative prompts, set aside a balanced validation subset before editing, and repeat runs to account for variation.
Use the other prompts to guide edits and the held-out subset to check whether the changes generalize.
Verify the final description on fresh prompts if practical.
See [optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions).

## Check the result after activation

1. Start with two or three realistic prompts, including one that exercises an edge case or action boundary.
   Record the prompt, any input files, and the expected output for each case.
2. Run each case in clean sessions with the same client, model, prompt, and inputs.
   Compare the new skill against the previous version for maintenance or against no skill for a new workflow.
   Keep outputs in separate locations and use fixtures or dry runs for operations with side effects.
3. Check observable results against the expected output and record evidence for each pass or fail.
   Use code for mechanical checks and human review for qualitative judgments.
   For example, for a review-only request, check both the findings and whether tracked files were left unchanged.
4. Inspect the traces to distinguish unclear instructions from faulty tools, skipped checks, or unnecessary steps.
   Fix the underlying problem and rerun the relevant cases rather than adding a rule for only one prompt.

Keep test data and outputs in the location the target repository permits, or use a temporary workspace if it does not maintain eval fixtures.
See [evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills).

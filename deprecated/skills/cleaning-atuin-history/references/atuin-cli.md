# Atuin CLI Notes

## Transactional Automation Is Disabled

The bundled `cleanup-typos` automation is disabled. Its current interface can recompute candidates, issue query-wide deletion, drive a TUI, and perform remote synchronization without binding execution to approved candidate IDs. Do not offer or execute it until those boundaries are implemented and verified.

## User-Run Single-Entry Deletion

- Give the user `atuin search -i --search-mode prefix <query>` to open the interactive search view.
- Add `--cwd <cwd>` when the original working directory is known.
- The user opens the entry inspector with `Ctrl+O`, confirms the exact row, then presses `Ctrl+D`.
- An agent must not open or drive this TUI.

Avoid manual `atuin search --delete`: it deletes every match under the selected or configured search mode, not one chosen ID.

## Global Duplicate Cleanup

- Use a fixed `--before` cutoff; do not carry a relative value such as `now` from approval to later execution.
- Immediately before every mutation, rerun the audit and `atuin history dedup --dry-run --before "<fixed-cutoff>" --dupkeep <n>`.
- Compare the exact window, groups, and deletion count with the approved result. Obtain renewed approval if any differ.
- Only then run the identical command without `--dry-run`.
- `history dedup` is global across the selected history window, not a single-command deletion.

## Retroactive Filter Cleanup

Use `atuin history prune` only for already-approved `history_filter` or `cwd_filter` rules and an exact reviewed scope. Do not use it as a typo or duplicate cleanup substitute.

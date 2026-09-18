---
name: operate-ghostty
description: Inspect, launch, configure, validate, and troubleshoot an installed Ghostty terminal, including helper CLI actions, keybind actions, themes, fonts, configuration files, and platform-specific behavior.
---

# Operating Ghostty

Treat the installed binary and its help output as the source of truth because Ghostty behavior varies by version, build, and platform.

## Establish Context

1. Run `command -v ghostty`, `ghostty +version`, and `ghostty --help` before relying on remembered syntax.
2. Run `ghostty +<cli-action> --help` before using a helper action whose flags or effects are uncertain.
3. Use `ghostty +help` to list CLI helper actions.
4. Use `ghostty +list-actions --docs` to list documented keybind and command-palette actions.
5. Use `ghostty +list-keybinds --plain` for active keybinds and add `--default` when inspecting built-in bindings.

Do not confuse the two action systems.
CLI helper actions have names such as `+show-config` and are invoked as commands.
Names from `+list-actions`, such as `new_tab`, `reload_config`, and `toggle_fullscreen`, are configuration actions and cannot generally be invoked as `ghostty +<name>`.

## Keep Commands Non-Interactive

- Add `--plain` to `+list-themes`, `+list-keybinds`, and other listing commands when available.
- Do not run `ghostty +edit-config` because it opens an interactive editor.
- Do not launch an interactive child command with `ghostty -e` from an agent shell.
- Do not invoke crash, quit, close, reset, clear, or other disruptive behavior unless the user explicitly requested that exact effect.
- Treat unsupported-action errors as platform or build evidence instead of retrying with guessed syntax.

## Inspect and Troubleshoot

- Use `ghostty +show-config --changes-only` to inspect effective non-default settings.
- Use `ghostty +show-config --default --docs` only when full option documentation is needed because its output is large.
- Use `ghostty +list-fonts --family='<family>'` to diagnose font discovery.
- Use `ghostty +show-face --string='<text>'` or `--cp=<codepoint>` to identify the selected font face.
- Use `ghostty +list-themes --plain` with `--color=dark`, `--color=light`, or `--color=all` to discover theme names without opening the preview TUI.
- Use `ghostty +list-colors --plain` for named colors.

Report the Ghostty version, platform-relevant limitation, command evidence, and the smallest next action that resolves the request.

## Change Configuration

1. Inspect `ghostty +edit-config --help` and existing platform-specific config paths without launching the editor.
2. Prefer the existing non-empty config selected by Ghostty, and do not create competing config files in multiple locations.
3. Read the current file and `ghostty +show-config --changes-only` before editing it.
4. For a keybind, confirm the action and argument with `ghostty +list-actions --docs`, then inspect current and default bindings for trigger conflicts.
5. Add the smallest requested setting in Ghostty configuration syntax, such as `keybind = super+t=new_tab`.
6. Run `ghostty +validate-config --config-file='<path>'` after editing.
7. Re-read the changed lines and relevant `+show-config` or `+list-keybinds --plain` output.
8. Explain that reloading is an in-app keybind or menu action rather than inventing a `ghostty +reload_config` command.

Preserve comments and unrelated settings.
Do not overwrite an existing keybind unless the user requested that conflict resolution.
Check action documentation for platform restrictions before adding a binding.

## Launch Ghostty

On macOS, direct CLI launching is unsupported, so use `open -na Ghostty.app` and pass configuration arguments only with `open -na Ghostty.app --args ...`.
On supported non-macOS builds, use the launch syntax shown by the installed `ghostty --help`.
Do not claim that a window opened successfully without observable process, window, or command evidence.

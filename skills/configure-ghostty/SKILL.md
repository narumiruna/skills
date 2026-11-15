---
name: configure-ghostty
description: Create, inspect, edit, validate, troubleshoot, or apply Ghostty configuration, including files, precedence, includes, themes, fonts, keybindings, reload behavior, runtime diagnostics, launch behavior, and platform or version constraints.
---

# Configuring Ghostty

Treat the installed Ghostty version and its bundled documentation as authoritative because options and platform support can change between releases.
Keep Ghostty's defaults unless a setting serves the user's stated goal.

## Establish the Target

1. Identify the requested behavior, operating system, and whether the user wants an explanation, a config snippet, a local config change, runtime diagnosis, or an authorized launch.
2. Run `command -v ghostty` and `ghostty +version` when Ghostty is available.
3. Use `ghostty +help` to list CLI helper actions.
4. Inspect `ghostty --help` and the relevant `ghostty +<cli-action> --help` before relying on helper-action syntax.
5. If Ghostty is unavailable, use documentation that matches the user's target version and mark generated configuration as unvalidated.

Do not confuse CLI helper actions such as `+show-config` with keybind actions such as `reload_config`.
Keybind actions cannot generally be invoked as `ghostty +<action>` commands.

## Keep Commands Non-Interactive

- Do not invoke `ghostty +edit-config` because it opens an editor.
- Do not launch an interactive child command with `ghostty -e` from an agent shell.
- Do not invoke crash, quit, close, reset, clear, or other disruptive behavior unless the user explicitly requests that exact effect.
- Treat unsupported-action errors as platform or build evidence instead of retrying with guessed syntax.

## Locate the Effective Configuration

Check these files in load order and read every file that exists:

1. `$XDG_CONFIG_HOME/ghostty/config.ghostty`.
2. `$XDG_CONFIG_HOME/ghostty/config`.
3. `$HOME/Library/Application Support/com.mitchellh.ghostty/config.ghostty` on macOS.
4. `$HOME/Library/Application Support/com.mitchellh.ghostty/config` on macOS.

Treat `$XDG_CONFIG_HOME` as `$HOME/.config` when it is unset.
Later macOS files override conflicting values from earlier XDG files.
Run `ghostty +edit-config --help` without invoking `+edit-config` to confirm the installed version's preferred default path.
Prefer an existing non-empty file, and do not create competing configuration files in multiple locations.
If no file exists and the request authorizes a change, create `config.ghostty` at the preferred path reported by the installed version.

Read the selected file and run `ghostty +show-config --changes-only` before editing when the command is available.
Account for every `config-file` include before deciding which file owns a setting.

## Verify Options

- Use `ghostty +show-config --default --docs` for the installed version's complete option reference, but capture and search its large output non-interactively.
- Use `ghostty +list-fonts --family='<family>'` to verify a font family.
- Use `ghostty +show-face --string='<text>'` or `--cp=<codepoint>` to diagnose the selected font face.
- Use `ghostty +list-themes --plain` with `--color=dark`, `--color=light`, or `--color=all` to verify a theme name without opening the preview interface.
- Use `ghostty +list-colors --plain` to verify named colors.
- Use `ghostty +list-actions --docs` to verify a keybind action, its argument, and platform restrictions.
- Use `ghostty +list-keybinds --plain` and `ghostty +list-keybinds --default --plain` to detect active and built-in trigger conflicts.

Do not invent an option, enum value, action, or platform capability when matching documentation is unavailable.

## Edit the Smallest Configuration

Use Ghostty's case-sensitive lowercase `key = value` syntax.
Preserve comments, ordering conventions, quoting style, and unrelated settings.
Use an empty value such as `font-family =` only when the user intends to reset that option to its default.
Do not duplicate a scalar setting in the same effective configuration when updating the existing setting is clearer.

A `config-file` path is relative to the file that declares it unless it is absolute.
Prefix an optional include with `?`, as in `config-file = ?local.ghostty`.
Remember that includes are processed after the containing file, so included values override conflicting values even when the include directive appears earlier in the file.

## Configure Keybindings

Use `keybind = trigger=action` after verifying the action and any parameter.
Valid modifier names include `shift`, `ctrl`, `alt`, and `super`, with documented aliases such as `cmd` on macOS.
Check installed documentation before using `global:`, `all:`, `unconsumed:`, or `performable:` because support and behavior can be platform-specific.
Treat triggers with different prefixes as the same trigger for conflict resolution because a later binding can replace an earlier one.
Do not replace an existing user binding unless the request authorizes that conflict resolution.

Separate a key sequence with `>`, as in `keybind = ctrl+a>n=new_window`.
A sequence has no timeout, can replace a standalone binding that shares its prefix, and cannot be combined with `global:` or `all:`.
Quote a sequence passed as a shell argument so `>` is not interpreted as redirection.

## Validate and Report

1. Run `ghostty +validate-config --help` to confirm supported validation syntax.
2. Run `ghostty +validate-config --config-file='<path>'` for the changed file when supported.
3. Re-read the changed lines and inspect the relevant `+show-config`, `+list-keybinds`, font, or theme output.
4. Report the Ghostty version, relevant file or runtime evidence, validation result when applicable, platform or reload limitations, and the smallest next action.

The default reload binding is `ctrl+shift+,` on Linux and `cmd+shift+,` on macOS.
Some options require new terminals or a full restart, so use the exact option documentation instead of promising a live reload.
Do not restart Ghostty, change operating-system permissions, or install external fonts or themes unless the user explicitly requests that action.
Do not expose unrelated `env`, command, or path values from the user's configuration in the report.

## Launch Ghostty

Launch Ghostty only when the user requests opening the application or a window.
On macOS, use `open -na Ghostty.app` and pass configuration arguments only with `open -na Ghostty.app --args ...` because direct CLI launching is unsupported.
On supported non-macOS builds, use the launch syntax shown by the installed `ghostty --help`.
Do not claim that a window opened successfully without observable process, window, or command evidence.

## Documentation

Use the [configuration guide](https://ghostty.org/docs/config) for file locations, syntax, includes, and reload behavior when installed documentation is unavailable.
Use the [configuration reference](https://ghostty.org/docs/config/reference) for exact option semantics and platform limitations.
Use the [keybinding guide](https://ghostty.org/docs/config/keybind) and [action reference](https://ghostty.org/docs/config/keybind/reference) for triggers, sequences, and actions.

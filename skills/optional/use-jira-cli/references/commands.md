# Jira CLI Command Shapes

JiraCLI flags vary by release and server configuration. Use these as discovery patterns, then check `--help` for the installed command before execution.

## Read

```sh
jira me
jira project list
jira board list
jira issue view ISSUE-1
jira issue view ISSUE-1 --comments 5
jira issue list --plain --columns key,status,assignee,summary --no-headers
jira issue list --raw
jira issue list --csv
```

Filters commonly include assignee, status, free-text query, or JQL. Confirm their short/long flags from `jira issue list --help` instead of relying on remembered syntax.

## Issue Writes

Common resource forms:

```sh
jira issue create --help
jira issue edit ISSUE-1 --help
jira issue assign ISSUE-1 --help
jira issue move ISSUE-1 --help
jira issue comment add ISSUE-1 --help
jira issue worklog add ISSUE-1 --help
jira issue delete ISSUE-1 --help
```

Use `--no-input` only after installed help confirms it and all required fields are explicit. Prefer a template or stdin for long descriptions and comments:

```sh
jira issue create --template ./issue-template.md
jira issue comment add ISSUE-1 --template - < ./comment.md
```

## Planning Resources

Inspect the relevant help before changing relationships or membership:

```sh
jira epic list --help
jira epic create --help
jira epic add --help
jira epic remove --help
jira sprint list --help
jira sprint add --help
jira release list --help
jira project list --help
jira board list --help
```

Do not assume every list command supports `--plain` or the same columns.

## Script Output

When supported, prefer explicit stable fields:

```sh
jira issue list --plain --columns key,status,assignee,summary --no-headers
jira issue list --raw
jira issue list --csv
```

Treat raw output as versioned external data: inspect its schema before parsing fields. Keep config selection explicit so reads and writes cannot silently target different Jira instances.

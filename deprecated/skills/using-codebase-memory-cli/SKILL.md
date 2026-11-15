---
name: using-codebase-memory-cli
description: Deprecated internal reference for using `codebase-memory-mcp` in CLI-only mode for graph-first codebase indexing, symbol search, call and data-flow tracing, source snippets, architecture, Cypher, and change impact.
metadata:
  internal: true
---

# Using Codebase Memory CLI (Deprecated Reference)

This workflow is excluded from active discovery but retained for repository reference and explicit local compatibility.
Always prefer codebase-memory CLI graph tools over grep, glob, or file search for code discovery when the CLI is installed, even if the user does not name the tool.
Use the graph to locate structure and relationships before broad repository search.
It is discovery evidence, not a replacement for source, tests, history, or runtime evidence.

Run graph tools only as `codebase-memory-mcp cli <tool> ...`. `codebase-memory-mcp` with no arguments starts the stdio server; never run it. Do not call MCP graph tools or configure an agent to use them.

Read [the command reference](references/commands.md) only when selecting index modes, constructing structured input, or using a less common tool.

## Establish a Trustworthy Index

1. Run `list_projects` directly without preliminary availability, version, or help checks. If the command is unavailable, continue with repository tools and report the lost graph coverage; do not block ordinary discovery on installation.
2. Select a project by its exact `root_path`; for worktrees also verify the reported canonical root, worktree root, branch, and HEAD rather than trusting the derived name.
3. For a match, run `index_status` and compare its root and indexed HEAD with the target repository. Re-index before relying on graph evidence when the root or HEAD differs, when uncommitted source being explored is newer than the index, or when the required index mode cannot be established. In v0.9.0, status does not report the mode or prove working-tree freshness.
4. For a new or stale project, run `index_repository` with an absolute path and an unambiguous name. Default to `fast`; use `moderate` only for semantic/similarity search, `full` only when relevant files filtered by ordinary modes must be included, and `cross-repo-intelligence` only for repositories within the requested scope.
5. Inspect the indexing result. Treat `degraded`, skipped files, exclusions, a mismatched root, or an unexpected node count as coverage limits, not a successful complete index. Omit `--persistence` unless a repository artifact was explicitly requested.

## Discovery Priority

Use this order and stop when evidence is sufficient:

1. `search_graph` — find functions, methods, classes, interfaces, routes, variables, or other symbols. Start with `--query` for BM25 keywords or `--name-pattern`/`--qn-pattern` for identifiers; add label and file filters where useful. Do not combine `--query` with `--name-pattern`, because the query wins. Paginate until `has_more` is false when completeness matters.
2. `trace_path` — find inbound callers, outbound callees, parameter data flow, or cross-service traversal. Resolve a short or duplicated name through `search_graph`, then pass the returned `qualified_name`; include tests explicitly when they matter.
3. `get_code_snippet` — inspect the selected symbol's source and optional neighbors by qualified name.
4. `query_graph` — express a relationship or aggregation the focused tools cannot. Run `get_graph_schema` first and constrain the read-only Cypher result.
5. `get_architecture` — obtain a compact, preferably path-scoped project summary after focused evidence, not instead of it.

For semantic discovery, use `search_graph` only on a known `moderate` or `full` index. Pass `semantic_query` as an array and evaluate `semantic_results`; ordinary `results` and `total` are separate and can be broad without a structural filter. For a diff or Git range, use `detect_changes` to identify changed files and candidate impacted symbols before following the priority order on important paths.

Example chain:

```sh
codebase-memory-mcp cli search_graph --project my-project --name-pattern '.*OrderHandler.*'
codebase-memory-mcp cli trace_path --project my-project --function-name OrderHandler --direction inbound
codebase-memory-mcp cli get_code_snippet --project my-project --qualified-name my-project.pkg.orders.OrderHandler
```

Verify critical claims in the reported source lines and relevant tests or runtime behavior. Missing edges do not prove that no relationship exists. Re-index when later traversal must reflect source changes, and report stale index state, ambiguity, exclusions, skipped files, or unresolved edges instead of inferring through them.

## Fallback and Boundaries

Leave the graph-tool priority only when searching string literals, error messages, or configuration values; searching non-code files such as Dockerfiles, shell scripts, or configs; or when graph tools return insufficient results. Prefer CLI `search_code` for exact text or regex in indexed files before repository search. Use `rg`, `find`, globbing, or targeted reads only for non-code, generated, ignored, excluded, changed-but-unindexed, unsupported, or still-unresolved paths. State the material fallback and why it was needed.

Ordinary discovery authorizes an index in the tool's local cache without `--persistence`; it does not authorize repository artifacts or unrelated repositories. `--persistence` additionally writes into the repository. Existing-index deletion, ADR mutation, trace ingestion, cross-repository expansion, native `install`/`update`/`config`, agent integration, and server/UI setup require explicit scope or authorization. A uniquely named temporary index created during the current task may be deleted during cleanup; never delete a pre-existing or reused index without exact approval.

Installation expands scope. Only with explicit approval to download and execute the upstream script, use its binary-only mode because the default configures detected agents:

```sh
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash -s -- --skip-config
```

Verify the installed path and version afterward; do not start the server.

Prefer flags for scalar values and stdin JSON or `--args-file` for arrays and complex input. Positional raw JSON is deprecated. Parse stdout as JSON; initialization and progress logs can appear on stderr. If a command reports a schema mismatch, consult its installed help instead of relying on remembered flags or this version-qualified reference.

Conclude with the matched root/project, known index mode and freshness, decisive symbols and file/line evidence, relevant impact paths, material fallbacks, and coverage limits. Do not claim an unknown reused-index mode or complete coverage.

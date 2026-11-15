# Codebase Memory CLI Command Reference

Verified with `codebase-memory-mcp 0.9.0` and its release documentation. Do not run availability, version, or help commands as routine preflight; invoke the required tool directly. Installed schemas override this reference.

## Invocation Contract

```sh
codebase-memory-mcp cli <tool> --flag value
codebase-memory-mcp cli <tool> --args-file /tmp/codebase-memory-args.json
printf '%s\n' '{"project":"my-project"}' | codebase-memory-mcp cli index_status
```

Use flags for scalar values and stdin or `--args-file` JSON for arrays. Positional raw JSON still works in v0.9.0 but emits a deprecation warning. Tool results are JSON on stdout; initialization logs are written to stderr. Bare `codebase-memory-mcp` starts the MCP stdio server.

## Project Identity and Indexing

```sh
codebase-memory-mcp cli list_projects
codebase-memory-mcp cli index_status --project my-project
codebase-memory-mcp cli index_repository \
  --repo-path /absolute/path/to/repository \
  --mode fast \
  --name my-project
```

Match `list_projects` output against `root_path` and, for Git worktrees, its `git.canonical_root`, `git.worktree_root`, branch, and `head_sha`. `index_status` in v0.9.0 reports identity and indexed Git state but not index mode or working-tree freshness. `--name` is optional; use an unambiguous value to avoid path- or worktree-derived collisions.

Index modes from installed help:

- `fast`: filtered files and type-aware per-file/cross-file call and usage resolution; no similarity or semantic edges.
- `moderate`: filtered files plus similarity and semantic edges.
- `full`: all normally indexable files plus similarity and semantic edges; safety exclusions and unsupported paths can still limit coverage.
- `cross-repo-intelligence`: route/channel matching across specified projects; pass `target_projects` as an array.

```sh
printf '%s\n' '{
  "repo_path": "/absolute/path/to/repository",
  "mode": "cross-repo-intelligence",
  "name": "orders-service",
  "target_projects": ["billing-service", "notifications-service"]
}' | codebase-memory-mcp cli index_repository
```

Every index is stored in the local codebase-memory cache. `--persistence true` additionally writes `.codebase-memory/graph.db.zst` in the repository for sharing; omit it during ordinary discovery. Inspect `status`, `excluded`, `skipped_count` or `skipped`, node/edge counts, and any degraded result before trusting coverage.

## Symbol Search

BM25 keyword search:

```sh
codebase-memory-mcp cli search_graph \
  --project my-project \
  --query 'extension loader' \
  --label Function \
  --file-pattern 'src/*' \
  --limit 20 \
  --offset 0
```

Identifier search:

```sh
codebase-memory-mcp cli search_graph \
  --project my-project \
  --name-pattern '.*OrderHandler.*' \
  --label Function \
  --include-connected true \
  --limit 20
```

`--query` is whitespace-tokenized BM25 search and can be broad; it ignores `--name-pattern` when both are supplied. Use `--qn-pattern` for qualified-name matching. Responses expose `total` and `has_more`; increase `offset` by `limit` until complete when exhaustive coverage is required.

Semantic search requires `moderate` or `full` and an array:

```sh
printf '%s\n' '{
  "project": "my-project",
  "semantic_query": ["send", "pubsub", "publish"],
  "limit": 20
}' | codebase-memory-mcp cli search_graph
```

The keywords are combined as an all-keyword semantic match. Read `semantic_results` and its scores separately. With no structural query or filters, ordinary `results`/`total` can describe a broad graph listing rather than semantic matches.

## Trace and Source

```sh
codebase-memory-mcp cli trace_path \
  --project my-project \
  --function-name my-project.pkg.orders.OrderHandler \
  --direction inbound \
  --depth 3 \
  --mode calls \
  --risk-labels true \
  --include-tests true

codebase-memory-mcp cli trace_path \
  --project my-project \
  --function-name my-project.pkg.orders.OrderHandler \
  --direction outbound \
  --depth 3 \
  --mode data_flow \
  --parameter-name order

codebase-memory-mcp cli get_code_snippet \
  --project my-project \
  --qualified-name my-project.pkg.orders.OrderHandler \
  --include-neighbors true
```

Trace modes are `calls`, `data_flow`, and `cross_service`. Cross-service mode follows available HTTP, async, data-flow, and cross-repository edges. Tests are excluded by default. The optional risk labels classify proximity by hop distance; they are not a domain-specific risk assessment.

## Schema, Cypher, and Architecture

```sh
codebase-memory-mcp cli get_graph_schema --project my-project

codebase-memory-mcp cli query_graph \
  --project my-project \
  --query "MATCH (n:Function) WHERE n.name = 'OrderHandler' RETURN n.name, n.qualified_name, n.file_path LIMIT 20" \
  --max-rows 20

printf '%s\n' '{
  "project": "my-project",
  "path": "packages/orders",
  "aspects": ["overview"]
}' | codebase-memory-mcp cli get_architecture
```

Build Cypher only from labels, properties, and edge types returned by `get_graph_schema`. `query_graph` supports a read-only openCypher subset, has no CLI offset, and defaults up to a 100,000-row ceiling; include Cypher `LIMIT` and `--max-rows`. Prefer `search_graph` for paginated browsing. Scope architecture by path and request only needed aspects to control output size.

## Literal Search and Change Impact

```sh
codebase-memory-mcp cli search_code \
  --project my-project \
  --pattern 'ORDER_NOT_FOUND' \
  --file-pattern '*.ts' \
  --path-filter '^src/' \
  --mode compact \
  --context 2 \
  --limit 20

codebase-memory-mcp cli detect_changes \
  --project my-project \
  --scope all \
  --depth 2

codebase-memory-mcp cli detect_changes \
  --project my-project \
  --since HEAD~5 \
  --depth 2
```

`search_code` searches indexed files only. Modes are `compact`, `full`, and `files`; results report grep and enriched totals but provide no offset, so narrow `file_pattern`/`path_filter` or raise the limit. In v0.9.0, `detect_changes --scope all` maps current changes, while `--since <ref>` compares `<ref>...HEAD`. Deduplicate repeated `changed_files`, and verify the paths directly before treating `changed_count` or impacted symbols as complete.

## Stateful or Sensitive Tools

`delete_project` removes cached graph data. `manage_adr` mutates stored architectural decisions. `ingest_traces` mutates graph state and can expose sensitive runtime metadata. Inspect installed help and verify the exact project and payload before an explicitly scoped use. During ordinary discovery, use none of them except `delete_project` to remove a uniquely named index created in the same task.

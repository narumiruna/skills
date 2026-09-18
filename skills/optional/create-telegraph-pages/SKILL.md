---
name: create-telegraph-pages
description: Prepare and publish one explicitly authorized public Telegra.ph article through the official Telegraph API, including safe node conversion, optional account setup, credential handling, and page verification.
---

# Creating Telegraph Pages

Use the bundled `scripts/telegraph.py` by absolute path. A page is a public external write. An exact request authorizes one page only when final title, content, and any byline/link are explicit; otherwise present those fields for approval before publishing. Account creation is a separate external-state change.

## Prepare

1. Preserve the user's language and wording unless editing was requested. Reject secrets, private data, and local-only asset links.
2. Convert the body to a temporary JSON array of Telegraph nodes. Text may be a string; elements use `tag`, optional `attrs`, and optional `children`.
3. Allow only `a`, `aside`, `b`, `blockquote`, `br`, `code`, `em`, `figcaption`, `figure`, `h3`, `h4`, `hr`, `i`, `iframe`, `img`, `li`, `ol`, `p`, `pre`, `s`, `strong`, `u`, `ul`, or `video`. Attributes are string-valued `href` or `src`. Convert larger Markdown headings to `h3`/`h4` and keep encoded content at or below 64 KB.
4. Record an explicit byline decision along with the final title, links, node structure, and one-page publication scope. Approve either exact author values or no public byline; do not infer omission from missing fields.

## Credentials and Account Boundary

Do not preflight, read, or print credentials. Invoke the helper directly; for `create-page`, it automatically resolves a non-empty `TELEGRAPH_ACCESS_TOKEN`, then an explicit trusted `--token-file`, then `$XDG_CONFIG_HOME/telegraph/access-token` (or `~/.config/telegraph/access-token`). Only if the helper reports that no usable credential exists should you request a token or propose account creation. Never place a token in arguments, repository files, captured output, logs, or the response.

Only when no usable token exists, obtain separate approval for account creation, short name, and a new secret-file path. Then run:

```shell
uv run --no-project python "$SKILL_DIR/scripts/telegraph.py" create-account \
  --short-name '<approved-name>' \
  --token-file '<approved-secret-path>'
```

The helper refuses overwrite, uses owner-only permissions, and redacts token/auth URL output. Do not read the token through a captured-output tool or create replacement accounts to avoid credential recovery.

## Publish and Verify

With exact publication authorization and `SKILL_DIR` resolved to this skill directory:

```shell
uv run --no-project python "$SKILL_DIR/scripts/telegraph.py" create-page \
  --title '<approved-title>' \
  --author-name '<approved-author-or-empty>' \
  --author-url '<approved-author-url-or-empty>' \
  /tmp/telegraph-content.json
```

For another existing token file, add `--token-file '<trusted-secret-path>'`; the helper reads it internally so its contents do not enter captured output.

Pass the approved byline values explicitly. To suppress account-default identity, include `--author-name '' --author-url ''`; omitting these fields can publish the account's default author name or URL.

Require an `https://telegra.ph/...` result, then fetch or open the public page and verify title, byline, links, and content structure. Report the URL and any unavailable check. Remove sensitive temporary drafts after successful publication.

On invalid credentials, stop and request a valid token. Fix deterministic node validation errors before one retry; do not repeatedly retry ambiguous, rate, or service errors. Preserve enough error detail to diagnose without revealing secrets.

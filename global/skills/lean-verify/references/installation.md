# Installation and Project Setup

Install only the tools and dependencies needed for the current verification task.
Reuse the existing project rather than rebuilding the environment for each claim.

## Check Existing Tools

Check `command -v elan`, `command -v lean`, `command -v lake`, and `command -v git`.
If the commands are missing from `PATH`, check `~/.elan/bin` before reinstalling.
When elan is available, run `elan --version` and `elan toolchain list`.
Lean and Lake version commands can trigger toolchain downloads, so run them only after selecting the project toolchain.
Git is required to fetch Lake dependencies; curl is required for the installer below.

Run downloaded installers only when installation is authorized.
Ask before changing global toolchain defaults or upgrading a shared project that contains existing proofs.
Ask before large dependency or cache downloads, or expensive source builds, when their cost is not already authorized.

## Install elan

[elan](https://github.com/leanprover/elan) manages Lean toolchains and supplies the `lean` and `lake` command proxies.
The upstream command for a person to run interactively on a Unix-like system is:

```shell
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh
```

Do not run that interactive form from an agent shell.
For an authorized, non-interactive installation that leaves shell configuration and the global default toolchain unchanged, use:

```shell
curl https://elan.lean-lang.org/elan-init.sh -sSf | \
  sh -s -- -y --no-modify-path --default-toolchain none
export PATH="$HOME/.elan/bin:$PATH"
elan --version
```

The `PATH` change applies only to that shell; preserve it in later agent commands when needed.
For Windows or other platform-specific installation, follow the upstream elan instructions instead of translating this shell recipe blindly.

## Initialize or Reuse the Project

These steps use the default workspace; substitute the user's chosen path when one was specified.

1. Inspect `~/.agents/lean` before writing there.
   - If it contains a `lean-toolchain` and either `lakefile.toml` or `lakefile.lean`, inspect and reuse that project.
   - If it contains unrelated files or an incomplete project, stop and resolve the layout with the user rather than overwriting or reinitializing it.
   - Initialize only when the directory is absent or confirmed empty.
2. Select a Lean 4 toolchain.
   - For an existing project, retain its recorded toolchain and dependency revisions.
   - For a new core/Std-only project, prefer a suitable installed toolchain; use a stable Lean 4 release if none is available.
   - When using a library, select a compatible revision first and inspect its `lean-toolchain`, Lake configuration, and transitive dependency pins at that revision.
   - Do not combine independently selected latest revisions and assume they are compatible.
3. Create the directory with `mkdir -p "$HOME/.agents/lean"`, then run `cd "$HOME/.agents/lean"`.
4. Run `lake +<toolchain> init verifier lib`, replacing `<toolchain>` with the selected full toolchain ID.
   - For example, an installed `leanprover/lean4:v4.35.0` can be selected with `lake +leanprover/lean4:v4.35.0 init verifier lib`.
   - This creates a library project with a `Verifier` root module and records the toolchain in `lean-toolchain`.
   - Do not run this initialization command when reusing a project.
5. Run `lake env lean --version` and `lake --version` inside the project to confirm the selected versions.

Keep `lean-toolchain`, the Lake configuration, and `lake-manifest.json` with the proof sources for reproducibility.
If a needed dependency cannot use the existing toolchain, report the conflict before migrating the shared project or creating another project.

## Choose Libraries

Start without external dependencies when Lean core or Std is sufficient.
Choose libraries by the definitions and tactics needed, not by installing all three in advance.
The root imports below identify the libraries; prefer more specific imports when practical.

| Package | Use | Root import | Repository |
| --- | --- | --- | --- |
| `mathlib` | Mathematics and supporting proof tactics. | `Mathlib` | [mathlib4](https://github.com/leanprover-community/mathlib4) |
| `cslib` | Computer science theories and software-verification infrastructure. | `Cslib` | [CSLib](https://github.com/leanprover/cslib) |
| `batteries` | Extended data structures, utilities, and tactics beyond core and Std. | `Batteries` | [Batteries](https://github.com/leanprover-community/batteries) |

Inspect the dependency graph before adding requirements.
CSLib can already bring in mathlib, and mathlib can already bring in Batteries; preserve their compatible pins instead of adding conflicting independent versions.

## Add a Needed Dependency

1. Choose a compatible release tag or commit and confirm the project toolchain matches its requirements.
2. Add only the needed requirement to the existing Lake configuration.
   - For `lakefile.toml`, use the template below after replacing all placeholders.
   - For `lakefile.lean`, use the equivalent `require` declaration documented by the selected library; do not create a second Lake configuration file.

   ```toml
   [[require]]
   name = "<package-name>"
   git = "<repository-url>"
   rev = "<compatible-tag-or-commit>"
   ```

3. Run `lake update <package-name>`, replacing the placeholder with the package being added or deliberately updated.
   - Inspect the resolved revisions in `lake-manifest.json` and any toolchain changes before proceeding.
   - Do not run a bare `lake update` routinely; it can upgrade unrelated dependencies.
4. If mathlib is in the resolved graph and its build cache is not populated, run `lake exe cache get` from the project root before checking proofs.
   - An update hook may already fetch the cache; do not repeat a completed download.
   - If the cache is unavailable, report that limitation instead of silently starting a large source build.
5. Return to the skill's proof-checking workflow using imports that match the resolved library version.

Use the selected revision's upstream documentation and `lake help init` or `lake help update` when installed command behavior differs from these instructions.

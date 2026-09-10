# Spec: "CI/CD for Semantic Models" — new documentation section

| | |
|---|---|
| **Status** | Decisions locked (see §7) — ready for article-tree lock and stubs |
| **Branch** | `user-pg/cicd-section` |
| **Authors** | Peer Grønnerup + Claude |
| **Last updated** | 2026-08-12 |

## 1. Goal

Create a new area on docs.tabulareditor.com that tells the **end-to-end CI/CD story for semantic models with Tabular Editor**: parallel development, validation/testing, and deployment — covering workspace organization (Microsoft Fabric), repo setup, branching strategies, deployment strategies, and ways-of-working. It should include **copy-paste reference pipelines for Azure DevOps and GitHub Actions**, all based on the **new TE CLI** (not the TE2 CLI).

This modernizes and eventually supersedes the 2019–2020 *"You're Deploying it Wrong (AS edition)"* blog series (parts 1–5, https://tabulareditor.com/blog/tag/ci-cd), which targets Analysis Services and the TE2 CLI.

## 2. Existing source material (inventory)

| Content | Where today | Relation to new section |
|---|---|---|
| **Enabling parallel development using Git and Save to Folder** (`parallel-development`) | `content/getting-started/parallel-development.md` — updated version on test site; lives under Getting started > "Parallel development" group | Core foundation article: TOM as source, Save to Folder, serialization, branching strategies (GitHub Flow + Octopus, GitFlow, trunk-based) |
| **GitHub Flow and the Octopus Merge pattern** (`github-flow`) | `content/getting-started/github-flow.md` — **currently orphaned from TOC** (only reachable via xrefs); contains a full 5-job reference pipeline (Octopus merge, download TE, BPA gate, schema validation, deploy) | Substantially a CI/CD pipeline article already — natural fit for the new section |
| **Optimizing development workflow using Workspace Mode** (`optimizing-workflow-workspace-mode`) | `content/getting-started/optimizing-workflow-workspace-mode.md` — thin wrapper around `features/workspace-mode.partial.md` | Ways-of-working / local dev isolation |
| **Sharing macros, BPA rules and preferences across a team** (`sharing-macros-bpa-rules`) | Branch `users-jtb/sharing-macros-and-bpa` — new page under `content/getting-started/`, inserted into the same "Parallel development" TOC group | Stays there (decided); new section links to it, and its repo-setup aspects inform "Setting up your repository" |
| **TE CLI docs** (Overview, Install, Auth, Commands, Config, Interactive, Automation, **CI/CD Integration**, AI Skill, Migrate from TE2, Limitations) | `content/features/te-cli/` under Features > "Command Line and Integration" | Tool-centric **reference**; `te-cli-cicd.md` already has GitHub Actions + ADO snippets, BPA gates, secret handling. New section should be scenario-centric and link here rather than duplicate |
| **`powerbi-cicd` and `as-cicd` stubs** | `content/todo/` — body is `(WIP)`, **not built** (folder excluded from docfx.json), but their uids are already linked from `parallel-development.md` "Next steps" | Reserved uids we can claim for new articles (fixes today's dangling links) |
| **TE2 CLI page** (`command-line-options`) | `content/features/Command-line-Options.md` — has ADO integration sections | Legacy; new section should not build on it. Link to `te-cli-migrate` instead |
| **Old blog series + related posts** | tabulareditor.com/blog (AS edition parts 1–5; "CI/CD scripts for TE2 CLI"; "Fabric Git integration"; "How to get value from the TE CLI") | Source material for concepts (build/validate/deploy stages); needs full rewrite for Fabric/Power BI + TE CLI |

## 3. Proposed placement

**Decided (2026-08-12): a new main section group under Tutorials**, titled **"CI/CD for Semantic Models"**, living in a dedicated subfolder:

```
content/tutorials/cicd/
```

Rationale:

- No `docfx.json`, root `toc.yml`, or Crowdin config changes needed (Tutorials is already registered) — a new *top-level* site section would require all of those.
- Tutorials is the natural home per the site's own content taxonomy (scenario/guide-oriented, vs. Features = tool reference).
- Tool reference stays in `features/te-cli/`; the new section links to it.

**Relationship to Getting started (decided):** the detailed articles move into the new Tutorials section. The two existing published Getting started articles — `parallel-development` and `optimizing-workflow-workspace-mode` — **remain in Getting started but get trimmed to high-level overviews** that draw the big picture and link into the detailed tutorial articles. This keeps published URLs/uids stable (no redirects needed for those two) while the full story lives in one place.

## 4. Structure (implemented as stubs 2026-08-12)

Stub pages exist under `content/tutorials/cicd/`; TOC group added to `content/tutorials/toc.md` (order = reading order = the end-to-end story). File/uid map:

| Article | File | uid |
|---|---|---|
| Overview (section landing) | `cicd/index.md` | `cicd-overview` |
| Organizing workspaces in Microsoft Fabric | `cicd/fabric-workspaces.md` | `cicd-fabric-workspaces` |
| Setting up your repository | `cicd/repository-setup.md` | `cicd-repository-setup` |
| Branching strategies | `cicd/branching-strategies.md` | `cicd-branching-strategies` |
| GitHub Flow and the Octopus Merge pattern | `cicd/github-flow.md` (moved from getting-started) | `github-flow` (unchanged) |
| Parallel development with Git | `cicd/parallel-development.md` | `cicd-parallel-development` |
| Isolated development with Workspace Mode | `cicd/workspace-mode.md` | `cicd-workspace-mode` |
| Validating models in the pipeline | `cicd/validating-models.md` | `cicd-validation` |
| Testing semantic models | `cicd/testing-models.md` | `cicd-testing` |
| Deployment strategies | `cicd/deployment-strategies.md` | `cicd-deployment-strategies` |
| Deploying with the Tabular Editor CLI | `cicd/deploying-with-te-cli.md` | `powerbi-cicd` (claimed from todo stub) |
| Azure DevOps pipeline reference | `cicd/azure-devops-pipeline.md` | `cicd-azure-devops-pipeline` |
| GitHub Actions workflow reference | `cicd/github-actions-workflow.md` | `cicd-github-actions-workflow` |

`github-flow` is slotted under Foundations as the deep dive of the recommended branching strategy; its embedded reference-implementation content seeds the Reference pipelines articles during the content phase.

```
# CI/CD for Semantic Models
## Overview: the end-to-end story          (new: cicd/index.md)

## Foundations
### Organizing workspaces in Microsoft Fabric   (new)
### Setting up your repository                  (new)
### Branching strategies                        (new — extracted/adapted from parallel-development)

## Ways of working
### Parallel development with Git               (detailed version of parallel-development moves here;
                                                 trimmed high-level page stays in Getting started)
### Isolated development with Workspace Mode    (detailed version moves here; trimmed high-level page
                                                 stays in Getting started)
### (Sharing macros, BPA rules and preferences  — stays in Getting started's Parallel development
                                                 group as planned on the users-jtb branch; the new
                                                 section links to it and includes only the parts
                                                 relevant to the CI/CD story, e.g. repo setup)

## Validation and testing
### Validating models in the pipeline           (new: BPA gates, schema/source validation with TE CLI)
### Testing semantic models                     (new: DAX/data tests, expected-value checks, RLS testing
                                                 via TE CLI — capabilities to be confirmed, see §6)

## Deployment
### Deployment strategies                       (new: XMLA deploy vs Fabric Git integration vs
                                                 Fabric deployment pipelines; environment promotion)
### Deploying with the TE CLI                   (new: PBI/Fabric via XMLA; claims uid `powerbi-cicd`;
                                                 AAS/SSAS differences as inline callouts — no dedicated
                                                 AS article; retire uid `as-cicd` here too)

## Reference pipelines
### Azure DevOps pipeline reference             (new: complete annotated YAML)
### GitHub Actions workflow reference           (new: complete annotated workflow)
```

### Article notes

- **Overview (`cicd/index.md`)** — the "modern deployment story": a diagram of the full loop (branch → develop in workspace → PR → validate → merge → deploy dev/test/prod), one paragraph per stage linking to the deep-dive article. This is the successor to "You're Deploying it Wrong" part 1.
- **Organizing workspaces in Microsoft Fabric** — dev/test/prod workspace patterns, feature/developer workspaces, capacity considerations, service principal & workspace permissions, XMLA read/write requirements.
- **Setting up your repository** — folder serialization format choice (TE folder structure vs TMDL), repo layout (model + BPA rules + macros + pipeline definitions together vs split — connects to sharing-macros article), what to `.gitignore`, PR policies.
- **Branching strategies** — GitHub Flow + Octopus Merge (recommended), GitFlow, trunk-based; how each maps to workspaces and deployment environments. Today this lives *inside* `parallel-development.md`; extracted into its own Foundations article now that the detailed content moves to Tutorials.
- **Validating models in the pipeline** — TE CLI BPA gates (error vs warning thresholds, exit codes), schema validation against source, structured output for pipeline annotations. Scenario-centric; command details link to `te-cli-commands` / `te-cli-cicd`.
- **Testing semantic models** — DAX/data tests in the pipeline: executing test queries via the TE CLI, expected-value assertions, RLS/OLS testing. Exact patterns depend on TE CLI capabilities at GA — confirm with the CLI team before writing (§6).
- **Deployment strategies** — the decision article: metadata deploy via XMLA (TE CLI) vs Fabric Git integration vs Fabric deployment pipelines; how they combine; handling partitions/roles/connections per environment; refresh-after-deploy. AAS/SSAS differences (auth, endpoints, no Fabric Git integration) covered as inline callouts here and in "Deploying with the TE CLI" — no dedicated AS article.
- **Reference pipelines (ADO + GitHub)** — complete, copy-paste, annotated pipelines built on TE CLI: trigger → checkout → acquire CLI → validate (BPA + schema) → deploy → refresh. Both should implement the same conceptual pipeline so readers can diff the platforms. `github-flow.md`'s 5-job reference implementation is the seed. **Canonical YAML lives in the public [TabularEditor/CLI](https://github.com/TabularEditor/CLI) repo** (decided, see Q-C); these docs articles walk through the pipelines and link there for the maintained source.

### Content principles

1. **TE CLI only** — all automation examples use the new TE CLI. TE2 CLI is mentioned once, as a pointer to `te-cli-migrate`.
2. **Fabric/Power BI first** — primary narrative targets Fabric/Power BI semantic models; AS is secondary (see Q-D).
3. **Scenario-centric here, tool-centric in Features** — no duplication of command reference; `te-cli-cicd.md` may slim down to pure tool mechanics once this section owns the scenarios.
4. **Runnable examples** — pipeline YAML must be complete and copy-paste runnable (given documented prerequisites), not fragments.
5. Front matter `applies_to` follows existing TE CLI page conventions (product: Tabular Editor CLI) where CLI-specific; team/dev-workflow pages apply to TE2/TE3 as today.

## 5. TOC / navigation / redirect changes

- Add the new group to `content/tutorials/toc.md` **and** mirror it in `content/tutorials/index.md` (the landing page duplicates the TOC manually).
- `content/getting-started/toc.md`: the "Parallel development" group keeps three entries — `parallel-development` and `optimizing-workflow-workspace-mode` (both rewritten as trimmed high-level overviews linking into the new Tutorials section) plus `sharing-macros-bpa-rules` (landing there via the users-jtb branch, unchanged). Existing uids and URLs are kept — no redirects needed.
- The detailed tutorial versions of those two topics are **new pages with new uids** under `content/tutorials/cicd/`.
- `sharing-macros-bpa-rules` (from the users-jtb branch) lands in Getting started's "Parallel development" group as that branch plans — it does **not** move. The new section links to it (and its repo-setup aspects inform the "Setting up your repository" article).
- Fix the orphaned `github-flow.md` (currently reachable only via xrefs) by homing it in the new section. ✅ Done — moved to `content/tutorials/cicd/`, with a server 301 redirect `/en/getting-started/github-flow.html` → `/en/tutorials/cicd/github-flow.html` added to `metadata/redirects.json`.
- Claim uid `powerbi-cicd` for "Deploying with the TE CLI" and retire `as-cicd` (point its inbound links to the same deployment articles), removing both stubs from `content/todo/`. ✅ Done — legacy `/onboarding/{as-cicd,powerbi-cicd}.html` client redirects now point to the new deployment articles; `parallel-development.md` and `github-flow.md` "Next steps" updated.
- Two stub references to `sharing-macros-bpa-rules` are plain text with TODO comments until `users-jtb/sharing-macros-and-bpa` merges (the English build fails on unresolved xref warnings).
- Localization: new pages flow through Crowdin automatically once under a registered folder; no `crowdin.yml` change expected for `content/tutorials/`.

## 6. Coordination

- **`users-jtb/sharing-macros-and-bpa`** adds `sharing-macros-bpa-rules.md` into the Getting started "Parallel development" TOC group, where it stays (decided). Merge-order sensitivity is low since this branch no longer moves that page — only cross-links to it and its "Next steps" wiring touch the same files, so ideally the users-jtb branch merges first.
- **TE CLI GA alignment (decided, Q-F)**: the section publishes together with TE CLI GA. Articles are written GA-first — no preview banners. Coordinate the publish date with the CLI GA doc pass (which also removes the preview notices/warnings from `content/features/te-cli/*`).
- **Reference pipeline hosting (decided, Q-C)**: canonical pipeline YAML/actions live in the public [TabularEditor/CLI](https://github.com/TabularEditor/CLI) repo. Coordinate with the plan for adding pipelines to that repo so docs and repo land together.

## 7. Decisions

All decided 2026-08-12:

- **Q-A (placement):** ✅ Tutorials group — `content/tutorials/cicd/`, section title working name "CI/CD for Semantic Models" (final name: see Q-H).
- **Q-B (existing pages):** ✅ Detailed content moves into the new section. The two published Getting started articles (`parallel-development`, `optimizing-workflow-workspace-mode`) stay as **trimmed high-level overviews** that sketch the big picture and link to the detailed tutorials.
- **Q-D (Analysis Services scope):** ✅ Inline callout notes only where AS differs (auth, endpoints, no Fabric Git integration) — no dedicated AS article.
- **Q-E (testing scope):** ✅ Include DAX/data tests — a dedicated "Testing semantic models" article (test queries, expected-value checks, RLS testing via TE CLI). Confirm CLI capabilities before writing.
- **Q-C (pipeline examples delivery):** ✅ Reference pipelines/actions are authored and hosted in the existing public **[TabularEditor/CLI](https://github.com/TabularEditor/CLI)** repo (the public hub that already exposes the `te-cli` AI agent skill under `skills/te-cli/`; plan for hosting pipelines there already exists). The docs articles explain the pipelines and link/embed from that repo as the canonical source, so samples don't rot in the docs.

- **Q-F (timing vs CLI GA):** ✅ The section won't be finished before the CLI reaches GA, so publication is **coordinated with TE CLI GA**. No preview notices/banners needed on the new articles; write them GA-first. (The preview warning in `te-cli-cicd.md` gets removed as part of the GA doc pass, outside this spec.)

- **Q-G (blog series):** ✅ Old blog posts remain as-is — no redirects. A note pointing to the new section will be added to them **manually** (the blog lives in a different repo; out of scope for this spec).

- **Q-H (naming):** ✅ Section title is **"CI/CD for Semantic Models"**.
- **Q-I (which pages stay):** ✅ Confirmed — `parallel-development` and `optimizing-workflow-workspace-mode` stay in Getting started as trimmed high-level overviews, and `github-flow` moves fully into the new section. **Revised 2026-08-12:** `sharing-macros-bpa-rules` also **stays** in Getting started's Parallel development group (it's a new, not-yet-published article landing there via the users-jtb branch). The new section links to it, pulling in only the parts relevant to the CI/CD story (e.g. into "Setting up your repository").

*All open questions resolved — spec is ready for the article-tree lock and stub creation.*

## 8. Out of scope (for this section, v1)

- Report/paginated-report deployment (semantic models only).
- TE2 CLI-based pipelines (covered by legacy page + migration guide).
- General Git tutorials (link out).

## 9. Next steps

1. ~~Resolve open questions~~ — all resolved (see §7).
2. Confirm TE CLI testing capabilities (for the "Testing semantic models" article) with the CLI team.
3. Lock the article tree and create stub pages with uids + front matter.
4. Write Foundations + Reference pipelines first (highest value), then Validation/Deployment, then move detailed Ways-of-working content in and trim the two Getting started pages.
5. Coordinate merge order with `users-jtb/sharing-macros-and-bpa`.
6. Coordinate pipeline YAML landing in TabularEditor/CLI and overall publish timing with TE CLI GA.

---
uid: sharing-macros-bpa-rules
title: Sharing macros, BPA rules, and preferences across a team
author: Just Blindbæk
updated: 2026-07-06
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Sharing macros, BPA rules, and preferences across a team

Tabular Editor reads several configuration files from a fixed location on each user's machine — `%LOCALAPPDATA%\TabularEditor3\` for Tabular Editor 3, or `%LOCALAPPDATA%\TabularEditor\` for Tabular Editor 2 — most notably `MacroActions.json` (the user's macros), `BPARules.json` (the user's local BPA rules), and `Preferences.json` (general application preferences). That's a sensible default for a single developer, but teams that want a shared, consistent set of macros or preferences — across everyone on the team, across a department, or between local development and CI — run into an obvious question: **how do you keep a file at a fixed local path in sync with something version-controlled and shared?**

**If what you're trying to share is BPA rules, this is already solved** — see [Sharing BPA rules](#sharing-bpa-rules) below. The rest of this page is mainly about macros and preferences, which don't have the same native support.

## Start with a central Git repository

Whichever mechanism you use to get files onto an individual developer's machine, it should be pulling from a **single, central Git repository** dedicated to shared configuration — macros, and optionally a shared baseline `Preferences.json`. Treating this repository as the source of truth, rather than any one developer's machine, is what actually makes "sharing" meaningful:

- Changes to a macro are reviewable via pull request, the same way you'd review a change to a semantic model.
- You get a full history of who changed what macro and when, and can revert a bad change the same way you'd revert any other commit.
- New team members get the whole team's macro library by cloning one repository, rather than copying files from a colleague's machine.
- The same repository can double as the source for BPA rule collections (see below), so a team's shared standards live in one place rather than scattered across multiple sync mechanisms.

## Same repo as your semantic model, or a separate repo?

Before choosing a sync mechanism, it's worth deciding where the shared macros and BPA rules should actually live: inside the same repository as your semantic model, or in their own dedicated repository.

**The same repository as your semantic model is the simpler default, and generally the right starting point.** Macros and rules are just files alongside the model, versioned together. Under [GitHub Flow](xref:github-flow), creating a feature branch off `main` gets you whatever macros and rules were current at that moment, with no separate step — freshness comes for free from branching, which you're doing anyway for every piece of work. A change to a macro is just another feature branch and pull request, like any other change — reviewers see from the diff that it only touches `MacroActions.json`, so there's no confusion about what's being reviewed.

**A separate, dedicated repository** starts to make sense once you have **multiple, genuinely independent semantic model repositories** — for example, different teams or departments each maintaining their own. Without it, every model repository needs its own copy of the shared macros and rules, and keeping those copies in sync becomes its own manual problem — the opposite of what centralizing them was supposed to solve.

Even in that multi-team case, it's worth checking whether the real need is a single, separate macros repository, or a **shared baseline with room for local additions** — an organization-wide set of macros with a department's own layered on top, for example. That's less a same-repo-vs-separate-repo choice than a multi-source one: BPA rule collections already support it natively (see [Sharing BPA rules](#sharing-bpa-rules) above), and for macros, see [Combining multiple macro sources](#combining-multiple-macro-sources) below.

If your team only maintains a single semantic model repository today, the same-repo approach is the simplest choice and the duplication concern doesn't apply yet — but it's worth considering whether that will still be true in a year, since migrating shared macros out of a model repo later is more work than starting with them separate.

Whichever you choose, the sync mechanisms described later on this page work the same way regardless — a dedicated macros repository just means they need to reach into a second repository rather than one you already have checked out.

## Sharing BPA rules

Tabular Editor already has first-class support for combining Best Practice Analyzer rules from multiple sources, with no symlinks or workarounds required:

- **Rule collections** let a model draw rules from the current model, the local user's `BPARules.json`, a machine-wide `BPARules.json`, and any number of additional collections you add explicitly — including a file elsewhere on disk (with support for paths relative to the model, so the rule file can live in the same repository), a network share, or an HTTP/HTTPS URL. Collections have a defined precedence order, so a shared, central rule can be overridden at the model level where needed. See [Managing Best Practice Rules](xref:best-practice-analyzer#managing-best-practice-rules) for how to add and prioritize collections.
- **Built-in rules** (Tabular Editor 3) ship a curated, versioned set of best-practice rules directly in the application, updated automatically with each release, with knowledge-base articles linked from each rule. These sit alongside your custom rules rather than replacing them. See [Built-in BPA Rules](xref:built-in-bpa-rules).

Between these two features, most "how do we share BPA rules across the team" scenarios are already covered natively: a shared rule file committed to a repository, included as a collection via a relative path, network share, or URL, is often all you need — no symlink or hook required, since Tabular Editor is reading the collection directly rather than through a fixed personal path.

> [!NOTE]
> Because rule collections can point at a relative path, a network share, or a URL, the same-repo-vs-separate-repo question above matters much less for BPA rules than it does for macros — a rule collection works the same way regardless of which repository the rule file lives in, since nothing needs to be copied or symlinked onto a fixed local path first. This is one of the practical advantages of BPA's native multi-source support over the file-copying mechanisms macros currently require.

### Which collection type to use

Of the three ways to add an external rule collection, **a relative-path file in a Git repository is the recommended default** for most teams, for a combination of reasons the other two options don't share:

- **URL-based collections are read-only.** Tabular Editor explicitly does not allow editing a rule collection loaded from an HTTP/HTTPS URL. That's a reasonable restriction for something like Microsoft's [standard Analysis Services BPA rules](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules), which you're consuming as-is, but it rules out a URL as the home for a rule set your own team actively edits — you'd have to maintain the actual file somewhere else entirely and treat the URL as a read-only mirror, which is more moving parts than it's worth.
- **Network shares assume everyone's machine can reach the same network location**, which fits an on-premises or single-office setup but is a poor match for a distributed team, anyone working remotely, or a cloud-first CI/CD pipeline agent that won't have your internal network mounted.
- **A relative path checked into the semantic model's own Git repository** avoids both problems: it's fully editable (a normal file, edited and reviewed like any other file in the repo), and it needs no network topology assumptions — whatever machine has the repo cloned has the rule file too, whether that's a developer's laptop or a CI/CD build agent.

One constraint worth knowing: relative paths only resolve when the model is loaded from disk (a Save to Folder model), not when Tabular Editor connects directly to a live Analysis Services or Power BI instance. This rarely matters for parallel development built on Git and [Save to Folder](xref:parallel-development#what-is-save-to-folder), since the model is on disk throughout — but it's worth checking if part of your team connects directly to a live workspace instead.

If your team already has a shared, reachable network location and prefers not to introduce a per-repo file, a network share is a workable alternative — it just trades portability for whatever convenience your existing file-share setup already offers. A URL-based collection is best reserved for consuming an external, read-only rule set (like Microsoft's standard rules) rather than for rules your own team maintains.

## Sharing macros

Macros are different: Tabular Editor reads a single `MacroActions.json` file per user, from a fixed path, with no equivalent to BPA's rule-collection system. See the [Macros view reference](xref:macros-view-reference) for how the file itself is structured.

> [!NOTE]
> **Why there's no built-in remote-loading feature:** Macros are C# scripts. Tabular Editor deliberately does not include built-in functionality to automatically download or load macros from a location outside the user's own control — a webpage, a GitHub repository, a public "marketplace." Loading and executing arbitrary code from a remote source without an explicit step by the user would be a real security risk. Any sharing mechanism needs to involve something the user or team sets up themselves.

Three approaches teams use to bridge the gap between a central repository and Tabular Editor's fixed local path:

### Option A: symbolic link

The fixed path becomes a link into your repository, so Tabular Editor transparently reads and writes your working copy of `MacroActions.json`.

```powershell
New-Item -ItemType SymbolicLink -Path "$env:LOCALAPPDATA\TabularEditor3\MacroActions.json" -Target "C:\path\to\your\repo\MacroActions.json"
```

(For Tabular Editor 2, use `%LOCALAPPDATA%\TabularEditor\` instead of `%LOCALAPPDATA%\TabularEditor3\`.)

- **Two-way**: edits made in Tabular Editor's GUI land directly in your working copy, ready to review and commit like any other file change.
- Still needs an explicit `git pull` to bring down a teammate's changes — the symlink removes the manual copy step, not the need to sync with the remote.
- Creating a symlink on Windows needs Developer Mode enabled or an elevated prompt — often blocked by policy on locked-down machines. Where that's the case, IT can grant the permission centrally (via device policy or the `SeCreateSymbolicLinkPrivilege` right) as part of deploying Tabular Editor itself, so individual developers don't need to self-elevate; a separate small script can then create the link once a developer has cloned the repo.

### Option B: pre-commit hook

A [Git pre-commit hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks), checked into the repository, that copies `MacroActions.json` from the repo to `%LOCALAPPDATA%\TabularEditor3\` every time you commit (`%LOCALAPPDATA%\TabularEditor\` for Tabular Editor 2).

- **No elevated permissions or Developer Mode needed** — a plain file copy is all it takes, and it works regardless of where any developer cloned the repo (the source is relative to the repo root; the destination, `%LOCALAPPDATA%`, resolves per-user automatically).
- **One-way**, and it syncs on **commit**, not on **pull** — though since you can't see a teammate's change any sooner than after their PR merges and you pull it yourself anyway, this rarely matters unless your branch goes a long time without picking up `main`. A `post-merge`/`post-checkout` hook closes that gap if it does.
- A GUI-made edit in Tabular Editor stays local until you manually copy it back into the repo and commit — otherwise it's silently overwritten next time the hook runs.

### Option C: a copy-on-apply tool

Dotfiles managers like [chezmoi](https://www.chezmoi.io/) solve the same problem generally: keep the file in a repository, and explicitly copy it to its target location with an `apply` command, and copy local edits back with an `add` command — nothing links or writes through automatically.

- Same practical benefits as Option B (no elevated permissions, no dependency on a specific local clone path), but both directions are explicit commands, which some teams prefer over a symlink's silent write-through.
- The trade-off is learning a real third-party tool with its own concepts — likely more than a single JSON file needs on its own, unless your team already manages other developer-machine configuration this way (shared VS Code or Git config, for example), in which case macros become one more file in a system you've already adopted.

> [!NOTE]
> None of these is "the" official mechanism — they're different trade-offs for the same problem. Pick one and use it consistently rather than mixing mechanisms per file.

### Combining multiple macro sources

None of the three options above can combine more than one source at once — they're all just moving a single file from one place to another. If you need to combine a central set of macros with a department or personal set, you need a script that merges them before Tabular Editor reads the file. This is a workaround, not a first-class feature (unlike BPA rules, macros have no native rule-collection equivalent) — keep it simple enough that any developer can understand and fix it.

## Sharing preferences

`Preferences.json` has the same fixed-path constraint as macros, with no native multi-source support. Any of the three options above works identically for it.

## Summary

| Goal | Approach |
|---|---|
| Decide where shared macros/rules should live | Same repo as a semantic model if you only maintain one such repo; a separate dedicated repo if you maintain several — see [Same repo or a separate repo?](#same-repo-as-your-semantic-model-or-a-separate-repo) |
| Share BPA rules across a team | Relative-path file collection in a Git repository (recommended default) — see [Which collection type to use](#which-collection-type-to-use). Network share or URL collection also possible, see linked section for trade-offs. |
| Get a curated, maintained baseline rule set with no setup | [Built-in BPA Rules](xref:built-in-bpa-rules) (TE3) |
| Share macros or preferences, two-way | Symbolic link (Option A) — still needs `git pull` for a teammate's changes; may need IT to grant permission on locked-down machines |
| Share macros or preferences, no elevated permissions | Pre-commit hook (Option B) — one-way, syncs on commit not on pull |
| Share macros or preferences, explicit and reviewable | A dotfiles-manager tool like chezmoi (Option C) — more to learn, best if already used for other config |
| Combine multiple macro sources (central + department + personal) | A merge script that concatenates the arrays into the single file Tabular Editor reads — a workaround, not built-in |
| Load macros from a location the user doesn't control | Not supported, by design — macros are executable code |

## Next steps

- [Managing Best Practice Rules](xref:best-practice-analyzer#managing-best-practice-rules)
- [Built-in BPA Rules](xref:built-in-bpa-rules)
- [Macros view reference](xref:macros-view-reference)
- [Enabling parallel development using Git and Save to Folder](xref:parallel-development)
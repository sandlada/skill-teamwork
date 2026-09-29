# skill-teamwork

A skill library providing multi-agent teamwork orchestration for AI coding agents, aligned to Google Antigravity Teamwork.

## What it does

The `teamwork` skill lets a single model run a disciplined multi-agent team
using its own native subagent capability. The invoking model acts as
**Sentinel**: it runs the scoping interview, selects exactly one execution
path, writes `.teamwork/brief.md`, waits for approval, then spawns a
**Project Orchestrator** subagent that runs milestones via pattern role
teams with per-path verification gates and a final success audit.

Five execution paths (Sentinel auto-selects, explicit user statement wins):
General (Distributed coding, default), Iterative coding (small scope, never
parallelizes), Document Review (no source edits), Math / Proof (single
tournament round), Math / Proof Large Team (full tournament network).

For a project request, the skill drives this flow:

1. **Scope & brief** — Sentinel interviews (scope, requirements,
   verification, acceptance criteria, working directory, integrity mode,
   speed knobs), selects the path, writes `.teamwork/brief.md`, and stops
   for approval.
2. **Plan** — Orchestrator breaks the brief into milestones with
   non-overlapping tracks and exclusive file ownership, maintaining
   `.teamwork/plan.md` / `.teamwork/progress.md` plus one Context Packet
   (explorer output format) per milestone.
3. **Execute** — per-path gates over fresh subagent sessions:
   - General: `explorer -> workers -> critic -> challenger (skip when deep=off) -> auditor`
   - Iterative: `explorer -> single worker -> critic -> auditor`
   - Document Review: `reviewers -> synthesizer -> critic -> auditor`
   - Math: `provers -> falsifier -> verifier`
   - Large Team: parallel prover+falsifier pairs, synthesis tree in
     dependency order, `.teamwork/knowledge/` registry
4. **Success audit** — Sentinel spawns a fresh success auditor for a
   targeted end-to-end pass. Partial passes are failures.

Core discipline enforced throughout:

- **Reports, not vibes** — every verdict cites concrete evidence: exact
  commands and relevant output, `file:line` references, `.teamwork/`
  artifact paths. Fabricated evidence is an automatic failure.
- **Exclusive file ownership** — a file appears in at most one builder
  track per milestone.
- **Independent verification** — verifiers run in fresh sessions, separate
  from whoever built the work, and are read-only over project sources.
- **Fixed path** — the orchestrator may not change the Sentinel's selected
  path; it stops and reports with evidence instead.
- **Manual speed knobs** — `workers=N` (parallel cap), `team=S|M|L`
  (scale), `deep=on|off` (depth switch), via plain words (`人少点`,
  `快一点`, `大队伍`, `别上强验证`).

## Usage

```
@teamwork <project request>
```

Example: `@teamwork Add a rate limiter to the public API with tests.`

The skill requires a tool that spawns isolated subagent sessions (e.g. a
`subagent`, `task`, or `agent` tool). If the host agent lacks one, the skill
either stops or proceeds solo — the same workflow, but verification
degrades to self-review by the session that wrote the code, which the skill
must disclose to the user before starting.

## Roles

| File | Role | Dispatched to |
| --- | --- | --- |
| `roles/sentinel.md` | Sentinel | the main model |
| `roles/orchestrator.md` | Project Orchestrator | subagent, dispatch only |
| `roles/shared/base.md` | evidence / scratch / report spec | prepended to every subagent prompt |
| `roles/coding/explorer.md` | Explorer | subagent, read-only |
| `roles/coding/worker.md` | Worker | subagent, edits |
| `roles/coding/critic.md` | Critic | subagent, read-only |
| `roles/coding/challenger.md` | Challenger | subagent, scratch |
| `roles/coding/auditor.md` | Auditor | subagent, read-only |
| `roles/math/prover.md` | Prover | subagent, scratch |
| `roles/math/falsifier.md` | Falsifier | subagent, scratch |
| `roles/math/verifier.md` | Verifier | subagent, read-only |
| `roles/review/reviewer.md` | Reviewer | subagent, read-only |
| `roles/review/synthesizer.md` | Synthesizer | subagent, writes synthesis artifact |
| `roles/success-auditor.md` | Success Auditor | subagent, read-only |

Each subagent prompt is built as: `roles/shared/base.md` contents, then
the verbatim role file contents, then the task block (project, working
directory, integrity mode, speed knobs, path, assigned files, Context
Packet, acceptance criteria) and the required report block.

## Repository layout

```
SKILL.md                    # skill entry point: paths, phases, gates, rules
roles/sentinel.md           # Sentinel prompt (main model)
roles/orchestrator.md       # Orchestrator prompt (dispatch only)
roles/shared/base.md       # evidence / scratch / report spec
roles/coding/               # explorer, worker, critic, challenger, auditor
roles/math/                 # prover, falsifier, verifier
roles/review/               # reviewer, synthesizer
roles/success-auditor.md    # final acceptance audit prompt
```

Runtime artifacts land in the target project's `.teamwork/` directory:
`brief.md`, `request.md`, `plan.md`, `progress.md`, `scratch/<agent>/`,
`knowledge/` (Math paths only).

Integrity modes (`development` / `demo` / `benchmark`) control which
shortcuts are forbidden; they are scoped during the Phase 1 interview and
passed into every subagent prompt.

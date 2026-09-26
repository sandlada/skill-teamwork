# skill-teamwork

A skill library providing multi-agent teamwork orchestration for AI coding agents.

## What it does

The `teamwork` skill lets a single model run a disciplined multi-agent team using
its own native subagent capability. The invoking model acts as
**Sentinel + Orchestrator**: it owns sequencing, delegation, and gate decisions,
but never implements code itself.

For a project request, the skill drives this flow:

1. **Scope** — restate testable acceptance criteria, or ask focused questions
   first (scope, requirements, verification method, integrity mode).
2. **Plan** — an ordered milestone plan with non-overlapping work tracks and
   exclusive file ownership per track.
3. **Execute** — each milestone dispatches role prompts to isolated subagent
   sessions: explorers research (read-only), workers implement, then
   independent verifiers gate every implementation milestone:
   - **Critic** — adversarial code review (read-only)
   - **Challenger** — adversarial testing from scratch (scratch files only)
   - **Auditor** — re-runs claimed commands itself, hunts fabricated evidence
4. **Success audit** — after the final milestone, a fresh success auditor runs a
   full end-to-end pass against the acceptance criteria. Partial passes are
   failures.

Core discipline enforced throughout:

- **Reports, not vibes** — every verdict must cite concrete evidence: commands
  actually run and their real output, file:line references.
- **Exclusive file ownership** — a file appears in at most one worker track per
  milestone; no two concurrent workers ever touch the same file.
- **Independent verification** — verifiers run in fresh sessions, separate from
  whoever wrote the code.
- **Bounded retries** — 2 fix attempts per failed gate; a third failure stops
  the milestone and is reported to the user with the evidence.

## Usage

```
@teamwork <project request>
```

Example: `@teamwork Add a rate limiter to the public API with tests.`

The skill requires a tool that spawns isolated subagent sessions (e.g. a
`subagent`, `task`, or `agent` tool). If the host agent lacks one, the skill says
so and either stops or proceeds solo while keeping the same verification-gate
discipline.

## Roles

| File                        | Role            | Dispatched to         |
| --------------------------- | --------------- | --------------------- |
| `roles/orchestrator.md`     | Orchestrator    | the main model        |
| `roles/explorer.md`         | Explorer        | subagent, read-only   |
| `roles/worker.md`           | Worker          | subagent, edits       |
| `roles/critic.md`           | Critic          | subagent, read-only   |
| `roles/challenger.md`       | Challenger      | subagent, scratch     |
| `roles/auditor.md`          | Auditor         | subagent, read-only   |
| `roles/success-auditor.md`  | Success Auditor | subagent, read-only   |

Each role file is a self-contained subagent prompt: the skill sends its verbatim
contents, followed by task-specific context (project, working directory,
integrity mode, assigned files, acceptance criteria) and a required structured
report block (`verdict / findings / evidence / blockers / artifacts written`).

## Repository layout

```
SKILL.md                    # skill entry point: workflow, rules, role table
roles/orchestrator.md       # planning & dispatch prompt (main model)
roles/explorer.md           # research prompt (read-only)
roles/worker.md             # implementation prompt
roles/critic.md             # adversarial review prompt
roles/challenger.md         # adversarial testing prompt
roles/auditor.md            # evidence-verification prompt
roles/success-auditor.md    # final acceptance audit prompt
```

Integrity modes (`development` / `demo` / `benchmark`) control which shortcuts
are forbidden; they are scoped during the initial interview and passed into
every subagent prompt.

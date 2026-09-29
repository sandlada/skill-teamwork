# AGENTS

This repo is the `teamwork` skill, aligned to Google Antigravity Teamwork. The main model acts as Sentinel (scoping, path selection, approval, final audit) and spawns a dedicated Project Orchestrator to run milestones with per-path gates executed by pattern role teams.

## Repository structure

- `SKILL.md` — skill entry point: 5 execution paths, two-phase workflow, per-path gates, role table
- `roles/sentinel.md` — Sentinel prompt (main model): scoping, path selection, `brief.md` + approval
- `roles/orchestrator.md` — Orchestrator prompt (subagent): milestones and gate sequencing (must not change path)
- `roles/shared/base.md` — prefix for every subagent prompt: evidence / scratch / report-block spec
- `roles/coding/` — explorer / worker / critic / challenger / auditor
- `roles/math/` — prover / falsifier / verifier (tournament + knowledge)
- `roles/review/` — reviewer / synthesizer (gates reuse critic + auditor)
- `roles/success-auditor.md` — final acceptance audit (spawned by Sentinel after the orchestrator reports done)
- `README.md` — public documentation

Runtime artifacts land in the target project root `.teamwork/`: `brief.md` /
`request.md` / `plan.md` / `progress.md`, `scratch/<agent>/`,
`knowledge/` (Math paths only).

## Constraints (read `SKILL.md` before changing code)

- The Sentinel selects the path (General by default; `keep small`→Iterative; `review`→Review; `prove`→Math; `very large team`→Large Team). The orchestrator must not change it; on a wrong path it stops and reports.
- Exclusive file ownership: within one milestone, a file belongs to at most one builder track.
- Verification roles are strictly read-only over project sources, run only the acceptance commands, and inspect only assigned files + Context Packet.
- Google-style evidence: exact commands + relevant output, `file:line` refs, `.teamwork/` artifact references; fabricated evidence is an automatic failure; the orchestrator judges when to stop retrying, no fixed ceiling.
- Three manual speed knobs: `workers=N` (fewer hands / faster) / `team=S|M|L` (large team) / `deep=off` (skip deep verification, i.e. challenger/falsifier).
- Every subagent prompt = `shared/base.md` + verbatim role file + task block; a session without a report block is treated as failed and re-dispatched.

## Technical references

- [Teamwork: When AI Becomes a Research Partner](https://antigravity.google/blog/teamwork-when-ai-becomes-a-research-partner) — Official Antigravity Teamwork tech blog: multi-agent patterns (Iterative/Distributed Coding, Long Proof, Self-Verification, Document Review), decoupling of orchestration from agent descriptions, runtime-adaptive teaming, and empirical results in mathematics, systems, and open-source optimization. This skill's roles and gates map to its Distributed Coding pattern.
- [Teamwork (/teamwork-preview) official docs](https://antigravity.google/docs/teamwork) — `/teamwork-preview` spec: Sentinel / Orchestrator / Explorer / Worker / Critic / Challenger / Auditor / Success Auditor responsibilities, two-phase workflow (Phase 1 scoping interview → prompt artifact → Phase 2 autonomous execution), integrity modes (`development` / `demo` / `benchmark`), dedicated working directories and scratch isolation. This repo's `SKILL.md` and `roles/` are the skill-ified implementation of that spec; the official docs win on semantic conflicts.

## Google Teamwork design summary (per the two docs above)

1. Positioning: `/teamwork-preview` (paid), for large/open-ended problems unreliable for a single agent: multi-file refactoring, systems simulation, math proofs. Core loop: generate candidates → stress-test → synthesize stronger solutions.
2. Pattern/orchestration decoupling: a pattern is a spec, not an executable program; the framework auto-selects by task and dynamically decides agent count and structure. 5 patterns: Iterative Coding, Distributed Coding (default), Long Proof, Self-Verification, Document Review.
3. Role layers: Sentinel (takes over after approval) / Project Orchestrator (splits milestones, fresh session across milestones) / Explorer (read-only) / Worker (exclusive file tracks) / Critic (review) / Challenger (adversarial testing) / Auditor (fabricated-evidence hunt) / Success Auditor (final E2E).
4. Two-phase workflow: Phase 1 scoping interview (Specify What, Not How: objectives → requirements → independent verification → acceptance criteria → working directory → prompt artifact pending approval); Phase 2 autonomous execution (Request / Plan / Progress artifact handoffs).
5. Integrity modes: `development` (only fabricated/facade violations), `demo` (+ no copying core logic, no outsourcing core work, no reading tests to reverse-engineer), `benchmark` (from-scratch, standard library only). Plus dedicated working directories, exclusive file ownership, per-agent scratch.
6. Long Proof essentials: competitive strategy search (candidates + dedicated falsifiers), proof-plan dependency graph (independent-parallel / dependent-topological), per-subproblem tournament-network synthesis, cross-round learning (pitfall registry + shared knowledge directory).

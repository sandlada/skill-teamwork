# Example: Iterative Bugfix Workflow

This example demonstrates how `@teamwork` runs an **Iterative Coding** workflow for a small, focused bugfix task.

## Request
`@teamwork Fix null pointer exception when user profile has no email. Keep it small.`

## 1. Phase 1 — Scoping & Brief (Sentinel)
The Sentinel detects `Keep it small` and selects the **Iterative Coding** path.

`.teamwork/brief.md`:
```markdown
# Brief: Fix NPE in Profile Email Access

- Path: Iterative coding
- Integrity mode: development
- Speed knobs: workers=1, deep=off
- Working directory: E:/projects/myapp

## Objectives
Fix NullPointerException in UserProfile.getEmailDomain() when email is null or empty.

## Acceptance Criteria
- Unit test `test_get_email_domain_null()` passes.
- `mvn test -Dtest=UserProfileTest` passes with 0 failures.
```

## 2. Phase 2 — Autonomous Execution (Orchestrator)

Gates per Iterative path:
`Quick Explorer -> Single Worker -> Critic -> Auditor`

### Explorer Context Packet
```markdown
Context Packet:
- Relevant files: `src/main/java/com/app/UserProfile.java:42-55`
- Acceptance command: `mvn test -Dtest=UserProfileTest`
```

### Worker Report Block
```yaml
verdict: pass
findings: Added null-check in getEmailDomain returning empty Optional.
evidence: mvn test -Dtest=UserProfileTest exited with code 0 (12 tests passed).
blockers: none
artifacts written: src/main/java/com/app/UserProfile.java
```

### Critic Report Block
```yaml
verdict: pass
findings: Changes conform to existing Optional-based pattern in UserProfile.
evidence: Verified diff in UserProfile.java:45-48.
blockers: none
artifacts written: none
```

### Auditor Report Block
```yaml
verdict: pass
findings: No facades or mocked test passes detected.
evidence: Spot-checked git diff and verified test output authenticity.
blockers: none
artifacts written: none
```

## 3. Success Audit (Sentinel)
Sentinel spawns `Success Auditor`, which reruns `mvn test -Dtest=UserProfileTest`. Upon pass, final result is presented to the user.

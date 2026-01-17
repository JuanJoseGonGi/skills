# Development Workflow and Iteration

## Evaluation-Driven Development

**Create evaluations BEFORE writing extensive documentation.**

### Step 1: Identify Gaps
Run the agent on representative tasks **without** a skill. Document where it lacks context or uses the wrong approach.

### Step 2: Create Evaluations
Build test scenarios that exercise identified gaps (e.g., specific input files or complex requirements).

### Step 3: Write Minimal Instructions
Create just enough content to address the gaps. Ensure compliance with the specification.

### Step 4: Validate
Use the [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) library to validate:
```bash
skills-ref validate ./my-skill
```

### Step 5: Iterate
Run evaluations → Identify failures → Refine instructions → Repeat.

## Workflow Patterns

### Validated Workflow (Recommended)
For critical operations, provide a checklist or validation step:
```markdown
## Workflow
1. Analyze input
2. Create plan
3. Validate plan: Run `python scripts/validate.py plan.json`
4. Execute only after validation passes
```

### Feedback Loop
1. Generate initial output.
2. Validate output (manual or scripted).
3. If errors found, fix and repeat validation.

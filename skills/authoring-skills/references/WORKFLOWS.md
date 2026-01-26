# Workflow Patterns and Iteration

## Sequential Workflows

For complex tasks, break operations into clear steps. Provide an overview at the start:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** -> Follow "Creation workflow" below
   **Editing existing content?** -> Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## Validated Workflow Pattern

For critical operations, include validation checkpoints:

```markdown
## Workflow

1. Analyze input
2. Create plan
3. Validate plan: Run `python scripts/validate.py plan.json`
4. Execute only after validation passes
```

## Evaluation-Driven Development

### Step 1: Identify Gaps
Run the agent on representative tasks **without** a skill. Document where it:
- Lacks context
- Uses the wrong approach
- Produces suboptimal output

### Step 2: Create Evaluations
Build test scenarios that exercise identified gaps.

### Step 3: Write Minimal Instructions
Create just enough content to address the gaps.

### Step 4: Validate
```bash
python scripts/quick_validate.py ./my-skill
```

### Step 5: Iterate
Run evaluations -> Identify failures -> Refine instructions -> Repeat.

## Iteration Workflow

After initial deployment:

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes
5. Test again with real scenarios

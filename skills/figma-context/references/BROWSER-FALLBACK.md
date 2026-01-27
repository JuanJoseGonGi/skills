# Browser Fallback Patterns

Complete patterns for extracting Figma design context via browser when MCP is rate-limited.

## Table of Contents
- [Complete Workflow](#complete-workflow)
- [Extraction Patterns by Data Type](#extraction-patterns-by-data-type)
- [Session State Persistence](#session-state-persistence)
- [Selector Reference](#selector-reference)
- [Selector Recovery](#selector-recovery)
- [Free vs Dev Mode](#free-vs-dev-mode)
- [Chrome DevTools MCP Patterns](#chrome-devtools-mcp-patterns)
- [Error Handling](#error-handling)

## Complete Workflow

### Step 1: Verify User Login
Confirm user is logged into Figma. Do not proceed until confirmed.

### Step 2: Navigate to Design
```bash
agent-browser open "https://figma.com/design/{fileKey}/{name}?node-id={nodeId}"
```

### Step 3: Wait for Load
```bash
agent-browser wait 3000
# Or wait for specific element:
agent-browser wait --text "Properties"
```

### Step 4: Extract Needed Data
Use patterns below based on what's needed.

### Step 5: Close Immediately
```bash
agent-browser close
```

## Extraction Patterns by Data Type

### Pattern A: Screenshot Only
**Use when:** Visual reference is sufficient, lowest token cost.

```bash
agent-browser open "{figma_url}"
agent-browser wait 3000
agent-browser screenshot ./figma-design.png
agent-browser close
```

### Pattern B: Layer Structure
**Use when:** Need hierarchy and layer names.

```bash
agent-browser open "{figma_url}"
agent-browser wait --text "Layers"
# Layers panel is in left sidebar
agent-browser snapshot -i -s "[data-testid='left-panel']"
# Refs like @e1, @e2 will show layer names
# Extract specific layers:
agent-browser get text @e{N}
agent-browser close
```

### Pattern C: Design Properties (Dev Mode)
**Use when:** Need colors, typography, spacing specs.

```bash
agent-browser open "{figma_url}"
agent-browser press "Shift+D"  # Toggle Dev Mode
agent-browser wait 2000
agent-browser snapshot -i -s "[data-testid='right-panel']"
# Parse property values from refs
agent-browser close
```

### Pattern D: Code Snippets (Dev Mode Only)
**Use when:** Need CSS/Swift/Kotlin code output.

```bash
agent-browser open "{figma_url}"
agent-browser press "Shift+D"
agent-browser wait --text "Code"
agent-browser snapshot -i -s "[data-testid='code-panel']"
# Code content in refs
agent-browser get text @e{code-ref}
agent-browser close
```

### Pattern E: CSS via Right-Click (Free Accounts)
**Use when:** No Dev Mode seat, need basic CSS.

```bash
agent-browser open "{figma_url}"
agent-browser wait 3000
# Select element in canvas (may need click at coordinates)
agent-browser press "Shift+C"  # Copy as CSS shortcut
# CSS now in system clipboard - inform user to paste
agent-browser close
```

### Pattern F: Multiple Extractions (Higher Cost)
**Use when:** Need several data types at once.

```bash
agent-browser open "{figma_url}"
agent-browser press "Shift+D"
agent-browser wait 2000

# Get properties
agent-browser snapshot -i -s "[data-testid='right-panel']"
# Store/parse refs...

# Get layers  
agent-browser snapshot -i -s "[data-testid='left-panel']"
# Store/parse refs...

# Get screenshot
agent-browser screenshot ./design.png

agent-browser close
```

## Session State Persistence

Save login state to avoid re-authentication:

### Initial Login (Once)
```bash
agent-browser open "https://figma.com"
# Instruct user to complete login
agent-browser wait --text "Drafts"  # Or other logged-in indicator
agent-browser state save figma-auth.json
agent-browser close
```

### Subsequent Sessions
```bash
agent-browser state load figma-auth.json
agent-browser open "{figma_url}"
# Already authenticated
```

**Note:** Auth state may expire. If login wall appears, re-run initial login flow.

## Selector Reference

Known Figma UI selectors (may change with Figma updates):

| Element | Primary Selector | Fallback |
|---------|-----------------|----------|
| Right panel (properties) | `[data-testid='right-panel']` | `.right_panel` |
| Left panel (layers) | `[data-testid='left-panel']` | `.layers_panel` |
| Code panel | `[data-testid='code-panel']` | `.code_panel` |
| Properties section | `[data-testid='properties']` | `.properties_panel` |
| Canvas | `canvas` | `.fig-canvas` |
| Dev Mode toggle | `[data-testid='dev-mode-toggle']` | — |

## Selector Recovery

When selectors fail (Figma updated their UI):

### Step 1: Full Page Snapshot
```bash
agent-browser snapshot -i
```

### Step 2: Identify Panel Refs
Look for refs containing "Properties", "Layers", "Code", etc. in the output.

### Step 3: Use Refs Directly
```bash
agent-browser get text @e{identified-ref}
```

### Step 4: Document Working Selectors
Note which selectors/refs worked for future reference.

## Free vs Dev Mode

| Feature | Free Account | Dev Mode |
|---------|--------------|----------|
| Dimensions | Yes | Yes |
| Colors (hex) | Yes | Yes |
| Design variables | No | Yes |
| CSS snippets | Right-click only | Panel |
| Multi-language code | No | Yes (CSS, Swift, Kotlin, etc.) |
| Typography tokens | No | Yes |
| Spacing display | Manual measurement | Auto |
| Component properties | Limited | Full |

**Free account workarounds:**
- Use `Shift+C` to copy CSS via keyboard
- Measure spacing by selecting multiple elements
- Extract hex colors from Properties panel

## Chrome DevTools MCP Patterns

Alternative when `agent-browser` unavailable. Requires browser open with DevTools.

### Navigate
```
mcp_chrome-devtools_navigate_page(url="{figma_url}")
```

### Wait
```
mcp_chrome-devtools_wait_for(text="Properties")
```

### Snapshot
```
mcp_chrome-devtools_take_snapshot()
```

### Screenshot
```
mcp_chrome-devtools_take_screenshot()
```

### Click Element
```
mcp_chrome-devtools_click(uid="{ref}")
```

### Get Text
```
mcp_chrome-devtools_evaluate_script(function="(el) => el.innerText", args=[{uid: "{ref}"}])
```

### Press Key
```
mcp_chrome-devtools_press_key(key="Shift+D")
```

### Close
```
mcp_chrome-devtools_close_page(pageId={id})
```

## Error Handling

### Login Wall Appears
**Cause:** User not logged in or session expired.
**Solution:** 
1. Stop automation
2. Instruct user to log in manually
3. Save new auth state
4. Retry

### Selector Not Found
**Cause:** Figma UI changed or wrong selector.
**Solution:**
1. Run full page `snapshot -i`
2. Identify elements from refs
3. Use refs directly

### Canvas Blank / Not Rendering
**Cause:** Page not fully loaded or permissions issue.
**Solution:**
1. Increase wait: `agent-browser wait 5000`
2. Verify URL is correct
3. Check if file requires access permissions

### Dev Mode Not Available
**Cause:** User on free plan without Dev seat.
**Solution:**
1. Use free account patterns
2. Right-click CSS copy (`Shift+C`)
3. Extract from basic Properties panel

### Rate Limit in Browser
**Cause:** Rapid page loads triggered Figma's browser-side limits.
**Solution:**
1. Add delays between extractions
2. Reduce extraction frequency
3. Wait and retry

### Element Not Interactable
**Cause:** Element hidden, covered, or not loaded.
**Solution:**
1. Wait longer for load
2. Scroll element into view: `agent-browser scrollintoview @ref`
3. Check if modal/overlay is blocking

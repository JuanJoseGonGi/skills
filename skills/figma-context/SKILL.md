---
name: figma-context
description: Obtains Figma design context with browser fallback when MCP is rate-limited. Use when implementing UI from Figma and MCP returns rate limit errors, user mentions being rate-limited, or browser-based extraction is explicitly needed. Complements the official implement-design skill.
---

# Figma Context with Browser Fallback

Provides design context extraction from Figma using MCP (primary) or browser automation (fallback). Use when MCP is rate-limited or unavailable.

## When to Use This Skill

- MCP returns rate limit or quota error (e.g., "429 Too Many Requests")
- User says "I'm rate limited" or "MCP isn't working"
- User has Starter plan (6 calls/month limit)
- Browser-based extraction explicitly requested

For normal MCP-based implementation, use the official `implement-design` skill.

## Decision Flow

```
1. Have Figma URL with node-id?
   ├─ No → Ask user for URL (format: figma.com/design/:fileKey/:name?node-id=X-Y)
   └─ Yes → Continue

2. Try MCP first
   ├─ get_design_context succeeds → Use context, done
   └─ Error (rate limit, quota, 429) → Continue to fallback

3. Browser fallback needed
   ├─ Ensure user logged into Figma browser
   └─ Use browser extraction patterns
```

## Rate Limit Detection

### Automatic (from MCP response)
- Error contains: "rate limit", "quota exceeded", "429", "too many requests"
- Response indicates usage exceeded

### User-Stated
- User mentions: rate limits, quota, MCP errors, Starter plan limits
- User explicitly requests browser method

## Browser Fallback

### Prerequisites

Before browser automation, user must be logged into Figma.

**Instruct user:**
> "I need to access Figma through the browser to work around the rate limit.
> Please:
> 1. Open your browser and go to figma.com
> 2. Log in to your Figma account  
> 3. Tell me when you're ready"

Wait for confirmation before proceeding.

### Token Efficiency Rules (CRITICAL)

Browser automation consumes significantly more tokens than MCP. Follow strictly:

| Rule | Why |
|------|-----|
| Never browse exploratorily | Each snapshot costs tokens |
| Use targeted selectors | Full page snapshots are expensive |
| Extract once per panel | Don't re-snapshot unchanged DOM |
| Close immediately after | Don't leave browser idle |
| Prefer screenshot when visual reference suffices | Lower token cost than DOM parsing |

### Quick Extraction Patterns

#### Screenshot Only (Lowest Cost)
```bash
agent-browser open "{figma_url}"
agent-browser wait 3000
agent-browser screenshot ./design.png
agent-browser close
```

#### Design Properties
```bash
agent-browser open "{figma_url}"
agent-browser press "Shift+D"  # Toggle Dev Mode
agent-browser wait 2000
agent-browser snapshot -i -s "[data-testid='right-panel']"
# Extract from refs
agent-browser close
```

#### Layer Structure
```bash
agent-browser open "{figma_url}"
agent-browser wait --text "Layers"
agent-browser snapshot -i -s "[data-testid='left-panel']"
# Extract layer names from refs
agent-browser close
```

For complete patterns including CSS extraction, selector recovery, and session persistence, see [BROWSER-FALLBACK.md](references/BROWSER-FALLBACK.md).

### Free Account Limitations

Without Dev Mode seat:
- No code snippet panel (use right-click → Copy as CSS)
- No design variables/tokens
- Basic properties only (dimensions, hex colors)
- 6 MCP calls/month

## URL Parsing

Extract `fileKey` and `nodeId` from Figma URLs:

| URL Format | fileKey | nodeId |
|------------|---------|--------|
| `figma.com/design/ABC123/Name?node-id=1-2` | `ABC123` | `1:2` |
| `figma.com/design/ABC/branch/XYZ/Name?node-id=3-4` | `XYZ` | `3:4` |
| `figma.com/file/ABC123/Name?node-id=1-2` | `ABC123` | `1:2` |

Note: Convert `node-id` format from `1-2` to `1:2` for MCP tools.

## Tool Choice: agent-browser vs Chrome DevTools MCP

Both can be used. Choose based on availability:

| Task | agent-browser | chrome-devtools MCP |
|------|---------------|---------------------|
| Navigate | `open {url}` | `navigate_page url={url}` |
| Snapshot | `snapshot -i` | `take_snapshot` |
| Screenshot | `screenshot` | `take_screenshot` |
| Click | `click @ref` | `click uid={ref}` |
| Get text | `get text @ref` | `evaluate_script` |
| Close | `close` | `close_page` |

Chrome DevTools requires browser already open with DevTools attached.

## References

- [BROWSER-FALLBACK.md](references/BROWSER-FALLBACK.md) - Complete browser patterns, selectors, error handling
- [Figma MCP Server Guide](https://github.com/figma/mcp-server-guide) - Official MCP documentation
- [Figma REST API Limits](https://developers.figma.com/docs/rest-api/rate-limits/) - Rate limit details

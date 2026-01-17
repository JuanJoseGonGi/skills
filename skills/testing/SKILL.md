---
name: testing
description: Provides comprehensive testing and TDD guidance. Use for writing tests before implementing new features, creating reproduction tests for bug fixes, running regression tests during refactoring, and checking test coverage during code reviews. Enforces AAA pattern and 100% coverage goal.
---

# Test-First Approach

## 📑 Table of Contents

This skill consists of the following files:

- **SKILL.md** (this file): Overview and when to use.
- **[TDD.md](references/TDD.md)**: TDD cycle and implementation patterns.
- **[TEST-TYPES.md](references/TEST-TYPES.md)**: Test Pyramid (Unit, Integration, E2E).
- **[TESTABLE-DESIGN.md](references/TESTABLE-DESIGN.md)**: Principles of testable design.
- **[REFERENCE.md](references/REFERENCE.md)**: Best practices, coverage, and checklists.

## 🎯 When to Use

- **Implementing new features (create tests before implementation)**
- **Fixing bugs (create reproduction tests)**
- **During refactoring (run regression tests)**
- **During code reviews (check test coverage)**

## 📋 Basic Principles

### Test-First Development

We recommend "TDD (Test-Driven Development)," where tests are written before implementation.

**Basic Cycle:**
```
1. Red (Write a failing test)
   ↓
2. Green (Pass with minimal code)
   ↓
3. Refactor (Improve code quality)
   ↓
Repeat
```

See [TDD.md](references/TDD.md) for details.

### Test Pyramid

```
        /\
       /  \      E2E (Few)
      /____\     Integration Tests (Medium)
     /______\    Unit Tests (Many)
```

**Principles:**
- Create the largest number of Unit Tests.
- Keep Integration Tests moderate.
- Keep E2E Tests to a minimum.

See [TEST-TYPES.md](references/TEST-TYPES.md) for details.

### AAA Pattern (Required)

All tests must follow the **Arrange-Act-Assert** pattern:

```typescript
it('should create user with valid data', () => {
  // Arrange (Preparation)
  const userData = { name: 'John', email: 'john@example.com' }

  // Act (Execution)
  const user = userService.createUser(userData)

  // Assert (Verification)
  expect(user.name).toBe('John')
})
```

## 🎯 Coverage Goals

### Recommended Coverage Standards

```
- Business Logic: 100%
- Utility Functions: 100%
- Controllers: 80% or higher
- UI Components: 70% or higher
```

See [REFERENCE.md](references/REFERENCE.md) for details.

## 🎨 Testable Design

Design principles for writing testable code:

**1. Dependency Injection (DI)**
- Inject dependencies via constructor.
- Design for mockability.

**2. Pure Functions**
- Functions without side effects.
- Same output for the same input.

**3. Interface Abstraction**
- Depend on interfaces rather than concrete classes.
- Easy to create mocks for testing.

See [TESTABLE-DESIGN.md](refereneces/TESTABLE-DESIGN.md) for details.

## 📊 Quick Start

### Basic Flow for New Features

```
1. Write tests first (Red)
   ↓
2. Minimal implementation (Green)
   ↓
3. Refactoring (Refactor)
   ↓
4. Verify coverage
   ↓
5. Done
```

### Basic Flow for Bug Fixes

```
1. Write a test that reproduces the bug
   ↓
2. Verify that the test fails
   ↓
3. Fix the bug
   ↓
4. Verify that the test passes
   ↓
5. Done
```

## 🚀 Practical Examples

### TypeScript + Jest

```typescript
// Test
describe('calculateTotal', () => {
  it('should calculate total with discount', () => {
    expect(calculateTotal([100, 200], 0.1)).toBe(270)
  })
})

// Implementation
function calculateTotal(items: number[], discount: number): number {
  const subtotal = items.reduce((sum, item) => sum + item, 0)
  return subtotal * (1 - discount)
}
```

### E2E Testing (Playwright)

```typescript
test('user registration flow', async ({ page }) => {
  await page.goto('/register')
  await page.fill('#email', 'john@example.com')
  await page.click('button[type="submit"]')
  await expect(page.locator('.success')).toBeVisible()
})
```

## 📋 Minimum Checklist

Check before completing implementation:
- [ ] Does it follow the AAA pattern?
- [ ] Does the test name describe the specification?
- [ ] Has the coverage goal been achieved?
- [ ] Are the tests independent?

See [REFERENCE.md](references/REFERENCE.md) for the full checklist.

## 🔗 Related Skills

- **applying-solid-principles** - Principles for testable design
- **enforcing-type-safety** - Type-safe test code
- **mcp-browser-auto** - E2E test implementation
- **implementing-as-tachikoma** - Developer Agent implementation guide

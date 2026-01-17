# TDD Cycle and Implementation Patterns

This file explains the detailed methodology and implementation patterns for Test-Driven Development (TDD).

## 📋 Table of Contents

- [TDD Cycle](#tdd-cycle)
- [Detailed Implementation Examples](#detailed-implementation-examples)
- [Benefits of TDD](#benefits-of-tdd)
- [Practical TDD Workflow](#practical-tdd-workflow)

## 🔄 TDD Cycle

### The Three Basic Steps

```
1. Red (Write a failing test)
   ↓
2. Green (Pass with minimal code)
   ↓
3. Refactor (Improve code quality)
   ↓
Repeat
```

### Details of Each Step

**Step 1: Red (Write a failing test)**
- Write a test for a feature that doesn't exist yet.
- Verify that the test fails (Red state).
- It is crucial that the test fails for the right reason.

**Step 2: Green (Pass with minimal code)**
- Write the minimum amount of code required to pass the test.
- Prioritize "making it work" over "elegance" at this stage.
- Verify that all tests become Green.

**Step 3: Refactor (Improve code quality)**
- Improve the code while keeping the tests passing.
- Remove duplication and improve readability.
- Perform this while verifying that tests remain Green.

## 💡 Detailed Implementation Examples

### Example 1: Basic Calculation Function

**Step 1: Red (Write test first)**
```typescript
// calculate.test.ts
describe('calculateTotal', () => {
  it('should calculate total with discount', () => {
    expect(calculateTotal([100, 200], 0.1)).toBe(270)
  })
})

// Run test at this point -> FAIL (Function does not exist)
```

**Step 2: Green (Minimal implementation)**
```typescript
// calculate.ts
function calculateTotal(items: number[], discount: number): number {
  const subtotal = items.reduce((sum, item) => sum + item, 0)
  return subtotal * (1 - discount)
}

// Run test -> PASS
```

**Step 3: Refactor**
```typescript
// calculate.ts (After refactoring)
function calculateTotal(items: number[], discount: number): number {
  validateItems(items)
  validateDiscount(discount)

  const subtotal = sumItems(items)
  return applyDiscount(subtotal, discount)
}

function validateItems(items: number[]): void {
  if (!Array.isArray(items)) {
    throw new Error('Items must be an array')
  }
  if (items.some(item => item < 0)) {
    throw new Error('Items must be non-negative')
  }
}

function validateDiscount(discount: number): void {
  if (discount < 0 || discount > 1) {
    throw new Error('Discount must be between 0 and 1')
  }
}

function sumItems(items: number[]): number {
  return items.reduce((sum, item) => sum + item, 0)
}

function applyDiscount(subtotal: number, discount: number): number {
  return subtotal * (1 - discount)
}

// Run test -> PASS (Tests remain green)
```

**Step 4: Adding Tests (Edge cases)**
```typescript
describe('calculateTotal', () => {
  it('should calculate total with discount', () => {
    expect(calculateTotal([100, 200], 0.1)).toBe(270)
  })

  it('should handle empty array', () => {
    expect(calculateTotal([], 0.1)).toBe(0)
  })

  it('should throw error for negative items', () => {
    expect(() => calculateTotal([-100], 0.1)).toThrow('Items must be non-negative')
  })

  it('should throw error for invalid discount', () => {
    expect(() => calculateTotal([100], 1.5)).toThrow('Discount must be between 0 and 1')
  })
})
```

### Example 2: Class-based Implementation

**Step 1: Red (Write test first)**
```typescript
// user-service.test.ts
describe('UserService', () => {
  it('should create user with valid data', () => {
    const userService = new UserService()
    const user = userService.createUser({
      name: 'John Doe',
      email: 'john@example.com'
    })

    expect(user.id).toBeDefined()
    expect(user.name).toBe('John Doe')
    expect(user.email).toBe('john@example.com')
  })
})

// Run test -> FAIL
```

**Step 2: Green (Minimal implementation)**
```typescript
// user-service.ts
interface UserData {
  name: string
  email: string
}

interface User extends UserData {
  id: string
}

class UserService {
  createUser(data: UserData): User {
    return {
      id: crypto.randomUUID(),
      ...data
    }
  }
}

// Run test -> PASS
```

**Step 3: Refactor (Add validation)**
```typescript
// user-service.ts (After refactoring)
class UserService {
  createUser(data: UserData): User {
    this.validateUserData(data)

    return {
      id: this.generateId(),
      name: this.normalizeName(data.name),
      email: this.normalizeEmail(data.email)
    }
  }

  private validateUserData(data: UserData): void {
    if (!data.name || data.name.trim() === '') {
      throw new Error('Name is required')
    }
    if (!this.isValidEmail(data.email)) {
      throw new Error('Invalid email format')
    }
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  private generateId(): string {
    return crypto.randomUUID()
  }

  private normalizeName(name: string): string {
    return name.trim()
  }

  private normalizeEmail(email: string): string {
    return email.toLowerCase().trim()
  }
}

// Run test -> PASS
```

**Step 4: Adding Tests**
```typescript
describe('UserService', () => {
  let service: UserService

  beforeEach(() => {
    service = new UserService()
  })

  it('should create user with valid data', () => {
    const user = service.createUser({
      name: 'John Doe',
      email: 'john@example.com'
    })

    expect(user.id).toBeDefined()
    expect(user.name).toBe('John Doe')
    expect(user.email).toBe('john@example.com')
  })

  it('should normalize email to lowercase', () => {
    const user = service.createUser({
      name: 'John',
      email: 'JOHN@EXAMPLE.COM'
    })

    expect(user.email).toBe('john@example.com')
  })

  it('should trim whitespace from name', () => {
    const user = service.createUser({
      name: '  John Doe  ',
      email: 'john@example.com'
    })

    expect(user.name).toBe('John Doe')
  })

  it('should throw error for empty name', () => {
    expect(() => service.createUser({
      name: '',
      email: 'john@example.com'
    })).toThrow('Name is required')
  })

  it('should throw error for invalid email', () => {
    expect(() => service.createUser({
      name: 'John',
      email: 'invalid-email'
    })).toThrow('Invalid email format')
  })
})
```

## 🎯 Benefits of TDD

### 1. Improved Design
- By writing tests first, you are forced to consider the usability of the API.
- Tends toward modular and loosely coupled designs.

### 2. Role as Documentation
- Test code functions as a specification.
- Usage examples become clear.

### 3. Confidence in Refactoring
- Existing tests allow you to refactor with peace of mind.
- Early detection of regression bugs.

### 4. Reduced Debugging Time
- Bugs are less likely to be introduced.
- Even if introduced, they are discovered early.

### 5. Clear Completion Criteria for Implementation
- It's done when all tests turn Green.

## 🚀 Practical TDD Workflow

### Workflow for New Feature Development

```
1. Verify user stories/requirements
   ↓
2. List test cases
   - Happy path
   - Negative cases
   - Edge cases
   ↓
3. Write the first test (Red)
   ↓
4. Minimal implementation (Green)
   ↓
5. Refactor
   ↓
6. Move to the next test case (Return to step 3)
   ↓
7. All test cases completed
   ↓
8. Verify coverage
   ↓
9. Code review
```

### Workflow for Bug Fixes

```
1. Verify bug report
   ↓
2. Write a test that reproduces the bug
   ↓
3. Verify that the test fails (Red)
   ↓
4. Fix the bug (Green)
   ↓
5. Verify that the test passes
   ↓
6. Add tests for related edge cases
   ↓
7. Refactor
   ↓
8. Run regression tests
```

### Introducing TDD to Legacy Code

```
1. Understand existing code
   ↓
2. Write tests to guarantee current behavior
   ↓
3. Verify that tests pass
   ↓
4. Perform small refactors
   ↓
5. Verify that tests remain Green
   ↓
6. Repeat (Return to step 4)
   ↓
7. Add new features using the normal TDD cycle
```

## 💡 TDD Tips

### Tip 1: Start Small
Don't aim for perfection from the start; begin with the simplest case.

```typescript
// ❌ Bad Example: Complex from the start
it('should calculate total with discount, tax, and shipping', () => {
  // Too complex
})

// ✅ Good Example: Start simple
it('should sum items', () => {
  expect(sumItems([100, 200])).toBe(300)
})
```

### Tip 2: Take One at a Time
Focus on only one test case at a time.

### Tip 3: Trust the Tests
- If a test fails, first check if the test itself is correct.
- If the test is correct, fix the implementation.

### Tip 4: Don't Fear Refactoring
- Green is your chance to refactor.
- Tests give you the confidence to improve the code.

## 🔗 Related Files

- **[SKILL.md](../SKILL.md)** - Back to Overview
- **[TEST-TYPES.md](./TEST-TYPES.md)** - Types of tests
- **[TESTABLE-DESIGN.md](./TESTABLE-DESIGN.md)** - Testable design
- **[REFERENCE.md](./REFERENCE.md)** - Best practices

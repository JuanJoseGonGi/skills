# Test Best Practices and Reference

This file provides best practices for implementing tests, coverage goals, checklists, and command references.

## 📋 Table of Contents

- [Coverage Goals](#coverage-goals)
- [Best Practices](#best-practices)
- [Test Command Reference](#test-command-reference)
- [Implementation Checklist](#implementation-checklist)
- [Troubleshooting](#troubleshooting)

## 🎯 Coverage Goals

### Recommended Coverage by Layer

```
Business Logic Layer:  100% (Required)
Utility Functions:     100% (Required)
Service Layer:         90% or higher (Recommended)
Controller Layer:      80% or higher (Recommended)
UI Component Layer:    70% or higher (Recommended)
Integration Tests:     Main flow (Required)
E2E Tests:             Critical path (Required)
```

### Coverage Metrics

**Metrics to measure:**
1. **Line Coverage**
   - The percentage of executed lines.
   - The most basic indicator.

2. **Branch Coverage**
   - Whether all branches (if/else, etc.) were executed.
   - Verify logical comprehensiveness.

3. **Function Coverage**
   - The percentage of functions called.
   - Detect unused code.

4. **Statement Coverage**
   - The percentage of statements executed.
   - More precise than line coverage.

### Coverage Check Commands

```bash
# Generate coverage report with Jest
npm test -- --coverage

# Generate coverage report with Vitest
npm run test:coverage

# Set coverage thresholds (in package.json or jest.config.js)
{
  "jest": {
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

### Coverage Priorities

**High Priority (100% Mandatory):**
- Business logic
- Validation functions
- Security-related code
- Amount calculation logic
- Data transformation functions

**Medium Priority (80% or higher recommended):**
- API endpoints
- Service layer
- Controllers
- Middleware

**Low Priority (Aspirational Goal):**
- UI components (if they have little logic)
- Configuration files
- Type definition files

## ✅ Best Practices

### Best Practices for Test Structure

#### 1. Thorough Adherence to the AAA Pattern

```typescript
it('should calculate total with discount', () => {
  // Arrange (Preparation)
  const items = [100, 200, 300]
  const discountRate = 0.1

  // Act (Execution)
  const result = calculateTotal(items, discountRate)

  // Assert (Verification)
  expect(result).toBe(540)
})
```

#### 2. Test Names Should Describe the Specification

```typescript
// ❌ Bad Example
it('test 1', () => { ... })
it('user test', () => { ... })

// ✅ Good Example
it('should throw error when email is invalid', () => { ... })
it('should return null when user not found', () => { ... })
it('should calculate discount correctly for multiple items', () => { ... })
```

#### 3. One Test, One Assertion (Principle)

```typescript
// ❌ Bad Example: Multiple assertions
it('should create user', () => {
  const user = createUser(userData)
  expect(user.id).toBeDefined()
  expect(user.name).toBe('John')
  expect(user.email).toBe('john@example.com')
  expect(user.createdAt).toBeInstanceOf(Date)
})

// ✅ Good Example: Split
describe('createUser', () => {
  it('should generate user id', () => {
    const user = createUser(userData)
    expect(user.id).toBeDefined()
  })

  it('should set user name from input', () => {
    const user = createUser({ ...userData, name: 'John' })
    expect(user.name).toBe('John')
  })

  it('should set user email from input', () => {
    const user = createUser({ ...userData, email: 'john@example.com' })
    expect(user.email).toBe('john@example.com')
  })
})
```

#### 4. Independence of Tests

```typescript
// ❌ Bad Example: Dependent on previous test
let user: User

it('should create user', () => {
  user = createUser(userData) // Store in global variable
})

it('should update user', () => {
  updateUser(user.id, { name: 'Jane' }) // Dependent on previous test
})

// ✅ Good Example: Each test is independent
describe('User operations', () => {
  it('should create user', () => {
    const user = createUser(userData)
    expect(user.id).toBeDefined()
  })

  it('should update user', () => {
    const user = createUser(userData) // Prepare independently
    const updated = updateUser(user.id, { name: 'Jane' })
    expect(updated.name).toBe('Jane')
  })
})
```

### Best Practices for Mocks and Stubs

#### 1. Minimum Necessary Mocking

```typescript
// ❌ Bad Example: Excessive mocking
const mockUser = {
  id: '1',
  name: 'John',
  email: 'john@example.com',
  address: { /* ... */ },
  preferences: { /* ... */ },
  // Mock unnecessary fields
}

// ✅ Good Example: Only what's needed
const mockUser = {
  id: '1',
  name: 'John'
}
```

#### 2. Reusing Mocks

```typescript
// ✅ Good Example: Create test helpers
function createMockUser(overrides?: Partial<User>): User {
  return {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
    ...overrides
  }
}

// Usage example
it('should process user', () => {
  const user = createMockUser({ name: 'Jane' })
  // ...
})
```

#### 3. Leveraging Spies

```typescript
// ✅ Good Example: Call implementation while recording the call
const logger = {
  info: jest.fn(), // Spy
  error: jest.fn()
}

const service = new UserService(db, logger)
await service.createUser(userData)

expect(logger.info).toHaveBeenCalledWith(
  expect.stringContaining('User created')
)
```

### Best Practices for Asynchronous Tests

#### 1. Use `async/await`

```typescript
// ❌ Bad Example: Callback hell
it('should fetch user', (done) => {
  fetchUser('1').then((user) => {
    expect(user.name).toBe('John')
    done()
  })
})

// ✅ Good Example: async/await
it('should fetch user', async () => {
  const user = await fetchUser('1')
  expect(user.name).toBe('John')
})
```

#### 2. Error Handling

```typescript
// ✅ Good Example: Testing for errors
it('should throw error for invalid id', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('Invalid ID')
})

// OR
it('should throw error for invalid id', async () => {
  try {
    await fetchUser('invalid')
    fail('Should have thrown error')
  } catch (error) {
    expect(error.message).toBe('Invalid ID')
  }
})
```

#### 3. Setting Timeouts

```typescript
// ✅ Good Example: Timeout setting
it('should complete within 5 seconds', async () => {
  const start = Date.now()
  await longRunningOperation()
  const duration = Date.now() - start

  expect(duration).toBeLessThan(5000)
}, 10000) // Timeout for entire test: 10 seconds
```

## 🛠️ Test Command Reference

### Jest Commands

```bash
# Run all tests
npm test

# Run a specific file only
npm test user.test.ts

# Run tests with pattern matching
npm test -- --testPathPattern=user

# Watch mode (monitors changes)
npm test -- --watch

# Generate coverage report
npm test -- --coverage

# Re-run only failed tests
npm test -- --onlyFailures

# Detailed output
npm test -- --verbose

# Control parallel execution
npm test -- --maxWorkers=4

# Only specific test suite
npm test -- --testNamePattern="should create user"
```

### Vitest Commands

```bash
# Run all tests
npm run test

# Watch mode
npm run test:watch

# UI mode
npm run test:ui

# Coverage
npm run test:coverage

# Specific file
npm run test user.test.ts

# Filter
npm run test -- --grep="user"
```

### Playwright Commands

```bash
# Run all E2E tests
npx playwright test

# Run on specific browser
npx playwright test --project=chromium

# Disable headless mode (debugging)
npx playwright test --headed

# UI mode
npx playwright test --ui

# Debug mode
npx playwright test --debug

# Show report
npx playwright show-report

# Specific test file
npx playwright test login.spec.ts

# Control number of parallel workers
npx playwright test --workers=4
```

### Example Test Script Configuration (package.json)

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:unit": "jest --testPathPattern=unit",
    "test:integration": "jest --testPathPattern=integration",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:all": "npm run test:unit && npm run test:integration && npm run test:e2e"
  }
}
```

## 📝 Implementation Checklist

### Checklist Before Test Implementation

- [ ] Do you understand the requirements?
- [ ] Is the code to be tested already implemented? (Not required for TDD)
- [ ] Is the design testable? (Dependency injection, etc.)
- [ ] Is test data preparation complete?

### Checklist During Test Creation

- [ ] Does it follow the naming convention for test files? (`*.test.ts` or `*.spec.ts`)
- [ ] Does it follow the AAA pattern?
- [ ] Does the test name describe the specification?
- [ ] Did you write tests for the happy path?
- [ ] Did you write tests for negative cases?
- [ ] Did you consider edge cases?
- [ ] Are mocks/stubs used appropriately?
- [ ] Are tests independent? (Not dependent on order)

### Checklist After Test Execution

- [ ] Do all tests pass?
- [ ] Has the coverage goal been achieved?
- [ ] Are there no warnings or error messages?
- [ ] Is the test execution time within acceptable limits? (Unit tests are fast)
- [ ] Do tests also pass in the CI/CD pipeline?

### Checklist During Code Review

- [ ] Is the test code highly readable?
- [ ] Is there no duplicated test code?
- [ ] Are test helpers utilized appropriately?
- [ ] Are magic numbers constantized?
- [ ] Are comments necessary and sufficient?
- [ ] Is test data meaningful? (Avoid `foo`, `bar`, etc.)

### Checklist Before Release

- [ ] Do all tests pass?
- [ ] Did you check the coverage report?
- [ ] Do E2E tests pass?
- [ ] Did you perform performance testing?
- [ ] Did you perform security testing? (CodeGuard, etc.)
- [ ] Did you perform cross-browser testing? (If applicable)

## 🔧 Troubleshooting

### Common Problems and Solutions

#### Problem 1: Flaky Tests

**Symptoms:**
- The same test passes or fails inconsistently.
- Fails in CI/CD but passes locally.

**Causes and Solutions:**
```typescript
// ❌ Cause: Timing dependency
it('should update UI', async () => {
  clickButton()
  expect(getDisplayText()).toBe('Updated') // Verifies before async process completes
})

// ✅ Solution: Wait for completion of async process
it('should update UI', async () => {
  await clickButton()
  await waitFor(() => {
    expect(getDisplayText()).toBe('Updated')
  })
})

// ❌ Cause: Dependent on current time
it('should check expiry', () => {
  const item = { expiryDate: new Date() }
  expect(isExpired(item)).toBe(true) // Result changes based on timing of execution
})

// ✅ Solution: Fix the time
it('should check expiry', () => {
  const now = new Date('2024-01-01')
  const item = { expiryDate: new Date('2023-12-31') }
  expect(isExpired(item, now)).toBe(true)
})
```

#### Problem 2: Slow Tests

**Symptoms:**
- Test execution takes a long time.
- Slow CI/CD pipeline.

**Causes and Solutions:**
```typescript
// ❌ Cause: Uses actual DB
beforeEach(async () => {
  await db.connect()
  await db.migrate()
})

// ✅ Solution: Use in-memory DB or mocks
beforeEach(() => {
  db = createInMemoryDatabase()
})

// ❌ Cause: Unnecessary waiting
await page.waitForTimeout(5000) // Wait 5 seconds

// ✅ Solution: Conditional waiting
await page.waitForSelector('.element', { timeout: 5000 })
```

#### Problem 3: Mocks are not functioning

**Symptoms:**
- Actual function is called despite setting up a mock.
- Test attempts to connect to external dependencies.

**Causes and Solutions:**
```typescript
// ❌ Cause: Timing of mock setup is late
import { fetchUser } from './api'
jest.mock('./api') // Too late after import

// ✅ Solution: Mock before import
jest.mock('./api')
import { fetchUser } from './api'

// OR
beforeEach(() => {
  jest.clearAllMocks()
  jest.resetAllMocks()
})
```

#### Problem 4: Coverage does not increase

**Symptoms:**
- Specific lines are not covered even after writing tests.
- Branch coverage is low.

**Causes and Solutions:**
```typescript
// ❌ Uncovered branch
function processValue(value: number | null): number {
  if (value === null) {
    return 0
  }
  return value * 2
}

// Test (Case for null is not tested)
it('should process value', () => {
  expect(processValue(5)).toBe(10)
})

// ✅ Solution: Test all branches
describe('processValue', () => {
  it('should process valid value', () => {
    expect(processValue(5)).toBe(10)
  })

  it('should return 0 for null', () => {
    expect(processValue(null)).toBe(0)
  })
})
```

### Debugging Techniques

#### 1. `console.log` Debugging

```typescript
it('should calculate total', () => {
  const items = [100, 200]
  const result = calculateTotal(items)

  console.log('Items:', items)
  console.log('Result:', result)

  expect(result).toBe(300)
})
```

#### 2. Using the Debugger

```typescript
it('should process data', () => {
  const data = prepareData()

  debugger // Browser debugger will launch

  const result = processData(data)
  expect(result).toBeDefined()
})

// For Node.js
// node --inspect-brk node_modules/.bin/jest --runInBand
```

#### 3. Isolated Execution of Tests

```bash
# Only specific test
npm test -- --testNamePattern="should calculate total"

# Only specific file
npm test user.test.ts

# Use .only (temporary)
it.only('should calculate total', () => {
  // Only this test will run
})
```

## 📊 Tracking Test Metrics

### Recommended Measurements

1. **Test Coverage**: Maintain 80% or higher.
2. **Test Execution Time**: Within 5 minutes for Unit Tests.
3. **Test Failure Rate**: Goal of 5% or less.
4. **Flaky Test Rate**: Goal of 1% or less.
5. **Trend in Number of Tests**: Maintain an upward trend.

### Test Strategy in CI/CD

```yaml
# Example for GitHub Actions
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit -- --coverage

      - name: Run integration tests
        run: npm run test:integration

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 🔗 Related Files

- **[SKILL.md](../SKILL.md)** - Back to Overview
- **[TDD.md](./TDD.md)** - TDD Cycle
- **[TEST-TYPES.md](./TEST-TYPES.md)** - Test Types
- **[TESTABLE-DESIGN.md](./TESTABLE-DESIGN.md)** - Testable Design

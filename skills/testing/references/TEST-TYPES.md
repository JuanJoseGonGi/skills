# Test Types and the Test Pyramid

This file explains the purpose, implementation methods, and best practices for various types of tests.

## 📋 Table of Contents

- [Test Pyramid](#test-pyramid)
- [Unit Test](#unit-test)
- [Integration Test](#integration-test)
- [End-to-End Test (E2E Test)](#end-to-end-test-e2e-test)
- [How to Choose Tests](#how-to-choose-tests)

## 🔺 Test Pyramid

### Basic Structure

```
        /\
       /  \      E2E (Few, slow, high cost)
      /____\     Integration Tests (Medium, medium speed, medium cost)
     /______\    Unit Tests (Many, fast, low cost)
```

### Ideal Allocation Ratio

```
- Unit Tests: 70%
- Integration Tests: 20%
- E2E Tests: 10%
```

### Reasons for the Pyramid Structure

**Why many lower-level (Unit) tests:**
- Can be executed quickly.
- Easy to identify the cause of failure.
- Low maintenance cost.
- Can be run frequently during development.

**Why few upper-level (E2E) tests:**
- Long execution time.
- Complex environment setup.
- Difficult to identify the cause of failure.
- High maintenance cost.

### Anti-pattern: The Inverted Pyramid (The Ice Cream Cone)

```
     ______      Too many E2E tests
    /      \     Few integration tests
   /________\    Minimal unit tests
      /  \
     /____\
```

**Problems:**
- Test execution takes a long time.
- Slows down CI/CD pipelines.
- Debugging is difficult.
- Maintenance cost is high.

## 🔬 Unit Test

### Purpose and Characteristics

**Purpose:**
- Verify the behavior of individual functions, methods, or classes.
- Run independently from other components.
- Guarantee the accuracy of business logic.

**Characteristics:**
- **Fast**: Executed in milliseconds.
- **Independence**: No external dependencies (DB, API, etc., are mocked).
- **Fine granularity**: Tests only one function/method.
- **High frequency**: Run many times during development.

### Implementation Example (TypeScript + Jest)

#### Basic Unit Test

```typescript
// sum.ts
export function sum(a: number, b: number): number {
  return a + b
}

// sum.test.ts
import { sum } from './sum'

describe('sum', () => {
  it('should add two positive numbers', () => {
    expect(sum(2, 3)).toBe(5)
  })

  it('should add negative numbers', () => {
    expect(sum(-2, -3)).toBe(-5)
  })

  it('should handle zero', () => {
    expect(sum(0, 5)).toBe(5)
  })
})
```

#### Unit Test Using Mocks

```typescript
// user-service.ts
export class UserService {
  constructor(private db: Database) {}

  async getUser(id: string): Promise<User | null> {
    return await this.db.findUser(id)
  }
}

// user-service.test.ts
import { UserService } from './user-service'

describe('UserService', () => {
  let mockDb: jest.Mocked<Database>
  let service: UserService

  beforeEach(() => {
    // Mock the database
    mockDb = {
      findUser: jest.fn()
    } as any

    service = new UserService(mockDb)
  })

  it('should return user when found', async () => {
    const mockUser = { id: '1', name: 'John' }
    mockDb.findUser.mockResolvedValue(mockUser)

    const result = await service.getUser('1')

    expect(result).toEqual(mockUser)
    expect(mockDb.findUser).toHaveBeenCalledWith('1')
  })

  it('should return null when user not found', async () => {
    mockDb.findUser.mockResolvedValue(null)

    const result = await service.getUser('999')

    expect(result).toBeNull()
  })
})
```

#### Edge Case Testing

```typescript
// validation.ts
export function validateEmail(email: string): boolean {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}

// validation.test.ts
describe('validateEmail', () => {
  // Happy path
  it('should accept valid email', () => {
    expect(validateEmail('user@example.com')).toBe(true)
  })

  // Negative cases
  it('should reject email without @', () => {
    expect(validateEmail('userexample.com')).toBe(false)
  })

  it('should reject email without domain', () => {
    expect(validateEmail('user@')).toBe(false)
  })

  // Edge cases
  it('should reject empty string', () => {
    expect(validateEmail('')).toBe(false)
  })

  it('should reject email with spaces', () => {
    expect(validateEmail('user @example.com')).toBe(false)
  })
})
```

### Best Practices for Unit Testing

**1. One Test, One Assertion Principle (as much as possible)**
```typescript
// ❌ Bad Example: Multiple verifications
it('should create and validate user', () => {
  const user = createUser({ name: 'John' })
  expect(user.name).toBe('John')
  expect(user.id).toBeDefined()
  expect(user.createdAt).toBeInstanceOf(Date)
})

// ✅ Good Example: Split
it('should set user name', () => {
  const user = createUser({ name: 'John' })
  expect(user.name).toBe('John')
})

it('should generate user id', () => {
  const user = createUser({ name: 'John' })
  expect(user.id).toBeDefined()
})
```

**2. Test names should describe the specification**
```typescript
// ❌ Bad Example
it('test user creation', () => { ... })

// ✅ Good Example
it('should throw error when email is invalid', () => { ... })
```

**3. Mock external dependencies**
```typescript
// ✅ Good Example: Mock the database
const mockDb = { save: jest.fn() }

// ❌ Bad Example: Connect to actual DB (this is an Integration Test)
const db = new Database('localhost:5432')
```

## 🔗 Integration Test

### Purpose and Characteristics

**Purpose:**
- Verify interaction between multiple components.
- Confirm integration with databases, external APIs, etc.
- Guarantee that parts of the system work correctly together.

**Characteristics:**
- **Medium speed**: Executed in seconds.
- **Partial integration**: Combines parts of the system.
- **Close to production**: Uses test DBs or APIs.
- **Medium frequency**: Run before commits or in CI/CD.

### Implementation Example (TypeScript + Jest)

#### Database Integration Test

```typescript
// user-repository.test.ts
import { UserRepository } from './user-repository'
import { setupTestDatabase, teardownTestDatabase } from './test-utils'

describe('UserRepository Integration Tests', () => {
  let db: Database
  let repository: UserRepository

  beforeAll(async () => {
    // Setup test DB
    db = await setupTestDatabase()
  })

  afterAll(async () => {
    // Cleanup test DB
    await teardownTestDatabase(db)
  })

  beforeEach(async () => {
    // Clear data before each test
    await db.query('DELETE FROM users')
    repository = new UserRepository(db)
  })

  it('should save and retrieve user', async () => {
    // Arrange
    const userData = {
      name: 'John Doe',
      email: 'john@example.com'
    }

    // Act
    const savedUser = await repository.save(userData)
    const retrievedUser = await repository.findById(savedUser.id)

    // Assert
    expect(retrievedUser).toEqual(savedUser)
  })

  it('should update existing user', async () => {
    const user = await repository.save({
      name: 'John',
      email: 'john@example.com'
    })

    const updated = await repository.update(user.id, {
      name: 'John Doe'
    })

    expect(updated.name).toBe('John Doe')
    expect(updated.email).toBe('john@example.com')
  })
})
```

#### API Integration Test

```typescript
// api.test.ts
import request from 'supertest'
import { app } from './app'
import { setupTestDatabase } from './test-utils'

describe('User API Integration Tests', () => {
  beforeAll(async () => {
    await setupTestDatabase()
  })

  describe('POST /users', () => {
    it('should create new user', async () => {
      const response = await request(app)
        .post('/users')
        .send({
          name: 'John Doe',
          email: 'john@example.com'
        })
        .expect(201)

      expect(response.body).toMatchObject({
        name: 'John Doe',
        email: 'john@example.com'
      })
      expect(response.body.id).toBeDefined()
    })

    it('should return 400 for invalid email', async () => {
      await request(app)
        .post('/users')
        .send({
          name: 'John',
          email: 'invalid-email'
        })
        .expect(400)
    })
  })

  describe('GET /users/:id', () => {
    it('should return user by id', async () => {
      // Create user first
      const createResponse = await request(app)
        .post('/users')
        .send({ name: 'John', email: 'john@example.com' })

      const userId = createResponse.body.id

      // Retrieve created user
      const response = await request(app)
        .get(`/users/${userId}`)
        .expect(200)

      expect(response.body).toMatchObject({
        id: userId,
        name: 'John'
      })
    })
  })
})
```

### Best Practices for Integration Testing

**1. Independence of Test Data**
```typescript
beforeEach(async () => {
  // Clear data before each test
  await db.query('TRUNCATE TABLE users CASCADE')
})
```

**2. Isolation of Test Environment**
```typescript
// ❌ Bad Example: Use production DB
const db = new Database(process.env.PRODUCTION_DB_URL)

// ✅ Good Example: Dedicated test DB
const db = new Database(process.env.TEST_DB_URL)
```

**3. Leverage Transactions**
```typescript
let transaction: Transaction

beforeEach(async () => {
  transaction = await db.beginTransaction()
})

afterEach(async () => {
  await transaction.rollback() // Rollback after test
})
```

## 🌐 End-to-End Test (E2E Test)

### Purpose and Characteristics

**Purpose:**
- Verify system-wide behavior from a user's perspective.
- Simulate actual user flows.
- Comprehensive confirmation including UI, backend, and database.

**Characteristics:**
- **Slow**: Takes seconds to minutes.
- **Complete integration**: Connects the entire system.
- **Production environment**: Runs in an environment close to production.
- **Low frequency**: Run before release or in CI.

### Implementation Example (Playwright)

#### Basic E2E Test

```typescript
// login.spec.ts
import { test, expect } from '@playwright/test'

test.describe('User Login Flow', () => {
  test('should successfully login with valid credentials', async ({ page }) => {
    // Arrange: Go to login page
    await page.goto('/login')

    // Act: Enter credentials
    await page.fill('input[name="email"]', 'user@example.com')
    await page.fill('input[name="password"]', 'password123')
    await page.click('button[type="submit"]')

    // Assert: Redirect to dashboard
    await expect(page).toHaveURL('/dashboard')
    await expect(page.locator('h1')).toContainText('Welcome')
  })

  test('should show error message with invalid credentials', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[name="email"]', 'wrong@example.com')
    await page.fill('input[name="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')

    // Error message is displayed
    await expect(page.locator('.error-message')).toBeVisible()
    await expect(page.locator('.error-message')).toContainText('Invalid credentials')
  })
})
```

#### Complex User Flow

```typescript
// checkout.spec.ts
test('should complete purchase flow', async ({ page }) => {
  // 1. Login
  await page.goto('/login')
  await page.fill('[name="email"]', 'user@example.com')
  await page.fill('[name="password"]', 'password')
  await page.click('[type="submit"]')

  // 2. Add product to cart
  await page.goto('/products')
  await page.click('button[data-product-id="123"]')
  await expect(page.locator('.cart-count')).toContainText('1')

  // 3. Verify cart
  await page.click('[href="/cart"]')
  await expect(page.locator('.cart-item')).toHaveCount(1)

  // 4. Checkout
  await page.click('button:has-text("Checkout")')

  // 5. Enter shipping info
  await page.fill('[name="address"]', '123 Main St')
  await page.fill('[name="city"]', 'Tokyo')
  await page.fill('[name="zipcode"]', '100-0001')

  // 6. Enter payment info
  await page.fill('[name="cardNumber"]', '4242424242424242')
  await page.fill('[name="expiry"]', '12/25')
  await page.fill('[name="cvv"]', '123')

  // 7. Place order
  await page.click('button:has-text("Place Order")')

  // 8. Confirmation page
  await expect(page.locator('.success-message')).toBeVisible()
  await expect(page.locator('.order-number')).toBeVisible()
})
```

#### Visual Regression Testing

```typescript
test('should match screenshot', async ({ page }) => {
  await page.goto('/dashboard')

  // Compare screenshots
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixels: 100 // Allowed difference in pixels
  })
})
```

### Best Practices for E2E Testing

**1. Use Page Object Pattern**
```typescript
// pages/login-page.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email)
    await this.page.fill('[name="password"]', password)
    await this.page.click('[type="submit"]')
  }

  async getErrorMessage() {
    return await this.page.locator('.error-message').textContent()
  }
}

// login.spec.ts
test('should login', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.goto()
  await loginPage.login('user@example.com', 'password')

  await expect(page).toHaveURL('/dashboard')
})
```

**2. Prepare Test Data**
```typescript
test.beforeEach(async ({ page, request }) => {
  // Create test user via API
  await request.post('/api/test/users', {
    data: {
      email: 'test@example.com',
      password: 'password'
    }
  })
})
```

**3. Waiting Strategy**
```typescript
// ❌ Bad Example: Wait for fixed time
await page.waitForTimeout(3000)

// ✅ Good Example: Wait for element appearance
await page.waitForSelector('.dashboard')

// ✅ Good Example: Wait for network idle
await page.waitForLoadState('networkidle')
```

## 🎯 How to Choose Tests

### Decision Flowchart

```
What are you testing?
    ↓
Individual function/method?
    ├─ Yes → Unit Test
    └─ No → Multiple components?
        ├─ Yes → Integration Test
        └─ No → Entire user flow?
            └─ Yes → E2E Test
```

### Choice by Example

| Test Target | Test Type | Reason |
|-----------|-----------|------|
| Validation function | Unit Test | No other dependencies, can be verified quickly |
| API endpoint | Integration Test | Includes interaction with DB |
| From login to dashboard display | E2E Test | Entire flow from UI to DB |
| Calculation logic | Unit Test | Pure function, no external dependencies |
| Data persistence | Integration Test | Interaction with DB is required |
| Payment flow | E2E Test | Multiple screens, external API interaction |

### Balancing Tests

**Recommended Approach:**
1. **First, build a foundation with Unit Tests**
   - Cover 100% of business logic.
   - Early bug detection.

2. **Verify interactions with Integration Tests**
   - Integration tests for critical APIs.
   - Verify DB interaction parts.

3. **Guarantee major flows with E2E**
   - Only for critical user flows.
   - Keep the number to a minimum.

**Target time allocation:**
- Unit test creation: 50%
- Integration test creation: 30%
- E2E test creation: 20%

## 🔗 Related Files

- **[SKILL.md](../SKILL.md)** - Back to Overview
- **[TDD.md](./TDD.md)** - TDD Cycle
- **[TESTABLE-DESIGN.md](./TESTABLE-DESIGN.md)** - Testable Design
- **[REFERENCE.md](./REFERENCE.md)** - Best Practices

# Testable Design Principles

This file explains detailed design principles and implementation patterns for writing testable code.

## 📋 Table of Contents

- [Importance of Testability](#importance-of-testability)
- [Dependency Injection (DI)](#dependency-injection-di)
- [Pure Functions](#pure-functions)
- [Interface Abstraction](#interface-abstraction)
- [Other Design Principles](#other-design-principles)
- [Anti-patterns](#anti-patterns)

## 🎯 Importance of Testability

### What is Testable Code?

**Definition:**
- Can be tested independently
- Dependencies are explicit
- Side effects are predictable
- Mocking/Stubbing is easy

**Benefits:**
- Early bug detection
- Refactoring safety
- Value as documentation
- Improved design quality

### Factors Inhibiting Testability

**1. Hidden Dependencies**
```typescript
// ❌ Bad Example: Dependent on global state
class UserService {
  getUser(id: string) {
    return globalDatabase.find(id) // Difficult to test
  }
}
```

**2. Many Side Effects**
```typescript
// ❌ Bad Example: Too many side effects
function processOrder(order: Order) {
  sendEmail(order.email)        // Send email
  updateInventory(order.items)  // Update inventory
  logToFile(order)              // Log to file
  return calculateTotal(order)
}
```

**3. Tight Coupling**
```typescript
// ❌ Bad Example: Directly dependent on a concrete class
class OrderService {
  private db = new PostgresDatabase() // Tightly coupled

  async saveOrder(order: Order) {
    return await this.db.save(order)
  }
}
```

## 💉 Dependency Injection (DI)

### Basic Concept

**Principles:**
- Inject dependent objects from the outside.
- Accept via constructor, method, or property.
- Do not use `new` internally.

### Constructor Injection (Recommended)

```typescript
// ✅ Good Example: Inject via constructor
interface Database {
  save(data: any): Promise<void>
  find(id: string): Promise<any>
}

class UserService {
  // Receive dependency via constructor
  constructor(private db: Database) {}

  async createUser(userData: UserData): Promise<User> {
    const user = { ...userData, id: generateId() }
    await this.db.save(user)
    return user
  }

  async getUser(id: string): Promise<User | null> {
    return await this.db.find(id)
  }
}

// Inject mock during testing
const mockDb: Database = {
  save: jest.fn(),
  find: jest.fn()
}
const service = new UserService(mockDb)
```

### Method Injection

```typescript
// ✅ Good Example: Inject via method
class ReportGenerator {
  generateReport(data: Data, formatter: Formatter): string {
    const processed = this.processData(data)
    return formatter.format(processed) // Use injected formatter
  }

  private processData(data: Data) {
    // Data processing logic
    return processed
  }
}

// During testing
const mockFormatter = { format: jest.fn().mockReturnValue('formatted') }
const generator = new ReportGenerator()
const result = generator.generateReport(data, mockFormatter)
```

### Property Injection

```typescript
// ✅ Good Example: Inject via property (used in frameworks)
class EmailService {
  // Declare dependency as a property
  logger?: Logger

  async sendEmail(to: string, subject: string, body: string) {
    try {
      await this.send(to, subject, body)
      this.logger?.info(`Email sent to ${to}`)
    } catch (error) {
      this.logger?.error(`Failed to send email: ${error}`)
      throw error
    }
  }
}

// During testing
const service = new EmailService()
service.logger = mockLogger
```

### Testing Example for DI

```typescript
// user-service.test.ts
describe('UserService', () => {
  let mockDb: jest.Mocked<Database>
  let service: UserService

  beforeEach(() => {
    // Prepare mock DB
    mockDb = {
      save: jest.fn(),
      find: jest.fn()
    }

    // Inject mock via DI
    service = new UserService(mockDb)
  })

  it('should create user', async () => {
    const userData = { name: 'John', email: 'john@example.com' }

    await service.createUser(userData)

    expect(mockDb.save).toHaveBeenCalledWith(
      expect.objectContaining(userData)
    )
  })

  it('should get user by id', async () => {
    const mockUser = { id: '1', name: 'John' }
    mockDb.find.mockResolvedValue(mockUser)

    const result = await service.getUser('1')

    expect(result).toEqual(mockUser)
    expect(mockDb.find).toHaveBeenCalledWith('1')
  })
})
```

## 🔬 Pure Functions

### Definition and Characteristics

**Conditions for a Pure Function:**
1. Same output for the same input
2. No side effects (doesn't modify external state)
3. No dependency on external state

**Benefits:**
- Easy to test
- Parallel processing safe
- Predictable results
- Memoization possible

### Examples of Pure Functions

```typescript
// ✅ Pure functions
function add(a: number, b: number): number {
  return a + b
}

function calculateDiscount(price: number, rate: number): number {
  return price * (1 - rate)
}

function formatName(firstName: string, lastName: string): string {
  return `${lastName}, ${firstName}`
}

// Tests
describe('Pure Functions', () => {
  it('should always return same result', () => {
    expect(add(2, 3)).toBe(5)
    expect(add(2, 3)).toBe(5) // Always the same no matter how many times it's run
  })

  it('should not have side effects', () => {
    const price = 100
    calculateDiscount(price, 0.1)
    expect(price).toBe(100) // Original value doesn't change
  })
})
```

### Making Impure Functions Pure

```typescript
// ❌ Impure function: Modifies external state
let total = 0
function addToTotal(value: number): void {
  total += value // Side effect
}

// ✅ Pure function: Returns a new value
function calculateNewTotal(currentTotal: number, value: number): number {
  return currentTotal + value
}

// ❌ Impure function: Directly modifies array
function sortItems(items: number[]): number[] {
  return items.sort() // Modifies original array
}

// ✅ Pure function: Returns a new array
function sortItems(items: number[]): number[] {
  return [...items].sort() // Sort a copy
}
```

### Passing External Dependencies as Arguments

```typescript
// ❌ Impure function: Dependent on current time
function isExpired(expiryDate: Date): boolean {
  return expiryDate < new Date() // Result changes depending on when it's run
}

// ✅ Pure function: Current time passed as an argument
function isExpired(expiryDate: Date, now: Date): boolean {
  return expiryDate < now
}

// Test
it('should check expiry correctly', () => {
  const expiryDate = new Date('2024-01-01')
  const now = new Date('2024-06-01')

  expect(isExpired(expiryDate, now)).toBe(true)
})
```

### Segregation of Side Effects

```typescript
// ✅ Good Example: Segregate logic and side effects
class OrderProcessor {
  // Pure function: Business logic
  calculateOrderTotal(items: Item[]): number {
    return items.reduce((sum, item) => sum + item.price, 0)
  }

  validateOrder(order: Order): ValidationResult {
    const errors: string[] = []

    if (order.items.length === 0) {
      errors.push('Order must have at least one item')
    }

    if (order.total < 0) {
      errors.push('Total cannot be negative')
    }

    return {
      isValid: errors.length === 0,
      errors
    }
  }

  // Function containing side effects: Explicitly segregated
  async processOrder(order: Order): Promise<void> {
    // 1. Validate with pure function
    const validation = this.validateOrder(order)
    if (!validation.isValid) {
      throw new Error(validation.errors.join(', '))
    }

    // 2. Execute side effects (DB, email, etc.)
    await this.saveOrder(order)
    await this.sendConfirmationEmail(order)
    await this.updateInventory(order.items)
  }
}
```

## 🏗️ Interface Abstraction

### Basic Principle

**Dependency Inversion Principle (DIP):**
- High-level modules should not depend on low-level modules.
- Both should depend on abstractions (interfaces).

### Interface Definition

```typescript
// ✅ Define abstraction (interface)
interface EmailProvider {
  send(to: string, subject: string, body: string): Promise<void>
}

interface Logger {
  info(message: string): void
  error(message: string, error?: Error): void
}

interface CacheService {
  get(key: string): Promise<any>
  set(key: string, value: any, ttl?: number): Promise<void>
  delete(key: string): Promise<void>
}
```

### Switching Implementations

```typescript
// Production implementation
class SendGridEmailProvider implements EmailProvider {
  async send(to: string, subject: string, body: string): Promise<void> {
    // Use SendGrid API
    await sendgridClient.send({ to, subject, html: body })
  }
}

// Testing implementation
class MockEmailProvider implements EmailProvider {
  sentEmails: Array<{ to: string; subject: string; body: string }> = []

  async send(to: string, subject: string, body: string): Promise<void> {
    this.sentEmails.push({ to, subject, body })
  }
}

// Service (depends on interface)
class UserRegistrationService {
  constructor(
    private emailProvider: EmailProvider, // Dependency on abstraction
    private logger: Logger
  ) {}

  async registerUser(userData: UserData): Promise<User> {
    const user = await this.createUser(userData)

    // Use via interface
    await this.emailProvider.send(
      user.email,
      'Welcome!',
      'Thank you for registering'
    )

    this.logger.info(`User registered: ${user.id}`)

    return user
  }
}

// Test
describe('UserRegistrationService', () => {
  it('should send welcome email', async () => {
    const mockEmail = new MockEmailProvider()
    const mockLogger = { info: jest.fn(), error: jest.fn() }
    const service = new UserRegistrationService(mockEmail, mockLogger)

    await service.registerUser({ email: 'user@example.com' })

    expect(mockEmail.sentEmails).toHaveLength(1)
    expect(mockEmail.sentEmails[0].to).toBe('user@example.com')
  })
})
```

### Strategy Pattern

```typescript
// ✅ Good Example: Abstracting strategy
interface PaymentStrategy {
  processPayment(amount: number): Promise<PaymentResult>
}

class CreditCardPayment implements PaymentStrategy {
  async processPayment(amount: number): Promise<PaymentResult> {
    // Credit card payment
    return { success: true, transactionId: 'CC123' }
  }
}

class PayPalPayment implements PaymentStrategy {
  async processPayment(amount: number): Promise<PaymentResult> {
    // PayPal payment
    return { success: true, transactionId: 'PP456' }
  }
}

class PaymentService {
  constructor(private strategy: PaymentStrategy) {}

  async pay(amount: number): Promise<PaymentResult> {
    return await this.strategy.processPayment(amount)
  }
}

// Test
describe('PaymentService', () => {
  it('should process payment with strategy', async () => {
    const mockStrategy: PaymentStrategy = {
      processPayment: jest.fn().mockResolvedValue({
        success: true,
        transactionId: 'TEST123'
      })
    }

    const service = new PaymentService(mockStrategy)
    const result = await service.pay(100)

    expect(result.success).toBe(true)
    expect(mockStrategy.processPayment).toHaveBeenCalledWith(100)
  })
})
```

## 🎨 Other Design Principles

### Single Responsibility Principle (SRP)

```typescript
// ❌ Bad Example: Multiple responsibilities
class UserManager {
  createUser(data: UserData) { /* ... */ }
  validateEmail(email: string) { /* ... */ }
  sendWelcomeEmail(user: User) { /* ... */ }
  generateReport() { /* ... */ }
}

// ✅ Good Example: Segregate responsibilities
class UserService {
  createUser(data: UserData): User { /* ... */ }
}

class EmailValidator {
  validate(email: string): boolean { /* ... */ }
}

class EmailService {
  sendWelcomeEmail(user: User): void { /* ... */ }
}

class ReportGenerator {
  generateUserReport(): Report { /* ... */ }
}
```

### Small Methods

```typescript
// ❌ Bad Example: Long method
class OrderService {
  processOrder(order: Order) {
    // Validation (20 lines)
    if (!order.items || order.items.length === 0) { /* ... */ }
    // Inventory check (30 lines)
    for (const item of order.items) { /* ... */ }
    // Amount calculation (20 lines)
    let total = 0
    // Payment processing (40 lines)
    // Email sending (15 lines)
  }
}

// ✅ Good Example: Split into small methods
class OrderService {
  processOrder(order: Order) {
    this.validateOrder(order)
    this.checkInventory(order)
    const total = this.calculateTotal(order)
    this.processPayment(order, total)
    this.sendConfirmation(order)
  }

  private validateOrder(order: Order): void { /* ... */ }
  private checkInventory(order: Order): void { /* ... */ }
  private calculateTotal(order: Order): number { /* ... */ }
  private processPayment(order: Order, total: number): void { /* ... */ }
  private sendConfirmation(order: Order): void { /* ... */ }
}
```

### Factory Pattern

```typescript
// ✅ Good Example: Abstracting creation with a factory
interface NotificationService {
  send(message: string): void
}

class NotificationFactory {
  static create(type: 'email' | 'sms' | 'push'): NotificationService {
    switch (type) {
      case 'email':
        return new EmailNotification()
      case 'sms':
        return new SmsNotification()
      case 'push':
        return new PushNotification()
    }
  }
}

// Use mock factory during testing
class MockNotificationFactory {
  static create(): NotificationService {
    return { send: jest.fn() }
  }
}
```

## ⚠️ Anti-patterns

### Singleton

```typescript
// ❌ Bad Example: Difficult to test
class DatabaseSingleton {
  private static instance: DatabaseSingleton

  private constructor() {}

  static getInstance(): DatabaseSingleton {
    if (!DatabaseSingleton.instance) {
      DatabaseSingleton.instance = new DatabaseSingleton()
    }
    return DatabaseSingleton.instance
  }

  query(sql: string) { /* ... */ }
}

// Problem: Cannot mock during testing
class UserService {
  getUser(id: string) {
    const db = DatabaseSingleton.getInstance() // Tightly coupled
    return db.query(`SELECT * FROM users WHERE id = ${id}`)
  }
}

// ✅ Good Example: Use DI
class UserService {
  constructor(private db: Database) {} // Injectable

  getUser(id: string) {
    return this.db.query(`SELECT * FROM users WHERE id = ${id}`)
  }
}
```

### Overuse of Static Methods

```typescript
// ❌ Bad Example: Dependent on static methods
class Utils {
  static getCurrentTime(): Date {
    return new Date() // Difficult to test
  }
}

class OrderService {
  createOrder(items: Item[]) {
    const now = Utils.getCurrentTime() // Non-mockable
    return { items, createdAt: now }
  }
}

// ✅ Good Example: Inject time
interface Clock {
  now(): Date
}

class OrderService {
  constructor(private clock: Clock) {}

  createOrder(items: Item[]) {
    const now = this.clock.now() // Mockable during testing
    return { items, createdAt: now }
  }
}

// Test
const mockClock = { now: () => new Date('2024-01-01') }
const service = new OrderService(mockClock)
```

### Direct Use of `new` Operator

```typescript
// ❌ Bad Example: internal new
class OrderService {
  processOrder(order: Order) {
    const emailService = new EmailService() // Tightly coupled
    emailService.send(order.email, 'Confirmation', '...')
  }
}

// ✅ Good Example: Inject dependency
class OrderService {
  constructor(private emailService: EmailService) {}

  processOrder(order: Order) {
    this.emailService.send(order.email, 'Confirmation', '...')
  }
}
```

### Dependency on Global State

```typescript
// ❌ Bad Example: Dependent on global variable
let currentUser: User | null = null

class OrderService {
  createOrder(items: Item[]) {
    if (!currentUser) { // Dependent on global state
      throw new Error('Not authenticated')
    }
    return { items, userId: currentUser.id }
  }
}

// ✅ Good Example: Explicitly pass state
class OrderService {
  createOrder(items: Item[], user: User) {
    return { items, userId: user.id }
  }
}
```

## 🔗 Related Files

- **[SKILL.md](../SKILL.md)** - Back to Overview
- **[TDD.md](./TDD.md)** - TDD Cycle
- **[TEST-TYPES.md](./TEST-TYPES.md)** - Types of tests
- **[REFERENCE.md](./REFERENCE.md)** - Best practices

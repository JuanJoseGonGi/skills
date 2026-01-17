# Details of SOLID Principles

A detailed explanation of the five SOLID principles. For each principle, we contrast "Bad" and "Good" examples.

## 📋 Table of Contents
1. [Single Responsibility Principle](#1-single-responsibility-principle)
2. [Open/Closed Principle](#2-openclosed-principle)
3. [Liskov Substitution Principle](#3-liskov-substitution-principle)
4. [Interface Segregation Principle](#4-interface-segregation-principle)
5. [Dependency Inversion Principle](#5-dependency-inversion-principle)

---

## 1. Single Responsibility Principle (SRP)

### Definition
**Each class or function should have only one responsibility.**

Design so that there is only "one reason to change."

### Why it Matters
- **Improved Maintainability**: The scope of impact for changes is limited.
- **Easier Testing**: You only need to test a single function.
- **Reusability**: Components with clear responsibilities are easier to reuse.

### ❌ Bad Example: Class with multiple responsibilities
```typescript
class User {
  name: string
  email: string

  // ❌ User class has the responsibility of DB operations
  saveToDatabase() {
    const db = new Database()
    db.insert('users', this)
  }

  // ❌ User class has the responsibility of sending emails
  sendEmail(subject: string, body: string) {
    const emailService = new EmailService()
    emailService.send(this.email, subject, body)
  }

  // ❌ User class has the responsibility of report generation
  generateReport(): string {
    return `User Report: ${this.name} (${this.email})`
  }
}
```

**Problems**:
- You must modify the `User` class when the DB schema changes.
- You must modify the `User` class when email sending logic changes.
- You must modify the `User` class when the report format changes.
- Testing is complex (requires mocking DB, email, and reports).

### ✅ Good Example: Separated Responsibilities
```typescript
// User Entity: Data storage only
class User {
  constructor(
    public readonly name: string,
    public readonly email: string
  ) {}
}

// Separating responsibility for DB operations
class UserRepository {
  save(user: User): void {
    const db = new Database()
    db.insert('users', user)
  }

  findById(id: string): User | null {
    const db = new Database()
    return db.findOne('users', { id })
  }
}

// Separating responsibility for sending emails
class UserEmailService {
  sendWelcomeEmail(user: User): void {
    const emailService = new EmailService()
    emailService.send(
      user.email,
      'Welcome!',
      `Hello ${user.name}, welcome to our service!`
    )
  }
}

// Separating responsibility for report generation
class UserReportGenerator {
  generate(user: User): string {
    return `User Report: ${user.name} (${user.email})`
  }
}
```

**Improvements**:
- Each class has a single responsibility.
- The scope of impact for changes is limited.
- Testing is easy (classes can be tested independently).
- Reusability is improved.

---

## 2. Open/Closed Principle (OCP)

### Definition
**Software entities should be open for extension, but closed for modification.**

New features should be added through extension without modifying existing code.

### Why it Matters
- **Safety**: Risk of breaking existing features is low as existing code isn't modified.
- **Extensibility**: Easier to add new features.
- **Maintainability**: Understanding existing code isn't strictly necessary to add new ones.

### ❌ Bad Example: Adding new types requires modifying existing code
```typescript
class Shape {
  type: 'circle' | 'square' | 'rectangle'
  radius?: number
  side?: number
  width?: number
  height?: number
}

function getArea(shape: Shape): number {
  if (shape.type === 'circle') {
    return Math.PI * shape.radius! ** 2
  }
  if (shape.type === 'square') {
    return shape.side! ** 2
  }
  if (shape.type === 'rectangle') {
    return shape.width! * shape.height!
  }
  // If adding a new shape (e.g., Triangle)
  // -> This function must be modified
  throw new Error('Unknown shape type')
}
```

**Problems**:
- Modifying the `getArea` function every time a new shape is added.
- Risk of breaking existing functionality during modification.
- Test cases keep growing in a single place.

### ✅ Good Example: Extending with Interfaces
```typescript
// Abstraction through interface
interface Shape {
  getArea(): number
}

class Circle implements Shape {
  constructor(private radius: number) {}

  getArea(): number {
    return Math.PI * this.radius ** 2
  }
}

class Square implements Shape {
  constructor(private side: number) {}

  getArea(): number {
    return this.side ** 2
  }
}

class Rectangle implements Shape {
  constructor(
    private width: number,
    private height: number
  ) {}

  getArea(): number {
    return this.width * this.height
  }
}

// Adding a new shape (No modification to existing code)
class Triangle implements Shape {
  constructor(
    private base: number,
    private height: number
  ) {}

  getArea(): number {
    return (this.base * this.height) / 2
  }
}

// Consumer code doesn't need to change
function printArea(shape: Shape): void {
  console.log(`Area: ${shape.getArea()}`)
}
```

**Improvements**:
- Existing code is not modified when adding new shapes.
- Logic for each shape is independent.
- Tests can be conducted independently for each shape.

---

## 3. Liskov Substitution Principle (LSP)

### Definition
**Objects of a superclass should be replaceable with objects of its subclasses without breaking the application.**

Subclasses must not break the contract (behavior) of the parent class.

### Why it Matters
- **Reliability**: Behavior of inheritance hierarchies is predictable.
- **Polymorphism**: Can be handled safely via base class types.
- **Maintainability**: Inheritance relationships are clear.

### ❌ Bad Example: Inheritance that breaks the parent's contract
```typescript
class Bird {
  fly(): void {
    console.log('Flying in the sky')
  }
}

class Sparrow extends Bird {
  fly(): void {
    console.log('Sparrow flying fast')
  }
}

// ❌ Penguins cannot fly, breaking the parent's contract
class Penguin extends Bird {
  fly(): void {
    throw new Error('Penguins cannot fly!')
  }
}

// Problem occurs on the consumer side
function makeBirdFly(bird: Bird): void {
  bird.fly()  // Causes an error if the bird is a Penguin
}

makeBirdFly(new Sparrow())  // OK
makeBirdFly(new Penguin())  // ❌ Exception occurs
```

**Problems**:
- Functions expecting `Bird` type break when given a `Penguin`.
- Inheritance relationship is inappropriate.

### ✅ Good Example: Proper Abstraction
```typescript
// Base class: Common to all birds
class Bird {
  constructor(public name: string) {}
}

// Separate flying capability via interface
interface Flyable {
  fly(): void
}

// Separate swimming capability via interface
interface Swimmable {
  swim(): void
}

// Sparrow: A bird that can fly
class Sparrow extends Bird implements Flyable {
  fly(): void {
    console.log(`${this.name} is flying`)
  }
}

// Penguin: A bird that can swim
class Penguin extends Bird implements Swimmable {
  swim(): void {
    console.log(`${this.name} is swimming`)
  }
}

// Duck: A bird that can fly and swim
class Duck extends Bird implements Flyable, Swimmable {
  fly(): void {
    console.log(`${this.name} is flying`)
  }

  swim(): void {
    console.log(`${this.name} is swimming`)
  }
}

// Consumer: Functions according to capabilities
function makeFly(flyable: Flyable): void {
  flyable.fly()
}

function makeSwim(swimmable: Swimmable): void {
  swimmable.swim()
}

makeFly(new Sparrow('Tweety'))  // OK
makeSwim(new Penguin('Pingu'))  // OK
makeFly(new Duck('Donald'))     // OK
makeSwim(new Duck('Donald'))    // OK
```

**Improvements**:
- Proper use of inheritance and interfaces.
- Each class only possesses the capabilities it can implement.
- Type-safe usage.

---

## 4. Interface Segregation Principle (ISP)

### Definition
**No client should be forced to depend on methods it does not use.**

Prepare multiple small, specialized interfaces rather than one large one.

### Why it Matters
- **Flexibility**: Implement only necessary features.
- **Maintainability**: Impact of interface changes is limited.
- **Understandability**: Roles are clear.

### ❌ Bad Example: Monolithic Interface
```typescript
interface Worker {
  work(): void
  eat(): void
  sleep(): void
  takeBreak(): void
}

class Human implements Worker {
  work() { console.log('Working') }
  eat() { console.log('Eating') }
  sleep() { console.log('Sleeping') }
  takeBreak() { console.log('Taking a break') }
}

// ❌ Robots don't need to eat or sleep
class Robot implements Worker {
  work() { console.log('Processing tasks') }

  // Must implement unnecessary methods
  eat() { throw new Error('Robots do not eat') }
  sleep() { throw new Error('Robots do not sleep') }
  takeBreak() { throw new Error('Robots do not take breaks') }
}
```

**Problems**:
- Unnecessary methods implemented for the Robot.
- Large impact when the interface changes.

### ✅ Good Example: Segregated Interfaces
```typescript
// Capability to work
interface Workable {
  work(): void
}

// Capability to eat
interface Eatable {
  eat(): void
}

// Capability to sleep
interface Sleepable {
  sleep(): void
}

// Capability to take breaks
interface Breakable {
  takeBreak(): void
}

// Human: Has all capabilities
class Human implements Workable, Eatable, Sleepable, Breakable {
  work() { console.log('Working') }
  eat() { console.log('Eating') }
  sleep() { console.log('Sleeping') }
  takeBreak() { console.log('Taking a break') }
}

// Robot: Only has capability to work
class Robot implements Workable {
  work() { console.log('Processing tasks') }
}

// Consumer: Requires only necessary capabilities
function assignWork(worker: Workable): void {
  worker.work()
}

function serveMeal(eater: Eatable): void {
  eater.eat()
}

assignWork(new Human())   // OK
assignWork(new Robot())   // OK
serveMeal(new Human())    // OK
// serveMeal(new Robot()) // Compile error (Type safe)
```

**Improvements**:
- Each interface defines a single capability.
- Classes implement only the capabilities they need.
- Type-safe usage.

---

## 5. Dependency Inversion Principle (DIP)

### Definition
**High-level modules should not depend on low-level modules. Both should depend on abstractions.**

Depend on interfaces (abstractions) rather than concrete classes.

### Why it Matters
- **Flexibility**: Easy to switch implementations.
- **Testability**: Mocks or stubs can be injected.
- **Loose Coupling**: Weak dependency between modules.

### ❌ Bad Example: Directly depending on concrete classes
```typescript
// Concrete class
class MySQLDatabase {
  save(data: any): void {
    console.log('Saving to MySQL:', data)
  }
}

// ❌ UserService directly depends on MySQLDatabase
class UserService {
  private db = new MySQLDatabase()  // Dependency on concrete class

  saveUser(user: User): void {
    this.db.save(user)
  }
}

// If switching to PostgreSQL
// -> UserService must be modified
```

**Problems**:
- UserService must be modified when the DB implementation changes.
- Actual DB is required during testing.
- UserService and MySQLDatabase are tightly coupled.

### ✅ Good Example: Depending on Abstractions (Interfaces)
```typescript
// Abstraction (Interface)
interface Database {
  save(data: any): void
  findById(id: string): any
}

// Concrete Class 1: MySQL implementation
class MySQLDatabase implements Database {
  save(data: any): void {
    console.log('Saving to MySQL:', data)
  }

  findById(id: string): any {
    console.log('Finding in MySQL:', id)
    return null
  }
}

// Concrete Class 2: PostgreSQL implementation
class PostgreSQLDatabase implements Database {
  save(data: any): void {
    console.log('Saving to PostgreSQL:', data)
  }

  findById(id: string): any {
    console.log('Finding in PostgreSQL:', id)
    return null
  }
}

// Concrete Class 3: In-Memory implementation (for testing)
class InMemoryDatabase implements Database {
  private data = new Map()

  save(data: any): void {
    this.data.set(data.id, data)
  }

  findById(id: string): any {
    return this.data.get(id)
  }
}

// ✅ UserService depends on abstractions (Dependency Injection)
class UserService {
  constructor(private db: Database) {}  // Dependency on abstraction

  saveUser(user: User): void {
    this.db.save(user)
  }

  getUser(id: string): User {
    return this.db.findById(id)
  }
}

// Inject implementation at usage
const mysqlService = new UserService(new MySQLDatabase())
const postgresService = new UserService(new PostgreSQLDatabase())
const testService = new UserService(new InMemoryDatabase())
```

**Improvements**:
- UserService depends on abstractions (interfaces).
- DB implementations can be switched easily.
- Mocks can be injected during testing.
- UserService and DB implementations are loosely coupled.

### Practical Example of Dependency Injection (DI)
```typescript
// Simple example of a DI container
class Container {
  private services = new Map<string, any>()

  register(name: string, service: any): void {
    this.services.set(name, service)
  }

  resolve<T>(name: string): T {
    return this.services.get(name)
  }
}

// Usage example
const container = new Container()
container.register('database', new MySQLDatabase())
container.register('userService',
  new UserService(container.resolve('database'))
)

const userService = container.resolve<UserService>('userService')
```

---

## 🔗 Related Documents

- [Clean Code Basics](./CLEAN-CODE-BASICS.md)
- [Quality Checklist](./QUALITY-CHECKLIST.md)
- [Quick Reference](./QUICK-REFERENCE.md)

## 📖 Reference Links

- [SOLID Principles Main Page](../SKILL.md)

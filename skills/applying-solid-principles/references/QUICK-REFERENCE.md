# Quick Reference

A reference consolidating concise information for quick lookup.

## 📋 Table of Contents
1. [One-line Summaries of SOLID Principles](#one-line-summaries-of-solid-principles)
2. [Common Mistakes and Fixes](#common-mistakes-and-fixes)
3. [Code Review Points](#code-review-points)
4. [Design Pattern Quick Lookup](#design-pattern-quick-lookup)

---

## One-line Summaries of SOLID Principles

### S - Single Responsibility (SRP)
**"Only one reason to change."**
```typescript
// ❌ class User { save(), sendEmail(), generateReport() }
// ✅ class User { }, class UserRepository { }, class EmailService { }
```

### O - Open/Closed (OCP)
**Open for extension, closed for modification.**
```typescript
// ❌ if (type === 'A') { } else if (type === 'B') { }
// ✅ interface Handler { handle() }; class HandlerA implements Handler { }
```

### L - Liskov Substitution (LSP)
**Derived classes are substitutable for base classes.**
```typescript
// ❌ class Penguin extends Bird { fly() { throw Error } }
// ✅ class Penguin extends Bird implements Swimmable { }
```

### I - Interface Segregation (ISP)
**No enforcement of dependency on unused methods.**
```typescript
// ❌ interface Worker { work(), eat(), sleep() }
// ✅ interface Workable { work() }; interface Eatable { eat() }
```

### D - Dependency Inversion (DIP)
**Depend on abstractions, not concretions.**
```typescript
// ❌ class UserService { db = new MySQLDatabase() }
// ✅ class UserService { constructor(private db: Database) }
```

---

## Common Mistakes and Fixes

### 1. Huge Classes or Functions
```typescript
// ❌ Bad Example
class UserManager {
  // 500+ lines...
  validateUser() { }
  saveUser() { }
  sendEmail() { }
  generateReport() { }
  // ...
}

// ✅ Good Example
class UserValidator { validateUser() { } }
class UserRepository { saveUser() { } }
class EmailService { sendEmail() { } }
class ReportGenerator { generateReport() { } }
```

### 2. Magic Numbers
```typescript
// ❌ Bad Example
if (user.age > 18) { }
setTimeout(() => {}, 5000)

// ✅ Good Example
const ADULT_AGE = 18
const DEFAULT_TIMEOUT_MS = 5000

if (user.age > ADULT_AGE) { }
setTimeout(() => {}, DEFAULT_TIMEOUT_MS)
```

### 3. Deep Nesting
```typescript
// ❌ Bad Example
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      // Process
    }
  }
}

// ✅ Good Example (Early Return)
if (!user) return
if (!user.isActive) return
if (!user.hasPermission) return
// Process
```

### 4. Too Many Arguments
```typescript
// ❌ Bad Example
function createUser(name, email, age, address, phone, country) { }

// ✅ Good Example
interface UserData {
  name: string
  email: string
  age: number
  address: string
  phone: string
  country: string
}

function createUser(data: UserData) { }
```

### 5. Ambiguous Naming
```typescript
// ❌ Bad Example
function getData(id) { }
let temp = {}
const result = process()

// ✅ Good Example
function getUserById(userId: string): User { }
let temporaryUserData: User = {}
const validationResult: ValidationResult = validateUser()
```

### 6. Function with Side Effects
```typescript
// ❌ Bad Example (Modifies argument)
function addItem(items: Item[], newItem: Item): void {
  items.push(newItem)  // Modifies original array
}

// ✅ Good Example (Returns new array)
function addItem(items: Item[], newItem: Item): Item[] {
  return [...items, newItem]
}
```

### 7. Direct Dependency on Concrete Classes
```typescript
// ❌ Bad Example
class UserService {
  private db = new MySQLDatabase()  // Dependency on concretion
  saveUser(user: User) {
    this.db.save(user)
  }
}

// ✅ Good Example (Dependency Injection)
interface Database {
  save(data: any): void
}

class UserService {
  constructor(private db: Database) { }  // Dependency on abstraction
  saveUser(user: User) {
    this.db.save(user)
  }
}
```

---

## Code Review Points

### 🔴 Mandatory Checks (Reasons for Rejection)

#### Security
- [ ] SQL Injection countermeasures
- [ ] XSS countermeasures
- [ ] CSRF countermeasures
- [ ] Input validation
- [ ] Authentication/Authorization

#### Type Safety (TypeScript/Python)
- [ ] Not using `any` type (TypeScript)
- [ ] Not using `Any` type (Python)
- [ ] Appropriate type annotations present
- [ ] null/undefined checks present

#### Error Handling
- [ ] try-catch is appropriate
- [ ] Error messages are clear
- [ ] Error logs are output

### 🟡 Recommended Checks (Encourage Improvement)

#### SOLID Principles
- [ ] Single Responsibility Principle
- [ ] Open/Closed Principle
- [ ] Dependency Inversion Principle

#### Clean Code
- [ ] Functions are small (20 lines or less)
- [ ] Arguments are few (0-2)
- [ ] No deep nesting (3 layers or less)
- [ ] No magic numbers

#### Naming
- [ ] Intent-revealing
- [ ] Consistent
- [ ] Searchable

#### Testing
- [ ] Unit tests present
- [ ] Edge cases covered
- [ ] Tests contain meaningful content

---

## Design Pattern Quick Lookup

### Creational Patterns

#### Singleton
**Use**: Guarantees only one instance
```typescript
class Singleton {
  private static instance: Singleton

  private constructor() { }

  static getInstance(): Singleton {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton()
    }
    return Singleton.instance
  }
}
```

#### Factory
**Use**: Abstract object creation
```typescript
interface Product {
  operation(): string
}

class ConcreteProductA implements Product {
  operation() { return 'Product A' }
}

class ConcreteProductB implements Product {
  operation() { return 'Product B' }
}

class Factory {
  createProduct(type: string): Product {
    if (type === 'A') return new ConcreteProductA()
    if (type === 'B') return new ConcreteProductB()
    throw new Error('Unknown type')
  }
}
```

---

### Structural Patterns

#### Adapter
**Use**: Convert interfaces
```typescript
interface Target {
  request(): string
}

class Adaptee {
  specificRequest(): string {
    return 'Adaptee'
  }
}

class Adapter implements Target {
  constructor(private adaptee: Adaptee) { }

  request(): string {
    return this.adaptee.specificRequest()
  }
}
```

#### Decorator
**Use**: Dynamically add functionality
```typescript
interface Component {
  operation(): string
}

class ConcreteComponent implements Component {
  operation() { return 'Base' }
}

class Decorator implements Component {
  constructor(protected component: Component) { }

  operation(): string {
    return `Decorated(${this.component.operation()})`
  }
}
```

---

### Behavioral Patterns

#### Strategy
**Use**: Make algorithms switchable
```typescript
interface Strategy {
  execute(data: any): any
}

class ConcreteStrategyA implements Strategy {
  execute(data: any) { return `Strategy A: ${data}` }
}

class ConcreteStrategyB implements Strategy {
  execute(data: any) { return `Strategy B: ${data}` }
}

class Context {
  constructor(private strategy: Strategy) { }

  setStrategy(strategy: Strategy) {
    this.strategy = strategy
  }

  executeStrategy(data: any) {
    return this.strategy.execute(data)
  }
}
```

#### Observer
**Use**: Implement event notification
```typescript
interface Observer {
  update(data: any): void
}

class Subject {
  private observers: Observer[] = []

  attach(observer: Observer) {
    this.observers.push(observer)
  }

  notify(data: any) {
    this.observers.forEach(observer => observer.update(data))
  }
}

class ConcreteObserver implements Observer {
  update(data: any) {
    console.log('Received:', data)
  }
}
```

---

## 🎯 Quick Check at Implementation

Items to verify quickly during implementation:

### When Writing Functions
```
✓ Within 20 lines? -> Split if exceeded
✓ 0-2 arguments? -> Pass as object if 3 or more
✓ No side effects? -> Prioritize pure functions
✓ Using early return? -> Reduce nesting
```

### When Writing Classes
```
✓ Single responsibility? -> Split if it does "A and B"
✓ Dependent on abstractions? -> DI instead of 'new'
✓ Interfaces are small? -> Segregate unused methods
```

### When Defining Variables
```
✓ Intent-revealing name? -> Avoid data, temp, result
✓ Not a magic number? -> Constantize
✓ Searchable? -> Avoid abbreviations
```

### Before Commit
```
✓ Adhering to SOLID principles?
✓ Wrote tests?
✓ No code smells?
✓ Security is fine?
```

---

## 📊 Code Quality Metrics

### Benchmarks for Good Values

| Metric | Ideal Value | Acceptable Range | Needs Improvement |
|---------|-------|---------|--------|
| Function Lines | <20 lines | <50 lines | >50 lines |
| Number of Arguments | 0-2 | 3 | >3 |
| Nesting Depth | 1-2 layers | 3 layers | >3 layers |
| Class Lines | <200 lines | <500 lines | >500 lines |
| Cyclomatic Complexity | <10 | <20 | >20 |
| Test Coverage | >80% | >60% | <60% |

---

## 🔗 Related Documents

- [Details of SOLID Principles](./SOLID-PRINCIPLES.md) - Detailed explanation of each principle
- [Clean Code Basics](./CLEAN-CODE-BASICS.md) - Naming, functions, comments
- [Quality Checklist](./QUALITY-CHECKLIST.md) - Verification items before completion

## 📖 Reference Links

- [Quick Reference Main Page](../SKILL.md)

---

## 💡 One-point Advice

### Criteria When in Doubt

**Prioritize Simplicity**
```
Complex Design vs Simple Design
-> If in doubt, choose the simple one
```

**Prioritize Testability**
```
Difficult to write tests
-> A sign to review the design
```

**Prioritize Readability**
```
Comments are long
-> Consider if it can be explained by code
```

**Prioritize Changeability**
```
Scope of impact for change is wide
-> Responsibilities might not be segregated
```

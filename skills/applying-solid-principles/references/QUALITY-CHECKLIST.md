# Quality Checklist

A checklist of items to verify before completing implementation.

## 📋 Table of Contents
1. [Pre-completion Checklist](#pre-completion-checklist)
2. [Code Smell Detection](#code-smell-detection)
3. [Refactoring Decisions](#refactoring-decisions)
4. [Verification of Design Principles](#verification-of-design-principles)

---

## Pre-completion Checklist

### 🎯 Adherence to SOLID Principles

#### Single Responsibility (SRP)
- [ ] Each class/function has only one responsibility.
- [ ] There is only one "reason to change."
- [ ] Multiple concerns are not mixed.

**Verification Method**:
```
Try explaining the class/function.
-> If it says "It does A and B," consider splitting.
-> If it simply says "It does A," the design is likely fine.
```

#### Open/Closed (OCP)
- [ ] Open for extension (easy to add new features).
- [ ] Closed for modification (existing code is not changed).
- [ ] Extensible via interfaces or abstract classes.

**Verification Method**:
```
When adding a new feature:
-> If you need to modify existing if or switch statements, it needs improvement.
-> If you just need to add a new class, it's a good design.
```

#### Liskov Substitution (LSP)
- [ ] Derived classes are substitutable for base classes.
- [ ] Subclasses do not break the parent class's contract.
- [ ] Composition is prioritized over inheritance.

**Verification Method**:
```
Assign a subclass to a variable of the parent class type.
-> Test if it works as expected.
-> If exceptions occur, review the inheritance relationship.
```

#### Interface Segregation (ISP)
- [ ] No enforcement of dependency on unused methods.
- [ ] Small, specialized interfaces.
- [ ] Only necessary features are implemented.

**Verification Method**:
```
Methods in implementation classes have empty implementations or throw errors.
-> The interface is too large.
-> Consider splitting.
```

#### Dependency Inversion (DIP)
- [ ] Depends on abstractions (interfaces).
- [ ] No direct dependency on concrete classes.
- [ ] Dependency Injection (DI) is utilized.

**Verification Method**:
```
Check places where the `new` operator directly creates classes.
-> If frequent, consider introducing a DI container.
-> Confirm if mocks can be injected during testing.
```

---

### 🎨 Clean Code Basics

#### Naming
- [ ] Intent-revealing names.
- [ ] Searchable names (use constants).
- [ ] Pronounceable names.
- [ ] Consistent naming conventions.

**Bad Example**:
```typescript
// ❌
let d: number  // Number of what days?
let temp: any  // Temporary variable for what?
let usrNm: string  // Too abbreviated

// ✅
let daysSinceCreation: number
let temporaryUserData: User
let userName: string
```

#### Functions
- [ ] Functions are small (ideally 20 lines or less).
- [ ] Single responsibility.
- [ ] 0-2 arguments (maximum 3).
- [ ] Side effects are avoided.

**Verification Method**:
```
Function doesn't fit on one screen -> Consider splitting.
3 or more arguments -> Pass as an object.
Difficult to write tests -> Possible multiple responsibilities.
```

#### Nesting
- [ ] Avoid deep nesting (3 layers or more).
- [ ] Use guard clauses for early returns.
- [ ] Functionalize complex conditions.

**Bad Example**:
```typescript
// ❌ Deep nesting
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      // Process
    }
  }
}

// ✅ Early return
if (!user) return
if (!user.isActive) return
if (!user.hasPermission) return
// Process
```

---

### 📐 Design and Architecture

#### DRY (Don't Repeat Yourself)
- [ ] Avoid code duplication.
- [ ] Common processes are functionalized or modularized.
- [ ] Magic Numbers are constantized.

**Verification Method**:
```
Same code appears 3 or more times -> Consider functionalization.
Numeric literals in multiple places -> Consider constantization.
```

#### YAGNI (You Aren't Gonna Need It)
- [ ] Unnecessary features are not implemented.
- [ ] Avoid over-abstraction for "future extensibility."
- [ ] Only currently needed features are implemented.

**Verification Method**:
```
There is a feature "that might be used in the future."
-> Reconfirm if it's needed now.
-> Delete if unnecessary.
```

#### KISS (Keep It Simple, Stupid)
- [ ] Simple design.
- [ ] Avoid over-abstraction.
- [ ] Code is easy to understand.

**Verification Method**:
```
Can other developers understand it?
-> If the explanation is long, it's too complex.
-> Consider simplification.
```

---

## Code Smell Detection

### 🚨 Red Flags (Fix immediately)

#### 1. Huge Classes or Functions
```typescript
// ❌ Class with 500+ lines
class UserManager {
  // Numerous methods...
}

// ✅ Separate responsibilities
class UserRepository { }
class UserService { }
class UserValidator { }
```

#### 2. Long Parameter Lists
```typescript
// ❌ 5 or more arguments
function createUser(name, email, age, address, phone) { }

// ✅ Pass as an object
function createUser(userData: UserData) { }
```

#### 3. Duplicated Code
```typescript
// ❌ Same process in multiple places
function processUserA(user) {
  if (!user.email.includes('@')) throw new Error('Invalid email')
  // ...
}

function processUserB(user) {
  if (!user.email.includes('@')) throw new Error('Invalid email')
  // ...
}

// ✅ Functionalize
function validateEmail(email: string) {
  if (!email.includes('@')) throw new Error('Invalid email')
}
```

#### 4. Magic Numbers
```typescript
// ❌
if (user.age > 18) { }
setTimeout(() => {}, 5000)

// ✅
const ADULT_AGE = 18
const DEFAULT_TIMEOUT_MS = 5000

if (user.age > ADULT_AGE) { }
setTimeout(() => {}, DEFAULT_TIMEOUT_MS)
```

#### 5. Dead Code
```typescript
// ❌ Unused functions or variables
function oldFunction() { }  // Never called
const unusedVariable = 10   // Never used

// ✅ Delete (manage via Git history)
```

---

### ⚠️ Yellow Flags (Consider improvement)

#### 1. Commented-out Code
```typescript
// ❌
// function oldImplementation() {
//   // Old code
// }

// ✅ Delete (restore from Git history if needed)
```

#### 2. Excessive Conditional Branching
```typescript
// ❌ Huge switch statement
switch (type) {
  case 'A': // Process A
  case 'B': // Process B
  case 'C': // Process C
  // ... 20 or more cases
}

// ✅ Polymorphism
interface Handler {
  handle(): void
}

const handlers: Record<string, Handler> = {
  A: new HandlerA(),
  B: new HandlerB(),
  C: new HandlerC()
}

handlers[type].handle()
```

#### 3. Deep Nesting
```typescript
// ❌ 3 or more layers
if (a) {
  if (b) {
    if (c) {
      // Process
    }
  }
}

// ✅ Early return
if (!a) return
if (!b) return
if (!c) return
// Process
```

#### 4. Long Method Chains
```typescript
// ❌ Hard to read
user.getOrders().filter(o => o.status === 'pending').map(o => o.total).reduce((a, b) => a + b, 0)

// ✅ Split into variables
const pendingOrders = user.getOrders().filter(o => o.status === 'pending')
const orderTotals = pendingOrders.map(o => o.total)
const totalAmount = orderTotals.reduce((a, b) => a + b, 0)
```

---

## Refactoring Decisions

### When to Refactor

#### 🔴 Refactor Immediately
- [ ] Causing bugs.
- [ ] Security risk present.
- [ ] Performance issue present.
- [ ] Obstacle to adding new features.

#### 🟡 Plan to Refactor
- [ ] Difficult to write tests.
- [ ] Scope of impact for changes is unpredictable.
- [ ] Same bug occurring repeatedly.
- [ ] Many points raised in code review.

#### 🟢 Refactor if Time Permits
- [ ] Code smells present.
- [ ] Inappropriate naming.
- [ ] Too many comments (could be explained by code).

### Refactoring Steps

1. **Write Tests**
   - Tests to ensure existing behavior.
   - Confirm identical operation after refactoring.

2. **Make Small Changes**
   - One improvement at a time.
   - Keep commits granular.

3. **Run Tests**
   - Test at each step.
   - Revert if it fails.

4. **Review**
   - Confirm via code review.
   - Discuss improvements.

---

## Verification of Design Principles

### ✅ Signs of Good Design

- [ ] Classes/functions are small.
- [ ] Responsibility is clear.
- [ ] Easy to write tests.
- [ ] Changes are local (limited scope of impact).
- [ ] Easy to add new features.
- [ ] Noted as easy to understand in code reviews.

### ❌ Signs of Bad Design

- [ ] Classes/functions are large (100+ lines).
- [ ] Responsibility is unclear (long explanation needed).
- [ ] Difficult to write tests (many mocks required).
- [ ] Changes have wide-reaching impacts.
- [ ] Existing code must be significantly modified every time a new feature is added.
- [ ] Many questions raised in code reviews.

---

## 🎯 Final Check Before Completion

Verify all the following at completion of implementation:

### Design and Architecture
- [ ] Adheres to SOLID principles.
- [ ] Follows the DRY principle.
- [ ] Follows YAGNI (no implementation of unnecessary features).
- [ ] Appropriate level of abstraction.

### Code Quality
- [ ] Are functions small and single-responsibility? (Ideally 20 lines or less)
- [ ] Are arguments minimal? (Ideally 0-2, maximum 3)
- [ ] Is deep nesting (3 layers or more) avoided?
- [ ] Are magic numbers constantized?

### Naming and Readability
- [ ] Is naming consistent and clear in intent?
- [ ] Are comments minimal? (No commenting on things obvious from code)
- [ ] Are early returns utilized?

### Error Handling
- [ ] Is there appropriate error handling?
- [ ] Are error messages clear?
- [ ] Are exceptions caught appropriately?

### Testing
- [ ] Are unit tests written?
- [ ] Are the tests meaningful? (Not just perfunctory)
- [ ] Are edge cases covered?

### Security
- [ ] Is input validation performed?
- [ ] Are SQL injection countermeasures in place?
- [ ] Are XSS countermeasures in place?
- [ ] Is authentication/authorization appropriate?

### Performance
- [ ] Are there unnecessary loops or calculations?
- [ ] Are database queries optimized?
- [ ] Is caching used appropriately?

### Documentation
- [ ] Does the public API have JSDoc?
- [ ] Are there explanatory comments for complex logic?
- [ ] Is the README updated?

---

## 🔗 Related Documents

- [Details of SOLID Principles](./SOLID-PRINCIPLES.md)
- [Clean Code Basics](./CLEAN-CODE-BASICS.md)
- [Quick Reference](./QUICK-REFERENCE.md)

## 📖 Reference Links

- [Quality Checklist Main Page](../SKILL.md)

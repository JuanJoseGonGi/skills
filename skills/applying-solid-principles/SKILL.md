---
name: applying-solid-principles
description: Applies SOLID principles and clean code practices. Required for all code implementations. Covers single responsibility, open-closed, and dependency injection principles.
---

# SOLID Principles and Clean Code

## 🎯 When to Use
- **All code implementations (Required)**
- **During refactoring**
- **During code reviews**
- **When making design decisions**

## 📚 Document Structure

This skill consists of the following documents:

### 1. [SOLID Principles Detail](references/SOLID-PRINCIPLES.md)
Detailed explanation and code examples for the five SOLID principles:
- **S**: Single Responsibility
- **O**: Open/Closed
- **L**: Liskov Substitution
- **I**: Interface Segregation
- **D**: Dependency Inversion

Each principle is explained by contrasting "Bad" and "Good" examples.

### 2. [Clean Code Basics](references/CLEAN-CODE-BASICS.md)
Fundamental principles to apply in daily coding:
- Naming conventions to clarify intent
- Small, single-responsibility function design
- Reducing nesting with early returns
- Eliminating magic numbers

### 3. [Quality Checklist](references/QUALITY-CHECKLIST.md)
Checklist items before completing implementation:
- Design principle compliance check
- Code smell detection
- Refactoring criteria

### 4. [Quick Reference](references/QUICK-REFERENCE.md)
Concise information for quick reference:
- One-line summaries of SOLID principles
- Common mistakes and fixes
- Code review points

## 🎯 Overview of SOLID Principles

### S - Single Responsibility Principle
**"Only one reason to change"**
- Each class or function has only one responsibility.
- Example: UserService for user management only, EmailService for sending emails only.

### O - Open/Closed Principle
**"Open for extension, closed for modification"**
- Add new features by extending rather than modifying existing code.
- Leverage interfaces and abstract classes.

### L - Liskov Substitution Principle
**"Derived classes must be substitutable for their base classes"**
- Subclasses must not break the contract of the parent class.
- Favor composition over inheritance.

### I - Interface Segregation Principle
**"Clients should not be forced to depend on methods they do not use"**
- Prefer small, specialized interfaces over large ones.
- Implement only the necessary methods.

### D - Dependency Inversion Principle
**"High-level modules should not depend on low-level modules"**
- Both should depend on abstractions.
- Actively utilize Dependency Injection (DI).

## 🚀 Implementation Approach

### 1. Design Phase
1. Design with SOLID principles in mind.
2. Clearly separate responsibilities.
3. Abstract with interfaces.

### 2. Implementation Phase
1. Apply basic clean code principles.
2. Create small, testable functions.
3. Strive for intent-revealing naming.

### 3. Review Phase
1. Verify using the Quality Checklist.
2. Detect code smells.
3. Determine if refactoring is necessary.

## 💡 Important Principles

### DRY (Don't Repeat Yourself)
- Avoid code duplication.
- Functionalize or modularize common processes.

### WET (Write Everything Twice)
- Write code twice to ensure correctness.
- Use tests to verify correctness.

### YAGNI (You Aren't Gonna Need It)
- Do not implement unnecessary features.
- Implement only when actually needed.

### KISS (Keep It Simple, Stupid)
- Aim for simple design.
- Avoid over-abstraction.

## 📖 Next Steps

1. **Newcomers**: Start reading from [SOLID Principles Detail](references/SOLID-PRINCIPLES.md).
2. **Daily Implementation**: Refer to [Clean Code Basics](references/CLEAN-CODE-BASICS.md).
3. **During Code Review**: Utilize the [Quality Checklist](references/QUALITY-CHECKLIST.md).
4. **Quick Check**: Verify key points in the [Quick Reference](references/QUICK-REFERENCE.md).

---
name: enforcing-type-safety
description: Enforces type safety in TypeScript/Python implementations. Any/any types strictly prohibited. Use when processing API responses, integrating external libraries, or implementing data validation. Supports strict mode configuration and type guard implementation.
---

# Principles of Type Safety

## 📑 Table of Contents

This skill consists of the following files:

- **SKILL.md** (this file): Overview and basic principles.
- **[TYPESCRIPT.md](references/TYPESCRIPT.md)**: TypeScript type safety details.
- **[PYTHON.md](references/PYTHON.md)**: Python type safety details.
- **[ANTI-PATTERNS.md](references/ANTI-PATTERNS.md)**: Code conventions to avoid.
- **[REFERENCE.md](references/REFERENCE.md)**: Checklists, tool settings, and type checkers.

## 🎯 When to Use

- **All code implementations (Mandatory)**
- **When using TypeScript/Python**
- **When processing API responses**
- **When integrating external libraries**
- **Quality checks during reviews**

## 🚫 Absolute Prohibition: Basic Principles of any/Any Types

### TypeScript

```typescript
❌ Absolutely Forbidden:
- Use of the 'any' type
- The 'Function' type (equivalent to any)
- Overuse of non-null assertions (!)

✅ Alternatives:
- Explicit type definitions (interface/type)
- 'unknown' + Type Guards
- Generics
- Utility Types
```

### Python

```python
❌ Absolutely Forbidden:
- Use of the 'Any' type
- bare except
- eval/exec

✅ Alternatives:
- Explicit Type Hints
- TypedDict
- Protocol (Structural Subtyping)
- Union types
```

## 💡 The Three Pillars of Type Safety

### 1. Explicit Type Definitions

Explicitly define types for all functions and variables.

**TypeScript**:
```typescript
function getUserById(id: string): User | null {
  // Implementation
}
```

**Python**:
```python
def get_user_by_id(user_id: str) -> Optional[User]:
    # Implementation
    pass
```

### 2. Utilizing Type Guards

Handle 'unknown' types or ambiguous types safely using type guards.

**TypeScript**:
```typescript
function isUser(data: unknown): data is User {
  return typeof data === 'object' &&
         data !== null &&
         'id' in data &&
         'name' in data
}

if (isUser(data)) {
  console.log(data.name)  // Type-safe
}
```

**Python**:
```python
from typing import TypeGuard

def is_user(data: object) -> TypeGuard[User]:
    return isinstance(data, dict) and \
           'id' in data and 'name' in data

if is_user(data):
    print(data['name'])  // Type-safe
```

### 3. Running Type Checkers

**TypeScript**: Enable strict mode
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

**Python**: Run mypy/pyright
```bash
mypy src/
pyright src/
```

## ⚡ Quick Reference

### Common Situations and Solutions

| Situation | Bad Example | Good Example |
|------|--------|--------|
| API Response | `response: any` | `response: ApiResponse` |
| Unknown Type | `data: any` | `data: unknown` + Type Guard |
| Multiple Types | `value: any` | `value: string \| number` |
| Optional | `user!.name` | `user?.name ?? 'Unknown'` |
| Array Operation | `items: any[]` | `items: User[]` |

### Recommended File Structure

```
src/
├── types/
│   ├── api.ts        # API type definitions
│   ├── models.ts     # Data model types
│   └── utils.ts      # Utility types
├── guards/
│   └── type-guards.ts # Type guard functions
└── ...
```

## 📊 Type Safety Levels

Code type safety is evaluated at the following levels:

### Level 1: Basic (Mandatory)
- [ ] No use of any/Any types.
- [ ] Type annotations on all functions.
- [ ] strict mode enabled.

### Level 2: Standard (Recommended)
- [ ] Proper use of Type Guards.
- [ ] Utilization of Generics.
- [ ] Utilization of Utility Types.

### Level 3: Advanced (Ideal)
- [ ] Utilization of Structural Subtyping (Protocol).
- [ ] Type-level programming.
- [ ] 100% Type coverage.

## 🔧 Pre-implementation Checklist

Before writing new code:

1. **Check Type Definition Files**
   - Can existing types be reused?
   - Is a new type definition required?

2. **Types for External Libraries**
   - Is the type definition included in the package?
   - Is a @types/package required?

3. **Scope of Shared Types**
   - Is a local type sufficient?
   - Should it be defined as a shared type?

## 🔗 Related Skills

- **applying-solid-principles**: SOLID principles and Clean Code.
- **testing**: Type-safe test code.
- **securing-code**: Secure use of types.
- **implementing-as-tachikoma**: Type safety when implementing as a Developer.

Refer to each file for details.

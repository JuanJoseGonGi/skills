# TypeScript Type Safety Details

This file explains detailed guidelines for type safety in TypeScript/JavaScript.

## 📋 Table of Contents

- [Absolute Prohibition of the any Type](#absolute-prohibition-of-the-any-type)
- [Correct Type Definition Methods](#correct-type-definition-methods)
- [TypeScript Best Practices](#typescript-best-practices)
- [Type Guard Patterns](#type-guard-patterns)
- [Utilizing Generics](#utilizing-generics)
- [Utilizing Utility Types](#utilizing-utility-types)

## 🚫 Absolute Prohibition of the any Type

### ❌ Patterns that Must Never Be Used

#### Pattern 1: Direct Use of the any Type

```typescript
// ❌ Bad Example
function processData(data: any) {
  return data.value  // Type safety is lost
}

const result: any = fetchData()  // Type checking is disabled
```

**Problems**:
- TypeScript's type checking is completely disabled.
- Becomes a source of runtime errors.
- IDE autocompletion does not work.
- Makes refactoring difficult.

#### Pattern 2: Use of the Function Type

```typescript
// ❌ Bad Example
const callback: Function = () => {}  // Equivalent to any
const handler: Function = (x) => x * 2
```

**Problems**:
- Types of arguments and return value are unknown.
- Type safety is lost.

**Correct Method**:
```typescript
// ✅ Good Example
type Callback = () => void
const callback: Callback = () => {}

type Handler = (x: number) => number
const handler: Handler = (x) => x * 2
```

#### Pattern 3: Abuse of non-null assertions (!)

```typescript
// ❌ Bad Example
const value = data!.value!.nested!  // Dangerous
const element = document.getElementById('app')!  // Ignores possibility of null
```

**Problems**:
- Ignores the possibility of null or undefined.
- Source of runtime errors.

**Correct Method**:
```typescript
// ✅ Good Example: Optional Chaining
const value = data?.value?.nested ?? defaultValue

// ✅ Good Example: Type Guard
const element = document.getElementById('app')
if (element !== null) {
  element.style.color = 'red'
}
```

## ✅ Correct Type Definition Methods

### 1. Explicit Interface Definitions

```typescript
// ✅ Type definition for API response
interface ApiResponse<T> {
  data: T
  status: number
  message: string
}

interface User {
  id: string
  name: string
  email: string
  createdAt: Date
}

interface Post {
  id: string
  title: string
  content: string
  authorId: string
}

// Usage example
async function fetchUser(id: string): Promise<ApiResponse<User>> {
  const response = await fetch(`/api/users/${id}`)
  return response.json()
}
```

### 2. Using the unknown Type (Pair with Type Guards)

```typescript
// ✅ Use unknown for ambiguous types
function handleUnknownData(data: unknown): string {
  // Handle safely with a type guard
  if (typeof data === 'object' && data !== null && 'value' in data) {
    const obj = data as { value: unknown }
    if (typeof obj.value === 'string') {
      return obj.value
    }
  }
  throw new Error('Invalid data structure')
}

// ✅ Safe JSON parsing
function parseJSON<T>(json: string, validator: (data: unknown) => data is T): T {
  const parsed: unknown = JSON.parse(json)
  if (validator(parsed)) {
    return parsed
  }
  throw new Error('Invalid JSON structure')
}

// Validator function
function isUser(data: unknown): data is User {
  return typeof data === 'object' &&
         data !== null &&
         'id' in data && typeof (data as any).id === 'string' &&
         'name' in data && typeof (data as any).name === 'string' &&
         'email' in data && typeof (data as any).email === 'string'
}

// Usage example
const userData = parseJSON(jsonString, isUser)
```

### 3. Utilization of Generics

```typescript
// ✅ Type-safe fetch function
async function fetchData<T>(
  url: string,
  validator: (data: unknown) => data is T
): Promise<T> {
  const response = await fetch(url)
  const data: unknown = await response.json()

  if (validator(data)) {
    return data
  }

  throw new Error(`Invalid response from ${url}`)
}

// Usage example
const user = await fetchData<User>('/api/user', isUser)
console.log(user.name)  // Type-safe
```

## 📚 TypeScript Best Practices

### 1. Enable strict mode (Mandatory)

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,                     // Enable all strict flags
    "noImplicitAny": true,             // Disallow implicit any
    "strictNullChecks": true,          // Strict null/undefined checks
    "strictFunctionTypes": true,       // Strict function type checks
    "strictBindCallApply": true,       // Strict bind/call/apply checks
    "strictPropertyInitialization": true, // Property initialization checks
    "noImplicitThis": true,            // Disallow implicit this
    "alwaysStrict": true               // Auto-insert 'use strict'
  }
}
```

### 2. Explicit Function Type Annotations

```typescript
// ✅ Type annotations for all functions
function getUserById(id: string): User | null {
  // Implementation
  return null
}

// ✅ async functions
async function fetchUserData(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`)
  return response.json()
}

// ✅ Higher-order functions
function createHandler(
  handler: (value: string) => void
): (event: Event) => void {
  return (event: Event) => {
    if (event.target instanceof HTMLInputElement) {
      handler(event.target.value)
    }
  }
}
```

### 3. Optional Chaining (?.) and Nullish Coalescing (??)

```typescript
// ✅ Optional Chaining
const userName = user?.profile?.name

// ✅ Nullish Coalescing
const displayName = userName ?? 'Unknown'

// ✅ Combination
const email = user?.contact?.email ?? 'no-email@example.com'

// ❌ Bad Example (non-null assertion)
const userName = user!.profile!.name  // Dangerous
```

### 4. Defining Type Guards

```typescript
// ✅ Type guard functions
function isString(value: unknown): value is string {
  return typeof value === 'string'
}

function isNumber(value: unknown): value is number {
  return typeof value === 'number'
}

function isUser(value: unknown): value is User {
  return typeof value === 'object' &&
         value !== null &&
         'id' in value &&
         'name' in value &&
         'email' in value
}

function isArray<T>(
  value: unknown,
  itemGuard: (item: unknown) => item is T
): value is T[] {
  return Array.isArray(value) && value.every(itemGuard)
}

// Usage example
if (isArray(data, isUser)) {
  data.forEach(user => {
    console.log(user.name)  // Type-safe
  })
}
```

### 5. const assertion

```typescript
// ✅ Use const assertion to maintain literal types
const COLORS = ['red', 'green', 'blue'] as const
type Color = typeof COLORS[number]  // 'red' | 'green' | 'blue'

const config = {
  api: {
    baseUrl: 'https://api.example.com',
    timeout: 5000
  }
} as const

type Config = typeof config
// {
//   readonly api: {
//     readonly baseUrl: "https://api.example.com"
//     readonly timeout: 5000
//   }
// }

// ✅ As an alternative to enum
const Status = {
  PENDING: 'pending',
  COMPLETED: 'completed',
  FAILED: 'failed'
} as const

type StatusValue = typeof Status[keyof typeof Status]
// 'pending' | 'completed' | 'failed'
```

## 🛡️ Type Guard Patterns

### Pattern 1: typeof Type Guard

```typescript
function processValue(value: string | number): string {
  if (typeof value === 'string') {
    return value.toUpperCase()
  }
  return value.toString()
}
```

### Pattern 2: instanceof Type Guard

```typescript
class ApiError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message)
  }
}

function handleError(error: unknown): void {
  if (error instanceof ApiError) {
    console.error(`API Error ${error.statusCode}: ${error.message}`)
  } else if (error instanceof Error) {
    console.error(`Error: ${error.message}`)
  } else {
    console.error('Unknown error')
  }
}
```

### Pattern 3: in Operator Type Guard

```typescript
type Dog = { name: string; bark: () => void }
type Cat = { name: string; meow: () => void }

function makeSound(animal: Dog | Cat): void {
  if ('bark' in animal) {
    animal.bark()  // Inferred as Dog
  } else {
    animal.meow()  // Inferred as Cat
  }
}
```

### Pattern 4: Custom Type Guard

```typescript
interface Success<T> {
  success: true
  data: T
}

interface Failure {
  success: false
  error: string
}

type Result<T> = Success<T> | Failure

function isSuccess<T>(result: Result<T>): result is Success<T> {
  return result.success === true
}

function processResult<T>(result: Result<T>): T {
  if (isSuccess(result)) {
    return result.data  // Inferred as Success<T>
  }
  throw new Error(result.error)  // Inferred as Failure
}
```

## 🔧 Utilizing Generics

### Pattern 1: Basic Generics

```typescript
// ✅ Generic function
function identity<T>(value: T): T {
  return value
}

const num = identity(42)        // number
const str = identity('hello')   // string
```

### Pattern 2: Constrained Generics

```typescript
interface HasId {
  id: string
}

function findById<T extends HasId>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id)
}

// Usage example
const users: User[] = [...]
const user = findById(users, '123')  // User | undefined
```

### Pattern 3: Multiple Type Parameters

```typescript
function map<T, U>(
  items: T[],
  mapper: (item: T) => U
): U[] {
  return items.map(mapper)
}

const numbers = [1, 2, 3]
const strings = map(numbers, n => n.toString())  // string[]
```

### Pattern 4: Generic Types

```typescript
interface ApiResponse<T> {
  data: T
  status: number
  timestamp: Date
}

type UserResponse = ApiResponse<User>
type PostsResponse = ApiResponse<Post[]>
```

## 🎨 Utilizing Utility Types

Leverage TypeScript's built-in Utility Types to improve type safety.

### Partial<T> - Makes all properties optional

```typescript
interface User {
  id: string
  name: string
  email: string
}

type PartialUser = Partial<User>
// {
//   id?: string
//   name?: string
//   email?: string
// }

function updateUser(id: string, updates: Partial<User>): User {
  // Only update some properties
  return { ...existingUser, ...updates }
}
```

### Required<T> - Makes all properties mandatory

```typescript
interface Config {
  apiKey?: string
  timeout?: number
}

type RequiredConfig = Required<Config>
// {
//   apiKey: string
//   timeout: number
// }
```

### Readonly<T> - Makes all properties read-only

```typescript
type ReadonlyUser = Readonly<User>
// {
//   readonly id: string
//   readonly name: string
//   readonly email: string
// }
```

### Pick<T, K> - Selects specific properties

```typescript
type UserCredentials = Pick<User, 'email' | 'password'>
// {
//   email: string
//   password: string
// }
```

### Omit<T, K> - Excludes specific properties

```typescript
type UserWithoutPassword = Omit<User, 'password'>
// User type excluding the password property
```

### Record<K, T> - Specifies key and value types

```typescript
type UserRoles = Record<string, 'admin' | 'user' | 'guest'>
// {
//   [key: string]: 'admin' | 'user' | 'guest'
// }

const roles: UserRoles = {
  'user-1': 'admin',
  'user-2': 'user'
}
```

### ReturnType<T> - Retrieves the return type of a function

```typescript
function createUser() {
  return {
    id: '123',
    name: 'John'
  }
}

type User = ReturnType<typeof createUser>
// {
//   id: string
//   name: string
// }
```

## 🔗 Related Files

- **[SKILL.md](../SKILL.md)** - Back to Overview
- **[PYTHON.md](./PYTHON.md)** - Python Type Safety
- **[ANTI-PATTERNS.md](./ANTI-PATTERNS.md)** - Patterns to Avoid
- **[REFERENCE.md](./REFERENCE.md)** - Checklists and Tool Settings

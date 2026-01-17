# Code Conventions to Avoid (Anti-patterns)

This file explains code patterns that should be avoided in TypeScript/JavaScript and Python.

## 📋 Table of Contents

- [Common Anti-patterns](#common-anti-patterns)
- [TypeScript-specific Anti-patterns](#typescript-specific-anti-patterns)
- [Python-specific Anti-patterns](#python-specific-anti-patterns)
- [Other General Anti-patterns](#other-general-anti-patterns)

## 🚫 Common Anti-patterns

These patterns should be avoided in both TypeScript and Python.

### 1. Magic Numbers

#### ❌ Bad Examples

```typescript
// TypeScript
function calculateDiscount(price: number): number {
  if (price > 10000) {
    return price * 0.1  // What is 0.1?
  }
  return 0
}
```

```python
# Python
def calculate_discount(price: float) -> float:
    if price > 10000:
        return price * 0.1  # What is 0.1?
    return 0
```

**Problems**:
- Meaning of the number is unclear.
- Prone to omissions when changing.
- Testing is difficult.

#### ✅ Good Examples

```typescript
// TypeScript
const DISCOUNT_THRESHOLD = 10000
const DISCOUNT_RATE = 0.1

function calculateDiscount(price: number): number {
  if (price > DISCOUNT_THRESHOLD) {
    return price * DISCOUNT_RATE
  }
  return 0
}
```

```python
# Python
DISCOUNT_THRESHOLD = 10000
DISCOUNT_RATE = 0.1

def calculate_discount(price: float) -> float:
    if price > DISCOUNT_THRESHOLD:
        return price * DISCOUNT_RATE
    return 0
```

### 2. Abuse of Global Variables

#### ❌ Bad Examples

```typescript
// TypeScript - Global variable
let userCache: Map<string, User> = new Map()

function getUser(id: string): User {
  return userCache.get(id)!  // Depends on global state
}

function setUser(user: User): void {
  userCache.set(user.id, user)  // Side effect
}
```

```python
# Python - Global variable
user_cache: Dict[str, User] = {}

def get_user(user_id: str) -> User:
    return user_cache[user_id]  # Depends on global state

def set_user(user: User) -> None:
    user_cache[user.id] = user  # Side effect
```

**Problems**:
- Testing is difficult.
- Issues arise in concurrent processing.
- Dependencies are ambiguous.

#### ✅ Good Examples

```typescript
// TypeScript - Dependency Injection
class UserRepository {
  private cache = new Map<string, User>()

  getUser(id: string): User | undefined {
    return this.cache.get(id)
  }

  setUser(user: User): void {
    this.cache.set(user.id, user)
  }
}

// At usage
const userRepo = new UserRepository()
const user = userRepo.getUser('123')
```

```python
# Python - Dependency Injection
class UserRepository:
    def __init__(self) -> None:
        self._cache: Dict[str, User] = {}

    def get_user(self, user_id: str) -> Optional[User]:
        return self._cache.get(user_id)

    def set_user(self, user: User) -> None:
        self._cache[user.id] = user

# At usage
user_repo = UserRepository()
user = user_repo.get_user('123')
```

### 3. Excessive Nesting

#### ❌ Bad Examples

```typescript
// TypeScript
function processUser(user: User | null): string {
  if (user !== null) {
    if (user.profile !== null) {
      if (user.profile.name !== null) {
        if (user.profile.name.length > 0) {
          return user.profile.name
        }
      }
    }
  }
  return 'Unknown'
}
```

```python
# Python
def process_user(user: Optional[User]) -> str:
    if user is not None:
        if user.profile is not None:
            if user.profile.name is not None:
                if len(user.profile.name) > 0:
                    return user.profile.name
    return 'Unknown'
```

**Problems**:
- Low readability.
- Maintenance is difficult.
- Bugs are easily introduced.

#### ✅ Good Examples

```typescript
// TypeScript - Early Return
function processUser(user: User | null): string {
  if (!user) return 'Unknown'
  if (!user.profile) return 'Unknown'
  if (!user.profile.name) return 'Unknown'
  if (user.profile.name.length === 0) return 'Unknown'

  return user.profile.name
}

// Even better: Optional Chaining
function processUserBetter(user: User | null): string {
  return user?.profile?.name || 'Unknown'
}
```

```python
# Python - Early Return
def process_user(user: Optional[User]) -> str:
    if user is None:
        return 'Unknown'
    if user.profile is None:
        return 'Unknown'
    if user.profile.name is None:
        return 'Unknown'
    if len(user.profile.name) == 0:
        return 'Unknown'

    return user.profile.name

# Even better: Using getattr and 'or'
def process_user_better(user: Optional[User]) -> str:
    return (
        getattr(getattr(user, 'profile', None), 'name', None)
        or 'Unknown'
    )
```

### 4. Huge Functions

#### ❌ Bad Examples

```typescript
// TypeScript - A massive function exceeding 100 lines
function processOrder(order: Order): OrderResult {
  // Verification (20 lines)
  // Inventory check (30 lines)
  // Payment processing (30 lines)
  // Notification sending (20 lines)
  // Total of 100+ lines...
}
```

**Problems**:
- Violation of Single Responsibility Principle.
- Testing is difficult.
- Cannot be reused.

#### ✅ Good Examples

```typescript
// TypeScript - Split into small functions
function processOrder(order: Order): OrderResult {
  validateOrder(order)
  checkInventory(order)
  processPayment(order)
  sendNotification(order)
  return createResult(order)
}

function validateOrder(order: Order): void {
  // Only verification (5-10 lines)
}

function checkInventory(order: Order): void {
  // Only inventory check (5-10 lines)
}

function processPayment(order: Order): void {
  // Only payment processing (5-10 lines)
}

function sendNotification(order: Order): void {
  // Only notification sending (5-10 lines)
}
```

```python
# Python - Split into small functions
def process_order(order: Order) -> OrderResult:
    validate_order(order)
    check_inventory(order)
    process_payment(order)
    send_notification(order)
    return create_result(order)

def validate_order(order: Order) -> None:
    # Only verification (5-10 lines)
    pass

def check_inventory(order: Order) -> None:
    # Only inventory check (5-10 lines)
    pass

def process_payment(order: Order) -> None:
    # Only payment processing (5-10 lines)
    pass

def send_notification(order: Order) -> None:
    # Only notification sending (5-10 lines)
    pass
```

### 5. Commented-out Code

#### ❌ Bad Examples

```typescript
// TypeScript
function calculateTotal(items: Item[]): number {
  // const tax = 0.1  // Old tax rate
  const tax = 0.08
  // return items.reduce((sum, item) => sum + item.price, 0)  // Old implementation
  return items.reduce((sum, item) => sum + item.price * (1 + tax), 0)
}
```

```python
# Python
def calculate_total(items: List[Item]) -> float:
    # tax = 0.1  # Old tax rate
    tax = 0.08
    # return sum(item.price for item in items)  # Old implementation
    return sum(item.price * (1 + tax) for item in items)
```

**Problems**:
- Bloats the code.
- Causes confusion.
- History in version control is sufficient.

#### ✅ Good Examples

```typescript
// TypeScript - Delete commented-out code
function calculateTotal(items: Item[]): number {
  const tax = 0.08
  return items.reduce((sum, item) => sum + item.price * (1 + tax), 0)
}
```

```python
# Python - Delete commented-out code
def calculate_total(items: List[Item]) -> float:
    tax = 0.08
    return sum(item.price * (1 + tax) for item in items)
```

## 🔴 TypeScript-specific Anti-patterns

### 1. Using `==` (Failure to use strict equality)

#### ❌ Bad Examples

```typescript
// ❌ == performs implicit type coercion
if (value == null) { }  // Matches both null and undefined
if (count == '0') { }   // Number 0 and string '0' are judged equal
if (flag == 1) { }      // true and 1 are judged equal
```

**Problems**:
- Implicit type coercion leads to unexpected behavior.
- Prone to bugs.
- Intent is ambiguous.

#### ✅ Good Examples

```typescript
// ✅ Use === (Strict Equality)
if (value === null || value === undefined) { }
// Or
if (value == null) { }  // This specific case might be exceptionally allowed

if (count === 0) { }  // Compare as number
if (flag === true) { }  // Compare as boolean
```

### 2. Dependency on Implicit Type Coercion

#### ❌ Bad Examples

```typescript
// ❌ Relying on implicit coercion
const num = +'42'  // Convert string to number
const str = 42 + ''  // Convert number to string
const bool = !!value  // Convert value to boolean

if (value) {  // 0, '', null, undefined, false, NaN are all falsy
  // ...
}
```

**Problems**:
- Intent is ambiguous.
- Source of bugs.
- Low readability.

#### ✅ Good Examples

```typescript
// ✅ Explicit type conversion
const num = Number('42')  // Or parseInt('42', 10)
const str = String(42)  // Or 42.toString()
const bool = Boolean(value)

// ✅ Explicit condition checks
if (value !== null && value !== undefined && value !== '') {
  // ...
}
```

### 3. Using the `Function` Type

#### ❌ Bad Examples

```typescript
// ❌ Function type is equivalent to any
const handler: Function = (x: number) => x * 2
const callback: Function = () => {}

function execute(fn: Function): any {
  return fn()  // Types of arguments and return value are unknown
}
```

**Problems**:
- Types of arguments and return value are unknown.
- Type safety is lost.

#### ✅ Good Examples

```typescript
// ✅ Define specific function signatures
type Handler = (x: number) => number
const handler: Handler = (x) => x * 2

type Callback = () => void
const callback: Callback = () => {}

function execute<T>(fn: () => T): T {
  return fn()
}
```

### 4. Using `for...in` for Array Operations

#### ❌ Bad Examples

```typescript
// ❌ for...in should not be used for arrays
const items = [1, 2, 3]
for (const index in items) {
  console.log(items[index])  // index is of type string
}
```

**Problems**:
- `index` is of type string.
- Properties from the prototype chain are also enumerated.
- Order is not guaranteed in some cases.

#### ✅ Good Examples

```typescript
// ✅ Use for...of or Array methods
const items = [1, 2, 3]

// for...of
for (const item of items) {
  console.log(item)
}

// forEach
items.forEach(item => console.log(item))

// When an index is needed
items.forEach((item, index) => console.log(index, item))
```

### 5. Use of Primitive Wrapper Objects

#### ❌ Bad Examples

```typescript
// ❌ Wrapper objects for String, Number, Boolean
const str: String = new String('hello')  // Object type
const num: Number = new Number(42)
const bool: Boolean = new Boolean(true)
```

**Problems**:
- These are object types, not primitive types.
- Do not behave as expected with comparison operators.
- Causes confusion.

#### ✅ Good Examples

```typescript
// ✅ Use primitive types
const str: string = 'hello'
const num: number = 42
const bool: boolean = true
```

## 🐍 Python-specific Anti-patterns

### 1. Mutable Default Arguments

#### ❌ Bad Example (Absolutely Forbidden)

```python
# ❌ Using mutable objects as default arguments
def add_item(item: str, items: List[str] = []) -> List[str]:
    items.append(item)
    return items

# Problem: The same list is shared across all calls
list1 = add_item('a')  # ['a']
list2 = add_item('b')  # ['a', 'b'] <- Not what was expected!
```

**Problems**:
- The same object is shared across all calls.
- Unexpected side effects occur.
- Debugging is difficult.

#### ✅ Good Examples

```python
# ✅ Default to None and initialize within the function
def add_item(item: str, items: Optional[List[str]] = None) -> List[str]:
    if items is None:
        items = []
    items.append(item)
    return items

# Or use field(default_factory=list) in a dataclass
from dataclasses import dataclass, field

@dataclass
class Container:
    items: List[str] = field(default_factory=list)
```

### 2. Use of bare `except`

#### ❌ Bad Example

```python
# ❌ Catching all exceptions
try:
    result = risky_operation()
except:  # Also catches KeyboardInterrupt and SystemExit
    print("Error occurred")
```

**Problems**:
- Catches system exceptions.
- Debugging is difficult.
- Prevents forced termination of the program.

#### ✅ Good Examples

```python
# ✅ Specify concrete exception classes
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
except KeyError as e:
    logger.error(f"Missing key: {e}")
except Exception as e:  # Use only as a last resort
    logger.exception("Unexpected error")
    raise  # Re-raise
```

### 3. Excessive Use of `lambda`

#### ❌ Bad Examples

```python
# ❌ Stuffing complex logic into a lambda
process = lambda x: x * 2 if x > 0 else x / 2 if x < 0 else 0

# ❌ Multi-line lambda (not possible, but attempting to force it)
# You can't actually write this, but the thought process itself is a problem.
```

**Problems**:
- Low readability.
- Debugging is difficult.
- Hard to understand because it lacks a name.

#### ✅ Good Examples

```python
# ✅ Define as a regular function
def process_value(x: float) -> float:
    """Processes a value"""
    if x > 0:
        return x * 2
    elif x < 0:
        return x / 2
    return 0

# Use lambda only for simple operations
items.sort(key=lambda x: x.name)  # This is fine
```

### 4. Not Using `get()` for Dictionaries

#### ❌ Bad Examples

```python
# ❌ Potential for KeyError
def get_user_name(user_dict: Dict[str, str]) -> str:
    return user_dict['name']  # Error if 'name' key is missing

# ❌ Redundant check
def get_user_name_verbose(user_dict: Dict[str, str]) -> str:
    if 'name' in user_dict:
        return user_dict['name']
    else:
        return 'Unknown'
```

**Problems**:
- KeyError is likely to occur.
- Code is redundant.

#### ✅ Good Examples

```python
# ✅ Use the get() method
def get_user_name(user_dict: Dict[str, str]) -> str:
    return user_dict.get('name', 'Unknown')

# ✅ Even safer if you use TypedDict
class UserDict(TypedDict):
    name: str
    email: str

def get_user_name_typed(user: UserDict) -> str:
    return user['name']  # Presence is guaranteed by type check
```

### 5. Inefficient String Concatenation

#### ❌ Bad Examples

```python
# ❌ String concatenation in a loop (inefficient)
result = ''
for item in items:
    result += item + ','  # Creates a new string object every time

# ❌ Inefficient string formatting
message = 'Hello, ' + name + '! You have ' + str(count) + ' messages.'
```

**Problems**:
- Strings are immutable, so a new object is created every time.
- Poor memory efficiency.
- Performance degrades.

#### ✅ Good Examples

```python
# ✅ Use join()
result = ','.join(items)

# ✅ Use f-strings
message = f'Hello, {name}! You have {count} messages.'

# ✅ Combine join with a list comprehension
result = ','.join(str(item) for item in items)
```

## 🔧 Other General Anti-patterns

### 1. Excessive Comments

#### ❌ Bad Example

```typescript
// ❌ Self-evident comments
// Gets user ID
function getUserId(): string {
  // Get id property from user variable
  return user.id  // Returns id
}
```

**Problems**:
- Duplicating what can be understood by reading the code.
- Increases maintenance cost.

#### ✅ Good Example

```typescript
// ✅ Comments explain "Why"
function calculateDiscount(price: number): number {
  // Apply special discount during the March 2024 campaign
  // Additional 5% discount on top of the usual 10%
  const baseDiscount = 0.10
  const campaignDiscount = 0.05
  return price * (1 - baseDiscount - campaignDiscount)
}
```

### 2. Argument Lists that are Too Long

#### ❌ Bad Example

```typescript
// ❌ Too many arguments
function createUser(
  id: string,
  firstName: string,
  lastName: string,
  email: string,
  age: number,
  address: string,
  phone: string,
  country: string,
  isActive: boolean
): User {
  // ...
}
```

**Problems**:
- Difficult to remember the order of arguments.
- Easy to make mistakes when calling.
- Low readability.

#### ✅ Good Example

```typescript
// ✅ Use an options object
interface CreateUserParams {
  id: string
  firstName: string
  lastName: string
  email: string
  age: number
  address: string
  phone: string
  country: string
  isActive: boolean
}

function createUser(params: CreateUserParams): User {
  // ...
}

// At usage
createUser({
  id: '123',
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com',
  age: 30,
  address: '123 Main St',
  phone: '555-1234',
  country: 'US',
  isActive: true
})
```

```python
# Python - Use a dataclass
@dataclass
class CreateUserParams:
    id: str
    first_name: str
    last_name: str
    email: str
    age: int
    address: str
    phone: str
    country: str
    is_active: bool = True

def create_user(params: CreateUserParams) -> User:
    # ...
    pass

# At usage
create_user(CreateUserParams(
    id='123',
    first_name='John',
    last_name='Doe',
    email='john@example.com',
    age=30,
    address='123 Main St',
    phone='555-1234',
    country='US'
))
```

### 3. Meaningless Variable Names

#### ❌ Bad Example

```typescript
// ❌ Cryptic variable names
const x = getUserById('123')
const tmp = calculateTotal(items)
const data = fetchData()
const result = processData(data)
```

**Problems**:
- Purpose of variables is unknown.
- Code is difficult to understand.

#### ✅ Good Example

```typescript
// ✅ Intent-revealing variable names
const currentUser = getUserById('123')
const orderTotal = calculateTotal(items)
const customerData = fetchCustomerData()
const validatedOrder = validateOrder(customerData)
```

## 🔗 Related Files

- **[SKILL.md](../SKILL.md)** - Back to Overview
- **[TYPESCRIPT.md](./TYPESCRIPT.md)** - TypeScript Type Safety
- **[PYTHON.md](./PYTHON.md)** - Python Type Safety
- **[REFERENCE.md](./REFERENCE.md)** - Checklists and Tool Settings

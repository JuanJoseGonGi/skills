# Clean Code Basics

Explanation of fundamental principles to apply in daily coding.

## 📋 Table of Contents
1. [Naming Conventions](#naming-conventions)
2. [Function Design](#function-design)
3. [Early Return](#early-return)
4. [Eliminating Magic Numbers](#eliminating-magic-numbers)
5. [Comments and Documentation](#comments-and-documentation)

---

## Naming Conventions

### Principle: Clarify Intent

**Conditions for good naming**:
- Purpose is obvious at a glance
- Searchable
- Pronounceable
- Culturally appropriate

### Function Names: Start with a Verb

#### ✅ Good Example: Clear intent
```typescript
// Action is clear
getUserById(id: string): User
calculateTotalPrice(items: Item[]): number
validateEmail(email: string): boolean
formatDate(date: Date): string
isAuthenticated(): boolean
hasPermission(user: User, resource: string): boolean

// Get state: get/is/has
getActiveUsers(): User[]
isEmailValid(email: string): boolean
hasUnreadMessages(): boolean

// Change state: set/update/create/delete
setUserName(name: string): void
updateUserProfile(profile: Profile): void
createOrder(items: Item[]): Order
deleteAccount(userId: string): void
```

#### ❌ Bad Example: Ambiguous naming
```typescript
// Unclear what it does
getUser(id: string): User  // Which user? What are the conditions?
calc(items: Item[]): number  // Calculates what?
check(email: string): boolean  // Checks what?
process(data: any): void  // Processes what?
handle(event: Event): void  // Handles how?

// Too abbreviated
usr(): User
calc(): number
chk(): boolean
proc(): void
```

### Variable Names: Express as Nouns

#### ✅ Good Example: Clear purpose
```typescript
// Specific and searchable
const MAX_RETRY_COUNT = 3
const DEFAULT_TIMEOUT_MS = 5000
const API_BASE_URL = 'https://api.example.com'

// Pluralize for arrays
const activeUsers: User[] = []
const completedOrders: Order[] = []
const errorMessages: string[] = []

// Booleans start with is/has/can
const isAuthenticated: boolean = true
const hasPermission: boolean = false
const canEdit: boolean = checkPermission()

// Meaningful names
const userRegistrationDate: Date = new Date()
const totalPriceIncludingTax: number = calculateTotal()
```

#### ❌ Bad Example: Magic numbers and ambiguous names
```typescript
// Magic number (meaning unknown)
setTimeout(() => {}, 5000)  // What does 5000 mean?
for (let i = 0; i < 3; i++) { }  // What does 3 mean?

// Ambiguous names
let data: any = {}  // What kind of data?
let temp: string = ''  // Temporary what?
let result: any = process()  // What kind of result?
let flag: boolean = true  // What kind of flag?

// Abbreviated (unpronounceable, hard to search)
let usrNm: string = ''  // userName
let dtFmt: string = ''  // dateFormat
let errCd: number = 0   // errorCode
```

### Class Names: Express as Nouns

#### ✅ Good Examples
```typescript
// Role is clear
class UserRepository { }
class EmailService { }
class PaymentProcessor { }
class OrderValidator { }
class ReportGenerator { }

// Specific with multiple words
class UserAuthenticationService { }
class ProductInventoryManager { }
class CustomerNotificationService { }
```

#### ❌ Bad Examples
```typescript
// Too ambiguous
class Manager { }  // Manages what?
class Handler { }  // Handles what?
class Helper { }   // Helps what?
class Util { }     // Utility for what?

// Starts with a verb (should not be function-like)
class ProcessUser { }
class HandleOrder { }
class ValidateData { }
```

---

## Function Design

### Principle 1: Small and Single Responsibility

#### ✅ Good Example: Split into small functions
```typescript
// Each function has a single responsibility
function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

function validatePassword(password: string): boolean {
  return password.length >= 8
}

function validateUserData(user: User): void {
  if (!validateEmail(user.email)) {
    throw new Error('Invalid email address')
  }
  if (!validatePassword(user.password)) {
    throw new Error('Password must be at least 8 characters')
  }
}

function saveUser(user: User): void {
  validateUserData(user)
  database.save(user)
}

function sendWelcomeEmail(user: User): void {
  const emailService = new EmailService()
  emailService.send(user.email, 'Welcome!', 'Welcome to our service!')
}

// Main processing: Combine each function
function registerUser(user: User): void {
  saveUser(user)
  sendWelcomeEmail(user)
}
```

**Benefits**:
- Clear responsibility for each function
- Easier to test
- Reusable
- Easy to understand

#### ❌ Bad Example: Huge with multiple responsibilities
```typescript
// ❌ Huge function with 100+ lines
function processUser(user: User) {
  // Validation (20 lines)
  if (!user.email || !user.email.includes('@')) {
    throw new Error('Invalid email')
  }
  if (!user.password || user.password.length < 8) {
    throw new Error('Invalid password')
  }
  // ... more validation logic

  // Database save (20 lines)
  const db = new Database()
  db.connect()
  db.insert('users', user)
  db.disconnect()
  // ... more DB operations

  // Email sending (20 lines)
  const emailService = new EmailService()
  emailService.configure()
  emailService.send(user.email, 'Welcome', 'Welcome!')
  // ... more email processing

  // Logging (20 lines)
  const logger = new Logger()
  logger.log('User registered')
  // ... more logging

  // Other processes...
}
```

**Problems**:
- Hard to understand what it's doing
- Testing is complex
- Changes in one part affect the whole
- Not reusable

### Principle 2: Minimal Arguments (0-2 is ideal)

#### ✅ Good Example: Few arguments
```typescript
// 0 arguments (Ideal)
function getCurrentUser(): User {
  return authService.getUser()
}

// 1 argument (Good)
function getUserById(id: string): User {
  return database.findOne({ id })
}

// 2 arguments (Acceptable)
function createUser(name: string, email: string): User {
  return { name, email }
}
```

#### ⚠️ If there are many arguments: Pass as an object
```typescript
// ❌ Too many arguments
function createUser(
  name: string,
  email: string,
  age: number,
  address: string,
  phone: string,
  country: string,
  zipCode: string
) { }

// ✅ Pass as an object
interface UserData {
  name: string
  email: string
  age: number
  address: string
  phone: string
  country: string
  zipCode: string
}

function createUser(data: UserData): User {
  return { ...data }
}

// At usage
createUser({
  name: 'John',
  email: 'john@example.com',
  age: 30,
  address: '123 Main St',
  phone: '123-456-7890',
  country: 'USA',
  zipCode: '12345'
})
```

**Benefits of passing as an object**:
- Order doesn't matter
- Optional properties can be defined
- Type-safe (in TypeScript)
- Easy to extend

### Principle 3: Avoid Side Effects

#### ✅ Good Example: Pure functions
```typescript
// No side effects: Returns a new array
function addItem(items: Item[], newItem: Item): Item[] {
  return [...items, newItem]
}

// No side effects: Returns a new object
function updateUserName(user: User, newName: string): User {
  return { ...user, name: newName }
}

// Calculation only: Doesn't change external state
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0)
}
```

#### ❌ Bad Example: Has side effects
```typescript
// ❌ Directly modifies argument (unpredictable)
function addItem(items: Item[], newItem: Item): void {
  items.push(newItem)  // Modifies original array
}

// ❌ Modifies global state
let totalPrice = 0
function calculateTotal(items: Item[]): void {
  totalPrice = items.reduce((sum, item) => sum + item.price, 0)
}
```

---

## Early Return

### Principle: Reduce nesting with guard clauses

#### ✅ Good Example: Nesting reduction with early return
```typescript
function processOrder(order: Order | null): void {
  // Guard clause: Early return
  if (!order) {
    console.log('Order is null')
    return
  }

  if (order.status !== 'pending') {
    console.log('Order is not pending')
    return
  }

  if (order.items.length === 0) {
    console.log('Order has no items')
    return
  }

  // Main logic (No nesting)
  const total = calculateTotal(order)
  sendConfirmation(order, total)
  updateInventory(order)
}
```

**Benefits**:
- Shallow nesting (easy to understand)
- Error cases are clear
- Main logic stands out

#### ❌ Bad Example: Deep nesting
```typescript
function processOrder(order: Order | null): void {
  if (order) {  // Nesting 1
    if (order.status === 'pending') {  // Nesting 2
      if (order.items.length > 0) {  // Nesting 3
        // Main logic (inside deep nesting)
        const total = calculateTotal(order)
        sendConfirmation(order, total)
        updateInventory(order)
      } else {
        console.log('Order has no items')
      }
    } else {
      console.log('Order is not pending')
    }
  } else {
    console.log('Order is null')
  }
}
```

**Problems**:
- Deep nesting (hard to understand)
- Main logic is buried
- Many `else` statements add complexity

### In case of complex conditions

#### ✅ Good Example: Functionalize conditions
```typescript
function canProcessOrder(order: Order | null): boolean {
  if (!order) return false
  if (order.status !== 'pending') return false
  if (order.items.length === 0) return false
  return true
}

function processOrder(order: Order | null): void {
  if (!canProcessOrder(order)) {
    console.log('Cannot process order')
    return
  }

  // Main logic
  const total = calculateTotal(order)
  sendConfirmation(order!, total)
  updateInventory(order!)
}
```

---

## Eliminating Magic Numbers

### Principle: Name your constants

#### ✅ Good Example: Meaningful constant names
```typescript
// Define as constants
const MAX_RETRY_COUNT = 3
const DEFAULT_TIMEOUT_MS = 5000
const API_RATE_LIMIT_PER_MINUTE = 100
const MIN_PASSWORD_LENGTH = 8
const MAX_FILE_SIZE_MB = 10

// Usage example
function retryRequest(request: Request): Promise<Response> {
  for (let i = 0; i < MAX_RETRY_COUNT; i++) {
    try {
      return await fetch(request)
    } catch (error) {
      if (i === MAX_RETRY_COUNT - 1) throw error
      await sleep(DEFAULT_TIMEOUT_MS)
    }
  }
}

function validatePassword(password: string): boolean {
  return password.length >= MIN_PASSWORD_LENGTH
}
```

**Benefits**:
- Clear intent
- Searchable
- Easy to change (managed in one place)
- Type-safe (in TypeScript)

#### ❌ Bad Example: Magic numbers
```typescript
// ❌ Meaning of numbers is unknown
function retryRequest(request: Request): Promise<Response> {
  for (let i = 0; i < 3; i++) {  // What does 3 mean?
    try {
      return await fetch(request)
    } catch (error) {
      if (i === 2) throw error  // Why 2?
      await sleep(5000)  // Why 5000ms?
    }
  }
}

function validatePassword(password: string): boolean {
  return password.length >= 8  // Why 8 characters?
}
```

### Leveraging Enums

#### ✅ Good Example: Manage state with Enums
```typescript
// TypeScript Enum
enum OrderStatus {
  Pending = 'pending',
  Processing = 'processing',
  Shipped = 'shipped',
  Delivered = 'delivered',
  Cancelled = 'cancelled'
}

function processOrder(order: Order): void {
  if (order.status === OrderStatus.Pending) {
    // Process
  }
}

// Or const assertion (Recommended)
const OrderStatus = {
  Pending: 'pending',
  Processing: 'processing',
  Shipped: 'shipped',
  Delivered: 'delivered',
  Cancelled: 'cancelled'
} as const

type OrderStatus = typeof OrderStatus[keyof typeof OrderStatus]
```

---

## Comments and Documentation

### Principle: Only comment what cannot be explained by code

#### ✅ Good Comments
```typescript
// Explanation of business logic
// If order amount is 10,000 or more, shipping is free
function calculateShippingFee(orderAmount: number): number {
  const FREE_SHIPPING_THRESHOLD = 10000
  return orderAmount >= FREE_SHIPPING_THRESHOLD ? 0 : 500
}

// Explanation of complex algorithm
// Quick Sort: Average O(n log n), Worst O(n^2)
function quickSort(arr: number[]): number[] {
  if (arr.length <= 1) return arr
  const pivot = arr[0]
  const left = arr.slice(1).filter(x => x <= pivot)
  const right = arr.slice(1).filter(x => x > pivot)
  return [...quickSort(left), pivot, ...quickSort(right)]
}

// TODO, FIXME, NOTE
// TODO: Add cache functionality in the future
// FIXME: Need to improve error handling
// NOTE: This process is executed asynchronously
```

#### ❌ Unnecessary Comments
```typescript
// ❌ Obvious from reading code
// Get user ID
const userId = user.id

// ❌ Contradicts code
// Delete user (actually deactivates)
function deleteUser(userId: string): void {
  database.update({ id: userId, active: false })
}

// ❌ Commented out code (should be deleted)
// function oldFunction() {
//   // Old implementation
// }

// ❌ Historical information (should be managed by Git history)
// 2023-01-01: John - Initial implementation
// 2023-02-01: Jane - Bug fix
```

### Leveraging JSDoc (TypeScript)

#### ✅ Good Example: Documentation for public API
```typescript
/**
 * Search for a user by ID
 *
 * @param userId - Unique identifier of the user
 * @returns Found user, or null
 * @throws {DatabaseError} On database error
 *
 * @example
 * const user = await getUserById('user-123')
 * if (user) {
 *   console.log(user.name)
 * }
 */
async function getUserById(userId: string): Promise<User | null> {
  return database.findOne({ id: userId })
}
```

---

## 🔗 Related Documents

- [Details of SOLID Principles](./SOLID-PRINCIPLES.md)
- [Quality Checklist](./QUALITY-CHECKLIST.md)
- [Quick Reference](./QUICK-REFERENCE.md)

## 📖 Reference Links

- [Clean Code Main Page](../SKILL.md)

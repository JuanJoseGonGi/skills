# Input Validation and Injection Countermeasures

[← Back to Secure Coding](../SKILL.md)

## 📖 Table of Contents

- [Basic Principles of Input Validation](#basic-principles-of-input-validation)
- [Implementation of Input Validation](#implementation-of-input-validation)
- [Sanitization](#sanitization)
- [SQL Injection Countermeasures](#sql-injection-countermeasures)
- [XSS Countermeasures](#xss-countermeasures)
- [CSRF Countermeasures](#csrf-countermeasures)
- [Command Injection Countermeasures](#command-injection-countermeasures)
- [Other Injection Countermeasures](#other-injection-countermeasures)

## Basic Principles of Input Validation

### Important Principles
1. **Assume all external input is untrusted**
   - User input
   - URL parameters
   - HTTP headers
   - Cookies
   - File uploads
   - External API responses

2. **Server-side validation is mandatory**
   - Client-side validation is auxiliary.
   - Do not omit server-side validation.

3. **Prioritize whitelisting**
   - Blacklisting (forbidden list) is fragile.
   - Use whitelisting (allowed list).

## Implementation of Input Validation

### ✅ Type-safe Input Validation with Zod

```typescript
import { z } from 'zod'

// Basic schema definition
const UserSchema = z.object({
  // Email validation
  email: z.string().email('Please enter a valid email address'),

  // Age validation (range)
  age: z.number().min(0).max(150),

  // Username validation (regex)
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be within 20 characters')
    .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain alphanumeric characters and underscores'),

  // Password validation (complexity requirements)
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must include at least one uppercase letter')
    .regex(/[a-z]/, 'Must include at least one lowercase letter')
    .regex(/[0-9]/, 'Must include at least one digit')
    .regex(/[^A-Za-z0-9]/, 'Must include at least one symbol'),

  // URL validation
  website: z.string().url().optional(),

  // Date validation
  birthdate: z.date().max(new Date(), 'Future dates are not allowed'),

  // Enum validation
  role: z.enum(['user', 'admin', 'moderator'])
})

// Validation for nested objects
const PostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1).max(10000),
  tags: z.array(z.string()).min(1).max(5),
  author: UserSchema,
  metadata: z.object({
    viewCount: z.number().min(0),
    lastUpdated: z.date()
  }).optional()
})

// Usage example
function createUser(input: unknown) {
  try {
    // Input validation
    const validated = UserSchema.parse(input)

    // Process with validated data
    return userRepository.create(validated)
  } catch (error) {
    if (error instanceof z.ZodError) {
      // Handling validation errors
      const errors = error.errors.map(err => ({
        field: err.path.join('.'),
        message: err.message
      }))
      throw new ValidationError('Input data is invalid', errors)
    }
    throw error
  }
}

// Validation for partial updates
const PartialUserSchema = UserSchema.partial()

function updateUser(userId: string, input: unknown) {
  const validated = PartialUserSchema.parse(input)
  return userRepository.update(userId, validated)
}
```

### ✅ Custom Validation

```typescript
// Custom validation function
const EmailDomainSchema = z.string().email().refine(
  (email) => {
    const allowedDomains = ['example.com', 'company.com']
    const domain = email.split('@')[1]
    return allowedDomains.includes(domain)
  },
  { message: 'Unauthorized domain' }
)

// Mutual validation of multiple fields
const DateRangeSchema = z.object({
  startDate: z.date(),
  endDate: z.date()
}).refine(
  (data) => data.endDate > data.startDate,
  {
    message: 'End date must be after start date',
    path: ['endDate']
  }
)

// Password confirmation
const PasswordConfirmSchema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string()
}).refine(
  (data) => data.password === data.confirmPassword,
  {
    message: 'Passwords do not match',
    path: ['confirmPassword']
  }
)
```

### ✅ Implementation Example in Express.js

```typescript
import express from 'express'
import { z } from 'zod'

// Validation middleware
function validateBody<T extends z.ZodType>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body)
      next()
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({
          error: 'Input data is invalid',
          details: error.errors
        })
      } else {
        next(error)
      }
    }
  }
}

// Validation for query parameters
function validateQuery<T extends z.ZodType>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.query = schema.parse(req.query)
      next()
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({
          error: 'Query parameters are invalid',
          details: error.errors
        })
      } else {
        next(error)
      }
    }
  }
}

// Usage example
app.post('/api/users',
  validateBody(UserSchema),
  async (req, res) => {
    const user = await createUser(req.body)
    res.json(user)
  }
)

const PaginationSchema = z.object({
  page: z.coerce.number().min(1).default(1),
  limit: z.coerce.number().min(1).max(100).default(20)
})

app.get('/api/users',
  validateQuery(PaginationSchema),
  async (req, res) => {
    const users = await userRepository.findMany(req.query)
    res.json(users)
  }
)
```

## Sanitization

### ✅ String Sanitization

```typescript
// Escaping HTML special characters
function escapeHtml(unsafe: string): string {
  return unsafe
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

// Normalizing whitespace
function normalizeWhitespace(str: string): string {
  return str.trim().replace(/\s+/g, ' ')
}

// Filename sanitization
function sanitizeFilename(filename: string): string {
  return filename
    .replace(/[^a-zA-Z0-9.-]/g, '_')  // Replace anything other than alphanumeric, dots, and hyphens with underscore
    .replace(/\.+/g, '.')  // Replace consecutive dots with a single dot
    .replace(/^\./, '')  // Remove leading dot
    .substring(0, 255)  // Limit to maximum length
}

// URL sanitization
function sanitizeUrl(url: string): string {
  try {
    const parsed = new URL(url)

    // Forbidden JavaScript protocol
    if (parsed.protocol === 'javascript:') {
      throw new Error('JavaScript URLs are not allowed')
    }

    // Allow only HTTPS (if necessary)
    if (parsed.protocol !== 'https:') {
      throw new Error('Only HTTPS is allowed')
    }

    return parsed.toString()
  } catch {
    throw new Error('Invalid URL')
  }
}
```

### ✅ HTML Sanitization with DOMPurify

```typescript
import DOMPurify from 'dompurify'
import { JSDOM } from 'jsdom'

// Server-side DOMPurify configuration
const window = new JSDOM('').window
const purify = DOMPurify(window as unknown as Window)

// Basic usage
function sanitizeHtml(dirty: string): string {
  return purify.sanitize(dirty)
}

// Strict custom configuration
function sanitizeHtmlStrict(dirty: string): string {
  return purify.sanitize(dirty, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'a'],
    ALLOWED_ATTR: ['href'],
    ALLOW_DATA_ATTR: false
  })
}

// Allow only links
function sanitizeLinks(dirty: string): string {
  return purify.sanitize(dirty, {
    ALLOWED_TAGS: ['a'],
    ALLOWED_ATTR: ['href', 'title'],
    ALLOWED_URI_REGEXP: /^https?:\/\//  // HTTP or HTTPS only
  })
}
```

## SQL Injection Countermeasures

### ✅ Prepared Statements (Most Important)

```typescript
// ❌ String concatenation (Vulnerable to SQL Injection)
async function getUserByIdUnsafe(userId: string) {
  const query = `SELECT * FROM users WHERE id = '${userId}'`
  return db.query(query)  // Dangerous!
}

// ✅ Prepared Statements (Safe)
async function getUserById(userId: string) {
  const query = 'SELECT * FROM users WHERE id = $1'
  return db.query(query, [userId])  // Safe
}

// ✅ Using an ORM (Example: Prisma)
async function getUserById(userId: string) {
  return prisma.user.findUnique({
    where: { id: userId }
  })
}

// ✅ Using a Query Builder (Example: Knex)
async function getUserById(userId: string) {
  return knex('users')
    .where('id', userId)
    .first()
}
```

### ✅ Safe Construction of Complex Queries

```typescript
// Constructing dynamic WHERE clauses
async function searchUsers(filters: {
  name?: string
  email?: string
  role?: string
  minAge?: number
}) {
  const conditions: string[] = []
  const values: any[] = []
  let paramIndex = 1

  if (filters.name) {
    conditions.push(`name ILIKE $${paramIndex}`)
    values.push(`%${filters.name}%`)
    paramIndex++
  }

  if (filters.email) {
    conditions.push(`email = $${paramIndex}`)
    values.push(filters.email)
    paramIndex++
  }

  if (filters.role) {
    conditions.push(`role = $${paramIndex}`)
    values.push(filters.role)
    paramIndex++
  }

  if (filters.minAge !== undefined) {
    conditions.push(`age >= $${paramIndex}`)
    values.push(filters.minAge)
    paramIndex++
  }

  const whereClause = conditions.length > 0
    ? `WHERE ${conditions.join(' AND ')}`
    : ''

  const query = `
    SELECT id, name, email, role, age
    FROM users
    ${whereClause}
    ORDER BY created_at DESC
  `

  return db.query(query, values)
}

// Implementation with ORM (Even safer)
async function searchUsersORM(filters: {
  name?: string
  email?: string
  role?: string
  minAge?: number
}) {
  return prisma.user.findMany({
    where: {
      name: filters.name ? { contains: filters.name, mode: 'insensitive' } : undefined,
      email: filters.email,
      role: filters.role,
      age: filters.minAge !== undefined ? { gte: filters.minAge } : undefined
    },
    orderBy: { createdAt: 'desc' }
  })
}
```

### ❌ Common Mistakes

```typescript
// ❌ String concatenation in LIKE clause
const query = `SELECT * FROM users WHERE name LIKE '%${searchTerm}%'`

// ✅ Correct implementation
const query = 'SELECT * FROM users WHERE name LIKE $1'
const params = [`%${searchTerm}%`]

// ❌ String concatenation in IN clause
const ids = [1, 2, 3]
const query = `SELECT * FROM users WHERE id IN (${ids.join(',')})`

// ✅ Correct implementation
const query = `SELECT * FROM users WHERE id = ANY($1::int[])`
const params = [ids]
```

## XSS Countermeasures

### ✅ Content Escaping

```typescript
// React (Automatic escaping)
function UserProfile({ user }: { user: User }) {
  return (
    <div>
      {/* Automatically escaped */}
      <h1>{user.name}</h1>
      <p>{user.bio}</p>
    </div>
  )
}

// ❌ Improper use of dangerouslySetInnerHTML
function UnsafeComponent({ content }: { content: string }) {
  return <div dangerouslySetInnerHTML={{ __html: content }} />  // Dangerous
}

// ✅ Use after sanitizing with DOMPurify
import DOMPurify from 'dompurify'

function SafeComponent({ content }: { content: string }) {
  const sanitized = DOMPurify.sanitize(content)
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />
}
```

### ✅ Content Security Policy (CSP)

```typescript
import helmet from 'helmet'

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: [
      "'self'",
      // Allow only trusted CDNs
      'https://cdn.jsdelivr.net'
    ],
    styleSrc: [
      "'self'",
      // Hashes for inline styles (if necessary)
      "'sha256-xyz...'"
    ],
    imgSrc: ["'self'", 'data:', 'https:'],
    connectSrc: ["'self'", 'https://api.example.com'],
    fontSrc: ["'self'"],
    objectSrc: ["'none'"],
    upgradeInsecureRequests: []
  }
}))
```

## CSRF Countermeasures

### ✅ Implementation of CSRF Tokens

```typescript
import csrf from 'csurf'
import cookieParser from 'cookie-parser'

// CSRF middleware configuration
app.use(cookieParser())
const csrfProtection = csrf({ cookie: true })

// Form display
app.get('/form', csrfProtection, (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() })
})

// Form submission
app.post('/submit', csrfProtection, (req, res) => {
  // CSRF token is automatically verified
  res.send('Data received')
})

// API endpoint (JSON)
app.post('/api/data', csrfProtection, (req, res) => {
  res.json({ success: true })
})
```

### ✅ SameSite Cookie Attribute

```typescript
app.use(session({
  secret: process.env.SESSION_SECRET!,
  cookie: {
    httpOnly: true,
    secure: true,  // HTTPS mandatory
    sameSite: 'strict',  // CSRF countermeasure
    maxAge: 24 * 60 * 60 * 1000  // 24 hours
  }
}))
```

### ✅ Origin Header Verification

```typescript
function validateOrigin(req: Request, res: Response, next: NextFunction) {
  const origin = req.get('origin')
  const allowedOrigins = [
    'https://example.com',
    'https://www.example.com'
  ]

  if (origin && !allowedOrigins.includes(origin)) {
    return res.status(403).json({ error: 'Invalid Origin' })
  }

  next()
}

app.post('/api/sensitive', validateOrigin, csrfProtection, handler)
```

## Command Injection Countermeasures

### ✅ Safe Command Execution

```typescript
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

// ❌ Using user input directly in a command
async function unsafeCommand(filename: string) {
  const { stdout } = await execAsync(`cat ${filename}`)  // Dangerous
  return stdout
}

// ✅ Whitelist approach
const ALLOWED_COMMANDS = ['ls', 'pwd', 'whoami'] as const
type AllowedCommand = typeof ALLOWED_COMMANDS[number]

async function safeCommand(command: AllowedCommand) {
  if (!ALLOWED_COMMANDS.includes(command)) {
    throw new Error('Unauthorized command')
  }

  const { stdout } = await execAsync(command)
  return stdout
}

// ✅ Use libraries (Avoid command execution)
import fs from 'fs/promises'

async function readFileSafe(filename: string) {
  // Filename validation
  if (!/^[a-zA-Z0-9._-]+$/.test(filename)) {
    throw new Error('Invalid filename')
  }

  // Path traversal countermeasure
  if (filename.includes('..')) {
    throw new Error('Invalid file path')
  }

  return fs.readFile(filename, 'utf8')
}
```

## Other Injection Countermeasures

### ✅ LDAP Injection Countermeasures

```typescript
// Escaping LDAP special characters
function escapeLDAP(input: string): string {
  return input
    .replace(/\\/g, '\\5c')
    .replace(/\*/g, '\\2a')
    .replace(/\(/g, '\\28')
    .replace(/\)/g, '\\29')
    .replace(/\0/g, '\\00')
}

function searchLDAP(username: string) {
  const escapedUsername = escapeLDAP(username)
  const filter = `(uid=${escapedUsername})`
  // Execute LDAP query
}
```

### ✅ XML Injection Countermeasures

```typescript
import { parseString } from 'xml2js'

// Disable XML Entities
const parserOptions = {
  explicitArray: false,
  ignoreAttrs: true,
  // XXE attack countermeasure
  xmlns: false,
  explicitCharkey: false
}

function parseXMLSafe(xmlString: string): Promise<any> {
  return new Promise((resolve, reject) => {
    parseString(xmlString, parserOptions, (err, result) => {
      if (err) reject(err)
      else resolve(result)
    })
  })
}
```

---

[← Back to Secure Coding](../SKILL.md) | [Next: Authentication, Authorization, and Secrets Management →](AUTH-SECRETS.md)

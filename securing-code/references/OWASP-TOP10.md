# OWASP Top 10 Countermeasures Guide

[← Back to Secure Coding](../SKILL.md)

## 📖 Table of Contents

- [Overview](#overview)
- [A01: Broken Access Control](#a01-broken-access-control)
- [A02: Cryptographic Failures](#a02-cryptographic-failures)
- [A03: Injection](#a03-injection)
- [A04: Insecure Design](#a04-insecure-design)
- [A05: Security Misconfiguration](#a05-security-misconfiguration)
- [A06: Vulnerable and Outdated Components](#a06-vulnerable-and-outdated-components)
- [A07: Identification and Authentication Failures](#a07-identification-and-authentication-failures)
- [A08: Software and Data Integrity Failures](#a08-software-and-data-integrity-failures)
- [A09: Security Logging and Monitoring Failures](#a09-security-logging-and-monitoring-failures)
- [A10: Server-Side Request Forgery (SSRF)](#a10-server-side-request-forgery-ssrf)
- [Pre-completion Checklist](#pre-completion-checklist)

## Overview

The OWASP (Open Web Application Security Project) Top 10 is a list of the most critical security risks to web applications. Countermeasures for these risks are mandatory in all web application development.

**Important**: Always perform a security check with CodeGuard upon completion of implementation.

## A01: Broken Access Control

### Overview
Vulnerabilities that allow users to access resources outside of their permissions.

### Countermeasures

#### ✅ Implementation of Authorization Checks
```typescript
// Authorization check
function deleteUser(userId: string, currentUser: User) {
  // Admin privilege check
  if (currentUser.role !== 'admin') {
    throw new UnauthorizedError('Admin privileges required')
  }

  // Prevent self-deletion
  if (userId === currentUser.id) {
    throw new ForbiddenError('You cannot delete your own account')
  }

  return userRepository.delete(userId)
}

// Resource ownership check
function updatePost(postId: string, currentUser: User, data: PostUpdateData) {
  const post = await postRepository.findById(postId)

  // Ownership check
  if (post.authorId !== currentUser.id && currentUser.role !== 'admin') {
    throw new ForbiddenError('You do not have permission to edit this resource')
  }

  return postRepository.update(postId, data)
}
```

#### ✅ Role-Based Access Control (RBAC)
```typescript
// Permission definitions
enum Permission {
  READ_POSTS = 'read:posts',
  CREATE_POSTS = 'create:posts',
  UPDATE_OWN_POSTS = 'update:own:posts',
  UPDATE_ANY_POSTS = 'update:any:posts',
  DELETE_POSTS = 'delete:posts'
}

// Role definitions
const ROLES = {
  user: [
    Permission.READ_POSTS,
    Permission.CREATE_POSTS,
    Permission.UPDATE_OWN_POSTS
  ],
  moderator: [
    Permission.READ_POSTS,
    Permission.CREATE_POSTS,
    Permission.UPDATE_ANY_POSTS
  ],
  admin: Object.values(Permission)
}

// Permission check middleware
function requirePermission(permission: Permission) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userPermissions = ROLES[req.user.role]

    if (!userPermissions.includes(permission)) {
      throw new ForbiddenError('Permission denied')
    }

    next()
  }
}

// Usage example
app.delete('/api/posts/:id',
  authenticate,
  requirePermission(Permission.DELETE_POSTS),
  deletePostHandler
)
```

### ❌ What Not to Do
```typescript
// Trusting permission info sent from the client
function deleteUser(userId: string, isAdmin: boolean) {  // Dangerous
  if (isAdmin) {
    return userRepository.delete(userId)
  }
}

// Access control using only URL parameters
app.get('/api/users/:userId', (req, res) => {  // Dangerous
  // No authentication/authorization check
  const user = await userRepository.findById(req.params.userId)
  res.json(user)
})
```

## A02: Cryptographic Failures

### Overview
Inadequate encryption of sensitive data, or storage/transmission in unencrypted states.

### Countermeasures

#### ✅ Password Hashing
```typescript
import bcrypt from 'bcrypt'

// Password hashing
async function hashPassword(plainPassword: string): Promise<string> {
  const saltRounds = 10
  return bcrypt.hash(plainPassword, saltRounds)
}

// Password verification
async function verifyPassword(
  plainPassword: string,
  hashedPassword: string
): Promise<boolean> {
  return bcrypt.compare(plainPassword, hashedPassword)
}

// User creation
async function createUser(data: UserCreateData) {
  const hashedPassword = await hashPassword(data.password)

  return userRepository.create({
    ...data,
    password: hashedPassword  // Store the hashed password
  })
}
```

#### ✅ Data Encryption
```typescript
import crypto from 'crypto'

// Encryption key (retrieved from environment variables)
const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY!  // 32-byte key
const IV_LENGTH = 16  // Initialization vector length for AES-256-CBC

// Encrypt data
function encrypt(text: string): string {
  const iv = crypto.randomBytes(IV_LENGTH)
  const cipher = crypto.createCipheriv(
    'aes-256-cbc',
    Buffer.from(ENCRYPTION_KEY),
    iv
  )

  let encrypted = cipher.update(text, 'utf8', 'hex')
  encrypted += cipher.final('hex')

  return iv.toString('hex') + ':' + encrypted
}

// Decrypt data
function decrypt(text: string): string {
  const parts = text.split(':')
  const iv = Buffer.from(parts[0], 'hex')
  const encryptedText = parts[1]

  const decipher = crypto.createDecipheriv(
    'aes-256-cbc',
    Buffer.from(ENCRYPTION_KEY),
    iv
  )

  let decrypted = decipher.update(encryptedText, 'hex', 'utf8')
  decrypted += decipher.final('utf8')

  return decrypted
}

// Usage example
const encryptedData = encrypt(sensitiveData)
await database.save({ data: encryptedData })
```

#### ✅ Enforcing HTTPS
```typescript
// HTTPS redirection
app.use((req, res, next) => {
  if (req.header('x-forwarded-proto') !== 'https' && process.env.NODE_ENV === 'production') {
    res.redirect(`https://${req.header('host')}${req.url}`)
  } else {
    next()
  }
})

// Strict-Transport-Security header
app.use(helmet.hsts({
  maxAge: 31536000,  // 1 year
  includeSubDomains: true,
  preload: true
}))
```

### ❌ What Not to Do
```typescript
// Storing passwords in plain text
const user = {
  username: 'alice',
  password: 'password123'  // Absolutely forbidden
}

// Weak hashing algorithms
const hash = crypto.createHash('md5').update(password).digest('hex')  // Dangerous
```

## A03: Injection

### Overview
Vulnerabilities where untrusted input is interpreted as part of a command or query.

### Countermeasures
See [Input Validation and Injection Countermeasures](INPUT-VALIDATION.md) for details.

#### Quick Reference
```typescript
// ✅ SQL Injection: Prepared statements
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId])

// ✅ Command Injection: Input validation
const allowedCommands = ['ls', 'pwd', 'whoami']
if (!allowedCommands.includes(command)) {
  throw new Error('Invalid command')
}
```

## A04: Insecure Design

### Overview
Vulnerabilities resulting from lack of security considerations during the design phase.

### Countermeasures

#### ✅ Threat Modeling
```typescript
// Definition of data flow diagrams and Trust Boundaries

// Example: User registration process
/**
 * Threat Model: User Registration
 *
 * Trust Boundaries:
 * 1. Client -> Server (Validation mandatory)
 * 2. Server -> Database (Trusted)
 *
 * Threats (STRIDE):
 * - Spoofing: Countered by email verification
 * - Tampering: Countered by HTTPS
 * - Repudiation: Countered by audit logs
 * - Information Disclosure: Countered by encryption
 * - Denial of Service: Countered by rate limiting
 * - Elevation of Privilege: Default privileges set to minimum
 */
async function registerUser(data: UserRegistrationData) {
  // Input validation (Verification at the Trust Boundary)
  const validated = UserRegistrationSchema.parse(data)

  // Generate email verification token
  const verificationToken = generateSecureToken()

  // Set minimum default privileges (Countermeasure for Elevation of Privilege)
  const user = await userRepository.create({
    ...validated,
    role: 'user',  // Default is least privilege
    emailVerified: false,
    verificationToken
  })

  // Audit log (Countermeasure for Repudiation)
  auditLog.info('User registered', {
    userId: user.id,
    email: user.email
  })

  return user
}
```

#### ✅ Principle of Least Privilege
```typescript
// Privilege separation for database users
const dbConfig = {
  read: {
    user: process.env.DB_READ_USER,
    password: process.env.DB_READ_PASSWORD,
    privileges: ['SELECT']  // Read-only
  },
  write: {
    user: process.env.DB_WRITE_USER,
    password: process.env.DB_WRITE_PASSWORD,
    privileges: ['SELECT', 'INSERT', 'UPDATE']  // Write privileges
  },
  admin: {
    user: process.env.DB_ADMIN_USER,
    password: process.env.DB_ADMIN_PASSWORD,
    privileges: ['ALL']  // Admin privileges (used only for migrations)
  }
}

// Read-only operations
const readOnlyDb = createConnection(dbConfig.read)
const users = await readOnlyDb.query('SELECT * FROM users')

// Write operations
const writeDb = createConnection(dbConfig.write)
await writeDb.query('INSERT INTO users ...', params)
```

## A05: Security Misconfiguration

### Overview
Inappropriate configurations, use of default values, excessively detailed error messages, etc.

### Countermeasures
See [Secure Headers and Other Measures](SECURE-HEADERS.md) for details.

#### Quick Reference
```typescript
// ✅ Secure configuration
app.use(helmet({
  contentSecurityPolicy: true,
  hsts: { maxAge: 31536000 }
}))

// Generic error messages
app.use((err, req, res, next) => {
  console.error(err)  // Details in server logs
  res.status(500).json({
    error: 'Internal Server Error'  // Generic message for clients
  })
})
```

## A06: Vulnerable and Outdated Components

### Overview
Using libraries or frameworks with known vulnerabilities.

### Countermeasures

#### ✅ Dependency Management
```bash
# Regular vulnerability scanning
npm audit

# Automatic fix of vulnerabilities
npm audit fix

# Scanning with Snyk
npx snyk test

# Enable Dependabot (GitHub)
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```

#### ✅ package.json Management
```json
{
  "dependencies": {
    "express": "^4.18.2",  // Fix major version; auto-update minor/patch
    "react": "~18.2.0"     // Fix minor version; auto-update patch only
  },
  "scripts": {
    "audit": "npm audit",
    "update-deps": "npm update && npm audit"
  }
}
```

## A07: Identification and Authentication Failures

### Overview
Vulnerabilities in authentication mechanisms, session management deficiencies, etc.

### Countermeasures
See [Authentication, Authorization, and Secrets Management](AUTH-SECRETS.md) for details.

#### Quick Reference
```typescript
// ✅ Secure authentication
import bcrypt from 'bcrypt'
import jwt from 'jsonwebtoken'

// Password complexity check
const passwordSchema = z.string()
  .min(8)
  .regex(/[A-Z]/, 'Must include uppercase')
  .regex(/[a-z]/, 'Must include lowercase')
  .regex(/[0-9]/, 'Must include digits')
  .regex(/[^A-Za-z0-9]/, 'Must include special characters')

// JWT token generation
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET!,
  { expiresIn: '1h' }
)
```

## A08: Software and Data Integrity Failures

### Overview
Inadequate verification of code and infrastructure integrity.

### Countermeasures

#### ✅ SubResource Integrity (SRI)
```html
<!-- Integrity check for scripts loaded from CDN -->
<script
  src="https://cdn.example.com/library.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/ux..."
  crossorigin="anonymous"
></script>
```

#### ✅ Code Signature Verification
```typescript
// Signature verification for npm packages
// Verify the integrity field in package-lock.json

// Signature verification for Docker images
// Use docker trust sign/verify commands
```

#### ✅ CI/CD Pipeline Security
```yaml
# Example for GitHub Actions
name: Security Scan
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      - name: Run npm audit
        run: npm audit --audit-level=high
```

## A09: Security Logging and Monitoring Failures

### Overview
Lack of logging or monitoring for security events.

### Countermeasures
See [Secure Headers and Other Measures](SECURE-HEADERS.md) for details.

#### Quick Reference
```typescript
// ✅ Secure log management
import winston from 'winston'

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'security.log', level: 'warn' })
  ]
})

// Logging security events
logger.warn('Failed login attempt', {
  userId: userId,
  ip: req.ip,
  timestamp: new Date().toISOString()
  // password: password  // Never log sensitive info
})
```

## A10: Server-Side Request Forgery (SSRF)

### Overview
Inadequate validation when a server accesses external resources.

### Countermeasures

#### ✅ URL Validation
```typescript
// URL whitelist
const ALLOWED_DOMAINS = [
  'api.example.com',
  'trusted-service.com'
]

async function fetchExternalResource(url: string) {
  const parsedUrl = new URL(url)

  // Whitelist check
  if (!ALLOWED_DOMAINS.includes(parsedUrl.hostname)) {
    throw new Error('Unauthorized domain')
  }

  // Prevent access to private IP addresses
  const ipv4Regex = /^(?:10|127|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\./
  if (ipv4Regex.test(parsedUrl.hostname)) {
    throw new Error('Access to private IP addresses is forbidden')
  }

  // Prevent access to localhost
  if (parsedUrl.hostname === 'localhost' || parsedUrl.hostname === '127.0.0.1') {
    throw new Error('Access to localhost is forbidden')
  }

  return fetch(url)
}
```

#### ✅ Redirect Restrictions
```typescript
// Redirect validation
async function fetchWithRedirectValidation(url: string) {
  const response = await fetch(url, {
    redirect: 'manual'  // Disable automatic redirection
  })

  if (response.status >= 300 && response.status < 400) {
    const redirectUrl = response.headers.get('location')

    if (redirectUrl) {
      // Validate the redirect target as well
      await validateUrl(redirectUrl)
      return fetchWithRedirectValidation(redirectUrl)
    }
  }

  return response
}
```

## Pre-completion Checklist

Verify at the completion of all code implementations:

### Mandatory Checks
- [ ] **CodeGuard security check performed**
- [ ] A01: Authorization checks implemented
- [ ] A02: Sensitive data encrypted
- [ ] A03: Injection countermeasures (Input validation, Prepared statements) in place
- [ ] A04: Threat modeling and Principle of Least Privilege applied
- [ ] A05: Secure configurations (Security headers, Error handling) set
- [ ] A06: Dependency vulnerability scanning performed
- [ ] A07: Secure authentication and authorization in place
- [ ] A08: Code integrity verification in place
- [ ] A09: Security logs recorded
- [ ] A10: SSRF countermeasures (URL validation) in place

### Recommended Checks
- [ ] Multi-Factor Authentication (MFA) implemented
- [ ] Rate limiting implemented
- [ ] Security testing automated
- [ ] Incident response plan formulated
- [ ] Periodic penetration testing performed

## 📚 References

- [OWASP Top 10 2021](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

---

[← Back to Secure Coding](../SKILL.md)

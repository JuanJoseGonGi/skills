# Secure Headers and Other Measures

[← Back to Secure Coding](../SKILL.md)

## 📖 Table of Contents

- [Secure HTTP Headers](#secure-http-headers)
- [File Upload Countermeasures](#file-upload-countermeasures)
- [Rate Limiting](#rate-limiting)
- [Secure Log Management](#secure-log-management)
- [Dependency Security Management](#dependency-security-management)
- [Error Handling](#error-handling)
- [CORS Configuration](#cors-configuration)

## Secure HTTP Headers

### ✅ Comprehensive Security Header Configuration with Helmet

```typescript
import helmet from 'helmet'
import express from 'express'

const app = express()

// Basic Helmet configuration
app.use(helmet())

// Custom configuration
app.use(helmet({
  // Content Security Policy
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: [
        "'self'",
        // Allow trusted CDNs only
        'https://cdn.jsdelivr.net',
        'https://unpkg.com'
      ],
      styleSrc: [
        "'self'",
        // Hashes for inline styles (if needed)
        "'sha256-xyz...'"
      ],
      imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'", 'https://api.example.com'],
      fontSrc: ["'self'", 'https://fonts.gstatic.com'],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
      upgradeInsecureRequests: []
    }
  },

  // Strict-Transport-Security (HSTS)
  hsts: {
    maxAge: 31536000,  // 1 year
    includeSubDomains: true,
    preload: true
  },

  // X-Frame-Options
  frameguard: {
    action: 'deny'  // Or 'sameorigin'
  },

  // X-Content-Type-Options
  noSniff: true,

  // X-XSS-Protection (Legacy)
  xssFilter: true,

  // Referrer-Policy
  referrerPolicy: {
    policy: 'strict-origin-when-cross-origin'
  },

  // Permissions-Policy (formerly Feature-Policy)
  permittedCrossDomainPolicies: {
    permittedPolicies: 'none'
  }
}))
```

### ✅ Setting Individual Headers

```typescript
// Content-Security-Policy (Detailed Configuration)
app.use((req, res, next) => {
  const nonce = crypto.randomBytes(16).toString('base64')
  res.locals.nonce = nonce

  res.setHeader(
    'Content-Security-Policy',
    `
      default-src 'self';
      script-src 'self' 'nonce-${nonce}' https://trusted-cdn.com;
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self' https://fonts.gstatic.com;
      connect-src 'self' https://api.example.com;
      frame-ancestors 'none';
      base-uri 'self';
      form-action 'self';
    `.replace(/\s{2,}/g, ' ').trim()
  )

  next()
})

// Strict-Transport-Security
app.use((req, res, next) => {
  res.setHeader(
    'Strict-Transport-Security',
    'max-age=31536000; includeSubDomains; preload'
  )
  next()
})

// X-Frame-Options
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'DENY')
  next()
})

// X-Content-Type-Options
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff')
  next()
})

// Referrer-Policy
app.use((req, res, next) => {
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin')
  next()
})

// Permissions-Policy
app.use((req, res, next) => {
  res.setHeader(
    'Permissions-Policy',
    'geolocation=(), microphone=(), camera=()'
  )
  next()
})
```

### ✅ Security Header Configuration in Next.js

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin'
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains; preload'
          },
          {
            key: 'Content-Security-Policy',
            value: `
              default-src 'self';
              script-src 'self' 'unsafe-eval' 'unsafe-inline';
              style-src 'self' 'unsafe-inline';
              img-src 'self' data: https:;
              font-src 'self';
            `.replace(/\s{2,}/g, ' ').trim()
          }
        ]
      }
    ]
  }
}
```

## File Upload Countermeasures

### ✅ Validation of File Uploads

```typescript
import multer from 'multer'
import path from 'path'
import crypto from 'crypto'

// Allowed file types
const ALLOWED_MIME_TYPES = [
  'image/jpeg',
  'image/png',
  'image/gif',
  'image/webp',
  'application/pdf'
]

// File size limit (5MB)
const MAX_FILE_SIZE = 5 * 1024 * 1024

// File type validation
function validateFileType(file: Express.Multer.File): boolean {
  // MIME type check
  if (!ALLOWED_MIME_TYPES.includes(file.mimetype)) {
    return false
  }

  // Extension check
  const ext = path.extname(file.originalname).toLowerCase()
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.pdf']

  if (!allowedExtensions.includes(ext)) {
    return false
  }

  return true
}

// Filename sanitization
function sanitizeFilename(filename: string): string {
  // Generate a random filename
  const ext = path.extname(filename)
  const randomName = crypto.randomBytes(16).toString('hex')

  return `${randomName}${ext}`
}

// Multer configuration
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // Upload directory (outside of the web server's document root)
    cb(null, '/var/uploads')
  },
  filename: (req, file, cb) => {
    const safeFilename = sanitizeFilename(file.originalname)
    cb(null, safeFilename)
  }
})

const upload = multer({
  storage,
  limits: {
    fileSize: MAX_FILE_SIZE,
    files: 5  // Max number of files
  },
  fileFilter: (req, file, cb) => {
    if (validateFileType(file)) {
      cb(null, true)
    } else {
      cb(new Error('Unauthorized file type'))
    }
  }
})

// File upload endpoint
app.post('/api/upload',
  authenticate,
  upload.single('file'),
  async (req, res) => {
    if (!req.file) {
      throw new BadRequestError('No file uploaded')
    }

    // Save file information
    const fileRecord = await fileRepository.create({
      userId: req.user.id,
      filename: req.file.filename,
      originalName: req.file.originalname,
      mimeType: req.file.mimetype,
      size: req.file.size,
      path: req.file.path
    })

    res.json({
      id: fileRecord.id,
      filename: fileRecord.filename
    })
  }
)
```

### ✅ Verification of File Content

```typescript
import fileType from 'file-type'
import fs from 'fs/promises'

// Verify the actual type of file content
async function validateFileContent(filePath: string, expectedMimeType: string): Promise<boolean> {
  const buffer = await fs.readFile(filePath)
  const type = await fileType.fromBuffer(buffer)

  if (!type) {
    return false
  }

  return type.mime === expectedMimeType
}

// Image metadata check
import sharp from 'sharp'

async function validateImageContent(filePath: string): Promise<boolean> {
  try {
    const metadata = await sharp(filePath).metadata()

    // Limit image dimensions (e.g., up to 10000x10000)
    if (metadata.width > 10000 || metadata.height > 10000) {
      return false
    }

    return true
  } catch {
    return false
  }
}

// File upload processing with content verification
app.post('/api/upload',
  authenticate,
  upload.single('file'),
  async (req, res) => {
    if (!req.file) {
      throw new BadRequestError('No file uploaded')
    }

    // Verification of file content
    const isValidContent = await validateFileContent(
      req.file.path,
      req.file.mimetype
    )

    if (!isValidContent) {
      // Delete malicious file
      await fs.unlink(req.file.path)
      throw new BadRequestError('Invalid file content')
    }

    // Additional verification for images
    if (req.file.mimetype.startsWith('image/')) {
      const isValidImage = await validateImageContent(req.file.path)

      if (!isValidImage) {
        await fs.unlink(req.file.path)
        throw new BadRequestError('Invalid image file')
      }
    }

    // Save file information
    const fileRecord = await fileRepository.create({
      userId: req.user.id,
      filename: req.file.filename,
      originalName: req.file.originalname,
      mimeType: req.file.mimetype,
      size: req.file.size,
      path: req.file.path
    })

    res.json({
      id: fileRecord.id,
      filename: fileRecord.filename
    })
  }
)
```

### ✅ Safe Implementation of File Downloads

```typescript
// File download
app.get('/api/files/:fileId',
  authenticate,
  async (req, res) => {
    const file = await fileRepository.findById(req.params.fileId)

    if (!file) {
      throw new NotFoundError('File not found')
    }

    // Ownership check
    if (file.userId !== req.user.id && req.user.role !== 'admin') {
      throw new ForbiddenError('You do not have permission to access this file')
    }

    // Path traversal countermeasure
    const safePath = path.normalize(file.path).replace(/^(\.\.[\/\\])+/, '')

    // Set Content-Type header
    res.setHeader('Content-Type', file.mimeType)

    // Content-Disposition header (Force download)
    res.setHeader(
      'Content-Disposition',
      `attachment; filename="${encodeURIComponent(file.originalName)}"`
    )

    // X-Content-Type-Options (Prevent MIME sniffing)
    res.setHeader('X-Content-Type-Options', 'nosniff')

    // Send file
    res.sendFile(safePath, { root: '/var/uploads' })
  }
)
```

## Rate Limiting

### ✅ Implementation with express-rate-limit

```typescript
import rateLimit from 'express-rate-limit'
import RedisStore from 'rate-limit-redis'
import { createClient } from 'redis'

// Redis client
const redisClient = createClient({
  url: process.env.REDIS_URL
})
redisClient.connect()

// Global rate limiting
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,  // Max 100 requests
  message: 'Too many requests. Please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:global:'
  })
})

// Stricter limits for login endpoints
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,  // Max 5 attempts
  skipSuccessfulRequests: true,  // Do not count successful requests
  message: 'Too many login attempts. Please try again after 15 minutes.',
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:login:'
  })
})

// Apply to the entire API
app.use('/api/', globalLimiter)

// Apply to specific endpoints
app.post('/api/auth/login', loginLimiter, loginHandler)

// Password reset
const passwordResetLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,  // 1 hour
  max: 3,  // Max 3 requests
  message: 'Too many password reset requests.',
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:reset:'
  })
})

app.post('/api/auth/reset-password',
  passwordResetLimiter,
  resetPasswordHandler
)
```

### ✅ IP-based + User-based Rate Limiting

```typescript
import { Request } from 'express'

// Generate custom key (IP + User ID)
function generateRateLimitKey(req: Request): string {
  const ip = req.ip
  const userId = req.user?.id || 'anonymous'

  return `${ip}:${userId}`
}

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  keyGenerator: generateRateLimitKey,
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:api:'
  })
})

app.use('/api/', apiLimiter)
```

### ✅ Throttling (Token Bucket Strategy)

```typescript
class TokenBucket {
  private tokens: number
  private lastRefill: number

  constructor(
    private capacity: number,
    private refillRate: number  // Tokens per second
  ) {
    this.tokens = capacity
    this.lastRefill = Date.now()
  }

  async consume(count: number = 1): Promise<boolean> {
    this.refill()

    if (this.tokens >= count) {
      this.tokens -= count
      return true
    }

    return false
  }

  private refill() {
    const now = Date.now()
    const elapsed = (now - this.lastRefill) / 1000
    const tokensToAdd = elapsed * this.refillRate

    this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd)
    this.lastRefill = now
  }
}

// Usage example
const buckets = new Map<string, TokenBucket>()

function throttle(capacity: number, refillRate: number) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const key = req.ip

    if (!buckets.has(key)) {
      buckets.set(key, new TokenBucket(capacity, refillRate))
    }

    const bucket = buckets.get(key)!

    if (await bucket.consume()) {
      next()
    } else {
      res.status(429).json({
        error: 'Too many requests'
      })
    }
  }
}

// Up to 10 requests per second
app.use('/api/expensive', throttle(10, 10))
```

## Secure Log Management

### ✅ Structured Logging with Winston

```typescript
import winston from 'winston'

// Log format
const logFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.errors({ stack: true }),
  winston.format.json()
)

// Logger creation
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: logFormat,
  defaultMeta: {
    service: 'myapp',
    environment: process.env.NODE_ENV
  },
  transports: [
    // Error log file
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error',
      maxsize: 10 * 1024 * 1024,  // 10MB
      maxFiles: 5
    }),

    // Combined log file
    new winston.transports.File({
      filename: 'logs/combined.log',
      maxsize: 10 * 1024 * 1024,
      maxFiles: 10
    }),

    // Dedicated log for security events
    new winston.transports.File({
      filename: 'logs/security.log',
      level: 'warn',
      maxsize: 10 * 1024 * 1024,
      maxFiles: 10
    })
  ]
})

// Output to console in non-production environments
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    )
  }))
}

export { logger }
```

### ✅ Logging Security Events

```typescript
// Successful login
logger.info('User login successful', {
  userId: user.id,
  email: user.email,
  ip: req.ip,
  userAgent: req.get('user-agent'),
  timestamp: new Date().toISOString()
})

// Failed login
logger.warn('Failed login attempt', {
  email: email,
  ip: req.ip,
  userAgent: req.get('user-agent'),
  reason: 'invalid_credentials',
  timestamp: new Date().toISOString()
})

// Account locked
logger.warn('Account locked due to multiple failed login attempts', {
  userId: user.id,
  email: user.email,
  ip: req.ip,
  attempts: user.loginAttempts,
  timestamp: new Date().toISOString()
})

// Authorization error
logger.warn('Unauthorized access attempt', {
  userId: req.user?.id,
  resource: req.path,
  method: req.method,
  ip: req.ip,
  timestamp: new Date().toISOString()
})

// Security settings change
logger.info('Security settings changed', {
  userId: req.user.id,
  changes: {
    mfaEnabled: true
  },
  ip: req.ip,
  timestamp: new Date().toISOString()
})
```

### ❌ No Logging of Sensitive Information

```typescript
// ❌ Absolutely forbidden
logger.info('User created', {
  user: {
    email: user.email,
    password: user.password  // Never log!
  }
})

logger.error('Login failed', {
  credentials: {
    username: username,
    password: password  // Never log!
  }
})

// ✅ Correct implementation
logger.info('User created', {
  userId: user.id,
  email: user.email
  // Do not log password
})

logger.warn('Login failed', {
  email: email,
  ip: req.ip
  // Do not log password
})
```

## Dependency Security Management

### ✅ Leveraging `npm audit`

```bash
# Scan for vulnerabilities
npm audit

# Automatically fix vulnerabilities
npm audit fix

# Fix including breaking changes
npm audit fix --force

# Detailed report
npm audit --json > audit-report.json
```

### ✅ Using Snyk

```bash
# Install Snyk
npm install -g snyk

# Authenticate
snyk auth

# Scan for vulnerabilities
snyk test

# Continuous monitoring
snyk monitor

# Automatic fix
snyk fix
```

### ✅ Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "security"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### ✅ Security Settings in `package.json`

```json
{
  "scripts": {
    "audit": "npm audit",
    "audit:fix": "npm audit fix",
    "snyk:test": "snyk test",
    "snyk:monitor": "snyk monitor",
    "security:check": "npm run audit && npm run snyk:test"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
```

## Error Handling

### ✅ Secure Error Handling

```typescript
// Custom error classes
class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public isOperational: boolean = true
  ) {
    super(message)
    Object.setPrototypeOf(this, AppError.prototype)
  }
}

class ValidationError extends AppError {
  constructor(message: string, public errors?: any[]) {
    super(message, 400)
  }
}

class UnauthorizedError extends AppError {
  constructor(message: string = 'Authentication required') {
    super(message, 401)
  }
}

class ForbiddenError extends AppError {
  constructor(message: string = 'Permission denied') {
    super(message, 403)
  }
}

// Error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  // Error log (detailed info)
  logger.error('Error occurred', {
    error: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
    ip: req.ip,
    userId: req.user?.id
  })

  // Generic error messages only for the client
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      error: err.message,
      ...(err instanceof ValidationError && { errors: err.errors })
    })
  } else {
    // Unexpected error
    res.status(500).json({
      error: 'Internal Server Error'
      // Do not include stack trace
    })
  }
})
```

## CORS Configuration

### ✅ Secure CORS Settings

```typescript
import cors from 'cors'

// Allowed origins
const ALLOWED_ORIGINS = [
  'https://example.com',
  'https://www.example.com',
  'https://app.example.com'
]

// Allow localhost in development
if (process.env.NODE_ENV === 'development') {
  ALLOWED_ORIGINS.push('http://localhost:3000')
}

// CORS settings
app.use(cors({
  origin: (origin, callback) => {
    // Allow same-origin (no origin header)
    if (!origin) {
      return callback(null, true)
    }

    // Whitelist check
    if (ALLOWED_ORIGINS.includes(origin)) {
      callback(null, true)
    } else {
      logger.warn('CORS blocked', { origin })
      callback(new Error('CORS policy violation'))
    }
  },
  credentials: true,  // Allow cookies
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  exposedHeaders: ['X-Total-Count'],
  maxAge: 86400  // Preflight request cache (24 hours)
}))

// Allow CORS only for specific endpoints
app.use('/api/public', cors({
  origin: '*',  // Allow all origins
  methods: ['GET']
}))
```

---

[← Authentication, Authorization, and Secrets Management](AUTH-SECRETS.md) | [Back to Secure Coding →](../SKILL.md)

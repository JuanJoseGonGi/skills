# Authentication, Authorization, and Secrets Management

[← Back to Secure Coding](../SKILL.md)

## 📖 Table of Contents

- [Implementation of Authentication](#implementation-of-authentication)
- [Authorization and Access Control](#authorization-and-access-control)
- [Password Management](#password-management)
- [Secrets Management](#secrets-management)
- [Session Management](#session-management)
- [JWT (JSON Web Token)](#jwt-json-web-token)
- [Multi-Factor Authentication (MFA)](#multi-factor-authentication-mfa)
- [OAuth 2.0 / OpenID Connect](#oauth-20--openid-connect)

## Implementation of Authentication

### ✅ Secure Authentication Flow

```typescript
import bcrypt from 'bcrypt'
import { z } from 'zod'

// Login Schema
const LoginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1)
})

// Login Processing
async function login(credentials: unknown) {
  // Input validation
  const { email, password } = LoginSchema.parse(credentials)

  // User search
  const user = await userRepository.findByEmail(email)

  // If user does not exist
  if (!user) {
    // Timing attack countermeasure: consume same amount of time as a success
    await bcrypt.hash('dummy', 10)
    throw new AuthenticationError('Invalid email or password')
  }

  // Account lock check
  if (user.loginAttempts >= 5) {
    const lockoutExpiry = new Date(user.lastLoginAttempt.getTime() + 30 * 60 * 1000)
    if (new Date() < lockoutExpiry) {
      throw new AccountLockedError('Account is locked')
    }
    // Reset login attempts after lockout period
    await userRepository.resetLoginAttempts(user.id)
  }

  // Password verification
  const isValid = await bcrypt.compare(password, user.password)

  if (!isValid) {
    // Increment login attempts
    await userRepository.incrementLoginAttempts(user.id)

    // Security log
    logger.warn('Failed login attempt', {
      userId: user.id,
      email: email,
      ip: req.ip,
      userAgent: req.get('user-agent')
    })

    throw new AuthenticationError('Invalid email or password')
  }

  // Successful login
  await userRepository.resetLoginAttempts(user.id)

  // Security log
  logger.info('Successful login', {
    userId: user.id,
    ip: req.ip
  })

  // Session or token generation
  const token = await generateToken(user)

  return {
    user: {
      id: user.id,
      email: user.email,
      role: user.role
    },
    token
  }
}
```

### ✅ Account Lock Functionality

```typescript
interface User {
  id: string
  email: string
  password: string
  loginAttempts: number
  lastLoginAttempt: Date
  accountLockedUntil?: Date
}

class UserRepository {
  async incrementLoginAttempts(userId: string): Promise<void> {
    const user = await this.findById(userId)

    const attempts = user.loginAttempts + 1
    const lockedUntil = attempts >= 5
      ? new Date(Date.now() + 30 * 60 * 1000)  // 30-minute lock
      : undefined

    await this.update(userId, {
      loginAttempts: attempts,
      lastLoginAttempt: new Date(),
      accountLockedUntil: lockedUntil
    })
  }

  async resetLoginAttempts(userId: string): Promise<void> {
    await this.update(userId, {
      loginAttempts: 0,
      accountLockedUntil: null
    })
  }

  async isAccountLocked(userId: string): Promise<boolean> {
    const user = await this.findById(userId)

    if (!user.accountLockedUntil) {
      return false
    }

    return new Date() < user.accountLockedUntil
  }
}
```

## Authorization and Access Control

### ✅ Role-Based Access Control (RBAC)

```typescript
// Permission definitions
enum Permission {
  // User Management
  READ_USERS = 'read:users',
  CREATE_USERS = 'create:users',
  UPDATE_USERS = 'update:users',
  DELETE_USERS = 'delete:users',

  // Post Management
  READ_POSTS = 'read:posts',
  CREATE_POSTS = 'create:posts',
  UPDATE_OWN_POSTS = 'update:own:posts',
  UPDATE_ANY_POSTS = 'update:any:posts',
  DELETE_OWN_POSTS = 'delete:own:posts',
  DELETE_ANY_POSTS = 'delete:any:posts',

  // System Management
  MANAGE_SETTINGS = 'manage:settings',
  VIEW_AUDIT_LOGS = 'view:audit_logs'
}

// Role definitions
const ROLES = {
  user: [
    Permission.READ_USERS,
    Permission.READ_POSTS,
    Permission.CREATE_POSTS,
    Permission.UPDATE_OWN_POSTS,
    Permission.DELETE_OWN_POSTS
  ],
  moderator: [
    Permission.READ_USERS,
    Permission.READ_POSTS,
    Permission.CREATE_POSTS,
    Permission.UPDATE_ANY_POSTS,
    Permission.DELETE_ANY_POSTS
  ],
  admin: Object.values(Permission)
}

// Permission check function
function hasPermission(user: User, permission: Permission): boolean {
  const userPermissions = ROLES[user.role]
  return userPermissions.includes(permission)
}

// Middleware
function requirePermission(...permissions: Permission[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = req.user

    if (!user) {
      throw new UnauthorizedError('Authentication required')
    }

    const hasRequiredPermission = permissions.some(permission =>
      hasPermission(user, permission)
    )

    if (!hasRequiredPermission) {
      throw new ForbiddenError('Permission denied')
    }

    next()
  }
}

// Usage examples
app.delete('/api/users/:id',
  authenticate,
  requirePermission(Permission.DELETE_USERS),
  deleteUserHandler
)

app.put('/api/posts/:id',
  authenticate,
  requirePermission(
    Permission.UPDATE_OWN_POSTS,
    Permission.UPDATE_ANY_POSTS
  ),
  updatePostHandler
)
```

### ✅ Resource-Based Access Control

```typescript
// Ownership check
async function canUpdatePost(user: User, postId: string): Promise<boolean> {
  // Admins always allowed
  if (user.role === 'admin') {
    return true
  }

  // Get post
  const post = await postRepository.findById(postId)

  // Ownership check
  return post.authorId === user.id
}

// Resource-based middleware
function requireResourceOwnership(
  resourceGetter: (req: Request) => Promise<{ ownerId: string }>
) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user

    if (!user) {
      throw new UnauthorizedError('Authentication required')
    }

    // Admins always allowed
    if (user.role === 'admin') {
      return next()
    }

    const resource = await resourceGetter(req)

    if (resource.ownerId !== user.id) {
      throw new ForbiddenError('Access to this resource is denied')
    }

    next()
  }
}

// Usage example
app.put('/api/posts/:id',
  authenticate,
  requireResourceOwnership(async (req) => {
    const post = await postRepository.findById(req.params.id)
    return { ownerId: post.authorId }
  }),
  updatePostHandler
)
```

## Password Management

### ✅ Secure Password Hashing

```typescript
import bcrypt from 'bcrypt'

// Password hashing
async function hashPassword(plainPassword: string): Promise<string> {
  const saltRounds = 10  // Recommended: 10-12
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
  // Password validation
  validatePassword(data.password)

  // Password hashing
  const hashedPassword = await hashPassword(data.password)

  return userRepository.create({
    ...data,
    password: hashedPassword
  })
}
```

### ✅ Password Complexity Requirements

```typescript
import { z } from 'zod'

// Password Schema
const PasswordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .max(128, 'Password must be within 128 characters')
  .regex(/[A-Z]/, 'Must include at least one uppercase letter')
  .regex(/[a-z]/, 'Must include at least one lowercase letter')
  .regex(/[0-9]/, 'Must include at least one digit')
  .regex(/[^A-Za-z0-9]/, 'Must include at least one symbol')
  .refine(
    (password) => !COMMON_PASSWORDS.includes(password.toLowerCase()),
    { message: 'Commonly used passwords are not allowed' }
  )

// List of commonly used passwords
const COMMON_PASSWORDS = [
  'password',
  '12345678',
  'password123',
  'admin',
  'letmein',
  // ... (In reality, list many more)
]

// Password validation function
function validatePassword(password: string): void {
  PasswordSchema.parse(password)
}
```

### ✅ Password Reset

```typescript
import crypto from 'crypto'

// Reset token generation
function generateResetToken(): string {
  return crypto.randomBytes(32).toString('hex')
}

// Password reset request
async function requestPasswordReset(email: string) {
  const user = await userRepository.findByEmail(email)

  if (!user) {
    // Security: return success response even if user doesn't exist
    logger.warn('Password reset requested for non-existent email', { email })
    return { success: true }
  }

  // Reset token generation
  const resetToken = generateResetToken()
  const resetTokenExpiry = new Date(Date.now() + 1 * 60 * 60 * 1000)  // 1 hour validity

  // Hash and save the token
  const hashedToken = crypto
    .createHash('sha256')
    .update(resetToken)
    .digest('hex')

  await userRepository.update(user.id, {
    resetToken: hashedToken,
    resetTokenExpiry
  })

  // Send email
  await sendPasswordResetEmail(user.email, resetToken)

  return { success: true }
}

// Perform password reset
async function resetPassword(token: string, newPassword: string) {
  // Hash the token
  const hashedToken = crypto
    .createHash('sha256')
    .update(token)
    .digest('hex')

  // User search
  const user = await userRepository.findByResetToken(hashedToken)

  if (!user) {
    throw new InvalidTokenError('Invalid reset token')
  }

  // Token expiry check
  if (new Date() > user.resetTokenExpiry) {
    throw new ExpiredTokenError('Reset token has expired')
  }

  // Password validation
  validatePassword(newPassword)

  // Password update
  const hashedPassword = await hashPassword(newPassword)

  await userRepository.update(user.id, {
    password: hashedPassword,
    resetToken: null,
    resetTokenExpiry: null
  })

  // Security log
  logger.info('Password reset completed', { userId: user.id })

  return { success: true }
}
```

## Secrets Management

### ✅ Management via Environment Variables

```typescript
// ❌ Hardcoding (Absolutely forbidden)
const dbPassword = "secret123"  // Dangerous
const apiKey = "key456"  // Dangerous
const jwtSecret = "mysecret"  // Dangerous

// ✅ Retrieve from environment variables
const dbPassword = process.env.DB_PASSWORD!
const apiKey = process.env.API_KEY!
const jwtSecret = process.env.JWT_SECRET!

// Environment variable validation
function validateEnv() {
  const requiredEnvVars = [
    'DB_PASSWORD',
    'API_KEY',
    'JWT_SECRET',
    'ENCRYPTION_KEY'
  ]

  const missingVars = requiredEnvVars.filter(
    varName => !process.env[varName]
  )

  if (missingVars.length > 0) {
    throw new Error(
      `Missing required environment variables: ${missingVars.join(', ')}`
    )
  }
}

// Validate on application startup
validateEnv()
```

### ✅ .env File Management

```bash
# .env (for development)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_dev
DB_USER=developer
DB_PASSWORD=dev_password_123

JWT_SECRET=dev_jwt_secret_key_change_in_production
API_KEY=dev_api_key_12345

# HTTPS configuration (production only)
HTTPS_ENABLED=false

# Log level
LOG_LEVEL=debug
```

```gitignore
# .gitignore (Required)
.env
.env.local
.env.*.local
*.pem
*.key
*.crt
secrets/
```

```bash
# .env.example (Version controlled)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=your_db_user
DB_PASSWORD=your_db_password

JWT_SECRET=your_jwt_secret_min_32_chars
API_KEY=your_api_key

HTTPS_ENABLED=true

LOG_LEVEL=info
```

### ✅ Use of Secret Management Services

```typescript
// AWS Secrets Manager
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager'

const client = new SecretsManagerClient({ region: 'ap-northeast-1' })

async function getSecret(secretName: string): Promise<string> {
  const command = new GetSecretValueCommand({ SecretId: secretName })
  const response = await client.send(command)

  if (!response.SecretString) {
    throw new Error('Secret not found')
  }

  return response.SecretString
}

// Usage example
const dbCredentials = JSON.parse(await getSecret('prod/database/credentials'))

// HashiCorp Vault
import vault from 'node-vault'

const vaultClient = vault({
  apiVersion: 'v1',
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN
})

async function getVaultSecret(path: string): Promise<any> {
  const result = await vaultClient.read(path)
  return result.data
}
```

## Session Management

### ✅ Secure Session Configuration

```typescript
import session from 'express-session'
import RedisStore from 'connect-redis'
import { createClient } from 'redis'

// Create Redis client
const redisClient = createClient({
  url: process.env.REDIS_URL
})
redisClient.connect()

// Session configuration
app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false,
  name: 'sessionId',  // Change default 'connect.sid'
  cookie: {
    secure: true,  // HTTPS mandatory
    httpOnly: true,  // Inaccessible from JavaScript
    maxAge: 24 * 60 * 60 * 1000,  // 24 hours
    sameSite: 'strict'  // CSRF countermeasure
  }
}))
```

### ✅ Session Fixation Countermeasure

```typescript
// Regenerate session ID on successful login
async function login(req: Request, credentials: LoginCredentials) {
  const user = await authenticate(credentials)

  // Destroy old session
  req.session.destroy((err) => {
    if (err) {
      logger.error('Failed to destroy session', err)
    }
  })

  // Create new session
  req.session.regenerate((err) => {
    if (err) {
      throw new SessionError('Failed to create session')
    }

    // Save user info in session
    req.session.userId = user.id
    req.session.role = user.role

    req.session.save()
  })

  return user
}
```

## JWT (JSON Web Token)

### ✅ JWT Generation and Verification

```typescript
import jwt from 'jsonwebtoken'

interface TokenPayload {
  userId: string
  email: string
  role: string
}

// Token generation
function generateToken(user: User): string {
  const payload: TokenPayload = {
    userId: user.id,
    email: user.email,
    role: user.role
  }

  return jwt.sign(
    payload,
    process.env.JWT_SECRET!,
    {
      expiresIn: '1h',  // Expires in 1 hour
      issuer: 'myapp',
      audience: 'myapp-users'
    }
  )
}

// Refresh token generation
function generateRefreshToken(user: User): string {
  return jwt.sign(
    { userId: user.id },
    process.env.JWT_REFRESH_SECRET!,
    {
      expiresIn: '7d'  // Valid for 7 days
    }
  )
}

// Token verification
function verifyToken(token: string): TokenPayload {
  try {
    return jwt.verify(
      token,
      process.env.JWT_SECRET!,
      {
        issuer: 'myapp',
        audience: 'myapp-users'
      }
    ) as TokenPayload
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      throw new TokenExpiredError('Token has expired')
    }
    if (error instanceof jwt.JsonWebTokenError) {
      throw new InvalidTokenError('Invalid token')
    }
    throw error
  }
}

// Authentication Middleware
function authenticate(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    throw new UnauthorizedError('Authentication token required')
  }

  const token = authHeader.substring(7)

  try {
    const payload = verifyToken(token)
    req.user = payload
    next()
  } catch (error) {
    throw new UnauthorizedError('Invalid authentication token')
  }
}
```

### ✅ Token Refresh

```typescript
// Save refresh token (Redis)
async function saveRefreshToken(userId: string, refreshToken: string) {
  const key = `refresh_token:${userId}`
  await redisClient.set(key, refreshToken, {
    EX: 7 * 24 * 60 * 60  // 7 days
  })
}

// Token Refresh Endpoint
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body

  try {
    // Verify refresh token
    const payload = jwt.verify(
      refreshToken,
      process.env.JWT_REFRESH_SECRET!
    ) as { userId: string }

    // Retrieve saved token from Redis
    const savedToken = await redisClient.get(`refresh_token:${payload.userId}`)

    if (savedToken !== refreshToken) {
      throw new InvalidTokenError('Invalid refresh token')
    }

    // Get user info
    const user = await userRepository.findById(payload.userId)

    // Generate new access token
    const newAccessToken = generateToken(user)

    res.json({ accessToken: newAccessToken })
  } catch (error) {
    throw new UnauthorizedError('Refresh token is invalid')
  }
})
```

## Multi-Factor Authentication (MFA)

### ✅ TOTP (Time-based One-Time Password)

```typescript
import speakeasy from 'speakeasy'
import QRCode from 'qrcode'

// MFA Secret Generation
async function generateMFASecret(user: User) {
  const secret = speakeasy.generateSecret({
    name: `MyApp (${user.email})`,
    issuer: 'MyApp'
  })

  // Generate QR code
  const qrCode = await QRCode.toDataURL(secret.otpauth_url!)

  // Save secret (encryption recommended)
  await userRepository.update(user.id, {
    mfaSecret: secret.base32,
    mfaEnabled: false  // Activate after confirmation
  })

  return {
    secret: secret.base32,
    qrCode
  }
}

// MFA Verification
function verifyMFAToken(secret: string, token: string): boolean {
  return speakeasy.totp.verify({
    secret,
    encoding: 'base32',
    token,
    window: 1  // Allow 30-second skew
  })
}

// Enable MFA
async function enableMFA(userId: string, token: string) {
  const user = await userRepository.findById(userId)

  if (!user.mfaSecret) {
    throw new Error('MFA secret is not set')
  }

  // Verify token
  const isValid = verifyMFAToken(user.mfaSecret, token)

  if (!isValid) {
    throw new InvalidTokenError('Invalid MFA token')
  }

  // Enable MFA
  await userRepository.update(userId, {
    mfaEnabled: true
  })

  return { success: true }
}

// MFA-aware Login
async function loginWithMFA(credentials: LoginCredentials, mfaToken?: string) {
  const user = await authenticate(credentials)

  if (user.mfaEnabled) {
    if (!mfaToken) {
      return {
        requiresMFA: true,
        tempToken: generateTempToken(user.id)
      }
    }

    const isValid = verifyMFAToken(user.mfaSecret, mfaToken)

    if (!isValid) {
      throw new InvalidTokenError('Invalid MFA token')
    }
  }

  const token = generateToken(user)

  return {
    requiresMFA: false,
    token
  }
}
```

## OAuth 2.0 / OpenID Connect

### ✅ OAuth 2.0 Client Implementation

```typescript
import passport from 'passport'
import { Strategy as GoogleStrategy } from 'passport-google-oauth20'

// Google OAuth configuration
passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  callbackURL: '/auth/google/callback'
},
async (accessToken, refreshToken, profile, done) => {
  try {
    // Search existing user
    let user = await userRepository.findByGoogleId(profile.id)

    if (!user) {
      // Create new user
      user = await userRepository.create({
        googleId: profile.id,
        email: profile.emails[0].value,
        name: profile.displayName
      })
    }

    done(null, user)
  } catch (error) {
    done(error)
  }
}))

// OAuth authentication route
app.get('/auth/google',
  passport.authenticate('google', {
    scope: ['profile', 'email']
  })
)

app.get('/auth/google/callback',
  passport.authenticate('google', { session: false }),
  (req, res) => {
    const user = req.user as User
    const token = generateToken(user)
    res.redirect(`/login?token=${token}`)
  }
)
```

---

[← Input Validation and Injection Countermeasures](INPUT-VALIDATION.md) | [Next: Secure Headers and Other Measures →](SECURE-HEADERS.md)

---
name: securing-code
description: Enforces secure coding practices. Required after all code implementations to run CodeGuard security check. Covers input validation, secrets management, and OWASP countermeasures.
---

# Secure Coding

## 📚 Table of Contents

### Basics
- [When to Use](#-when-to-use)
- [CodeGuard Integration](#-codeguard-integration-required)
- [Quick Reference](#-quick-reference)

### Detailed Guides
- [OWASP Top 10 Countermeasures](references/OWASP-TOP10.md) - Detailed explanation and measures for each OWASP Top 10 item.
- [Input Validation and Injection Countermeasures](references/INPUT-VALIDATION.md) - Input validation, sanitization, SQL Injection, XSS, and CSRF countermeasures.
- [Authentication, Authorization, and Secrets Management](references/AUTH-SECRETS.md) - Authentication, authorization, password management, environment variables, and encryption.
- [Secure Headers and Other Measures](references/SECURE-HEADERS.md) - HTTP headers, file uploads, rate limiting, and log management.

## 🎯 When to Use

**Mandatory Situations**:
- **Upon completion of all code implementations (Required)**
- **When processing external input**
- **When implementing authentication or authorization**
- **When handling sensitive information**

**Recommended Situations**:
- When implementing APIs
- During database operations
- During file upload processing
- When implementing session management

## 🔒 CodeGuard Integration (Required)

### Basic Flow
```
1. Completion of code implementation
   ↓
2. Execute CodeGuard (Required)
   Skill: codeguard-security
   ↓
3. Vulnerability detection
   ↓
4. Fix identified issues
   ↓
5. Re-verify with CodeGuard
   ↓
6. Confirm all checks passed
   ↓
7. Completion report
```

### CodeGuard Execution
use the codeguard-security skill

**Important**:
- Do not ignore CodeGuard findings.
- Ensure all issues are fixed before proceeding to the next step.
- Include CodeGuard check results in the completion report.

### CodeGuard Check Items
- SQL Injection
- XSS (Cross-Site Scripting)
- CSRF (Cross-Site Request Forgery)
- Authentication and Authorization issues
- Sensitive information leakage
- Insecure encryption
- Path Traversal
- Command Injection
- etc.

## ⚡ Quick Reference

### Top Priority Measures (Required)

#### 1. Validate All External Input
```typescript
// ✅ Input validation
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  age: z.number().min(0).max(150)
})

const validated = schema.parse(input)
```

#### 2. SQL Injection Countermeasures
```typescript
// ✅ Prepared statements
const user = await db.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]  // Parameter binding
)
```

#### 3. XSS Countermeasures
```typescript
// ✅ Escaping
import DOMPurify from 'dompurify'
const sanitized = DOMPurify.sanitize(userContent)
```

#### 4. Secrets Management
```typescript
// ✅ Environment variables
const apiKey = process.env.API_KEY

// ❌ No hardcoding
const apiKey = "key123"  // Absolutely forbidden
```

#### 5. Authentication and Authorization
```typescript
// ✅ Password hashing
import bcrypt from 'bcrypt'
const hashed = await bcrypt.hash(password, 10)

// ✅ Authorization check
if (currentUser.role !== 'admin') {
  throw new Error('Unauthorized')
}
```

### Checklist Before Completing Implementation

Always verify upon completion of code implementation:
- [ ] **CodeGuard security check performed**
- [ ] All external inputs validated and sanitized
- [ ] SQL Injection countermeasures (prepared statements) in place
- [ ] XSS countermeasures (escaping) in place
- [ ] CSRF countermeasures (token verification) in place
- [ ] Secrets managed via environment variables
- [ ] Passwords hashed
- [ ] Authorization checks implemented
- [ ] Secure headers configured
- [ ] Error messages do not contain sensitive information
- [ ] Logs do not contain sensitive information

## 📖 Navigation to Detailed Guides

### [OWASP Top 10 Countermeasures](references/OWASP-TOP10.md)
Detailed explanation and measures for each OWASP Top 10 vulnerability:
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable and Outdated Components
- A07: Identification and Authentication Failures
- A08: Software and Data Integrity Failures
- A09: Security Logging and Monitoring Failures
- A10: Server-Side Request Forgery

### [Input Validation and Injection Countermeasures](references/INPUT-VALIDATION.md)
Input validation, sanitization, and countermeasures against various injection attacks:
- Implementation of input validation
- Sanitization techniques
- SQL Injection countermeasures
- XSS (Cross-Site Scripting) countermeasures
- CSRF (Cross-Site Request Forgery) countermeasures
- Command Injection countermeasures

### [Authentication, Authorization, and Secrets Management](references/AUTH-SECRETS.md)
Secure management of authentication, authorization, and secrets:
- Secure authentication implementation
- Authorization and access control
- Best practices for password management
- Secrets management via environment variables
- Encryption and hashing
- Secure use of JWT tokens

### [Secure Headers and Other Measures](references/SECURE-HEADERS.md)
HTTP headers, file uploads, and other security measures:
- Configuration of secure HTTP headers
- File upload countermeasures
- Implementation of rate limiting
- Secure log management
- Dependency security management

## 💡 Best Practices

### Security-First Development
1. **Consider security from the design phase**
   - Threat Modeling
   - Principle of Least Privilege
   - Defense in Depth

2. **Implementation Mindset**
   - Assume all input is untrusted
   - Secure default configurations
   - Fail Fast

3. **Continuous Security Improvement**
   - Regular dependency updates
   - Automated security scanning
   - Formulation of incident response plans

### Utilizing Security Tools
- **CodeGuard**: AI-powered security code review (Required)
- **Dependency Scanning**: npm audit, Snyk, Dependabot
- **Static Analysis**: ESLint security plugins, SonarQube
- **Dynamic Analysis**: OWASP ZAP, Burp Suite

## ⚠️ Common Mistakes

### ❌ What Not to Do
- Skipping CodeGuard checks
- Including sensitive information in error messages
- Using `eval()` or `exec()` (unless for a specific reason)
- Relying solely on client-side validation
- Neglecting outdated dependencies
- Ignoring security warnings

### ✅ Correct Approach
- Execute CodeGuard after all code implementation
- Mandate server-side validation
- Regular dependency updates
- Prompt response to security warnings
- Automated security testing

## 📚 References

### Official Guides
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

### Security Tools
- [CodeGuard Documentation](https://github.com/project-codeguard/rules)
- [Snyk](https://snyk.io/)
- [npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit)

---

**Next Steps**: Refer to each detailed guide to implement secure code.

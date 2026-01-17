# Reference: Checklists, Tool Settings, and Type Checkers

This file provides practical reference information for ensuring type safety.

## 📋 Table of Contents

- [Type Safety Checklist](#type-safety-checklist)
- [TypeScript Settings](#typescript-settings)
- [Python Settings](#python-settings)
- [Type Checker Execution Commands](#type-checker-execution-commands)
- [Troubleshooting](#troubleshooting)
- [CI/CD Integration](#cicd-integration)

## ✅ Type Safety Checklist

### Pre-implementation Checklist

Items to verify before writing code:

- [ ] **Plan to avoid use of any/Any types?**
  - TypeScript: `any` -> `unknown` + Type Guard, or explicit type definition.
  - Python: `Any` -> `Union`, `Optional`, `Protocol`, or explicit type hint.

- [ ] **Check type definition files**
  - Verify if existing types can be reused.
  - If a new type definition is needed, plan where to place it.

- [ ] **Type definitions for external libraries**
  - TypeScript: Check for `@types/*` packages.
  - Python: Check for type stubs (`types-*`).

- [ ] **Scope of shared types**
  - Decide if a local type is sufficient or if it should be defined as a shared type.
  - Location for type definition files (`types/`, `models/`, etc.).

### During-implementation Checklist

Items to verify while writing code:

#### TypeScript/JavaScript

- [ ] **strict mode enabled**
  - Is `"strict": true` set in `tsconfig.json`?
  - Is `noImplicitAny: true` enabled?

- [ ] **Explicit type annotations**
  - Do all function arguments and return values have type annotations?
  - Do class properties have type annotations?

- [ ] **No use of 'any' type**
  - Is the `any` type avoided?
  - Is the `Function` type avoided?

- [ ] **Implementation of Type Guards**
  - Are type guards used when dealing with the `unknown` type?
  - Have custom type guard functions (`is` type predicates) been implemented?

- [ ] **Utilization of Optional Chaining**
  - Are `?.` used to handle null/undefined safely?
  - Are `??` (Nullish Coalescing) used to provide default values?

- [ ] **Avoid abuse of non-null assertions (!)**
  - Is `!` truly necessary where used?
  - Can it be replaced with a type guard or optional chaining?

- [ ] **Use of strict equality operators**
  - Are `===` / `!==` used? (`==` / `!=` are forbidden)

#### Python

- [ ] **Thorough Type Hinting**
  - Do all function arguments and return values have type hints?
  - Do class attributes have type hints?

- [ ] **No use of 'Any' type**
  - Is the `Any` type avoided?
  - Can it be replaced with `Union`, `Optional`, or `Protocol`?

- [ ] **Utilization of TypedDict**
  - Is `TypedDict` used for dictionary-based data?

- [ ] **Utilization of dataclass**
  - Are `@dataclass` used for data classes?
  - Are mutable default arguments avoided? (`field(default_factory=list)`)

- [ ] **Utilization of Protocol**
  - Is `Protocol` used when duck typing is needed?

- [ ] **Implementation of Type Guards**
  - Have type guard functions using `TypeGuard` been implemented?

- [ ] **Concretization of exception handling**
  - Is bare `except` avoided?
  - Are concrete exception classes specified?

### Post-implementation Checklist

Items to verify after finishing code:

- [ ] **Running Type Checkers**
  - TypeScript: Any errors with `tsc --noEmit`?
  - Python: Any errors with `mypy` / `pyright`?

- [ ] **Code Review Perspectives**
  - [ ] Are any/Any types avoided?
  - [ ] Do all functions have type annotations?
  - [ ] Are type guards appropriately implemented?
  - [ ] Is error handling appropriate?
  - [ ] Are unit tests type-safe?

- [ ] **Document Updates**
  - Are document comments for type definitions appropriate?
  - Are usage examples type-safe?

## ⚙️ TypeScript Settings

### tsconfig.json (Recommended Settings)

```json
{
  "compilerOptions": {
    // === Type Checking (Mandatory) ===
    "strict": true,                          // Enable all strict flags
    "noImplicitAny": true,                   // Disallow implicit any
    "strictNullChecks": true,                // Strict null/undefined checks
    "strictFunctionTypes": true,             // Strict function type checks
    "strictBindCallApply": true,             // Strict bind/call/apply checks
    "strictPropertyInitialization": true,    // Property initialization checks
    "noImplicitThis": true,                  // Disallow implicit this
    "alwaysStrict": true,                    // Auto-insert 'use strict'

    // === Additional Type Checking (Recommended) ===
    "noUnusedLocals": true,                  // Detect unused local variables
    "noUnusedParameters": true,              // Detect unused parameters
    "noImplicitReturns": true,               // Force returns on all code paths
    "noFallthroughCasesInSwitch": true,      // Detect switch fallthrough
    "noUncheckedIndexedAccess": true,        // Make index access possibly undefined
    "noImplicitOverride": true,              // override keyword required for overrides
    "allowUnusedLabels": false,              // Disallow unused labels
    "allowUnreachableCode": false,           // Disallow unreachable code

    // === Module Resolution ===
    "moduleResolution": "node",              // Node.js style resolution
    "esModuleInterop": true,                 // Interop between CommonJS and ES Modules
    "allowSyntheticDefaultImports": true,    // Flexible default export handling
    "resolveJsonModule": true,               // Allow importing JSON files
    "isolatedModules": true,                 // Treat each file as an independent module

    // === Output Settings ===
    "target": "ES2020",                      // Target ECMAScript version
    "module": "ESNext",                      // Module code generation method
    "lib": ["ES2020", "DOM"],                // Libraries to include
    "outDir": "./dist",                      // Output directory
    "rootDir": "./src",                      // Source root directory
    "sourceMap": true,                       // Generate source maps
    "declaration": true,                     // Generate .d.ts files
    "declarationMap": true,                  // Source maps for .d.ts

    // === Others ===
    "skipLibCheck": true,                    // Skip type checking of declaration files
    "forceConsistentCasingInFileNames": true // Ensure consistent casing in filenames
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### ESLint Configuration (for TypeScript)

```json
{
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2020,
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "plugins": ["@typescript-eslint"],
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking"
  ],
  "rules": {
    // Prohibition of any type
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unsafe-assignment": "error",
    "@typescript-eslint/no-unsafe-member-access": "error",
    "@typescript-eslint/no-unsafe-call": "error",
    "@typescript-eslint/no-unsafe-return": "error",

    // Strengthening Type Safety
    "@typescript-eslint/strict-boolean-expressions": "error",
    "@typescript-eslint/no-unnecessary-condition": "error",
    "@typescript-eslint/prefer-nullish-coalescing": "error",
    "@typescript-eslint/prefer-optional-chain": "error",

    // Naming Conventions
    "@typescript-eslint/naming-convention": [
      "error",
      {
        "selector": "interface",
        "format": ["PascalCase"]
      },
      {
        "selector": "typeAlias",
        "format": ["PascalCase"]
      }
    ],

    // Others
    "@typescript-eslint/explicit-function-return-type": "error",
    "@typescript-eslint/no-non-null-assertion": "warn",
    "@typescript-eslint/consistent-type-imports": "error"
  }
}
```

## 🐍 Python Settings

### mypy.ini (Recommended Settings)

```ini
[mypy]
# === Basic Settings ===
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True

# === Strict Prohibition of Any ===
disallow_any_unimported = True       # Disallow Any from imported types
disallow_any_expr = False             # Set to True for complete strictness
disallow_any_decorated = True         # Disallow Any in decorators
disallow_any_explicit = True          # Disallow explicit Any
disallow_any_generics = True          # Disallow Any in generics
disallow_subclassing_any = True       # Disallow subclassing Any

# === Stricter Type Checking ===
check_untyped_defs = True            # Check functions without type hints
strict_optional = True                # Strict Optional checks
strict_equality = True                # Stricter equality checks
strict_concatenate = True             # Stricter string concatenation

# === Error/Warning Settings ===
warn_redundant_casts = True          # Warn on redundant casts
warn_unused_ignores = True           # Warn on unused # type: ignore
warn_no_return = True                # Warn on functions missing returns
warn_unreachable = True              # Warn on unreachable code
warn_incomplete_stub = True          # Warn on incomplete type stubs

# === Import Settings ===
ignore_missing_imports = False       # Error if type definitions are missing for imports
follow_imports = normal              # Follow imports
namespace_packages = True            # Support namespace packages

# === Others ===
pretty = True                        # Make error messages readable
show_error_codes = True              # Show error codes
show_column_numbers = True           # Show column numbers
show_error_context = True            # Show error context

# === Plugins ===
plugins = pydantic.mypy              # For Pydantic

# === Third-party Libraries ===
# Configure individual libraries missing type definitions
[mypy-pytest.*]
ignore_missing_imports = True

[mypy-requests.*]
ignore_missing_imports = True

[mypy-celery.*]
ignore_missing_imports = True

# === Pydantic Plugin Settings ===
[pydantic-mypy]
init_forbid_extra = True
init_typed = True
warn_required_dynamic_aliases = True
```

### pyrightconfig.json (Recommended Settings)

```json
{
  "include": ["src"],
  "exclude": [
    "**/node_modules",
    "**/__pycache__",
    "**/.*",
    "tests"
  ],

  "typeCheckingMode": "strict",

  "reportMissingImports": true,
  "reportMissingTypeStubs": false,
  "reportImportCycles": true,
  "reportUnusedImport": true,
  "reportUnusedClass": true,
  "reportUnusedFunction": true,
  "reportUnusedVariable": true,
  "reportDuplicateImport": true,
  "reportOptionalSubscript": true,
  "reportOptionalMemberAccess": true,
  "reportOptionalCall": true,
  "reportOptionalIterable": true,
  "reportOptionalContextManager": true,
  "reportOptionalOperand": true,
  "reportTypedDictNotRequiredAccess": true,
  "reportUntypedFunctionDecorator": true,
  "reportUntypedClassDecorator": true,
  "reportUntypedBaseClass": true,
  "reportUntypedNamedTuple": true,
  "reportPrivateUsage": true,
  "reportConstantRedefinition": true,
  "reportIncompatibleMethodOverride": true,
  "reportIncompatibleVariableOverride": true,
  "reportUnnecessaryIsInstance": true,
  "reportUnnecessaryCast": true,
  "reportAssertAlwaysTrue": true,
  "reportSelfClsParameterName": true,
  "reportUnusedCoroutine": true,

  "pythonVersion": "3.11",
  "pythonPlatform": "Linux",

  "executionEnvironments": [
    {
      "root": "src",
      "pythonVersion": "3.11",
      "pythonPlatform": "Linux",
      "extraPaths": ["lib"]
    }
  ],

  "venvPath": ".",
  "venv": ".venv"
}
```

### Ruff Configuration (.ruff.toml)

```toml
# Python version
target-version = "py311"

# Checks to enable
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "ANN",    # flake8-annotations
    "ASYNC",  # flake8-async
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "DTZ",    # flake8-datetimez
    "T10",    # flake8-debugger
    "EXE",    # flake8-executable
    "ISC",    # flake8-implicit-str-concat
    "G",      # flake8-logging-format
    "PIE",    # flake8-pie
    "T20",    # flake8-print
    "PT",     # flake8-pytest-style
    "Q",      # flake8-quotes
    "RSE",    # flake8-raise
    "RET",    # flake8-return
    "SIM",    # flake8-simplify
    "TCH",    # flake8-type-checking
    "ARG",    # flake8-unused-arguments
    "PTH",    # flake8-use-pathlib
    "ERA",    # eradicate (commented-out code)
    "PL",     # pylint
    "TRY",    # tryceratops
    "RUF",    # Ruff-specific rules
]

# Rules to ignore
ignore = [
    "ANN101",  # Missing type annotation for self
    "ANN102",  # Missing type annotation for cls
]

# Max characters per line
line-length = 100

# Excluded directories
exclude = [
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "build",
    "dist",
]

[per-file-ignores]
"tests/**/*.py" = [
    "S101",    # Use of assert
    "ANN201",  # Missing return type annotation
]
```

## 🚀 Type Checker Execution Commands

### TypeScript

```bash
# Basic type check
tsc --noEmit

# watch mode (monitors file changes)
tsc --noEmit --watch

# Check only a specific file
tsc --noEmit src/main.ts

# Detailed output
tsc --noEmit --pretty --listFiles

# Combine with ESLint
eslint --ext .ts,.tsx src/

# Run everything together
npm run type-check  # Defined in package.json
```

**example package.json scripts**:
```json
{
  "scripts": {
    "type-check": "tsc --noEmit",
    "type-check:watch": "tsc --noEmit --watch",
    "lint": "eslint --ext .ts,.tsx src/",
    "lint:fix": "eslint --ext .ts,.tsx src/ --fix",
    "check": "npm run type-check && npm run lint"
  }
}
```

### Python

```bash
# === mypy ===
# Basic type check
mypy src/

# Strict mode
mypy --strict src/

# Check only a specific file
mypy src/main.py

# Generate HTML report
mypy --html-report ./mypy-report src/

# Clear cache
mypy --no-incremental src/

# === pyright ===
# Basic type check
pyright

# Check only a specific file
pyright src/main.py

# Specify configuration file
pyright --project pyrightconfig.json

# === Ruff ===
# Code check
ruff check src/

# Automatic fix
ruff check --fix src/

# Format
ruff format src/

# === Run everything together ===
# Example managing with a Makefile
make type-check
```

**example Makefile**:
```makefile
.PHONY: type-check lint format check

type-check:
	mypy src/
	pyright

lint:
	ruff check src/

format:
	ruff format src/

check: type-check lint
	@echo "All checks passed!"
```

## 🔧 Troubleshooting

### TypeScript

#### Q1. `Cannot find module` error

**Issue**:
```
Cannot find module '@/types/user' or its corresponding type declarations.
```

**Solution**:
```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

#### Q2. `Object is possibly 'null'` error

**Issue**:
```typescript
const element = document.getElementById('app')
element.textContent = 'Hello'  // Error: Object is possibly 'null'.
```

**Solution**:
```typescript
// Method 1: Type Guard
const element = document.getElementById('app')
if (element !== null) {
  element.textContent = 'Hello'
}

// Method 2: Optional Chaining
const element = document.getElementById('app')
if (element) {
  element.textContent = 'Hello'
}

// Method 3: Non-null Assertion (Only when certain)
const element = document.getElementById('app')!
element.textContent = 'Hello'
```

#### Q3. Circular reference error in types

**Issue**:
```
'User' implicitly has type 'any' because it does not have a type annotation and is referenced directly or indirectly in its own initializer.
```

**Solution**:
```typescript
// Bad Example
type User = {
  id: string
  friends: User[]  // Circular reference
}

// Good Example: Use interface
interface User {
  id: string
  friends: User[]  // OK
}

// Or forward reference with type
type User = {
  id: string
  friends: Array<User>  // OK
}
```

### Python

#### Q1. `Cannot find implementation or library stub` error

**Issue**:
```
error: Cannot find implementation or library stub for module named "requests"
```

**Solution**:
```bash
# Install type stubs
pip install types-requests

# Or ignore in mypy.ini
[mypy-requests.*]
ignore_missing_imports = True
```

#### Q2. `Incompatible types in assignment` error

**Issue**:
```python
def get_user() -> User:
    return None  // Error: Incompatible return value type
```

**Solution**:
```python
from typing import Optional

def get_user() -> Optional[User]:
    return None  // OK
```

#### Q3. `Name "X" is not defined` error (Forward Reference)

**Issue**:
```python
class User:
    def get_friend(self) -> User:  // Error: Name "User" is not defined
        pass
```

**Solution**:
```python
from __future__ import annotations  // Python 3.7+

class User:
    def get_friend(self) -> User:  // OK
        pass

# Or use quotes
class User:
    def get_friend(self) -> 'User':  // OK
        pass
```

## 🔄 CI/CD Integration

### GitHub Actions (TypeScript)

```yaml
name: Type Check (TypeScript)

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  type-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: TypeScript type check
        run: npm run type-check

      - name: ESLint
        run: npm run lint
```

### GitHub Actions (Python)

```yaml
name: Type Check (Python)

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  type-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install mypy pyright ruff
          pip install types-requests  # Type stubs

      - name: mypy type check
        run: mypy src/

      - name: pyright type check
        run: pyright

      - name: Ruff lint
        run: ruff check src/
```

### pre-commit Configuration

#### .pre-commit-config.yaml (TypeScript)

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.52.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$
        types: [file]
        args: ['--fix']
        additional_dependencies:
          - '@typescript-eslint/parser'
          - '@typescript-eslint/eslint-plugin'

  - repo: local
    hooks:
      - id: tsc
        name: TypeScript type check
        entry: npx tsc --noEmit
        language: system
        pass_filenames: false
        types: [typescript]
```

#### .pre-commit-config.yaml (Python)

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        args: [--strict]
        additional_dependencies:
          - types-requests

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## 🔗 Related Files

- **[SKILL.md](../SKILL.md)** - Back to Overview
- **[TYPESCRIPT.md](./TYPESCRIPT.md)** - TypeScript Type Safety
- **[PYTHON.md](./PYTHON.md)** - Python Type Safety
- **[ANTI-PATTERNS.md](./ANTI-PATTERNS.md)** - Patterns to Avoid

# Go Error Handling

## Basic Principles

### Errors are Values
In Go, errors are treated as values rather than exceptions:

```go
// Always check for errors
result, err := doSomething()
if err != nil {
    return err
}

// Do not ignore errors (use _ only if explicitly ignoring)
_ = file.Close()  // Intentional ignorance is explicit
```

### Error Propagation
Propagate errors by adding context:

```go
// Good: Adding context
func ProcessUser(id string) error {
    user, err := fetchUser(id)
    if err != nil {
        return fmt.Errorf("fetch user %s: %w", id, err)
    }

    if err := user.Validate(); err != nil {
        return fmt.Errorf("validate user %s: %w", id, err)
    }

    return nil
}

// Bad: No context
func ProcessUser(id string) error {
    user, err := fetchUser(id)
    if err != nil {
        return err  // Unclear where it failed
    }
    return nil
}
```

## Error Wrapping

### %w vs %v
```go
// %w: Wraps the error (inspectable with errors.Is/As)
return fmt.Errorf("open config: %w", err)

// %v: Stringifies the error (original error information is lost)
return fmt.Errorf("open config: %v", err)
```

### Usage
```go
// Using %w: When the caller needs to determine the error type
func ReadConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("read config file: %w", err)
        // Caller can use errors.Is(err, os.ErrNotExist)
    }
    return parseConfig(data)
}

// Using %v: When you want to hide implementation details
func (s *Service) Process(ctx context.Context) error {
    if err := s.internalStep(); err != nil {
        return fmt.Errorf("process failed: %v", err)
        // Do not leak internal implementation details to the outside
    }
    return nil
}
```

## Sentinel Errors

### Definition
```go
package mypackage

import "errors"

// Defined at the package level
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrInvalidInput = errors.New("invalid input")
)
```

### Usage
```go
// Checking for errors
if errors.Is(err, ErrNotFound) {
    // Return 404
}

// Checking with a switch statement
switch {
case errors.Is(err, ErrNotFound):
    return http.StatusNotFound
case errors.Is(err, ErrUnauthorized):
    return http.StatusUnauthorized
default:
    return http.StatusInternalServerError
}
```

## Custom Error Types

### Struct Errors
```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on %s: %s", e.Field, e.Message)
}

// Usage
func Validate(input Input) error {
    if input.Name == "" {
        return &ValidationError{
            Field:   "name",
            Message: "cannot be empty",
        }
    }
    return nil
}

// Type assertion with errors.As
var validErr *ValidationError
if errors.As(err, &validErr) {
    fmt.Printf("Field: %s, Message: %s\n", validErr.Field, validErr.Message)
}
```

### Nested Errors
```go
type QueryError struct {
    Query string
    Err   error
}

func (e *QueryError) Error() string {
    return fmt.Sprintf("query %s: %v", e.Query, e.Err)
}

// Implement Unwrap for error chain support
func (e *QueryError) Unwrap() error {
    return e.Err
}
```

## panic and recover

### Usage of panic
Use panic **only in truly unrecoverable situations**:

```go
// Good: Violation of program preconditions
func MustCompileRegex(pattern string) *regexp.Regexp {
    re, err := regexp.Compile(pattern)
    if err != nil {
        panic(fmt.Sprintf("invalid regex pattern: %s", pattern))
    }
    return re
}

// Use only during initialization
var emailRegex = MustCompileRegex(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)

// Bad: Using panic for normal error handling
func GetUser(id string) *User {
    user, err := db.FindUser(id)
    if err != nil {
        panic(err)  // This is not allowed
    }
    return user
}
```

### Usage of recover
```go
// Recovery in an HTTP handler
func RecoveryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if err := recover(); err != nil {
                log.Printf("panic recovered: %v\n%s", err, debug.Stack())
                http.Error(w, "Internal Server Error", http.StatusInternalServerError)
            }
        }()
        next.ServeHTTP(w, r)
    })
}
```

## Error Handling Patterns

### Early Return
```go
// Good: Guard clauses
func ProcessOrder(order *Order) error {
    if order == nil {
        return errors.New("order is nil")
    }
    if order.Items == nil || len(order.Items) == 0 {
        return errors.New("order has no items")
    }
    if order.CustomerID == "" {
        return errors.New("order has no customer")
    }

    // Main logic
    return processValidOrder(order)
}
```

### Grouping Errors
```go
// Consolidating multiple errors
func ValidateUser(u *User) error {
    var errs []error

    if u.Name == "" {
        errs = append(errs, errors.New("name is required"))
    }
    if u.Email == "" {
        errs = append(errs, errors.New("email is required"))
    }
    if u.Age < 0 {
        errs = append(errs, errors.New("age must be non-negative"))
    }

    if len(errs) > 0 {
        return errors.Join(errs...)  // Go 1.20+
    }
    return nil
}
```

### Error Handling in defer
```go
func WriteToFile(path string, data []byte) (err error) {
    f, err := os.Create(path)
    if err != nil {
        return fmt.Errorf("create file: %w", err)
    }

    // Set error from defer using named return value
    defer func() {
        if cerr := f.Close(); cerr != nil && err == nil {
            err = fmt.Errorf("close file: %w", cerr)
        }
    }()

    if _, err := f.Write(data); err != nil {
        return fmt.Errorf("write data: %w", err)
    }

    return nil
}
```

## Anti-patterns

| Pattern | Problem | Fix |
|---------|------|------|
| `if err != nil { return err }` | No context | `fmt.Errorf("context: %w", err)` |
| `panic(err)` | panic on normal errors | `return err` |
| `err.Error() == "not found"` | String comparison | `errors.Is(err, ErrNotFound)` |
| Ignoring errors | Breeding ground for bugs | Always check or explicitly ignore with `_` |
| return err again after logging | Double logging | Only do one or the other |

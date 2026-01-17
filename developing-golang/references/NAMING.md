# Go Naming Conventions

## Basic Principles

### MixedCaps (CamelCase)
In Go, use `MixedCaps` or `mixedCaps` instead of `snake_case`:

```go
// Good
var userID string
var XMLParser *Parser
func ServeHTTP(w ResponseWriter, r *Request)

// Bad
var user_id string
var xml_parser *Parser
```

### Short and Clear Names
Go prefers short names. The smaller the scope, the shorter the name:

```go
// Good: Loop variable is 1 character
for i, v := range items {
    process(v)
}

// Good: Receiver is 1-2 characters
func (c *Client) Do(req *Request) (*Response, error)

// Good: Short scope within a function
if err := validate(); err != nil {
    return err
}
```

### Rules for Abbreviations
Use common abbreviations consistently:

```go
// Good: Common abbreviations
var buf bytes.Buffer     // buffer
var ctx context.Context  // context
var req *http.Request    // request
var resp *http.Response  // response
var err error            // error

// Acronyms are all uppercase or all lowercase
var userID string   // Not: userId
var xmlParser       // Not: XMLparser (when not exported)
var XMLParser       // When exported
```

## Package Names

### Rules
- **Lowercase only**, no underscores or MixedCaps
- **Short and concise**
- Use **singular form**
- Avoid generic names like **util, common, misc**

```go
// Good
package user
package http
package json

// Bad
package userUtils
package http_client
package common
```

### Relationship with Package Paths
```go
// Package path: github.com/user/project/internal/database
package database  // Not: internal_database

// Exported names should not repeat the package name
database.Client   // Good
database.DatabaseClient  // Bad: Redundant
```

## Variable Names

### Local Variables
```go
// Good: Length according to scope
for i := 0; i < len(items); i++ { }  // Loop variable
if err := f(); err != nil { }        // Error variable
user := getUser(id)                  // Short scope

// Be descriptive in long scopes
userRepository := NewUserRepository(db)
requestTimeout := 30 * time.Second
```

### Parameter Names
```go
// Good: Short if the type makes the meaning clear
func Copy(dst, src []byte) int
func Read(p []byte) (n int, err error)

// Be descriptive if the type alone is unclear
func NewClient(baseURL string, timeout time.Duration) *Client
```

## Function Names

### Naming Patterns
```go
// New + TypeName: Constructor
func NewClient(cfg Config) *Client

// Get/Set: Accessors (though omitting Get is common in Go)
func (u *User) Name() string        // Not: GetName
func (u *User) SetName(name string) // Keep Set

// Is/Has/Can: Returns bool
func (u *User) IsActive() bool
func (f *File) HasPermission(p Permission) bool

// Verb + Noun: Action
func ProcessOrder(order *Order) error
func ValidateInput(input string) error
```

## Interface Names

### -er Suffix
Interfaces with a single method are named `MethodName + er`:

```go
// Good
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Stringer interface {
    String() string
}

type Handler interface {
    Handle(ctx context.Context, req Request) Response
}
```

### Multi-method Interfaces
```go
// Names representing the purpose
type ReadWriter interface {
    Reader
    Writer
}

type Repository interface {
    Find(id string) (*Entity, error)
    Save(entity *Entity) error
    Delete(id string) error
}
```

## Constants and Errors

### Constants
```go
// Unexported constants use camelCase
const maxRetries = 3
const defaultTimeout = 30 * time.Second

// Exported constants use PascalCase
const MaxConnections = 100
const DefaultBufferSize = 4096

// Enumeration using iota
type Status int

const (
    StatusPending Status = iota
    StatusActive
    StatusClosed
)
```

### Error Variables
```go
// Sentinel errors use Err prefix
var ErrNotFound = errors.New("not found")
var ErrInvalidInput = errors.New("invalid input")
var ErrTimeout = errors.New("operation timed out")

// Error types use Error suffix
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Message)
}
```

## Anti-patterns

| Pattern | Problem | Fix |
|---------|------|------|
| `userData` | Redundant suffix | `user` |
| `userList` | Obvious from type | `users` |
| `theUser` | Articles are unnecessary | `user` |
| `GetUser()` | Omit Get | `User()` |
| `DoProcess()` | Do is redundant | `Process()` |
| `IUserService` | I prefix is unnecessary | `UserService` |

## Context Arguments

```go
// context is always the first argument, named ctx
func (c *Client) Fetch(ctx context.Context, url string) (*Response, error)

// Not:
func (c *Client) Fetch(url string, ctx context.Context) (*Response, error)
func (c *Client) Fetch(context context.Context, url string) (*Response, error)
```

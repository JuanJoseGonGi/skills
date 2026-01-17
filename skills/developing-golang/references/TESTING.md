# Go Testing Strategy

## Basics

### File Placement
```
mypackage/
├── handler.go
├── handler_test.go      # Same package
├── service.go
└── service_test.go
```

### Basic Test
```go
// handler_test.go
package mypackage

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}
```

### Running Tests
```bash
# Run all tests
go test ./...

# Specific package
go test ./internal/handler

# Detailed output
go test -v ./...

# Specific test
go test -run TestAdd ./...

# Coverage
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## Table-Driven Tests

### Basic Pattern
```go
func TestCalculate(t *testing.T) {
    tests := []struct {
        name     string
        input    int
        expected int
    }{
        {"zero", 0, 0},
        {"positive", 5, 25},
        {"negative", -3, 9},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Calculate(tt.input)
            if result != tt.expected {
                t.Errorf("Calculate(%d) = %d; want %d", tt.input, result, tt.expected)
            }
        })
    }
}
```

### Including Error Cases
```go
func TestParse(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    int
        wantErr bool
    }{
        {"valid", "42", 42, false},
        {"invalid", "abc", 0, true},
        {"empty", "", 0, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Parse(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("Parse(%q) error = %v, wantErr %v", tt.input, err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("Parse(%q) = %d; want %d", tt.input, got, tt.want)
            }
        })
    }
}
```

### Comparing Structs
```go
import "reflect"

func TestCreateUser(t *testing.T) {
    tests := []struct {
        name  string
        input CreateUserInput
        want  *User
    }{
        {
            name:  "basic",
            input: CreateUserInput{Name: "John", Email: "john@example.com"},
            want:  &User{Name: "John", Email: "john@example.com"},
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := CreateUser(tt.input)
            if !reflect.DeepEqual(got, tt.want) {
                t.Errorf("CreateUser() = %+v; want %+v", got, tt.want)
            }
        })
    }
}
```

## t.Error vs t.Fatal

### t.Error: Continue Testing
```go
func TestMultipleAssertions(t *testing.T) {
    result := Process()

    if result.Status != "ok" {
        t.Errorf("Status = %q; want %q", result.Status, "ok")
    }
    if result.Count != 10 {
        t.Errorf("Count = %d; want %d", result.Count, 10)
    }
    // Both errors will be reported
}
```

### t.Fatal: Terminate Test Immediately
```go
func TestWithSetup(t *testing.T) {
    db, err := setupDatabase()
    if err != nil {
        t.Fatalf("setup failed: %v", err)  // Cannot continue
    }

    // Test using db
    result := db.Query()
    if result == nil {
        t.Error("result should not be nil")
    }
}
```

## Test Helpers

### t.Helper()
```go
func assertEqual(t *testing.T, got, want int) {
    t.Helper()  // Error line points to the caller
    if got != want {
        t.Errorf("got %d; want %d", got, want)
    }
}

func TestWithHelper(t *testing.T) {
    assertEqual(t, Add(2, 3), 5)  // This line will be reported
}
```

### Setup/Cleanup
```go
func setupTestDB(t *testing.T) *Database {
    t.Helper()
    db, err := NewDatabase(":memory:")
    if err != nil {
        t.Fatalf("setup: %v", err)
    }

    t.Cleanup(func() {
        db.Close()
    })

    return db
}

func TestDatabase(t *testing.T) {
    db := setupTestDB(t)  // Automatic cleanup

    // Test
}
```

## Subtests

### Parallel Tests
```go
func TestParallel(t *testing.T) {
    tests := []struct {
        name  string
        input int
    }{
        {"case1", 1},
        {"case2", 2},
        {"case3", 3},
    }

    for _, tt := range tests {
        tt := tt  // Required before Go 1.22
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()  // Execute in parallel
            result := SlowProcess(tt.input)
            if result < 0 {
                t.Errorf("unexpected negative result")
            }
        })
    }
}
```

### Grouping
```go
func TestUser(t *testing.T) {
    t.Run("Create", func(t *testing.T) {
        t.Run("valid input", func(t *testing.T) {
            // ...
        })
        t.Run("invalid input", func(t *testing.T) {
            // ...
        })
    })

    t.Run("Delete", func(t *testing.T) {
        // ...
    })
}
```

## Mocks

### Interface-based
```go
// Production code
type UserRepository interface {
    FindByID(id string) (*User, error)
}

type UserService struct {
    repo UserRepository
}

func (s *UserService) GetUser(id string) (*User, error) {
    return s.repo.FindByID(id)
}

// Test code
type MemoryUserRepository struct {
    users map[string]*User
    err   error
}

func (m *MemoryUserRepository) FindByID(id string) (*User, error) {
    if m.err != nil {
        return nil, m.err
    }
    return m.users[id], nil
}

func TestUserService_GetUser(t *testing.T) {
    mock := &MemoryUserRepository{
        users: map[string]*User{
            "1": {ID: "1", Name: "John"},
        },
    }
    service := &UserService{repo: mock}

    user, err := service.GetUser("1")
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if user.Name != "John" {
        t.Errorf("Name = %q; want %q", user.Name, "John")
    }
}
```

## HTTP Testing

### httptest.Server
```go
import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHTTPClient(t *testing.T) {
    // Create mock server
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte(`{"status":"ok"}`))
    }))
    defer server.Close()

    // Client test
    client := NewClient(server.URL)
    resp, err := client.GetStatus()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if resp.Status != "ok" {
        t.Errorf("Status = %q; want %q", resp.Status, "ok")
    }
}
```

### httptest.ResponseRecorder
```go
func TestHandler(t *testing.T) {
    req := httptest.NewRequest("GET", "/users/1", nil)
    rec := httptest.NewRecorder()

    handler := NewUserHandler()
    handler.ServeHTTP(rec, req)

    if rec.Code != http.StatusOK {
        t.Errorf("Status = %d; want %d", rec.Code, http.StatusOK)
    }
}
```

## Benchmarks

```go
func BenchmarkProcess(b *testing.B) {
    data := prepareData()

    for b.Loop() {
        Process(data)
    }
}

func BenchmarkProcessParallel(b *testing.B) {
    data := prepareData()

    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            Process(data)
        }
    })
}
```

```bash
go test -bench=. ./...
go test -bench=BenchmarkProcess -benchmem ./...
```

## TestMain

```go
func TestMain(m *testing.M) {
    // Setup
    setup()

    // Run tests
    code := m.Run()

    // Cleanup
    cleanup()

    os.Exit(code)
}
```

## Best Practices

| Practice | Description |
|------------|------|
| Table-driven | Structure multiple cases systematically |
| t.Helper() | Use in helper functions |
| t.Parallel() | Parallelize independent tests |
| Interfaces | Enable mocking with dependency injection |
| t.Cleanup() | Automatic resource cleanup |
| Subtests | Structure with t.Run() |

## Anti-patterns

| Pattern | Problem | Fix |
|---------|------|------|
| Dependent on global state | Flaky tests | Dependency injection |
| Direct dependency on external services | Fails in CI/CD | Mocks/Stubs |
| Dependent on execution order | Fails in parallel execution | Independent tests |
| magic number | Unclear intent | Named constants |
| Huge test functions | Difficult to maintain | Split into subtests |

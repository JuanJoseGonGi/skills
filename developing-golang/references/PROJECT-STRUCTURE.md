# Go Project Structure

## Standard Layout

### Simple Project
```
myproject/
├── go.mod
├── go.sum
├── main.go           # Entry point
├── handler.go        # HTTP handlers
├── service.go        # Business logic
├── repository.go     # Data access
└── handler_test.go   # Tests
```

### Medium-sized Project
```
myproject/
├── go.mod
├── go.sum
├── main.go
├── cmd/
│   └── myapp/
│       └── main.go       # Entry point
├── internal/             # Internal project packages
│   ├── handler/
│   │   ├── handler.go
│   │   └── handler_test.go
│   ├── service/
│   │   ├── service.go
│   │   └── service_test.go
│   └── repository/
│       ├── repository.go
│       └── repository_test.go
├── pkg/                  # Public packages (if necessary)
│   └── client/
│       └── client.go
└── Makefile
```

### Large-scale Project
```
myproject/
├── go.mod
├── go.sum
├── cmd/
│   ├── api/
│   │   └── main.go       # API server
│   ├── worker/
│   │   └── main.go       # Background worker
│   └── cli/
│       └── main.go       # CLI tool
├── internal/
│   ├── bounded-context-1/				# Bounded Context 1. The domain goes in the root of the context.
│   │   ├── application/					# Application layer
│   │   │   ├── create/ 					# Scream Architecture
│   │   │   │   ├── creator.go
│   │   │   │   ├── creator_test.go
│   │   │   │   ├── command.go
│   │   │   │   ├── command_test.go
│   │   │   │   ├── handler.go
│   │   │   │   ├── handler_test.go
│   │   │   │   ├── input.go
│   │   │   │   └── input_test.go
│   │   │   └── read/
│   │   │       ├── reader.go
│   │   │       ├── reader_test.go
│   │   │       ├── query.go
│   │   │       └── query_test.go
│   │   │       ├── input.go
│   │   │       └── input_test.go
│   │   ├── infrastructure/
│   │   │   ├── cache/
│   │   │   ├── repositories/
│   │   │   │   ├── repository.go
│   │   │   │   └── repository_test.go
│   │   │   └── external/
│   │   ├── user.go               # Entity
│   │   ├── repository.go					# Interface
│   │   └── service.go
├── pkg/                  # Public libraries
├── api/                  # API definitions
│   ├── openapi.yaml
│   └── proto/
├── migrations/           # DB migrations
├── scripts/              # Build/deploy scripts
├── deployments/          # Deployment configurations
│   ├── docker/
│   └── k8s/
├── docs/
├── Makefile
├── Dockerfile
└── docker-compose.yml
```

## Role of Directories

### cmd/
Entry points for executable files:

```go
// cmd/api/main.go
package main

import (
    "context"
    "log"
    "os/signal"
    "syscall"

    "github.com/username/myproject/internal/app/api"
    "github.com/username/myproject/internal/config"
)

func main() {
    ctx, stop := signal.NotifyContext(context.Background(),
        syscall.SIGINT, syscall.SIGTERM)
    defer stop()

    cfg, err := config.Load()
    if err != nil {
        log.Fatalf("load config: %v", err)
    }

    if err := api.Run(ctx, cfg); err != nil {
        log.Fatalf("run api: %v", err)
    }
}
```

### internal/
Code internal to the project. Cannot be imported from outside:

```go
// internal/handler/user.go
package handler

type UserHandler struct {
    service UserService
}

func NewUserHandler(service UserService) *UserHandler {
    return &UserHandler{service: service}
}
```

### pkg/
Packages exposed to the outside (use with caution):

```go
// pkg/client/client.go
package client

// Client is usable from outside
type Client struct {
    baseURL string
}

func New(baseURL string) *Client {
    return &Client{baseURL: baseURL}
}
```

## go.mod

### Initialization
```bash
go mod init github.com/username/myproject
```

### Basic Structure
```go
module github.com/username/myproject

go 1.22

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/lib/pq v1.10.9
)

require (
    // Indirect dependencies
    golang.org/x/net v0.17.0 // indirect
)
```

### Commands
```bash
# Add dependency
go get github.com/gin-gonic/gin

# Remove unnecessary dependencies
go mod tidy

# Verify dependencies
go mod verify

# Vendoring
go mod vendor
```

## Package Design

### Single Responsibility
```go
// Good: Clear responsibility
package user

type User struct { ... }
type Repository interface { ... }
type Service struct { ... }

// Bad: Multiple responsibilities
package models  // Mix of various entities
```

### Dependency Direction
```
cmd/
 └── depends on → internal/bounded-context-1/app/
                   └── depends on → internal/bounded-context-1/domain/
                   └── depends on → internal/bounded-context-1/infrastructure/
                                      └── depends on → internal/bounded-context-1/domain/ (interfaces)
```

### Placement of Interfaces
```go
// internal/auth/user_repository.go
// Interfaces are defined by the consumer
package auth

type Repository interface {
    FindByID(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
}

// internal/infrastructure/repositories/sql_user_repository.go
// Implementation is in the infrastructure layer
package repositories

type UserRepository struct {
    db *sql.DB
}

func (r *UserRepository) FindByID(ctx context.Context, id string) (*user.User, error) {
    // Implementation
}
```

## Configuration Management

### Environment Variable Based
```go
// internal/bounded-context-1/config/config.go
package config

import (
    "os"
    "strconv"
    "time"
)

type Config struct {
    Server   ServerConfig
    Database DatabaseConfig
}

type ServerConfig struct {
    Port         int
    ReadTimeout  time.Duration
    WriteTimeout time.Duration
}

type DatabaseConfig struct {
    Host     string
    Port     int
    User     string
    Password string
    Name     string
}

func Load() (*Config, error) {
    return &Config{
        Server: ServerConfig{
            Port:         getEnvInt("SERVER_PORT", 8080),
            ReadTimeout:  getEnvDuration("SERVER_READ_TIMEOUT", 30*time.Second),
            WriteTimeout: getEnvDuration("SERVER_WRITE_TIMEOUT", 30*time.Second),
        },
        Database: DatabaseConfig{
            Host:     getEnv("DB_HOST", "localhost"),
            Port:     getEnvInt("DB_PORT", 5432),
            User:     getEnv("DB_USER", "postgres"),
            Password: os.Getenv("DB_PASSWORD"),  // Required
            Name:     getEnv("DB_NAME", "mydb"),
        },
    }, nil
}

func getEnv(key, defaultValue string) string {
    if v := os.Getenv(key); v != "" {
        return v
    }
    return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
    if v := os.Getenv(key); v != "" {
        if i, err := strconv.Atoi(v); err == nil {
            return i
        }
    }
    return defaultValue
}

func getEnvDuration(key string, defaultValue time.Duration) time.Duration {
    if v := os.Getenv(key); v != "" {
        if d, err := time.ParseDuration(v); err == nil {
            return d
        }
    }
    return defaultValue
}
```

## Makefile

```makefile
.PHONY: build test lint run clean

# Variables
BINARY_NAME=myapp
BUILD_DIR=bin

# Build
build:
	go build -o $(BUILD_DIR)/$(BINARY_NAME) ./cmd/api

# Test
test:
	go test -v -race -cover ./...

# Lint
lint:
	golangci-lint run

# Start development server
run:
	go run ./cmd/api

# Clean
clean:
	rm -rf $(BUILD_DIR)

# Dependencies
deps:
	go mod tidy
	go mod verify

# All checks
check: lint test
```

## Best Practices

| Practice | Description |
|------------|------|
| Use internal/ | Protect internal code from external access |
| Small packages | Single responsibility, testability |
| Interface segregation | Defined by the consumer |
| Dependency injection | Testability, loose coupling |
| Env var config | 12-Factor App compliance |

## Anti-patterns

| Pattern | Problem | Fix |
|---------|------|------|
| Huge main.go | Difficult to test | Separate into cmd/ and internal/ |
| Circular imports | Build errors | Separate with interfaces |
| Global variables | Difficult to test | Dependency injection |
| utils/ package | Meaningless collection | Purpose-driven packages |
| pkg/ overuse | API pollution | Prioritize internal/ |

# Go Development Tooling

## Standard Tools

### gofmt
Official formatter. Mandatory for all Go code:

```bash
# Check format
gofmt -d .

# Apply format
gofmt -w .

# Apply with simplification
gofmt -s -w .
```

### goimports
gofmt + import organization:

```bash
# Install
go install golang.org/x/tools/cmd/goimports@latest

# Execute
goimports -w .
```

### go vet
Detects potential issues through static analysis:

```bash
go vet ./...
```

Examples of detection:
- Argument mismatch in Printf functions
- Unreachable code
- Copying values that should not be copied

### go mod
Dependency management:

```bash
# Initialization
go mod init github.com/username/project

# Add dependency
go get github.com/gin-gonic/gin@v1.9.1

# Remove unnecessary dependencies
go mod tidy

# Download dependencies
go mod download

# Vendoring
go mod vendor

# Show dependency graph
go mod graph
```

## golangci-lint

### Installation
```bash
# macOS
brew install golangci-lint

# Go
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Binary
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin
```

### Execution
```bash
# Run all checks
golangci-lint run

# Specific package
golangci-lint run ./internal/...

# Auto-fix
golangci-lint run --fix
```

### Configuration File (.golangci.yml)
```yaml
run:
  timeout: 5m
  tests: true

linters:
  enable:
    - errcheck      # Missing error checks
    - govet         # go vet
    - ineffassign   # Ineffectual assignments
    - staticcheck   # Static analysis
    - unused        # Unused code
    - gosimple      # Simplifiable code
    - gocritic      # Code review-like checks
    - gofmt         # Formatting
    - goimports     # Import organization
    - misspell      # Spelling errors
    - revive        # Successor to golint

linters-settings:
  errcheck:
    check-type-assertions: true
    check-blank: true

  govet:
    enable-all: true

  revive:
    rules:
      - name: exported
        severity: warning
      - name: blank-imports
        severity: warning
      - name: context-as-argument
        severity: warning
      - name: error-return
        severity: warning

issues:
  exclude-rules:
    - path: _test\.go
      linters:
        - errcheck
        - gocritic
```

## delve (Debugger)

### Installation
```bash
go install github.com/go-delve/delve/cmd/dlv@latest
```

### Usage
```bash
# Debug execution
dlv debug ./cmd/api

# Debug tests
dlv test ./internal/handler

# Attach to running process
dlv attach <pid>

# Debug core dump
dlv core ./myapp core.dump
```

### Basic Commands
```
(dlv) break main.main     # Set breakpoint
(dlv) break handler.go:42 # Specify line
(dlv) continue            # Continue execution
(dlv) next                # Step over
(dlv) step                # Step in
(dlv) print variable      # Show variable
(dlv) locals              # List local variables
(dlv) goroutines          # List goroutines
(dlv) stack               # Stack trace
```

## go generate

### Usage Example
```go
//go:generate mockgen -source=repository.go -destination=mock_repository.go -package=user

type Repository interface {
    FindByID(ctx context.Context, id string) (*User, error)
}
```

```bash
# Execute
go generate ./...
```

### Common Generators
- **mockgen**: Mock generation
- **stringer**: Generate String() method
- **sqlc**: Generate Go code from SQL
- **ent**: ORM code generation

## Makefile

```makefile
.PHONY: all build test lint clean

# Variables
BINARY_NAME := myapp
BUILD_DIR := bin
GO_FILES := $(shell find . -name '*.go' -not -path './vendor/*')

# Default target
all: lint test build

# Build
build:
	CGO_ENABLED=0 go build -ldflags="-s -w" -o $(BUILD_DIR)/$(BINARY_NAME) ./cmd/api

# Development build (with debug info)
build-dev:
	go build -o $(BUILD_DIR)/$(BINARY_NAME) ./cmd/api

# Test
test:
	go test -v -race -cover ./...

# Coverage report
coverage:
	go test -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

# Lint
lint:
	golangci-lint run

# Format
fmt:
	gofmt -s -w .
	goimports -w .

# Dependencies
deps:
	go mod tidy
	go mod verify

# Code generation
generate:
	go generate ./...

# Clean
clean:
	rm -rf $(BUILD_DIR)
	rm -f coverage.out coverage.html

# Development server (hot reload)
dev:
	air -c .air.toml

# Docker
docker-build:
	docker build -t $(BINARY_NAME) .

docker-run:
	docker run -p 8080:8080 $(BINARY_NAME)
```

## Air (Hot Reload)

### Installation
```bash
go install github.com/air-verse/air@latest
```

### Configuration (.air.toml)
```toml
root = "."
tmp_dir = "tmp"

[build]
  cmd = "go build -o ./tmp/main ./cmd/api"
  bin = "./tmp/main"
  include_ext = ["go", "tpl", "tmpl", "html"]
  exclude_dir = ["assets", "tmp", "vendor", "testdata"]
  delay = 1000

[log]
  time = false

[color]
  main = "magenta"
  watcher = "cyan"
  build = "yellow"
  runner = "green"

[misc]
  clean_on_exit = true
```

## pre-commit

### Installation
```bash
pip install pre-commit
```

### Configuration (.pre-commit-config.yaml)
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml

  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-imports
      - id: go-vet
      - id: golangci-lint

  - repo: local
    hooks:
      - id: go-mod-tidy
        name: go mod tidy
        entry: go mod tidy
        language: system
        pass_filenames: false
```

```bash
# Enable
pre-commit install

# Manual execution
pre-commit run --all-files
```

## CI/CD (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - name: golangci-lint
        uses: golangci/golangci-lint-action@v4
        with:
          version: latest

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - name: Test
        run: go test -v -race -coverprofile=coverage.out ./...
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: coverage.out

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - name: Build
        run: go build -o bin/myapp ./cmd/api
```

## Tool List

| Tool | Purpose | Command |
|-------|------|---------|
| gofmt | Formatting | `gofmt -w .` |
| goimports | Import organization | `goimports -w .` |
| go vet | Static analysis | `go vet ./...` |
| golangci-lint | Unified linting | `golangci-lint run` |
| delve | Debugging | `dlv debug` |
| air | Hot reload | `air` |
| mockgen | Mock generation | `go generate` |

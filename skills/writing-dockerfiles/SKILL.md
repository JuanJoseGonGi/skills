---
name: writing-dockerfiles
description: Guides Dockerfile creation and optimization. Use when Dockerfile or Docker Compose is detected. Supports multi-stage builds, cache optimization, security hardening, and image size minimization.
---

# Dockerfile Best Practices

## When to Use
- **Always refer to this skill when creating or modifying a Dockerfile**
- New creation of containerized projects
- Optimization of existing Dockerfiles
- Security reviews

---

## 1. Multi-Stage Builds (Required)

### Basic Principle
Separate the build environment from the runtime environment to significantly reduce the final image size (e.g., 916MB → 31.4MB).

### Go Language Example
```dockerfile
# Build stage
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Run stage
FROM gcr.io/distroless/static:nonroot
COPY --from=builder /app/main /main
USER 65532:65532
ENTRYPOINT ["/main"]
```

### Node.js Example
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Run stage
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/index.js"]
```

### Python Example
```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Run stage
FROM python:3.12-slim AS runner
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
USER nobody
CMD ["python", "-m", "app"]
```

---

## 2. Cache Optimization (Required)

### Layer Ordering Principle
**Place items that change infrequently first.**

```dockerfile
# Correct order
COPY package.json package-lock.json ./  # Dependency definitions (infrequent changes)
RUN npm ci                               # Dependency installation
COPY . .                                 # Application code (frequent changes)

# Incorrect: Dependency cache invalidated by any source code change
COPY . .
RUN npm ci
```

### Consolidate RUN Commands
Execute related operations in a single RUN to minimize the number of layers and image size.

```dockerfile
# Recommended
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Not recommended: Leaves unnecessary layers and cache
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y ca-certificates
```

---

## 3. .dockerignore (Required)

Always create a `.dockerignore` file in the project root.

```dockerignore
# Git
.git
.gitignore

# Dependencies (reinstall during build)
node_modules
.venv
__pycache__

# Build artifacts
dist
build
*.egg-info

# Tests and documentation
tests
docs
*.md
!README.md

# IDEs and editors
.vscode
.idea
*.swp

# Environment files (sensitive info)
.env*
!.env.example

# Docker-related
Dockerfile*
docker-compose*
.dockerignore
```

---

## 4. Security Hardening (Required)

### Run as Non-root User
```dockerfile
# Use UID 65532 (nonroot)
USER 65532:65532

# Or a named user
USER nobody

# For Node.js
USER node
```

### Distroless Base Images
Minimal images that do not include a shell or package manager.

```dockerfile
# For static binaries
FROM gcr.io/distroless/static:nonroot

# For dynamic linking
FROM gcr.io/distroless/base:nonroot

# For Python
FROM gcr.io/distroless/python3:nonroot

# For Node.js
FROM gcr.io/distroless/nodejs20:nonroot
```

### ENTRYPOINT vs CMD
```dockerfile
# ENTRYPOINT: Fixed command (cannot be easily overridden)
ENTRYPOINT ["python", "-m", "app"]

# CMD: Default arguments (can be overridden at runtime)
CMD ["--port", "8080"]

# Combination example
ENTRYPOINT ["python", "-m", "app"]
CMD ["--port", "8080"]
# Execution: docker run myapp --port 3000 -> python -m app --port 3000
```

---

## 5. Image Vulnerability Scanning (Recommended)

### Incorporate into CI/CD Pipelines
```yaml
# GitHub Actions example
- name: Scan for vulnerabilities
  uses: docker/scout-action@v1
  with:
    command: cves
    image: ${{ env.IMAGE_NAME }}
    only-severities: critical,high
    exit-code: true  # Fail on vulnerability detection
```

### Local Scanning
```bash
# Docker Scout
docker scout cves myimage:latest

# Trivy
trivy image myimage:latest
```

---

## 6. Static Analysis with Hadolint (Recommended)

### Common Issues Flagged
- Use of `latest` tag -> Version pinning recommended
- Inefficient layer structure
- Lack of cache optimization
- Security concerns

### How to Run
```bash
# Local execution
hadolint Dockerfile

# Via Docker
docker run --rm -i hadolint/hadolint < Dockerfile
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Lint Dockerfile
  uses: hadolint/hadolint-action@v3.1.0
  with:
    dockerfile: Dockerfile
```

---

## 7. Checklist

### Mandatory Requirements at Creation
- [ ] Use multi-stage builds
- [ ] COPY dependency files first
- [ ] Consolidate RUN commands
- [ ] Create .dockerignore
- [ ] Run as a non-root user
- [ ] Appropriate use of ENTRYPOINT and CMD
- [ ] Pin version tags (avoid `:latest`)

### Requirements at Review
- [ ] Unnecessary files not included in the image
- [ ] Sensitive information (API keys, etc.) not included in the image
- [ ] Health check configured
- [ ] Vulnerability scan passed

---

## 8. Reference Resources

- [Official Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Google Distroless Images](https://github.com/GoogleContainerTools/distroless)
- [Hadolint](https://github.com/hadolint/hadolint)
- [Docker Scout](https://docs.docker.com/scout/)

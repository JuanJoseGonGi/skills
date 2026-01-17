# Go Concurrency

## Design Philosophy

> "Do not communicate by sharing memory; instead, share memory by communicating."

## goroutines

### Basics
```go
// Starting a goroutine
go func() {
    // Concurrent processing
}()

// Executing a function as a goroutine
go process(data)
```

### Managing goroutine Termination
```go
// Bad: Potential goroutine leak
func serve() {
    go func() {
        for {
            handleRequest()  // No exit condition
        }
    }()
}

// Good: Cancellable with context
func serve(ctx context.Context) {
    go func() {
        for {
            select {
            case <-ctx.Done():
                return  // Terminate
            default:
                handleRequest()
            }
        }
    }()
}
```

## Channels

### Basic Operations
```go
// Creation
ch := make(chan int)        // Unbuffered
ch := make(chan int, 10)    // Buffered

// Sending
ch <- 42

// Receiving
value := <-ch

// Closing
close(ch)
```

### Channel Direction
```go
// Send-only
func producer(out chan<- int) {
    out <- 42
}

// Receive-only
func consumer(in <-chan int) {
    value := <-in
}

// Bidirectional (restricted to a direction within the function)
func worker(jobs <-chan Job, results chan<- Result) {
    for job := range jobs {
        results <- process(job)
    }
}
```

### Pattern: Worker Pool
```go
func workerPool(ctx context.Context, jobs <-chan Job, numWorkers int) <-chan Result {
    results := make(chan Result)

    var wg sync.WaitGroup
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for {
                select {
                case <-ctx.Done():
                    return
                case job, ok := <-jobs:
                    if !ok {
                        return
                    }
                    results <- process(job)
                }
            }
        }()
    }

    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}
```

### Pattern: Fan-out/Fan-in
```go
// Fan-out: Multiple workers reading from one channel
func fanOut(in <-chan int, n int) []<-chan int {
    outs := make([]<-chan int, n)
    for i := 0; i < n; i++ {
        outs[i] = worker(in)
    }
    return outs
}

// Fan-in: Combining multiple channels into one
func fanIn(channels ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for v := range c {
                out <- v
            }
        }(ch)
    }

    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}
```

## select Statement

### Basics
```go
select {
case msg := <-ch1:
    fmt.Println("received from ch1:", msg)
case msg := <-ch2:
    fmt.Println("received from ch2:", msg)
case ch3 <- value:
    fmt.Println("sent to ch3")
default:
    fmt.Println("no channel ready")
}
```

### Timeout
```go
select {
case result := <-resultCh:
    return result, nil
case <-time.After(5 * time.Second):
    return nil, errors.New("timeout")
}
```

### Combining with context
```go
func doWork(ctx context.Context) error {
    resultCh := make(chan Result)

    go func() {
        resultCh <- heavyComputation()
    }()

    select {
    case result := <-resultCh:
        return processResult(result)
    case <-ctx.Done():
        return ctx.Err()
    }
}
```

## Synchronization Primitives

### sync.Mutex
```go
type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Inc() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}
```

### sync.RWMutex
```go
type Cache struct {
    mu   sync.RWMutex
    data map[string]string
}

func (c *Cache) Get(key string) (string, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    v, ok := c.data[key]
    return v, ok
}

func (c *Cache) Set(key, value string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.data[key] = value
}
```

### sync.WaitGroup
```go
func processAll(items []Item) {
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)
        go func(item Item) {
            defer wg.Done()
            process(item)
        }(item)
    }

    wg.Wait()  // Wait until all goroutines are finished
}
```

### sync.Once
```go
var (
    instance *Singleton
    once     sync.Once
)

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{}
        instance.init()
    })
    return instance
}
```

### sync.Pool
```go
var bufferPool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 1024)
    },
}

func process() {
    buf := bufferPool.Get().([]byte)
    defer bufferPool.Put(buf)

    // Use buf
}
```

## context

### Basic Usage
```go
// Background: Root context
ctx := context.Background()

// TODO: Uncertain context (to be replaced later)
ctx := context.TODO()

// Cancellable
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

// With timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

// With deadline
ctx, cancel := context.WithDeadline(context.Background(), time.Now().Add(time.Hour))
defer cancel()
```

### Value Propagation
```go
type contextKey string

const userIDKey contextKey = "userID"

// Setting a value
ctx := context.WithValue(ctx, userIDKey, "user-123")

// Getting a value
if userID, ok := ctx.Value(userIDKey).(string); ok {
    fmt.Println("User ID:", userID)
}
```

### Usage in HTTP Handlers
```go
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    result, err := doWork(ctx)
    if err != nil {
        if errors.Is(err, context.Canceled) {
            // Client cancelled
            return
        }
        if errors.Is(err, context.DeadlineExceeded) {
            http.Error(w, "Timeout", http.StatusGatewayTimeout)
            return
        }
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    json.NewEncoder(w).Encode(result)
}
```

## Best Practices

### Prevent goroutine Leaks
```go
// Good: Cancellable with context
func stream(ctx context.Context) <-chan Data {
    ch := make(chan Data)
    go func() {
        defer close(ch)
        for {
            select {
            case <-ctx.Done():
                return
            case ch <- fetchData():
            }
        }
    }()
    return ch
}
```

### Channel Owner Closes the Channel
```go
// Sender closes the channel
func producer() <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)  // Sender closes
        for i := 0; i < 10; i++ {
            ch <- i
        }
    }()
    return ch
}
```

### Consider Buffer Size
```go
// Unbuffered: Synchronous communication
ch := make(chan int)

// Buffered: Asynchronous (sender does not block)
ch := make(chan int, 100)

// Buffer size should be set to an expected maximum or for limiting
```

## Anti-patterns

| Pattern | Problem | Fix |
|---------|------|------|
| Directly referencing loop variables in goroutines | Race condition | Pass as an argument |
| goroutines without context | Leaks | Use context.WithCancel |
| Sending/Receiving on nil channels | Permanent block | Always initialize |
| Sending to a closed channel | panic | Only the sender should close |
| Asynchronous access to shared variables | Data race | Use Mutex/Channels |

### Loop Variable Pitfall
```go
// Bad: All goroutines reference the same i
for i := 0; i < 10; i++ {
    go func() {
        fmt.Println(i)  // Unexpected values
    }()
}

// Good: Pass as an argument
for i := 0; i < 10; i++ {
    go func(n int) {
        fmt.Println(n)  // Correct values
    }(i)
}

// Fixed in Go 1.22+ due to changes in loop variable semantics
```

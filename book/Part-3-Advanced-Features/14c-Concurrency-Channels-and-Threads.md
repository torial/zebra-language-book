# 14c: Concurrency — Channels and Threads

**Audience:** All — required for servers, parallel computation, or any I/O at scale
**Time:** 120 minutes
**Prerequisites:** 04-Functions-and-Scope, 14b-Memory-Management-and-Lifetimes
**You'll learn:** `Chan(T)` channels, `sys.go()` for spawning threads, `Atomic(T)` for shared counters and flags, `ThreadPool(n)` for bounded worker pools, and which primitive to reach for in each situation

---

## The Big Picture

Concurrency in Zebra has two pillars:

- **Threads** — independent stacks running in parallel, sharing the same arena allocator
- **Channels** — typed, buffered queues that move values safely between threads

This is the [CSP model] popularised by Go: prefer **communicating** over
**sharing**. Most patterns reduce to "spawn a worker, give it a channel,
read from the channel." The compiler doesn't have a borrow checker, so
correctness comes from this discipline plus a small set of `Atomic`
primitives for the few cases where channels are overkill.

This chapter walks the four primitives — `Chan(T)`, `sys.go()`,
`Atomic(T)`, `ThreadPool(n)` — and the patterns that combine them.

---

## Channels: `Chan(T)`

`Chan(T)` is a thread-safe **buffered channel** carrying values of type
`T`. Construct it with a capacity:

```zebra
var ch: Chan(int) = Chan(int)(4)   # buffer up to 4 values
```

Three operations:

| Method | Returns | Behaviour |
|---|---|---|
| `ch.send(val)` | `void` | Sends a value; **blocks when full** |
| `ch.recv()` | `T?` | Receives a value; **blocks when empty**; returns `nil` when closed + empty |
| `ch.close()` | `void` | Signals "no more values"; outstanding `recv()` calls drain remaining, then receive `nil` |

```zebra
def main()
    var ch: Chan(int) = Chan(int)(4)
    ch.send(1)
    ch.send(2)
    ch.close()

    var v1: int? = ch.recv()       # 1
    var v2: int? = ch.recv()       # 2
    var v3: int? = ch.recv()       # nil — channel closed + empty

    if v1 as n: print n            # 1
    if v3 == nil: print("done")
```

### The `<-` operator

The `<-` operator is syntactic sugar for `send` / `recv`:

```zebra
ch <- 42                # equivalent to ch.send(42)

var v: int? = nil
v <- ch                 # equivalent to v = ch.recv()
```

`<-` reads naturally — left arrow into the channel for send, left arrow
into the variable for receive. Many Zebra programs use the sugar
exclusively.

> **Note on the other `<-`.** Chapter 14b covers `<-` as the
> **copy-out** operator inside `allocate` blocks. Both spellings are the
> same token; the compiler picks the meaning from the operand types.
> When the right-hand side is a `Chan(T)`, it's channel receive;
> otherwise it's a copy-out.

---

## Spawning Threads: `sys.go()`

`sys.go(lambda)` spawns a **fire-and-forget background thread** that
runs the lambda body:

```zebra
sys.go(lambda
    print("hello from a thread")
)
```

The lambda is zero-parameter and can capture variables from the
enclosing scope. Captured values are copied into the thread closure at
spawn time, so the spawning function can return immediately without
leaving dangling references.

```zebra
def main()
    var ch: Chan(int) = Chan(int)(4)

    sys.go(lambda
        ch.send(1)
        ch.send(2)
        ch.close()
    )

    # Main thread reads:
    var sum = 0
    var done = false
    while not done
        var v: int? = ch.recv()
        if v as n
            sum = sum + n
        else
            done = true
    print(sum)  # 3
```

### What `sys.go()` does NOT give you

- **No join.** Threads are detached. There's no `thread.wait()` or
  return-value collection — use a channel to signal completion or to
  return a result.
- **No backpressure.** Every `sys.go()` call spawns a new OS thread.
  If you need bounded concurrency, use `ThreadPool(n)` (below).
- **No panic recovery.** If the lambda raises, the thread terminates.
  Design tasks to validate inputs before running heavy work.

---

## Producer / Consumer Pattern

The canonical pattern: one or more producers `send` to a channel; one or
more consumers `recv` until the channel is closed + empty.

```zebra
# file: 14c_pipeline.zbr
# teaches: producer/consumer with Chan
# chapter: 14c-Concurrency-Channels-and-Threads

def main()
    var ch: Chan(int) = Chan(int)(4)

    # Producer: send 1..5, then close
    sys.go(lambda
        for i in 1..5
            ch.send(i)
        ch.close()
    )

    # Consumer: read until closed + empty
    var sum: int = 0
    var done: bool = false
    while not done
        var v: int? = ch.recv()
        if v as n
            sum = sum + n
        else
            done = true

    print(sum)  # 1+2+3+4 = 10
```

This is the workhorse of concurrent Zebra. Two takeaways:

1. **The producer is responsible for closing.** Without `ch.close()`,
   the consumer's `recv()` would block forever after the last value —
   it has no way to know the producer is finished.
2. **The consumer reads `T?`, not `T`.** `recv()` returns `nil` when the
   channel is closed and empty. The `if v as n` pattern is the
   idiomatic way to handle both cases.

---

## `Atomic(T)` — Lock-Free Counters and Flags

Some shared state doesn't need a channel — a counter incremented by many
threads, a "done" flag, a one-shot signal. For those, use `Atomic(T)`:

```zebra
var counter: Atomic(int) = Atomic(int)(0)
counter.add(1)
var n: int = counter.load()
```

| Method | Returns | Notes |
|---|---|---|
| `Atomic(T)(init)` | `Atomic(T)` | Create with initial value |
| `a.load()` | `T` | Atomic read |
| `a.store(v)` | `void` | Atomic write |
| `a.add(n)` / `a.sub(n)` | `T` | Fetch-and-add — returns the **old** value |
| `a.swap(v)` | `T` | Atomic exchange — returns the old value |

Supported `T`: `int` and `bool`.

All operations use **sequentially-consistent** memory ordering — the
safest and least-surprising default. For cases where relaxed ordering
would be sound and faster, drop into `zig"..."` and call
`@atomicRmw` directly.

### Shared counter

```zebra
def main()
    var total: Atomic(int) = Atomic(int)(0)

    sys.go(lambda  var _ = total.add(1)  )
    sys.go(lambda  var _ = total.add(1)  )
    sys.sleep(50)              # give threads time to finish

    print(total.load())  # 2
```

### One-shot done flag

```zebra
def main()
    var done: Atomic(bool) = Atomic(bool)(false)

    sys.go(lambda
        do_work()
        done.store(true)
    )

    while not done.load()
        sys.sleep(10)

    print("worker finished")
```

---

## `Atomic` vs. `Chan` — Which to Reach For

| | `Atomic(T)` | `Chan(T)` |
|---|---|---|
| Best for | Shared counters, flags, one-shot signals | Producer/consumer pipelines |
| Blocking | Never | `send` blocks when full; `recv` blocks when empty |
| Carries | A single value | A stream of values |
| Ordering | Atomic, but no message order | Message order preserved |

Rule of thumb: **if multiple threads write the value, reach for
`Atomic`**; **if one thread produces and another consumes, reach for
`Chan`**.

---

## `ThreadPool(n)` — Bounded Workers

`sys.go()` spawns an unbounded thread per call — fine for a handful, bad
for thousands. `ThreadPool(n)` runs a fixed `n` workers and queues
submitted tasks among them:

```zebra
def main()
    var pool: ThreadPool = ThreadPool(4)        # 4 worker threads
    var counter: Atomic(int) = Atomic(int)(0)

    var i: int = 0
    while i < 8
        pool.submit(def()
            capture
                var counter: Atomic(int) = counter
            var _: int = counter.add(1)
        )
        i = i + 1

    pool.wait()                  # blocks until all submitted tasks finish
    print(counter.load())  # 8
```

| Method | Notes |
|---|---|
| `ThreadPool(n)` | Constructs a pool with `n` workers |
| `pool.submit(lambda)` | Queue a zero-arg lambda for async execution |
| `pool.wait()` | Block until all queued tasks finish |

### Key behaviours

- **Reusable.** `submit` after `wait` queues more work. A subsequent
  `wait` blocks on the new tasks.
- **Workers run for the pool's lifetime** — they're spawned at
  construction.
- **Task panics terminate the worker, not the program** — and they are
  not recovered. Validate inputs before submitting.

### `ThreadPool` vs. `sys.go()`

| | `ThreadPool(n)` | `sys.go(lambda)` |
|---|---|---|
| Worker count | Fixed `n` | One new thread per call |
| Backpressure | Natural — `submit` waits if all workers are busy | None |
| Result collection | Via `Atomic` or `Chan` | Via `Chan` |
| Best for | CPU-bound parallel work | Fire-and-forget I/O |

For a 1000-item batch, `ThreadPool(8)` is almost always the right
choice. For two or three I/O tasks running alongside the main thread,
`sys.go()` is simpler.

### ThreadPool + Chan: collecting results

The standard pattern for parallel computation with a return value:

```zebra
def main()
    var ch: Chan(int) = Chan(int)(8)
    var pool: ThreadPool = ThreadPool(4)

    for i in 0..8
        pool.submit(def()
            capture
                var idx: int = i
                var ch: Chan(int) = ch
            ch.send(idx * idx)
        )

    pool.wait()                  # all tasks done; close the channel
    ch.close()

    var sum: int = 0
    var done: bool = false
    while not done
        var v: int? = ch.recv()
        if v as n
            sum = sum + n
        else
            done = true

    print(sum)  # 0+1+4+9+16+25+36+49 = 140
```

Three things to notice:

1. **The `capture` block names everything the closure uses** —
   captured-by-value semantics mean each task sees its own `idx`, not
   the shared loop variable.
2. **`pool.wait()` runs before `ch.close()`** — closing too early
   would race with sends still in flight.
3. **The consumer is the main thread** — no extra worker needed.

---

## Memory and Allocator Interactions

Two important caveats:

> **`Chan(T)` uses the page allocator, not the arena.** This is
> intentional — channels need to outlive any single `allocate` scope.
> But it means: **do not construct a channel inside a short-lived
> `allocate` block** if it's going to be used after the block exits.
> The channel itself survives, but its internal buffer storage may not.

> **`ThreadPool` also uses the page allocator.** Same rule: don't
> construct one inside a short-lived `allocate` scope.

For practical purposes: declare your channels and pools at function
scope (or higher) and pass them by reference. Don't nest them inside
`allocate Arena()` blocks unless you understand the lifetime implications.

---

## Real World: Parallel File Processor

A common shape: walk a directory, process each file in parallel with a
bounded pool, collect results via a channel.

```zebra
# file: 14c_parallel_files.zbr
# teaches: ThreadPool + Chan for parallel I/O
# chapter: 14c-Concurrency-Channels-and-Threads

class FileResult
    public var path: str = ""
    public var line_count: int = 0

def process_file(path: str): FileResult
    var src = File.read(path)
    var lines = src.split("\n")
    var r = FileResult()
    r.path = path
    r.line_count = lines.count()
    return r

def main()
    var paths = File.list_dir("./docs")
    var ch: Chan(FileResult) = Chan(FileResult)(paths.count())
    var pool: ThreadPool = ThreadPool(4)

    for p in paths
        pool.submit(def()
            capture
                var p: str = p
                var ch: Chan(FileResult) = ch
            ch.send(process_file(p))
        )

    pool.wait()
    ch.close()

    var results: List(FileResult) = List()
    var done = false
    while not done
        var r: FileResult? = ch.recv()
        if r as got
            results.add(got)
        else
            done = true

    for r in results
        print("${r.path}: ${r.line_count} lines")
```

This same shape — pool + channel + capture closure — covers parallel
HTTP requests, parallel database queries, parallel image processing, and
most other batch I/O patterns.

---

## Common Mistakes

> ❌ **Mistake:** Forgetting to close the channel
>
> ```zebra
> sys.go(lambda
>     for i in 1..5
>         ch.send(i)
>     # ch.close() omitted — consumer will block forever after the 4th value
> )
> ```
>
> ✅ **Better:**
> ```zebra
> sys.go(lambda
>     for i in 1..5
>         ch.send(i)
>     ch.close()
> )
> ```

> ❌ **Mistake:** Sending to a closed channel
>
> ```zebra
> ch.close()
> ch.send(1)              # PANIC at runtime
> ```
>
> ✅ **Better:** the producer is the only one who should close, and only after the last send.

> ❌ **Mistake:** Closing the channel before the producers finish
>
> ```zebra
> for i in 0..8
>     pool.submit(def()
>         capture; var ch = ch
>         ch.send(work())
>     )
> ch.close()              # WRONG: tasks are still running
> pool.wait()
> ```
>
> ✅ **Better:** wait first, then close:
> ```zebra
> for i in 0..8: pool.submit(...)
> pool.wait()             # all sends are complete
> ch.close()
> ```

> ❌ **Mistake:** Sharing a non-atomic counter across threads
>
> ```zebra
> var counter: int = 0
> sys.go(lambda  counter = counter + 1  )     # data race
> sys.go(lambda  counter = counter + 1  )
> ```
>
> ✅ **Better:** use `Atomic(int)`:
> ```zebra
> var counter: Atomic(int) = Atomic(int)(0)
> sys.go(lambda  var _ = counter.add(1)  )
> sys.go(lambda  var _ = counter.add(1)  )
> ```

> ❌ **Mistake:** Capturing the loop variable by reference
>
> ```zebra
> for i in 0..8
>     pool.submit(def()
>         # capture missing — task sees the LATEST value of i, not its own
>         print(i)
>     )
> ```
>
> ✅ **Better:** use a `capture` block to snapshot the value:
> ```zebra
> for i in 0..8
>     pool.submit(def()
>         capture
>             var idx: int = i
>         print(idx)
>     )
> ```

---

## Exercises

### Exercise 1: A Simple Pipeline

Write a program that uses one producer thread to send the integers 1
through 10 down a channel, and the main thread to print their sum.

<details>
<summary>Solution</summary>

```zebra
def main()
    var ch: Chan(int) = Chan(int)(4)

    sys.go(lambda
        for i in 1..11
            ch.send(i)
        ch.close()
    )

    var sum: int = 0
    var done: bool = false
    while not done
        var v: int? = ch.recv()
        if v as n
            sum = sum + n
        else
            done = true

    print(sum)  # 55
```

</details>

### Exercise 2: Parallel Squaring

Use `ThreadPool(4)` to compute the squares of 0..16 in parallel.
Collect the results in any order via a channel and print the sum.

<details>
<summary>Solution</summary>

```zebra
def main()
    var ch: Chan(int) = Chan(int)(16)
    var pool: ThreadPool = ThreadPool(4)

    for i in 0..16
        pool.submit(def()
            capture
                var idx: int = i
                var ch: Chan(int) = ch
            ch.send(idx * idx)
        )

    pool.wait()
    ch.close()

    var sum: int = 0
    var done: bool = false
    while not done
        var v: int? = ch.recv()
        if v as n: sum = sum + n
        else:      done = true

    print(sum)  # 0^2 + 1^2 + ... + 15^2 = 1240
```

</details>

### Exercise 3: Wait Without Joining

Threads don't expose a `join()` call. Use an `Atomic(bool)` flag to
have the main thread wait until a background thread signals completion.

<details>
<summary>Solution</summary>

```zebra
def main()
    var done: Atomic(bool) = Atomic(bool)(false)

    sys.go(lambda
        # ... do work ...
        sys.sleep(100)
        done.store(true)
    )

    while not done.load()
        sys.sleep(10)

    print("background work finished")
```

For a single signal, this is fine. For more than one — multiple
workers, or a sequence — use a `Chan` instead and `recv()` on it: a
channel `recv` blocks naturally without polling.

</details>

---

## Next Steps

- → **14b-Memory-Management-and-Lifetimes** — the memory model that underpins all of this
- → **22c-Testing-and-Validation** — concurrent code needs tests; the runner handles them like any other
- → **20-File-IO-and-System-Access** — combine with `sys.go` for non-blocking I/O patterns

---

## Key Takeaways

- **`Chan(T)`** is a thread-safe buffered channel: `send` blocks when full, `recv` blocks when empty, `close` signals end-of-stream
- **`<-` sugar** — `ch <- v` sends; `v <- ch` receives; reads naturally for pipelines
- **`sys.go(lambda)`** spawns a fire-and-forget thread; captures are copied at spawn time; **no join** (use a channel for completion)
- **`Atomic(T)`** (`T` = `int` or `bool`) is for shared counters, flags, and one-shot signals; never blocks
- **Rule of thumb:** multiple writers → `Atomic`; producer/consumer → `Chan`
- **`ThreadPool(n)`** is a bounded worker pool with `submit` / `wait`; natural backpressure; reusable
- **`ThreadPool` + `Chan`** is the standard pattern for parallel computation with collected results
- **Allocator caveat:** `Chan` and `ThreadPool` use the page allocator; declare them at function scope, not inside short-lived `allocate` blocks
- **Capture loop variables explicitly** in `for i in 0..N: pool.submit(...)` — otherwise every task sees the final value of `i`

---

**That's the end of the new chapters in Part 3.** The next chapter in
reading order is the existing **15-Pipelines-and-Function-Composition**;
when you're ready for the practical project arc, jump ahead to Part 4.

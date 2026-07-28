# 14b: Memory Management and Lifetimes

**Audience:** All — required for long-running services or bounded-memory work
**Time:** 120 minutes
**Prerequisites:** 07-Classes-and-Instances, 07b-Structs-Unions-and-Value-Types
**You'll learn:** The default arena allocator, scoped `allocate` blocks, the `<-` copy-out operator, the `using EXPR` resource pattern, and `^T` heap-indirection for recursive types

---

## The Big Picture

Most languages handle memory in one of three ways:
- **Garbage collection** (Python, Java, Go) — fast to write, periodic pauses
- **Manual `malloc`/`free`** (C, C++) — total control, easy to misuse
- **Borrow checker / ownership** (Rust) — compile-time safe, learning curve

Zebra picks a fourth option: **a program-wide arena allocator, with
optional bounded scopes**. By default every allocation lives until program
exit; you never write `free`. When you need to reclaim memory mid-program
— for a long-running server, a streaming file processor, a large batch
job — you wrap the work in an `allocate Arena()` block.

This model has two benefits worth naming:

1. **The 90% case has zero cognitive overhead.** Short-lived programs,
   CLI tools, scripts — they just work. No annotations, no ceremony.
2. **The 10% case is explicit.** When you need bounded memory, the
   `allocate` block is right there in the source: a reader can see
   exactly where the memory is reclaimed.

This chapter covers the default model, the scoped escape hatch, the
`<-` copy-out operator for passing values past a scope boundary, and the
`^T` heap-indirection syntax for recursive types.

---

## The Default Allocator

Every Zebra program starts with one `ArenaAllocator`, exposed internally
as `_allocator`. Every implicit allocation — string concatenation, `List`
growth, `class` instantiation — pulls from this arena.

```zebra
def main()
    var s = "hello"
    var t = " world"
    var combined = s + t          # allocates a new str — arena handles it
    var nums = List(int)()
    nums.add(1); nums.add(2)       # List growth — arena handles it
    var c = Circle(radius: 5.0)   # class instance — arena handles it
    print(combined)
    # Program exits; arena is destroyed; all of the above freed at once.
```

There's no `s.free()`, `nums.deinit()`, or `c.drop()`. There's no
`defer`. Allocations live until program exit.

### Why no individual `free`?

Two reasons:

1. **`ArenaAllocator` doesn't support targeted frees.** Calling
   `allocator.free(x)` on an arena either no-ops (middle of the arena) or
   rewinds the bump pointer (last allocation) — which corrupts any
   sub-slice still in use elsewhere. So even if Zebra emitted `defer
   allocator.free(x)`, it would not be safe.
2. **For typical programs it doesn't matter.** A CLI tool that runs for
   200ms doesn't care that its strings outlive a function call. The OS
   reclaims the whole arena on process exit.

For long-running programs that *do* care, the answer is `allocate`.

---

## Scoped Memory: `allocate` Blocks

The `allocate <expr>` block redirects `_allocator` to a different
allocator for a lexical scope. When the block exits, scoped allocators
clean up and `_allocator` reverts to the parent.

```zebra
def main()
    var summary = ""
    allocate Arena()
        var src = File.read("big_file.txt")
        var parsed = parse(src)
        summary <- summarise(parsed)        # copy result out (see below)
    # src, parsed, and all parse temporaries freed here.
    print(summary)
```

Inside the block, every implicit allocation goes through the inner
arena. When the block exits, the entire inner arena is reclaimed — even
if `big_file.txt` was 100MB and `parsed` produced thousands of intermediate
strings.

### Named allocator wrappers

`allocate` accepts any value that implements `AllocatorSource` (a class
with `def allocator(): Allocator` + `def deinit()`). The stdlib ships a
named wrapper for every common pattern:

| Wrapper | Backing allocator | Scoped? | Use when |
|---|---|---|---|
| `Arena()` | `std.heap.ArenaAllocator` | ✓ | General sub-arena; most common |
| `Debug()` | `std.heap.DebugAllocator` | ✓ | Leak detection during development |
| `FixedBuffer(buf)` | `std.heap.FixedBufferAllocator` | ✓ | Bounded-size scratch; `buf` is a `[]byte` |
| `StackFallback(N)()` | `std.heap.stackFallback(N, _allocator)` | ✓ | Try stack first, spill to parent arena |
| `Pool(T)()` | `std.heap.MemoryPool(T)` | ✓ | Single-type object pool |
| `ThreadSafe(inner)` | `std.heap.ThreadSafeAllocator` | ✓ | Wrap another scoped allocator for cross-thread use |
| `Page()` | `std.heap.page_allocator` | ✗ | Singleton; no cleanup |
| `Smp()` | `std.heap.smp_allocator` | ✗ | Thread-safe singleton; no cleanup |
| `C()` | `std.heap.c_allocator` | ✗ | libc `malloc`/`free`; no cleanup |

**Scoped** means the wrapper frees everything on block exit. **Non-scoped**
wrappers are singletons; allocations outlive the block naturally.

### Typical use cases

- **Streaming file processor.** Read → parse → reduce, in a loop. Wrap
  each iteration in `allocate Arena()` so the previous iteration's
  buffers don't pile up.
- **Leak detection in CI.** Swap `Arena()` for `Debug()` during
  development; `Debug()` reports any unmatched allocations on exit.
- **Stack-local scratch.** `allocate StackFallback(4096)()` keeps small
  work on the stack and only spills to the heap if the 4KB budget is
  exceeded.
- **Bounded peak memory.** Any batch operation where you want a hard
  ceiling on memory usage.

---

## What Does NOT Survive a Scoped Block

Anything allocated inside a scoped `allocate` block is **freed when the
block exits**. If you save a reference to it in an outer variable
directly, that reference becomes dangling.

```zebra
# UNSAFE — DO NOT DO THIS
var dangling: str
allocate Arena()
    var src = File.read("config.txt")
    dangling = src                # WRONG: src lives in the inner arena
print(dangling)  # dangling slice — undefined behaviour
```

The compiler can't always catch this — `dangling = src` looks like a
normal assignment. The right pattern is the `<-` copy-out operator.

---

## `<-` Copy-Out

The `<-` operator deep-copies a value from the inner allocator into the
parent allocator and assigns it to an outer variable:

```zebra
var summary: str = ""
allocate Arena()
    var src = File.read("big_file.txt")
    var s = process(src)
    summary <- s                  # deep-copies s into the parent allocator
# src + s + temporaries freed; summary survives.
print(summary)
```

For each supported type, `<-` does the right thing:

| Type | What `<-` does |
|---|---|
| `str` | Duplicates the bytes into the parent allocator |
| `List(T)` | Allocates a new ArrayList in the parent; deep-copies each element |
| `class` / `struct` | Recursively deep-copies every field (handles `^T?` chains) |
| `int`, `float`, `bool`, `char` | Plain assignment — no heap |
| **`HashMap`** | **Not supported** — compile error; rebuild manually if needed |

The HashMap limitation is by design. Deep-copying a HashMap requires
re-hashing every key, and the result almost always indicates the wrong
data structure for the lifetime pattern. If you need to surface
key/value data past a block boundary, iterate and rebuild:

```zebra
var out: HashMap(str, int) = HashMap(str, int)()
allocate Arena()
    var tmp: HashMap(str, int) = HashMap(str, int)()
    populate(tmp)
    # tmp <- out                                    # ERROR
    for k, v in tmp                                 # iterate + rebuild
        out.set(k, v)                               # k and v are str/int — copy-out implicit
```

### Outside a scoped block

`<-` is a normal assignment when used outside any scoped block (or
inside a non-scoped wrapper like `Page()`/`Smp()`/`C()`). You can write
`<-` defensively in code that might or might not be inside `allocate`
— it's always safe.

```zebra
def main()
    var x: str = ""
    x <- "hello"                  # outside any allocate block — plain assignment
```

---

## `using EXPR` — Resource Scope Blocks

The `using EXPR` block runs a body with a resource that has a
`begin()` / `end()` lifecycle. Any object with both methods works — no
interface declaration required:

```zebra
class CountGroup
    var entered: int = 0
    var exited: int = 0

    def begin()
        .entered = .entered + 1

    def end()
        .exited = .exited + 1

def main()
    var g = CountGroup()
    using g
        print("inside the using block")
    # Here: g.entered == 1, g.exited == 1
```

### Desugaring

`using EXPR { body }` expands to:

```zebra
{
    const _resource = EXPR
    _resource.begin()
    defer _resource.end()
    body...
}
```

`EXPR` is evaluated exactly once. `end()` fires only if `begin()`
completed successfully — if `begin()` raises, `end()` does not run.

### Why this matters for memory

`using` is the RAII pattern from C++ and the `with` statement from
Python, in one form. It pairs `begin`/`end` calls so a reader can see
the resource is cleaned up. The GUI stdlib uses it for layout groups:

```zebra
using g.vbox("##main", true)
    using g.hbox("##row", false)
        g.button("OK", .ok)
        g.button("Cancel", .cancel)
    g.text("Status: ready")
```

Each `vbox` and `hbox` opens a layout container in `begin()` and closes
it in `end()`. The body in between issues widget commands inside that
container.

### `using` vs. `allocate`

| Pattern | Use when |
|---|---|
| `allocate Arena()` | Want **memory** reclaimed at scope exit |
| `using x` | Want **arbitrary cleanup** (close file, release lock, end paint, leave layout group) |

They compose. A program can have `using` blocks inside `allocate`
blocks and vice versa.

---

## `^T` — Heap Indirection for Recursive Types

`^T` is a special field-type marker for **breaking recursive struct or
union cycles**. It's the only reason to reach for `^T` in Zebra; for
ordinary references, classes already give you reference semantics.

```zebra
struct Node
    var value: int
    var next:  ^Node?              # heap-boxed optional pointer

def main()
    var a = Node(1, nil)
    var b = Node(2, nil)
    a.next = b                     # auto-boxes b into a *Node on the heap
```

### The rules

| Rule | Detail |
|---|---|
| Type mapping | `^T` in a field → `*T` in the generated Zig; `^T?` → `?*T` |
| Auto-boxing | `^T` field = `T` value → compiler allocates a heap copy |
| Transparency | Inside a `branch` arm binding a `^T` payload, the binding has type `T` (pointer stripped) |
| `^ClassName` is illegal | Classes are already references; double-boxing is rejected |
| For-in transparency | `for n in List(^Node)` binds `n: Node`, not `^Node` |

### `^T?` and nil

```zebra
struct TreeNode
    var value: int
    var left:  ^TreeNode?
    var right: ^TreeNode?

def main()
    var root  = TreeNode(value: 5, left: nil, right: nil)
    var child = TreeNode(value: 3, left: nil, right: nil)
    root.left = child              # auto-boxes child into *TreeNode

    if root.left as n              # n: TreeNode — pointer is transparent
        print(n.value)
```

### Unions with `^T` payload

The classic AST shape:

```zebra
union Expr
    num(value: int)
    add(left: ^Expr, right: ^Expr)

def main()
    var e = Expr.add(left: Expr.num(1), right: Expr.num(2))
    branch e
        on Expr.add as a
            # a.left: Expr (not ^Expr — auto-deref'd)
            print("add")
        on Expr.num as n
            print(n.value)
```

This is exactly how Zebra's own compiler models its AST.

### Memory interaction

`^T` allocations go through whatever `_allocator` is active. Inside an
`allocate Arena()` block, the boxes live in the inner arena and are
freed on block exit. The `<-` copy-out operator recursively follows
`^T?` chains — copying out a linked list copies every node.

```zebra
var head: ^Node? = nil
allocate Arena()
    var n = Node(value: "a", next: Node(value: "b", next: nil))
    head <- n              # recursively copies the entire chain into parent
# inner nodes freed; head's chain is intact in the parent arena.
```

---

## Real World: Streaming File Processor

A pattern that benefits from every primitive in this chapter — a loop
that processes many files, with bounded peak memory and a structured
result that survives each iteration:

```zebra
# file: 14b_streaming_processor.zbr
# teaches: allocate + <- + using together
# chapter: 14b-Memory-Management-and-Lifetimes

class Summary
    public var filename: str = ""
    public var word_count: int = 0
    public var top_word: str = ""

def process_one(path: str): Summary
    var result = Summary()
    result.filename = path
    allocate Arena()
        var src = File.read(path)
        var words = src.split(" ")
        result.word_count = words.count()
        result.top_word <- most_frequent(words)   # copy-out the single str
    # All of src + words freed here; result survives.
    return result

def most_frequent(words: List(str)): str
    # ... implementation that allocates a HashMap internally ...
    return ""

def main()
    var summaries: List(Summary) = List()
    var paths = File.list_dir("./docs")
    for path in paths
        var s = process_one(path)
        summaries.add(s)               # Summary itself is in the outer arena

    for s in summaries
        print("${s.filename}: ${s.word_count} words, top=${s.top_word}")
```

Each call to `process_one` reads its file, computes its summary, copies
the relevant strings into the caller's arena, then frees everything
else. Peak memory stays bounded at one file's worth — regardless of
whether there are 10 files or 10,000.

---

## Common Mistakes

> ❌ **Mistake:** Storing a value from inside an `allocate` block without `<-`
>
> ```zebra
> var s: str
> allocate Arena()
>     s = File.read("config.txt")      # s now points into the inner arena
> # s is dangling here
> ```
>
> ✅ **Better:**
> ```zebra
> var s: str
> allocate Arena()
>     var tmp = File.read("config.txt")
>     s <- tmp                          # deep-copy into parent
> ```

> ❌ **Mistake:** Trying to copy out a HashMap
>
> ```zebra
> var out: HashMap(str, int) = HashMap(str, int)()
> allocate Arena()
>     var tmp: HashMap(str, int) = HashMap(str, int)()
>     out <- tmp                        # ERROR: HashMap copy-out not supported
> ```
>
> ✅ **Better:** iterate and rebuild outside:
> ```zebra
> for k, v in tmp
>     out.set(k, v)                     # primitives copy implicitly
> ```

> ❌ **Mistake:** Reaching for `^T` on a class field
>
> ```zebra
> class Tree
>     var left:  ^Tree?                 # ERROR: ^ClassName is illegal
> ```
>
> ✅ **Better:** `Tree` is already a reference type:
> ```zebra
> class Tree
>     var left:  Tree?                  # plain reference; no ^ needed
> ```

> ❌ **Mistake:** Forgetting that `allocate Page()` doesn't free
>
> ```zebra
> allocate Page()
>     var src = File.read("huge.bin")
> # src is NOT freed here — Page() is non-scoped
> ```
>
> ✅ **Better:** use `Arena()` for bounded scopes:
> ```zebra
> allocate Arena()
>     var src = File.read("huge.bin")
> # src freed here
> ```

---

## Exercises

### Exercise 1: A Bounded-Memory Loop

Rewrite this loop so peak memory stays bounded at one file at a time:

```zebra
def main()
    var paths = File.list_dir("./logs")
    var counts: List(int) = List()
    for path in paths
        var src = File.read(path)        # accumulates across iterations
        counts.add(src.split("\n").count())
```

<details>
<summary>Solution</summary>

```zebra
def main()
    var paths = File.list_dir("./logs")
    var counts: List(int) = List()
    for path in paths
        var n: int = 0
        allocate Arena()
            var src = File.read(path)
            n <- src.split("\n").count()
        counts.add(n)
```

`int` is a primitive — `<-` is a plain assignment — but the `src`
buffer is freed before the next iteration reads its file.

</details>

### Exercise 2: A Recursive Tree

Define a binary tree of integers using `^T?` and write a function that
counts the nodes recursively.

<details>
<summary>Solution</summary>

```zebra
struct TreeNode
    var value: int
    var left:  ^TreeNode?
    var right: ^TreeNode?

def count_nodes(t: ^TreeNode?): int
    if t as n                # n: TreeNode — pointer is transparent
        return 1 + count_nodes(n.left) + count_nodes(n.right)
    return 0

def main()
    var leaf  = TreeNode(value: 3, left: nil, right: nil)
    var leaf2 = TreeNode(value: 7, left: nil, right: nil)
    var root  = TreeNode(value: 5, left: leaf, right: leaf2)
    print(count_nodes(root))  # 3
```

</details>

### Exercise 3: A `using` Resource

Write a `Timer` class with `begin()` recording the start time and `end()`
printing the elapsed milliseconds. Use it with `using` to time a block.

<details>
<summary>Solution</summary>

```zebra
class Timer
    var label: str
    var start_ms: int = 0

    cue init(label: str)
        .label = label

    def begin()
        .start_ms = Time.monotonic_ms()

    def end()
        var elapsed = Time.monotonic_ms() - .start_ms
        print("${.label}: ${elapsed} ms")

def main()
    using Timer("file read")
        var src = File.read("big.txt")
        # ... work ...
    # Prints "file read: NN ms" when the block exits
```

</details>

---

## Next Steps

- → **14c-Concurrency-Channels-and-Threads** — concurrent primitives that share this memory model
- → **22-FFI-and-Interop** — `allocate C()` for libc-allocated values crossing the FFI boundary
- → **07b-Structs-Unions-and-Value-Types** — the value-type model that `^T` punches through

---

## Key Takeaways

- **Default model: arena allocator, no individual frees.** Allocations live until program exit; the OS reclaims the arena.
- **`allocate <wrapper>` scopes the allocator** for a block; on exit, scoped wrappers free everything inside.
- **Named wrappers** include `Arena()` (most common), `Debug()` (leak detection), `FixedBuffer(buf)`, `StackFallback(N)()`, `Pool(T)()`, and non-scoped singletons `Page()` / `Smp()` / `C()`.
- **`<-` copy-out** deep-copies a value past a scope boundary — works for `str`, `List(T)`, classes/structs (incl. recursive `^T?` chains), and primitives; **HashMap is intentionally not supported** — iterate and rebuild.
- **`using EXPR` blocks** call `begin()` / `end()` around a body; any class with both methods works. Use for arbitrary cleanup; pair with `allocate` for memory.
- **`^T` heap-indirection** is for recursive structs/unions only; auto-boxes, transparent in `branch` and for-loops; **`^ClassName` is illegal** (classes are already references).

---

**Next:** Chapter 14c covers concurrency — `Chan(T)` channels, `sys.go()` for spawning threads, and the `ThreadPool` / `Atomic` primitives — built on the memory model from this chapter.

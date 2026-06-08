# 10b: Modules, Namespaces, and Visibility

**Audience:** All
**Time:** 90 minutes
**Prerequisites:** 04-Functions-and-Scope, 07-Classes-and-Instances
**You'll learn:** Splitting code across files with `use`, qualified vs. exposed imports, visibility keywords (`public`/`private`/`internal`/`protected`), namespaces (flat and nested), `extend` for adding methods to existing types, partial files

---

## The Big Picture

A single `.zbr` file works for an example or a small tool. Real projects
need to split code across many files for the same reasons every other
language does:

- **Comprehension** — a 200-line file is readable; a 20,000-line file is not
- **Reuse** — the same `Vec2` struct shouldn't be re-defined in every script
- **Boundaries** — a `Wallet` class should hide its internal balance from the rest of the program
- **Naming** — `parse` could mean three different things in three different domains; the module name disambiguates

Zebra gives you four tools for this:

| Tool | What it does |
|---|---|
| **Modules** (one file = one module) | Reuse code across files |
| **Visibility keywords** (`public`/`private`/`internal`/`protected`) | Hide internals |
| **`namespace`** | Group related declarations inside a file |
| **`extend`** | Add methods to existing types without inheritance |

This chapter walks each in turn.

---

## Files as Modules

Every `.zbr` file is automatically a **module**. The module name is the
filename without the extension.

```zebra
# file: math_utils.zbr
def square(x: int): int
    return x * x

struct Vec2
    var x: float
    var y: float

    def length(): float
        return Math.sqrt(x*x + y*y)
```

To use this from another file, write `use math_utils` and then reference
the names with a `math_utils.` prefix:

```zebra
# file: main.zbr
use math_utils

def main()
    var n = math_utils.square(5)
    var v = math_utils.Vec2(3.0, 4.0)
    print v.length()
```

The compiler resolves `use math_utils` by looking for `math_utils.zbr`:
1. In the same directory as the importing file
2. In `selfhost/`, `test/`, and the stdlib path

That's the whole module model — one file, one module, lookup by name.

---

## `exposing` — Importing Specific Names

The qualified `math_utils.square(...)` form gets verbose if you call into
the module often. `exposing` lets you bind specific names directly into
your scope:

```zebra
# file: main.zbr
use math_utils exposing square, Vec2

def main()
    var n = square(5)            # no math_utils. prefix
    var v = Vec2(3.0, 4.0)
    print v.length()
```

Combine forms freely:

```zebra
use math_utils exposing square, Vec2  # also have math_utils.* available
```

After this line, `square` and `Vec2` are in scope unqualified; everything
else in `math_utils` is still reachable as `math_utils.something()`.

### Qualified vs. exposed — which to use

- **Exposed** — when the names are domain-specific and unambiguous in
  context (`square`, `Vec2`, `parseJson`).
- **Qualified** — when the unqualified name would collide with another
  module's name, or when the qualification adds useful context for the
  reader (`db.query(...)` is clearer than `query(...)`).

A common pattern: expose the types and qualify the operations.

```zebra
use http exposing Request, Response

def handle(req: Request): Response
    return http.json_response(req.body)
```

`Request` and `Response` are types you'll mention often; `json_response`
is an action where the `http.` prefix reads naturally.

---

## Cross-Module Type Annotations

Either form works in a type annotation:

```zebra
# Qualified:
var v: math_utils.Vec2 = math_utils.Vec2(1.0, 2.0)

# Exposed:
use math_utils exposing Vec2
var v: Vec2 = Vec2(1.0, 2.0)
```

Pick the one that matches the rest of your imports — consistency reads
better than micro-optimisation.

---

## Visibility Keywords

By default every top-level declaration in a module is **public** —
reachable from any file that imports the module. Use a visibility keyword
to narrow that:

| Keyword | Reachable from |
|---|---|
| `public` (default) | Anywhere |
| `protected` | The owning class and its subclasses |
| `internal` | The same module; excluded from cross-module interface tables |
| `private` | The owning class only |

Visibility applies to **fields and methods** inside a class, and to
top-level functions/types in a module:

```zebra
# file: wallet.zbr
class Wallet
    private var balance: float     # only Wallet's own methods can read/write

    public def deposit(amount: float)
        .balance = .balance + amount

    public def get_balance(): float
        return .balance

    private def log_event(msg: str)
        # internal bookkeeping — callers can't reach this
        print "[wallet] ${msg}"
```

```zebra
# file: main.zbr
use wallet exposing Wallet

def main()
    var w = Wallet()
    w.deposit(100.0)            # ok — deposit is public
    print w.get_balance()       # ok
    # w.balance                  # ERROR — balance is private
    # w.log_event("oops")        # ERROR — log_event is private
```

The compiler enforces visibility at use sites. The error message tells you
which keyword would unlock access.

### When to use each

- **`private`** — the default for state and helpers. Start `private`; promote
  to `public` only when an external caller actually needs the access.
- **`protected`** — used when subclasses need access but the public API
  doesn't. Rare in Zebra (composition is preferred over inheritance, see Ch09).
- **`internal`** — module-private. Useful when a top-level helper is shared
  among several classes in the same file but not part of the public API.
- **`public`** — the rest.

> **Note on `_underscore` prefix.** Earlier Zebra code used a leading
> `_` on identifiers to signal "compiler-internal." The visibility keywords
> superseded that convention for user code. The `_` prefix is now reserved
> for compiler-emitted symbols (`_io`, `_allocator`, etc.) — don't use it
> in your own code.

---

## Namespaces — Grouping Inside a File

A `namespace` block wraps top-level declarations under a named scope:

```zebra
# file: colors.zbr
namespace Colors
    struct Rgb
        var r: int
        var g: int
        var b: int

    def from_hex(hex: int): Rgb
        return Rgb(r: (hex >> 16) & 0xFF,
                   g: (hex >> 8)  & 0xFF,
                   b: hex & 0xFF)
```

Usage:

```zebra
use colors

def main()
    var red  = Colors.Rgb(r: 255, g: 0, b: 0)
    var blue = Colors.from_hex(0x0000FF)
```

All names declared inside `namespace Colors` are accessed as `Colors.X`.

**Inside the namespace**, methods can call each other without the prefix —
`from_hex` could call another helper inside `Colors` directly.

### When to use a namespace

- **Group related helpers that don't share state.** A class is overkill
  for utility functions; a namespace gives them a name without instantiation.
- **Cluster a small type with its operations.** `Colors.Rgb` and
  `Colors.from_hex` belong together; a namespace keeps them paired.
- **Avoid top-level pollution.** Without a namespace, every helper in
  every file lives in the module's top scope. Namespaces structure that.

### Nested namespaces

Two syntaxes — pick whichever reads better for your case.

**Dotted path** — concise for a single leaf:

```zebra
namespace Sql.Sqlite
    static def open(path: str): int
        # ...

def main()
    var db = Sql.Sqlite.open("mydb.db")
```

**Nested body** — natural when the outer namespace also has direct members:

```zebra
namespace Sql
    static def version(): str
        return "1.0"

    namespace Sqlite
        static def open(path: str): int
            # ...

    namespace Postgres
        static def connect(url: str): int
            # ...

def main()
    print Sql.version()
    var db = Sql.Sqlite.open("mydb.db")
    var pg = Sql.Postgres.connect("postgresql://localhost/mydb")
```

Both compile to the same nested struct in the generated Zig.

---

## `extend` — Adding Methods to Existing Types

`extend` adds methods to a type that's already defined — including
built-in types like `str` and `int`:

```zebra
extend str
    def shout(): str
        return this.to_upper() + "!"

    def word_count(): int
        return this.split(" ").len

# Anywhere in the same file:
var s = "hello world"
print s.shout()         # HELLO WORLD!
print s.word_count()    # 2
```

`this` inside an `extend` body is the receiver value. The extended type
can be any built-in (`str`, `int`, `float`, `bool`, `char`) or any user
class/struct.

### Common patterns

```zebra
extend int
    def is_even(): bool
        return this % 2 == 0

    def abs(): int
        if this < 0: return -this
        return this

extend List(str)
    def join_with(sep: str): str
        return this.join(sep)
```

`extend` can also conform an existing type to an interface or include
a mixin:

```zebra
extend str is Printable
    def show(): str
        return this
```

### Important: extensions are file-scoped

Methods added via `extend` are visible **only in the file where the
`extend` block appears**. They are not exported across module boundaries.

```zebra
# file: helpers.zbr
extend int
    def double(): int
        return this * 2
```

```zebra
# file: main.zbr
use helpers
def main()
    # var n = 5.double()    # ERROR — double() not visible here
    pass
```

If you need a cross-module extension, either:
- Repeat the `extend` block in each importing file (intentional, explicit), or
- Wrap the extension in a regular function: `def double(n: int): int { return n * 2 }`

This is a deliberate design — extensions are powerful but ambient. Forcing
them to be file-local keeps surprises out of large codebases.

---

## Partial Files

A class can be **split across multiple files** by naming convention. Given
a primary file `Foo.zbr` declaring `class Foo`, any file named `Foo.X.zbr`
(where `X` is any segment) is treated as a partial. Its `class Foo`
members are **merged into the primary class** at compile time.

```zebra
# file: Wallet.zbr  (primary)
class Wallet
    private var balance: float

    public def get_balance(): float
        return .balance
```

```zebra
# file: Wallet.transactions.zbr  (partial — merges into Wallet)
class Wallet
    public def deposit(amount: float)
        .balance = .balance + amount

    public def withdraw(amount: float) throws
        if amount > .balance
            raise "insufficient funds"
        .balance = .balance - amount
```

After compilation, `Wallet` has `balance`, `get_balance`, `deposit`, and
`withdraw` — as though they had all been declared in one file.

**When to use partials:** large classes whose methods cluster by concern
(persistence, JSON serialisation, UI binding). The compiler emits
identical code either way; partials are a source-organisation tool, not
a runtime concept.

---

## Real World: Multi-Module CLI Project

Here's a project layout that uses every primitive in this chapter:

```
my-tool/
├── build.zbr
└── src/
    ├── main.zbr               # entry point
    ├── cli.zbr                # argument parsing (public API)
    ├── cli.internal.zbr       # cli internals (partial of cli)
    └── work.zbr               # core logic
```

### `src/main.zbr`

```zebra
use cli exposing Options
use work

def main()
    var opts = cli.parse_args(sys.args())
    work.run(opts)
```

### `src/cli.zbr`

```zebra
class Options
    public var verbose: bool = false
    public var input_path: str = ""

namespace Cli
    static def usage(): str
        return "my-tool [--verbose] FILE"

def parse_args(args: List(str)): Options
    var opts = Options()
    for arg in args
        if arg == "--verbose"
            opts.verbose = true
        else
            opts.input_path = arg
    return opts
```

### `src/cli.internal.zbr` (partial — merges with `Cli` namespace)

```zebra
namespace Cli
    # internal helper — not exposed in cli.zbr's public surface
    static def normalize_path(p: str): str
        if p.starts_with("./")
            return p.slice(2, p.len)
        return p
```

### `src/work.zbr`

```zebra
use cli exposing Options

extend Options
    def describe(): str
        return "verbose=${.verbose}, input=${.input_path}"

def run(opts: Options)
    if opts.verbose
        print "Processing: ${opts.describe()}"
    # ... core logic ...
```

Two things worth noticing:

1. **`work.zbr` extends `Options`** (defined in `cli.zbr`) with a
   `describe()` method. The extension is local to `work.zbr` — other
   files see `Options` without `describe`.
2. **`cli.internal.zbr` is a partial** of the `Cli` namespace from
   `cli.zbr`. The compiler merges the two before resolving names. From
   `main.zbr`'s perspective, `Cli.normalize_path` and `Cli.usage` are in
   the same namespace.

---

## Common Mistakes

> ❌ **Mistake:** Forgetting to import a module
>
> ```zebra
> def main()
>     var v = math_utils.square(5)   # ERROR: math_utils not in scope
> ```
>
> ✅ **Better:**
> ```zebra
> use math_utils
>
> def main()
>     var v = math_utils.square(5)
> ```

> ❌ **Mistake:** Trying to use an `extend` method across files
>
> ```zebra
> # helpers.zbr
> extend int
>     def is_prime(): bool
>         # ...
>
> # main.zbr
> use helpers
> def main()
>     print 7.is_prime()         # ERROR: extension not visible here
> ```
>
> ✅ **Better:** wrap the logic in a regular function instead:
> ```zebra
> # helpers.zbr
> def is_prime(n: int): bool
>     # ...
>
> # main.zbr
> use helpers exposing is_prime
> def main()
>     print is_prime(7)
> ```

> ❌ **Mistake:** Making everything `public` by default
>
> ```zebra
> class Wallet
>     var balance: float           # default = public — leaks internal state
> ```
>
> ✅ **Better:** start `private`, promote when needed:
> ```zebra
> class Wallet
>     private var balance: float
>     public def get_balance(): float
>         return .balance
> ```

> ❌ **Mistake:** Confusing a namespace with a class
>
> ```zebra
> namespace Colors
>     struct Rgb
>         var r: int
>
> # Wrong — can't instantiate a namespace:
> # var c = Colors(...)
> ```
>
> ✅ **Better:** instantiate the type *inside* the namespace:
> ```zebra
> var c = Colors.Rgb(r: 255, g: 0, b: 0)
> ```

---

## Exercises

### Exercise 1: Split and Import

Split this single-file program into a `geometry.zbr` module and a
`main.zbr` that imports it. Expose the `Circle` class and the `area`
function.

```zebra
# Single file (start)
struct Circle
    var radius: float

    def area(): float
        return 3.14159 * radius * radius

def total_area(circles: List(Circle)): float
    var sum = 0.0
    for c in circles
        sum = sum + c.area()
    return sum

def main()
    var cs = [Circle(1.0), Circle(2.0), Circle(3.0)]
    print total_area(cs)
```

<details>
<summary>Solution</summary>

`geometry.zbr`:
```zebra
struct Circle
    var radius: float

    def area(): float
        return 3.14159 * radius * radius

def total_area(circles: List(Circle)): float
    var sum = 0.0
    for c in circles
        sum = sum + c.area()
    return sum
```

`main.zbr`:
```zebra
use geometry exposing Circle, total_area

def main()
    var cs = [Circle(1.0), Circle(2.0), Circle(3.0)]
    print total_area(cs)
```

</details>

### Exercise 2: Namespace Refactor

Convert this loose-functions module into a namespace-based one:

```zebra
def hex_to_rgb(hex: int): (int, int, int)
    return ((hex >> 16) & 0xFF, (hex >> 8) & 0xFF, hex & 0xFF)

def darken(rgb: (int, int, int), pct: int): (int, int, int)
    var (r, g, b) = rgb
    return (r * (100 - pct) / 100,
            g * (100 - pct) / 100,
            b * (100 - pct) / 100)
```

<details>
<summary>Solution</summary>

```zebra
namespace Colors
    def hex_to_rgb(hex: int): (int, int, int)
        return ((hex >> 16) & 0xFF, (hex >> 8) & 0xFF, hex & 0xFF)

    def darken(rgb: (int, int, int), pct: int): (int, int, int)
        var (r, g, b) = rgb
        return (r * (100 - pct) / 100,
                g * (100 - pct) / 100,
                b * (100 - pct) / 100)
```

Callers use `Colors.hex_to_rgb(...)` and `Colors.darken(...)`. The
operations group naturally under the domain name.

</details>

### Exercise 3: Visibility Audit

Take a class you've written and audit its visibility. Which fields are
truly private? Which methods are only called from inside the class?
Tighten the visibility, then make sure the rest of your program still
compiles.

This exercise has no programmatic solution — it's the workflow that
matters. Done well, visibility tightening usually finds at least one
field or method that shouldn't have been exposed.

---

## Next Steps

- → **22b-Build-System-and-Tooling** — multi-module project builds
- → **22c-Testing-and-Validation** — test each module independently
- → **08-Interfaces-and-Protocols** — pair modules with interface conformance

---

## Key Takeaways

- **One file = one module** — `use module_name` imports it; resolution is filename-based
- **`use M exposing X, Y`** binds names directly into scope; bare `use M` requires `M.X` qualification
- **`public` / `private` / `internal` / `protected`** control access; `private` is the right default for state, promote as needed
- **`namespace`** groups declarations inside a file; nested form (`namespace Outer.Inner` or `namespace Outer { namespace Inner { ... } }`) builds hierarchies
- **`extend`** adds methods to existing types, including built-ins — but the extension is **file-scoped**, not exported across modules
- **Partial files** (`Foo.X.zbr` merging into `Foo.zbr`) split a large class across files at compile time

---

**Next:** Chapter 14b shifts focus to runtime — memory lifetimes, the `allocate` block, the `<-` copy-out operator, and the heap-indirection `^T` syntax that ties them together.

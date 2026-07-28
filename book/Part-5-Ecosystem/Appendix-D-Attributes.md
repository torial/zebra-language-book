# Appendix D: Attribute Reference

This appendix is a one-page quick reference for every `@attribute` (and
the related `export` keyword) in Zebra. Use it to recall syntax and
behaviour; the chapter sections in this book teach each pattern in
context.

The attributes:

| Attribute | Applies to | Effect | Chapter |
|---|---|---|---|
| `@once` | method | Cache first call's result on the instance | 07 |
| `@profile` | method | Wrap body with `Profile.start/end` | 07 |
| `@tag("label", ...)` | test method | Mark for `zebra test --tag` filtering | 22c |
| `@derive(Debug, Eq, Hash)` | struct | Auto-generate `toString` / `eql` / `hash` | 07 |
| `@reflectable` | class | Opt into Tier-3 reflection + typed JSON parse | 25 (QUICKSTART) |
| `@export("symbol")` | class | Emit DynLib factory function | 22 |
| `export def name(...)` | top-level fn | Emit C-callable `pub export fn` | 22 |

---

## `@once` — Cache First Call

Wraps a method so the body runs at most once per instance. Subsequent
calls return the cached value without re-running:

```zebra
class Config
    @once
    def load(): str
        # body runs the first time .load() is called on this instance
        return File.read("config.json")

def main()
    var c = Config()
    var a = c.load()          # reads the file
    var b = c.load()          # returns cached value, no file read
```

**Generated code:** the compiler emits hidden per-instance fields
`_once_cache_<name>` and `_once_done_<name>` that guard the body.

**Notes:**

- The cache is per-**instance** — two `Config` objects each cache their own first call.
- Works for any non-void return type. `void` methods have the body suppressed after the first call.
- Not threadsafe — for multi-thread initialisation, wrap the field in an `Atomic(bool)` and check it manually, or initialise in a synchronised setup function.

---

## `@profile` — Automatic Profiling

Wraps a method body with `Profile.start("ClassName.method")` and
`defer Profile.end(...)`:

```zebra
class Renderer
    @profile
    def draw_frame()
        # body is timed automatically
        ...
```

**Requires** the `Profile` stdlib module to be linked (it's pulled in
automatically when `@profile` appears).

**Notes:**

- The label is `"ClassName.methodName"` — no way to customise per-call.
- Pairs naturally with the `Profile.report()` stdlib call for end-of-run summaries.
- Adds a small constant overhead per call; for tight loops, prefer profiling the caller, not the inner method.

---

## `@tag("label", ...)` — Test Filtering

Attaches one or more string tags to a `test_*` method so
`zebra test --tag <label>` can filter to it:

```zebra
@tag("unit", "fast")
def test_addition()
    assert_eq 1 + 1, 2

@tag("integration")
def test_database_roundtrip()
    # ...
```

Tags are unioned with **auto-tags** (file stem, class/struct name) at
filter time — see Chapter 22c for the full filtering model.

**Notes:**

- Multiple tags per attribute: `@tag("unit", "fast")` — both apply.
- Tags are strings; convention is lowercase kebab-case (`unit`, `slow`, `integration`).
- Outside of `test_*` methods, `@tag` is silently ignored.

---

## `@derive(Debug, Eq, Hash)` — Auto-Generated Methods

Tells the compiler to generate `toString`, `eql`, and/or `hash` for a
**struct** based on its fields:

```zebra
@derive(Debug, Eq, Hash)
struct Point
    var x: float
    var y: float
```

Equivalent hand-written methods:

| Trait | Generated method |
|---|---|
| `Debug` | `def toString(): str` — `"Point(x=1.0, y=2.0)"` |
| `Eq` | `def eql(other: Point): bool` — field-wise equality |
| `Hash` | `def hash(): int` — combined per-field hash; consistent with `eql` |

**Combine any subset:**

```zebra
@derive(Debug)              # just toString
@derive(Eq, Hash)           # equality + hashable
@derive(Debug, Eq, Hash)    # all three
```

**Notes:**

- **`@derive` is struct-only.** Classes have reference semantics; field-wise equality almost never matches what callers want for classes. For class methods, write them by hand.
- The generated methods follow the field declaration order. Adding/removing fields automatically updates the generated implementations.
- For unions (tagged unions), `@derive` is not supported; write the comparison logic by hand inside a `branch`.

---

## `@reflectable` — Opt-In Class Reflection

Marks a class as available for **Tier-3 reflection** — typed JSON
parsing via `Json.parseStrict(T, src): ?T`, and any future
metaprogramming that needs field/type lookup tables:

```zebra
@reflectable
class User
    var name: str = ""
    var age:  int = 0

def main()
    var src = "{\"name\":\"Alice\",\"age\":30}"
    if Json.parseStrict(User, src) as u
        print(u.name)  # "Alice"
    else
        print("parse failed")
```

**Generated code:** per-field name and type tables
(`_reflect_<T>_field_names`, `_reflect_<T>_field_types`).

**Notes:**

- **`@reflectable` is required** for `Json.parseStrict(T, ...)` — calling it on an unannotated class is a compile-time error.
- Without the annotation, no reflection tables are emitted — binary size stays minimal for classes that don't need it.
- Tier-1 reflection (`Reflect.className`, `Reflect.fieldNames`) works **without** `@reflectable` for any class; the constant arrays are linker-dead-stripped when unreferenced.
- Tier-2 reflection is not currently in the language — see QUICKSTART §25 for the most current status.

---

## `@export("symbol")` — DynLib Class Plugin

Tells the compiler to emit a C-callable factory function that wraps a
class instance in an interface fat-pointer, suitable for loading via
`DynLib.open` + `lib.lookup`:

```zebra
interface IGreeter
    def greet(name: str): str

@export("greeter")
class HelloGreeter implements IGreeter
    def greet(name: str): str
        return "Hello, " + name
```

Compile with `zebra --shared greeter.zbr` to produce a shared library;
the consumer loads with `DynLib.open("greeter.dll")` +
`lib.lookup(IGreeter, "greeter")`.

**Requirements:**

- The class must implement **at least one interface** — the factory wraps the first listed interface.
- The class `init` must take **no arguments** — the factory calls `ClassName.init()` internally.
- The symbol name must be unique across all plugins loaded into the same host process.

**Notes:**

- See Chapter 22 for the full producer/consumer workflow, the IDE-extension example, and OS-specific path conventions.

---

## `export def` — C-Callable Function

Not technically an `@`-attribute — `export` is a keyword — but
included here because its purpose is the same: marking something
for cross-binary visibility.

```zebra
export def addOne(x: int): int
    return x + 1
```

Emits `pub export fn addOne(x: i64) i64` — callable from C or any
language with FFI support.

**C-compatible types only:**

| Type | C-callable? |
|---|---|
| `int`, `float`, `bool`, `char` | ✓ |
| `str` | ✗ (Zig slice, not a C `const char *`) |
| `List(T)`, `HashMap(K, V)` | ✗ |
| Class / struct (by value) | ✗ |

For richer types, use `@export class` (above) and route through the
DynLib interface.

---

## Compatibility Notes

These attributes are stable as of Zebra 1.0. Anything not listed here
either does not exist or is not yet user-facing.

**Reserved for future use** (don't use these names):

- `@deprecated` — planned for the next milestone
- `@inline` — planned, currently a hint not enforced
- `@noinline` — same as above

When in doubt, the canonical reference is `QUICKSTART.md` §5
(method modifiers), §25 (reflection), §43 (derive), §44 (DynLib).

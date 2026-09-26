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
| `@derive(Debug, Eq, Hash)` | struct | Auto-generate the `toString` / `equals` / `hash` cues | 07 |
| `@deprecated("message")` | `def`, method, `static def` | Warn at every call site | — |
| `@reflectable` | class | Opt into Tier-3 reflection + typed JSON parse | 25 (QUICKSTART) |
| `@export("symbol")` | class | Emit DynLib factory function | 22 |
| `@node_export` | top-level `def`, or a method in a `static` block | Export to a Node.js native addon (`--target node-addon`) | QUICKSTART §45 |
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
    assert 1 + 1 == 2

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

Tells the compiler to generate the `toString`, `equals`, and/or `hash` cues
for a **struct** based on its fields:

```zebra
@derive(Debug, Eq, Hash)
struct Point
    var x: int
    var y: int
```

Equivalent hand-written cues (they are cues, not ordinary methods — the
compiler refuses `def toString()` and asks for `cue toString()`):

| Trait | Generated cue |
|---|---|
| `Debug` | `cue toString(): str` — `"Point(x=1, y=2)"` |
| `Eq` | `cue equals(other: Point): bool` — field-wise equality; `==` and `!=` call it |
| `Hash` | `cue hash(): int` — combined per-field hash; consistent with `equals` |

**Combine any subset:**

```zebra
@derive(Debug)              # just toString
@derive(Eq, Hash)           # equality + hashable (a HashMap / Set key)
@derive(Debug, Eq, Hash)    # all three
```

**Notes:**

- **`@derive` is struct-only.** Classes have reference semantics; field-wise equality almost never matches what callers want for classes. For class methods, write them by hand.
- The generated methods follow the field declaration order. Adding/removing fields automatically updates the generated implementations.
- If you write your own `cue toString` / `cue equals` / `cue hash`, yours wins for that trait.
- `Hash` needs every field to be hashable. A `float` field is not: calling `hash()` on such a struct fails to build (today with Zig's `unable to hash type f64`).
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

## `@deprecated("message")` — Deprecation Warnings

Marks a `def`, a method, or a `static def` as deprecated. Every call site gets a
**warning** naming the replacement; the program still builds and runs:

```zebra
# file: deprecated_demo.zbr
@deprecated("use addTwice instead")
def addOld(a: int): int
    return a + a

def addTwice(a: int): int
    return a * 2

def main()
    print(addOld(21))       # warning at this call; prints 42
```

```
deprecated_demo.zbr:10:11: warning: 'addOld' is deprecated: use addTwice instead
```

**Notes:**

- The message is optional: `@deprecated` alone also works.
- The warning follows the function across `use` into other modules.
- A warning never fails a build on its own. `zebra --warnings-as-errors file.zbr`
  turns it into a failed compile (`error: 1 warning(s) with --warnings-as-errors`).

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

These are the attributes this book covers, as accepted by the current compiler
(the 0.9.0 pre-releases). Zebra has not reached 1.0, so the list can still
change; `QUICKSTART.md` in the language repository is the authority on anything
newer.

`@inline` and `@noinline` are **not** attributes: the compiler warns
`unknown @-directive '@inline'; ignored` and carries on.

When in doubt, the canonical reference is `QUICKSTART.md` §5
(method modifiers), §25 (reflection), §43 (derive), §44 (DynLib).

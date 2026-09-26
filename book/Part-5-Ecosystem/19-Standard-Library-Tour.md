# Chapter 19: Standard Library Tour

**Time:** 90 min | **Audience:** Intermediate | **Prerequisites:** Chapters 01-06

---

## Learning Outcomes

After this chapter, you will:
- Know the major modules and APIs in Zebra's standard library
- Understand when to use built-in functions vs. writing your own
- Navigate API documentation effectively
- Use string, collection, math, and system operations fluently
- Recognize patterns you can apply to your own libraries

---

## Overview: What's Already Built

Zebra ships with a comprehensive standard library organized into builtin modules. Each module is available without importing — just use it by name.

| Module | Purpose |
|--------|---------|
| `List`, `HashMap` | Core collections |
| `StringBuilder` | Efficient string building |
| `Math` | Trig, rounding, constants (PI, E, TAU) |
| `File`, `Dir`, `Path` | File I/O and path utilities |
| `Shell` | Process execution |
| `Http`, `Tcp`, `Udp`, `Net` | Networking |
| `Json`, `JsonValue` | JSON parsing and generation |
| `Regex` | Regular expressions |
| `Csv`, `CsvWriter` | CSV parsing and writing |
| `Random` | Random number generation |
| `Arg`, `ArgResult` | Command-line argument parsing |
| `Terminal` | Terminal output with colors |
| `Log` | Structured logging |
| `DateTime`, `Calendar` | Date and time |
| `Hash` | Hashing utilities |
| `Uri` | URL parsing |
| `Compress` | gzip compression |
| `Timer` | Timing and benchmarks |
| `Reflect` | Runtime reflection |
| `sys` | Process control (args, exit) |
| `Gui` | UI toolkit (MVU; `libui_ng` native, `tui` terminal, and `stub` test backends — Chapter 18b) |

---

## String Operations

Strings are the most commonly used type. Zebra's string API covers the essentials.

### Basic Properties and Inspection

```zebra
# file: stdlib-string-inspect.zbr
# teaches: string properties and inspection methods
# chapter: 19

def main()
    var text = "Hello, World!"

    # Length
    print(text.len)  # 13

    # Character access — charAt returns a byte, not a str, so this prints
    # 72 (the ASCII code for 'H'), not "H"
    var first_char = text.charAt(0)
    print(first_char)

    # Check existence
    if text.contains("World")
        print("Found World")

    if text.startsWith("Hello")
        print("Greeting detected")

    if text.endsWith("!")
        print("Exclamation found")
```

### Case Conversion

```zebra
# file: stdlib-string-case.zbr
# teaches: case conversion methods
# chapter: 19

def main()
    var text = "Zebra Programming"

    var upper = text.upper()        # "ZEBRA PROGRAMMING"
    print(upper)

    var lower = text.lower()        # "zebra programming"
    print(lower)
```

### String Splitting and Joining

```zebra
# file: stdlib-string-split-join.zbr
# teaches: splitting and joining strings
# chapter: 19

def main()
    # Split by delimiter
    var csv_line = "John,25,Engineer,San Francisco"
    var fields = csv_line.split(",")

    print(fields.count())  # 4
    print(fields.at(0))  # "John"

    # Join with separator
    var rejoined = fields.join(" | ")
    print(rejoined)  # "John | 25 | Engineer | San Francisco"
```

### Whitespace Trimming

```zebra
# file: stdlib-string-trim.zbr
# teaches: removing whitespace from strings
# chapter: 19

def main()
    var input = "  Hello, World!  "
    var trimmed = input.trim()      # "Hello, World!"
    print(trimmed)
```

### String Building

For building strings incrementally (e.g., in loops), use `StringBuilder`:

```zebra
# file: stdlib-string-builder.zbr
# teaches: efficient string building
# chapter: 19

def main()
    var sb = StringBuilder()
    sb.append("Hello")
    sb.append(", ")
    sb.append("World!")
    var result = sb.toString()
    print(result)  # "Hello, World!"
```

---

## Collection Operations

### List Operations

Lists are ordered, mutable collections that grow dynamically.

```zebra
# file: stdlib-list-ops.zbr
# teaches: list operations and patterns
# chapter: 19

def main()
    var items = List(str)()

    # Add items
    items.add("apple")
    items.add("banana")
    items.add("cherry")
    print(items.count())  # 3

    # Access by index
    print(items.at(0))  # "apple"

    # Check contents
    if items.contains("banana")
        print("Found banana")

    # Remove a specific item BY VALUE: `.remove()` takes an index, not a
    # value — List has no indexOf either, so filter() is the idiom for
    # "everything except this value."
    var filtered: List(str) = items.filter(def(x) = x != "banana")
    print(filtered.count())  # 2

    # Iterate over list
    for fruit in filtered
        print("Fruit: ${fruit}")
```

### HashMap Operations

HashMaps store key-value pairs with `.set()` and `.get()` — despite reading
like they should be, `set` and `get` are **not** reserved words in Zebra;
they work fine as ordinary method (or variable) names, and `.set`/`.get`
are the documented HashMap API. (`.put`/`.fetch` also work as aliases on
today's compiler, but aren't in the documented method table — prefer
`.set`/`.get`.)

```zebra
# file: stdlib-hashmap-ops.zbr
# teaches: hashmap operations and patterns
# chapter: 19

def main()
    var scores = HashMap(str, int)()

    # Add key-value pairs
    scores.set("Alice", 95)
    scores.set("Bob", 87)
    scores.set("Charlie", 92)

    # Retrieve value — .get() returns V? (int? here)
    var alice_score = scores.get("Alice")
    if alice_score != nil
        print("Alice scored: ${alice_score}")

    # Check if key exists
    if scores.contains("Bob")
        print("Bob's record found")

    # Update value (overwrites previous)
    scores.set("Bob", 89)

    # Iterate over entries
    for name, score in scores
        print("${name}: ${score}")
```

---

## Math Module

Zebra provides a `Math` module with constants and functions:

### Constants

```zebra
# file: stdlib-math-constants.zbr
# teaches: Math module constants
# chapter: 19

def main()
    print(Math.PI)  # 3.14159...
    print(Math.E)  # 2.71828...
    print(Math.TAU)  # 6.28318... (2 * PI)
    print(Math.INF)  # infinity
    print(Math.NAN)  # not a number
```

### Functions

```zebra
# file: stdlib-math-functions.zbr
# teaches: Math module functions
# chapter: 19

def main()
    # Trigonometry
    print(Math.sin(Math.PI / 2))  # 1.0
    print(Math.cos(0.0))  # 1.0
    print(Math.atan2(1.0, 1.0))  # ~0.785

    # Powers and roots
    print(Math.sqrt(16.0))  # 4.0
    print(Math.pow(2.0, 10.0))  # 1024.0
    print(Math.exp(1.0))  # ~2.718

    # Rounding
    print(Math.floor(3.7))  # 3.0
    print(Math.ceil(3.2))  # 4.0
    print(Math.round(3.5))  # 4.0

    # Logarithms
    print(Math.log(Math.E))  # 1.0
    print(Math.log2(8.0))  # 3.0
    print(Math.log10(100.0))  # 2.0

    # Utilities
    print(Math.abs(-42))  # 42
    print(Math.min(3, 7))  # 3
    print(Math.max(3, 7))  # 7
```

---

## Type Conversions

Zebra's type system is strict — convert between types explicitly:

```zebra
# file: stdlib-type-conversions.zbr
# teaches: converting between types and strings
# chapter: 19

def main()
    # String to int
    var num_str = "42"
    var num = num_str.toInt()
    print(num)  # 42

    # String to float
    var float_str = "3.14"
    var float_val = float_str.toFloat()
    print(float_val)  # 3.14

    # Int to string
    var n = 100
    var s = n.toString()
    print(s)  # "100"

    # Safe conversions with nil checking — toInt() returns a plain int
    # (0 on bad input, not nil), so nil-checking it is a type error.
    # tryInt() is the nil-checkable form.
    var user_input = "not a number"
    var parsed = user_input.tryInt()
    if parsed == nil
        print("Invalid number")
```

---

## System Access

### Command-Line Arguments

Use `sys.args()` for raw access or `Arg.parse()` for structured parsing:

```zebra
# file: stdlib-sys-args.zbr
# teaches: accessing command-line arguments
# chapter: 19

def main()
    # Raw arguments
    var args = sys.args()
    for arg in args
        print(arg)

    # Exit with status code
    if args.count() == 0
        print("No arguments provided")
        sys.exit(1)
```

### Argument Parsing with `Arg`

`Arg.parse()` returns an `ArgResult` with accessor methods — printing the
result directly just dumps its internal representation, so use the
accessors instead:

```zebra
# file: stdlib-arg-parse.zbr
# teaches: structured argument parsing
# chapter: 19

def main()
    var args = Arg.parse()

    # flag() takes BOTH a long and a short form — there's no 1-argument
    # overload, even if you never plan to use the short form.
    var verbose = args.flag("--verbose", "-v")
    var output = args.option("--out", "default.txt")

    var path = args.positional(0)
    if path as p
        # Explicit `str` annotation works around a compiler bug where an
        # inferred string pulled through Arg/positional() prints as its
        # raw byte array instead of text (same bug as sys.cwd() in
        # Chapter 20's File I/O chapter — annotate the type to avoid it).
        var pstr: str = p
        print("path: ${pstr}")
    else
        print("no positional arg")

    print("verbose: ${verbose}")
    print("output: ${output}")
```

| Call | Returns | Notes |
|---|---|---|
| `args.positional(i)` | `str?` | i-th non-flag argument, 0-based |
| `args.flag(long, short)` | `bool` | true if either form is present; **both forms are required arguments** |
| `args.option(name, default)` | `str` | value after `name`, or `default` if absent |
| `args.optionInt(name, default)` | `int` | same, parsed as an integer |
| `args.contains(name)` | `bool` | true if `name` appears anywhere in argv |

---

## JSON

Parse and generate JSON with the `Json` and `JsonValue` modules. `Json.parse`
returns `JsonValue?` — printing it directly dumps the internal tagged-union
representation, so unwrap it and pull out fields with the typed accessors:

```zebra
# file: stdlib-json.zbr
# teaches: JSON parsing and generation
# chapter: 19

def main()
    var text = "{\"name\": \"Alice\", \"age\": 30}"
    var parsed = Json.parse(text)
    if parsed as v
        print(v.getStr("name"))
        print(v.getInt("age"))
    else
        print("invalid JSON")
```

---

## File I/O

Use `File`, `Dir`, and `Path` for file system operations:

```zebra
# file: stdlib-file-io.zbr
# teaches: file system operations
# chapter: 19

def main()
    # File.read/File.write are plain-value calls, not `throws` — they are
    # NOT paired with `catch`. A missing file panics the process, so guard
    # with File.exists() first. See Chapter 20 for the full explanation.
    if File.exists("data.txt")
        var content = File.read("data.txt")
        print(content)
    else
        print("could not read")

    # Write a file
    File.write("output.txt", "Hello from Zebra!")
```

See **Chapter 20** for a deeper dive into file I/O.

---

## Console I/O

```zebra
# file: stdlib-console-io.zbr
# teaches: printing to console
# chapter: 19

def main()
    # Simple output
    print("Hello, World!")

    # String interpolation
    var name = "Alice"
    var age = 30
    print("${name} is ${age} years old")

    # Formatted output
    var price = 19.99
    print("Price: $${price}")
```

---

## Structured Logging

`Log` writes timestamped lines to stderr (or a file you pick) at four
severity levels:

```zebra
def main()
    Log.info("server starting on :8080")
    Log.warn("config key missing — using default")
    # NOTE: the error-level call is `Log.err`, not `Log.error` — `Log.error`
    # both fails to compile if anything follows it (misread by the checker
    # as a noreturn/error-raising call) and isn't implemented in codegen
    # (`Log.error` alone gives "selfhost: unknown Log.error"). QUICKSTART's
    # own table documents `Log.error(msg)`, which is also wrong today.
    Log.err("database connection failed")

    # JSON-lines output for ingestion by log aggregators. `data` is a plain
    # str that gets embedded as the JSON-string value of the "data" field —
    # it is NOT merged in as structured key/value pairs, so pre-format it
    # yourself if you want nested JSON there.
    Log.json("info", "request handled", "method=GET path=/api")

    # Redirect to a file (subsequent calls write there):
    Log.setFile("./out.log")
    Log.info("now writing to a file")
```

| Call | Notes |
|---|---|
| `Log.info(msg)` / `Log.warn(msg)` | Timestamped line; uppercase level prefix |
| `Log.err(msg)` | Same, at error level — **not** `Log.error`, despite QUICKSTART documenting that name |
| `Log.json(level, msg, data)` | One JSON object per line; `data` is a `str`, embedded as the "data" field's string value |
| `Log.setFile(path)` | Redirect all subsequent log output to a file |

For interactive output use `print`; for diagnostic output meant for
operators or log files, use `Log`.

---

## SQL via `Sqlite`

`Sqlite` opens a SQLite database file (or an in-memory database) and
runs queries. The whole module is built on the SQLite C amalgamation
linked into the binary — no separate DB server.

```zebra
def main()
    # Sqlite.open returns SqliteDb? — nil on failure — so unwrap before
    # calling methods on it.
    var db = Sqlite.open("./data.db")!        # or ":memory:" for in-memory
    db.exec("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    db.exec("INSERT INTO users VALUES (1, 'Alice')")
    db.exec("INSERT INTO users VALUES (2, 'Bob')")

    for row in db.query("SELECT id, name FROM users")
        print("${row.asInt("id")}: ${row.asStr("name")}")

    db.close()
```

| Call | Returns | Notes |
|---|---|---|
| `Sqlite.open(path)` | `SqliteDb?` | `nil` on failure — always unwrap/check before use; `:memory:` for in-memory |
| `db.exec(sql)` | `void` | Run a statement without expecting rows |
| `db.query(sql)` | list | Snapshot of rows — `for row in db.query(...)` iterates it |
| `row.asInt(col)` / `asStr(col)` / `asFloat(col)` / `asBool(col)` | typed | Column value at `col` — the **column name**, not an index |
| `db.begin()` / `db.commit()` / `db.rollback()` | `void` | Transaction control |
| `db.close()` | `void` | Release the database handle |

For parameterised queries, build the SQL string explicitly — the API
doesn't yet have prepared statements. Use `Crypto` (below) for any
sensitive values.

---

## Compression: `Compress`

`Compress.gzip` and `gunzip` round-trip gzip. Both actually work on `str`
values, not `List(byte)` — the compressed bytes come back as a `str` (use
`.len`, not `.count()`), and `gunzip` returns `str?` since decompression
can fail on invalid input:

```zebra
def main()
    var src = "the quick brown fox jumps over the lazy dog"
    var compressed = Compress.gzip(src)
    print(compressed.len)  # smaller than src.len for typical input

    var decompressed = Compress.gunzip(compressed)
    if decompressed as d
        # Explicit `str` annotation works around a compiler bug where an
        # unwrapped optional prints as its raw byte array instead of text.
        var dstr: str = d
        print(dstr)  # same as src
    else
        print("gunzip failed")
```

| Call | Returns | Notes |
|---|---|---|
| `Compress.gzip(data)` | `str` | gzip-compress a string; result is raw bytes packed into a `str`, not text |
| `Compress.gunzip(data)` | `str?` | gzip-decompress; `nil` on invalid input |

Useful when reading or writing `.gz` files, or when sending compressed
payloads over the network without depending on the transport's
compression.

---

## Cryptography: `Crypto`

`Crypto` provides authenticated symmetric encryption (AES-256-GCM). It's
the right tool for "encrypt this value so an operator can't read it" —
not for password hashing (use bcrypt/argon2 via FFI) and not for TLS
(use the `Ws` / `Http` modules, which handle TLS themselves).

> **No key-derivation helper.** An earlier build of the compiler added
> `Crypto.deriveKey(password, salt)`, and it's still listed in some
> notes — but calling it today compiles fine under `zebra -c` (the
> checker accepts it) and then fails at full compile with `error:
> selfhost: unknown Crypto.deriveKey` — the code generator never
> learned about it. Until that's fixed, supply your own fixed-length
> key string (from a secrets manager, an environment variable, etc.)
> instead of deriving one from a password.

```zebra
def main()
    var key = "a-fixed-32-byte-demo-key-value!!"
    var ciphertext = Crypto.encrypt(key, "secret message")
    print(ciphertext)  # hex-encoded blob

    var plaintext = Crypto.decrypt(key, ciphertext)
    if plaintext as msg
        print(msg)  # "secret message"
    else
        print("decrypt failed — wrong key or tampered ciphertext")
```

| Call | Returns | Notes |
|---|---|---|
| `Crypto.encrypt(key, plaintext)` | `str` | AES-256-GCM; output is hex-encoded |
| `Crypto.decrypt(key, ciphertext)` | `str?` | `nil` on authentication failure (wrong key or tampered ciphertext) |

Notice the key comes **first** in both calls — some older notes show
`Crypto.encrypt(plaintext, key)` with the arguments reversed, which
compiles (both are `str`) but silently encrypts the wrong value and
then fails to decrypt. Check argument order against the table above.

The `str?` return on `decrypt` is the API's safety mechanism — checking
for `nil` is **mandatory** because that's how you detect a tampered or
forged ciphertext. Don't `!` the result without thinking about it.

---

## Dates with Time Zones: `DateTime.inZone`

The `DateTime` module ships with an embedded IANA timezone table covering
~75 zones. `inZone("Region/City")` is an **instance** method — call it on
a `DateTime` value (such as the one `DateTime.now()` returns), not on the
`DateTime` module itself. `DateTime.inZone(...)` called directly on the
module compiles under `zebra -c` but fails at full compile with `error:
use of undeclared identifier 'DateTime'` — a checker blind spot. There's
also no `toString()` on `DateTime`; printing a value directly dumps its
internal struct, so format it with `toIso8601()` (or `format(pattern)`,
covered in Appendix B) instead:

```zebra
def main()
    var now_utc   = DateTime.now()
    var now_ny    = now_utc.inZone("America/New_York")
    var now_tokyo = now_utc.inZone("Asia/Tokyo")
    var now_syd   = now_utc.inZone("Australia/Sydney")

    print("UTC:    ${now_utc.toIso8601()}")
    print("NY:     ${now_ny.toIso8601()}")
    print("Tokyo:  ${now_tokyo.toIso8601()}")
    print("Sydney: ${now_syd.toIso8601()}")
```

The table includes the major US, EU, AU, and NZ zones plus the typical
international set. DST is handled correctly for the included rule families
(US, EU, AU, NZ).

> **`DateTime.listZones()` is currently broken.** Calling it — as a
> static call, the only form documented — compiles under `zebra -c` but
> fails full compile with `error: unreachable code`. Until that's fixed,
> there's no way to enumerate the embedded zone table at runtime; treat
> the ~75-zone list above as the reference.

---

## Practical Patterns: Data Processing

```zebra
# file: stdlib-data-processing.zbr
# teaches: combining stdlib functions for data processing
# chapter: 19

def main()
    # Parse CSV and calculate statistics
    var data = "Alice,95\nBob,87\nCharlie,92"

    var lines = data.split("\n")
    var scores = HashMap(str, int)()

    for line in lines
        var parts = line.split(",")
        if parts.count() == 2
            var name = parts.at(0)
            # tryInt(), not toInt() — toInt() returns a plain int (0 on bad
            # input), which can't be nil-checked.
            if parts.at(1).tryInt() as score
                scores.set(name, score)

    # Report
    for name, value in scores
        print("${name}: ${value}")
```

---

## Key Takeaways

1. **Know Your Tools** — The standard library covers 80% of common tasks. Check the API before rolling your own.

2. **String Operations** — Master `.split()`, `.join()`, `.contains()`, `.replace()` and type conversions — you'll use them constantly.

3. **Collections** — `List` for sequences, `HashMap` for key-value lookups. Use `.set()` / `.get()` for HashMap access.

4. **Math Module** — `Math.sin()`, `Math.sqrt()`, `Math.PI` etc. — a real module, not just arithmetic operators.

5. **System Access** — `sys.args()` for raw args, `sys.exit()` for process control, `Arg.parse()` for structured CLI parsing.

6. **Read Documentation** — This chapter is a tour, not exhaustive. The full API reference is in **Appendix B**.

---

## Exercises

1. **Word Frequency Counter** — Split a string by spaces, count unique words with a HashMap
2. **Case Converter** — Read user input, convert to upper/lower case based on command-line flag
3. **CSV Validator** — Parse CSV data, ensure all rows have same number of columns, report errors
4. **Math Calculator** — Use `Math.sin`, `Math.cos`, and `Math.sqrt` to compute the distance between two points

---

## What's Next

You now understand what's available in the standard library. Chapter 20 covers extending that capability with file I/O and system access for real-world programs.

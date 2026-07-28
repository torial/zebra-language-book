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
| `Gui` | UI toolkit (Dear ImGui backend) |

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

    # Character access
    var first_char = text.charAt(0)     # 'H'
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

    # Remove specific item
    items.remove("banana")
    print(items.count())  # 2

    # Iterate over list
    for fruit in items
        print("Fruit: ${fruit}")
```

### HashMap Operations

HashMaps store key-value pairs with `.put()` and `.fetch()` (`set` and `get` are reserved keywords):

```zebra
# file: stdlib-hashmap-ops.zbr
# teaches: hashmap operations and patterns
# chapter: 19

def main()
    var scores = HashMap(str, int)()

    # Add key-value pairs
    scores.put("Alice", 95)
    scores.put("Bob", 87)
    scores.put("Charlie", 92)

    # Retrieve value
    var alice_score = scores.fetch("Alice")
    if alice_score != nil
        print("Alice scored: ${alice_score}")

    # Check if key exists
    if scores.contains("Bob")
        print("Bob's record found")

    # Update value (overwrites previous)
    scores.put("Bob", 89)

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

    # Safe conversions with nil checking
    var user_input = "not a number"
    var parsed = user_input.toInt()
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

```zebra
# file: stdlib-arg-parse.zbr
# teaches: structured argument parsing
# chapter: 19

def main()
    var result = Arg.parse()
    # Access parsed flags and positional arguments
    print(result)
```

---

## JSON

Parse and generate JSON with the `Json` and `JsonValue` modules:

```zebra
# file: stdlib-json.zbr
# teaches: JSON parsing and generation
# chapter: 19

def main()
    var text = "{\"name\": \"Alice\", \"age\": 30}"
    var parsed = Json.parse(text)
    print(parsed)
```

---

## File I/O

Use `File`, `Dir`, and `Path` for file system operations:

```zebra
# file: stdlib-file-io.zbr
# teaches: file system operations
# chapter: 19

def main()
    # Read a file
    var content = File.read("data.txt") catch "could not read"
    print(content)

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
    Log.error("database connection failed")

    # JSON-lines output for ingestion by log aggregators:
    Log.json("info", "request handled",
             HashMap(str, str)()
                .set("method", "GET")
                .set("path", "/api"))

    # Redirect to a file (subsequent calls write there):
    Log.setFile("./out.log")
    Log.info("now writing to a file")
```

| Call | Notes |
|---|---|
| `Log.info(msg)` / `Log.warn(msg)` / `Log.error(msg)` | Timestamped line; uppercase level prefix |
| `Log.json(level, msg, data)` | One JSON object per line; `data` is `HashMap(str, str)` |
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
    var db = Sqlite.open("./data.db")        # or ":memory:" for in-memory
    db.exec("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    db.exec("INSERT INTO users VALUES (1, 'Alice')")
    db.exec("INSERT INTO users VALUES (2, 'Bob')")

    for row in db.query("SELECT id, name FROM users")
        print("${row.asInt(0)}: ${row.asStr(1)}")

    db.close()
```

| Call | Returns | Notes |
|---|---|---|
| `Sqlite.open(path)` | `Sqlite` | Opens the file (creates if missing); `:memory:` for in-memory |
| `db.exec(sql)` | `void` | Run a statement without expecting rows |
| `db.query(sql)` | iterator | Yields one `row` at a time |
| `row.asInt(col)` / `asStr(col)` / `asFloat(col)` / `asBool(col)` | typed | Column value at `col` (zero-based) |
| `db.begin()` / `db.commit()` / `db.rollback()` | `void` | Transaction control |
| `db.close()` | `void` | Release the database handle |

For parameterised queries, build the SQL string explicitly — the API
doesn't yet have prepared statements. Use `Crypto` (below) for any
sensitive values.

---

## Compression: `Compress`

`Compress.gzip` and `gunzip` round-trip gzip:

```zebra
def main()
    var src = "the quick brown fox jumps over the lazy dog"
    var compressed = Compress.gzip(src)
    print(compressed.count())  # smaller than src.len for typical input

    var decompressed = Compress.gunzip(compressed)
    print(decompressed)  # same as src
```

| Call | Returns | Notes |
|---|---|---|
| `Compress.gzip(data)` | `List(byte)` | gzip-compress a string |
| `Compress.gunzip(data)` | `List(byte)` | gzip-decompress a `List(byte)` |

Useful when reading or writing `.gz` files, or when sending compressed
payloads over the network without depending on the transport's
compression.

---

## Cryptography: `Crypto`

`Crypto` provides authenticated symmetric encryption (AES-256-GCM) and a
key-derivation helper (HKDF-SHA256). It's the right tool for "encrypt
this value so an operator can't read it" — not for password hashing
(use bcrypt/argon2 via FFI) and not for TLS (use the `Ws` / `Http`
modules, which handle TLS themselves).

```zebra
def main()
    var key = Crypto.deriveKey("user-password", "fixed-salt-bytes")
    var ciphertext = Crypto.encrypt("secret message", key)
    print(ciphertext)  # base64-encoded blob

    var plaintext = Crypto.decrypt(ciphertext, key)
    if plaintext as msg
        print(msg)  # "secret message"
    else
        print("decrypt failed — wrong key or tampered ciphertext")
```

| Call | Returns | Notes |
|---|---|---|
| `Crypto.encrypt(plaintext, key)` | `str` | AES-256-GCM; output is base64-encoded |
| `Crypto.decrypt(ciphertext, key)` | `str?` | `nil` on authentication failure (wrong key or tampered ciphertext) |
| `Crypto.deriveKey(password, salt)` | `str` | HKDF-SHA256; 32-byte hex output suitable as a key |

The `str?` return on `decrypt` is the API's safety mechanism — checking
for `nil` is **mandatory** because that's how you detect a tampered or
forged ciphertext. Don't `!` the result without thinking about it.

---

## Dates with Time Zones: `DateTime.inZone`

The `DateTime` module ships with an embedded IANA timezone table covering
~75 zones. `DateTime.inZone("Region/City")` returns a calendar view of
the current instant in that zone:

```zebra
def main()
    var now_utc   = DateTime.now()
    var now_ny    = DateTime.inZone("America/New_York")
    var now_tokyo = DateTime.inZone("Asia/Tokyo")
    var now_syd   = DateTime.inZone("Australia/Sydney")

    print("UTC:    ${now_utc.toString()}")
    print("NY:     ${now_ny.toString()}")
    print("Tokyo:  ${now_tokyo.toString()}")
    print("Sydney: ${now_syd.toString()}")
```

The table includes the major US, EU, AU, and NZ zones plus the typical
international set. DST is handled correctly for the included rule families
(US, EU, AU, NZ). For an exhaustive zone list, run
`DateTime.listZones()`.

> **Binary size note.** The IANA table is included in the binary only
> if your program references `DateTime.inZone` or `listZones`. Programs
> that use `DateTime.now()` alone don't pay the ~50 KB cost.

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
            var score = parts.at(1).toInt()
            if score != nil
                scores.put(name, score)

    # Report
    for name, value in scores
        print("${name}: ${value}")
```

---

## Key Takeaways

1. **Know Your Tools** — The standard library covers 80% of common tasks. Check the API before rolling your own.

2. **String Operations** — Master `.split()`, `.join()`, `.contains()`, `.replace()` and type conversions — you'll use them constantly.

3. **Collections** — `List` for sequences, `HashMap` for key-value lookups. Use `.put()` / `.fetch()` for HashMap access (`set` and `get` are reserved keywords).

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

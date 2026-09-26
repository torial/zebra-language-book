# Appendix B: Standard Library Reference

API reference for Zebra's built-in functions and standard library.  For
detailed usage examples, see Chapter 19 (Standard Library Tour).

> **Status note (2026-04-29):** This appendix predates the 0.10 batteries
> rollout (Hash, Random, Arg, Terminal, Log, Uri, Compress, Mime, Timer)
> and the 0.9 reflection additions (`Reflect.*`, `@reflectable`,
> `Json.parseStrict`).  For coverage of the modules below *plus* the more
> recent ones, see **QUICKSTART §31** in the language repo
> (`zebra-language/QUICKSTART.md`) — it's the canonical agent-facing
> reference and is kept current.  The sections below will be expanded
> in a future pass.

---

## Console I/O

### Output Functions

```zebra
print(value)                # Output without newline
print(value)  # Output with newline
sys.errln(message)       # Error output to stderr
```

**Example:**
```zebra
print("Hello, World!")
print("Loading")
print(".")
print(" done")
```

---

## String Methods

All string methods are called on string values:

```zebra
var text = "Hello, World!"
```

### Properties

```zebra
text.len                    # Length of string (int)
```

### Case Conversion

```zebra
text.upper()                # Convert to UPPERCASE
text.lower()                # Convert to lowercase
```

### Searching

```zebra
text.contains(substring)    # bool: contains substring?
text.startsWith(prefix)     # bool: starts with prefix?
text.endsWith(suffix)       # bool: ends with suffix?
text.indexOf(substring)     # int: position of substring (-1 if not found)
text.lastIndexOf(substring) # int: position of last occurrence
```

**Example:**
```zebra
if text.contains("World")
    var pos = text.indexOf("World")
    print("Found at ${pos}")
```

### Manipulation

```zebra
text.substring(start, end)  # str: extract portion [start, end)
text.charAt(index)          # char: character at index
text.split(delimiter)       # List(str): split by delimiter
text.replace(old, new)      # str: replace first occurrence
text.replaceAll(old, new)   # str: replace all occurrences
text.trim()                 # str: remove leading/trailing whitespace
text.trimLeft()             # str: remove leading whitespace
text.trimRight()            # str: remove trailing whitespace
text.concat(other)          # str: concatenate strings
text.reverse()              # str: reverse string
```

**Example:**
```zebra
var parts = "a,b,c".split(",")
var clean = "  hello  ".trim()
var replaced = "hello world".replace("world", "zebra")
```

### Type Conversion

```zebra
text.toInt()                # int?: convert to integer (nil if invalid)
text.toFloat()              # float?: convert to float (nil if invalid)
```

**Example:**
```zebra
var num = "42".toInt()
if num != nil
    print(num + 1)
```

---

## List Methods

Create a list:
```zebra
var items = List(int)()          # the element type is part of the constructor
```

### Basic Operations

```zebra
items.add(element)          # Add element to end
items.remove(element)       # Remove specific element
items.clear()               # Remove all elements
items.count()               # int: number of elements
items.at(index)             # ElementType: element at index
items.contains(element)     # bool: contains element?
items.indexOf(element)      # int: position (-1 if not found)
```

**Example:**
```zebra
var numbers = List(int)()
numbers.add(1)
numbers.add(2)
numbers.add(3)
print(numbers.count())  # 3
print(numbers.at(0))  # 1
```

### Iteration

```zebra
for item in items
    print(item)
```

---

## HashMap Methods

Create a HashMap:
```zebra
var map = HashMap(str, int)()     # key and value types are part of the constructor
```

### Basic Operations

```zebra
map.put(key, value)         # Add or update key-value pair
map.fetch(key)              # ValueType?: get value (nil if key not found)
map.contains(key)           # bool: key exists?
map.remove(key)             # Remove key
map.clear()                 # Remove all entries
```

Note: `set` and `get` are reserved keywords in Zebra, so HashMap uses `put` and `fetch` instead.

### Iteration

```zebra
for key, value in map       # Iterate over key-value pairs
    print("${key}: ${value}")
```

**Example:**
```zebra
var scores = HashMap(str, int)()
scores.put("Alice", 95)
scores.put("Bob", 87)

if scores.contains("Alice")
    var score = scores.fetch("Alice")  # 95
    if score != nil
        print("Alice: ${score}")
```

---

## Deduplication Pattern (via HashMap)

Use HashMap keys for unique-value tracking:

```zebra
var seen: HashMap(str, bool) = HashMap()
seen.put("red", true)
seen.put("blue", true)
seen.put("red", true)       # Overwrites, same effect as no-op
print(seen.count())  # 2
```

---

## Numeric Methods

### Int Methods

```zebra
var n = 42

n.toString()                # str: convert to string
n.toFloat()                 # float: convert to floating-point

# Range generation
n.to(end)                   # List(int): numbers from n to end-1
# Example: 1.to(5) gives [1, 2, 3, 4]
```

**Example:**
```zebra
for i in 0.to(10)
    print(i)

var str = 42.toString()     # "42"
```

### Float Methods

```zebra
var x = 3.14

x.toString()                # str: convert to string
x.toInt()                   # int: truncate to integer
```

---

## Type Conversion Functions

### Standalone Conversions

```zebra
int_to_str(n)               # str: int to string
str_to_int(s)               # int?: string to int
float_to_str(f)             # str: float to string
str_to_float(s)             # float?: string to float
```

**Example:**
```zebra
var n = str_to_int("42")
if n != nil
    print(n)
```

---

## Math Functions

### Basic Arithmetic

```zebra
# Operators (not functions)
a + b                       # Addition
a - b                       # Subtraction
a * b                       # Multiplication
a / b                       # Integer or float division
a % b                       # Modulo (remainder)
```

### Comparison

```zebra
a < b                       # Less than
a > b                       # Greater than
a <= b                      # Less than or equal
a >= b                      # Greater than or equal
a == b                      # Equal
a != b                       # Not equal
```

### Logical

```zebra
a and b                     # Logical AND
a or b                      # Logical OR
not a                       # Logical NOT
```

---

## System Module

```zebra
sys.args()               # List(str): command-line arguments
sys.env(name)            # str?: get environment variable (nil if not set)
sys.cwd()                # str: current working directory
sys.exit(code)           # Exit program with code
sys.errln(message)       # Print to standard error
```

**Example:**
```zebra
var args = sys.args()
for arg in args
    print("Argument: ${arg}")

var home = sys.env("HOME")
if home != nil
    print("Home: ${home}")

print("Current directory")
```

---

## File I/O

```zebra
File.read(filename)         # str: read entire file (a missing file stops the program)
File.write(filename, content)  # write file (creates or truncates); returns nothing
File.exists(path)           # bool: file exists?
File.delete(path)           # delete file (a no-op if it is missing)
```

None of these is `throws` and none returns a `Result` (Zebra has no `Result`
type): guard a read with `File.exists`.

**Example:**
```zebra
if File.exists("data.txt")
    var content = File.read("data.txt")
    print(content)
else
    print("Error: data.txt not found")

File.write("output.txt", "Hello")
```

---

## Regular Expressions

```zebra
Regex.compile(pattern)      # Regex: compile pattern
```

**Methods on Regex:**

```zebra
var pattern = Regex.compile("\\d+")

pattern.matches(text)       # bool: does text match pattern exactly?
pattern.find(text)          # str?: find first match
pattern.findAll(text)       # List(str): find all matches
pattern.replace(text, replacement)      # str: replace first match
pattern.replaceAll(text, replacement)   # str: replace all matches
pattern.split(text)         # List(str): split by matches
```

**Example:**
```zebra
var email_pattern = Regex.compile("[a-z0-9]+@[a-z]+\\.[a-z]+")

if email_pattern.matches("user@example.com")
    print("Valid email")

var numbers = Regex.compile("\\d+")
var matches = numbers.findAll("abc 123 def 456")
# matches = ["123", "456"]
```

---

## Error Handling

Zebra uses `throws`/`raise`/`catch` for error handling.

**Declare a fallible function:**
```zebra
def divide(a: int, b: int): int throws
    if b == 0
        raise "Division by zero"
    return a / b
```

**Handle errors — three forms:**
```zebra
# 1. Catch expression (inline fallback)
var value = divide(10, 0) catch 0

# 2. Explicit propagation — every call to a `throws` function needs a `?`,
#    even in the same file; it re-raises to the caller, which must itself
#    be `throws`
def caller(): int throws
    var r = divide(10, 2)?
    return r

# 3. Method-level catch — a `catch` clause attached to a `def` at the same
#    indent, running when any `throws` call in the body raises; `e.message`
#    reads the error text
def risky()
    var v = divide(10, 0)
    print(v)
catch |e|
    print("Error: ${e.message}")
```

> There is no `try`/`catch` block form — `try` as a prefix keyword was
> removed. Use `expr?` to propagate or one of the two `catch` forms above.

---

## String Interpolation

Embed expressions in strings using `${}`:

```zebra
var name = "Alice"
var age = 30
print("${name} is ${age} years old")
print("Sum: ${10 + 5}")
print("Upper: ${"hello".upper(}"))
```

---

## Collections Initialization

### List

```zebra
var items = List(int)()        # Empty list
```

To initialize with values, add them after creation.

### HashMap

```zebra
var map = HashMap(str, int)()  # Empty map
```

---

## Common Type Methods

### All Types

```zebra
value.toString()            # str: convert to string representation
```

### Nullable Types (T?)

```zebra
var x: int? = 42

if x != nil
    # Safe to use x as int here
    print(x)
```

---

## Testing Utilities (if available)

```zebra
assert condition, "message"     # Assert that condition is true
```

**Example:**
```zebra
assert x > 0, "x must be positive"
assert items.count() == 3, "Expected 3 items"
```

---

## Pattern Matching

### Branch Expression

```zebra
var value: int? = 42

branch value
    on nil
        print("Value is nil")
    on _
        print("Value is ${value}")
```

### Result Pattern Matching

```zebra
var result = operation()

branch result
    on ok(value)
        print("Success: ${value}")
    on err(error)
        print("Error: ${error}")
```

---

## Common Patterns

### Safe Null Checking

```zebra
var x: int? = nil

if x != nil
    print(x + 1)
else
    print("x is nil")
```

### Error Handling

```zebra
def load(path: str): str throws
    if not File.exists(path)
        raise "not found: ${path}"
    return File.read(path)

def show(path: str)
    var content = load(path)
    print(content)
catch |err|
    print("Error: ${err.message}")
```

### Iteration

```zebra
var items = List(int)()
items.add(1)
items.add(2)

for item in items
    print(item)
```

### Type Conversion

```zebra
var num_str = "42"
var num = num_str.tryInt()      # int? -- nil if the text is not a number

if num != nil
    print(num + 1)
```

---

## Important Notes

1. **Nullable Return Values** — Many functions return nullable types (e.g., `str?`, `int?`). Check with `if x != nil` before using.

2. **No Result Types** — Operations that can fail are `throws` functions: handle them with `expr catch fallback` or a method-level `catch`. File I/O is not `throws`; check `File.exists` first.

3. **Collection Methods Return Nullable** — `HashMap.fetch()` returns `V?` (nullable value), not `V`.

4. **String Immutability** — Strings are immutable. Use `StringBuilder` for efficient string building in loops.

5. **Type Inference** — Most types can be inferred, but explicit types are recommended for clarity.

---

## Performance Tips

1. **StringBuilder for Loops** — Don't concatenate strings in loops. Use `StringBuilder` or build a `List(str)` and join.

2. **Batch File Operations** — Read entire file once, not line-by-line (unless memory-constrained).

3. **HashMap for Lookups** — O(1) lookup beats O(n) list search.

4. **Set for Uniqueness** — Set deduplication is O(1) per element, not O(n).

---

## Standard Library Organization

The standard library is organized by functionality:

| Module | Purpose | Chapter Reference |
|--------|---------|-------------------|
| String | String operations | Chapter 06, 19 |
| Collection | List, HashMap, Set | Chapter 03, 19 |
| Result | Error handling | Chapter 12, 19 |
| File | File I/O | Chapter 20 |
| Regex | Pattern matching | Chapter 21 |
| System | Environment, arguments | Chapter 19, 20 |
| Math | Numeric operations | Chapter 19 |

For more details and examples, consult the main chapters referenced above.

# Appendix B: Standard Library Reference

Complete API reference for Zebra's built-in functions and standard library. For detailed usage examples, see Chapter 19 (Standard Library Tour).

---

## Console I/O

### Output Functions

```zebra
print(value)                # Output without newline
println(value)              # Output with newline
System.errln(message)       # Error output to stderr
```

**Example:**
```zebra
println("Hello, World!")
print("Loading")
print(".")
println(" done")
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
    println("Found at ${pos}")
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
    println(num + 1)
```

---

## List Methods

Create a list:
```zebra
var items = List()
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
var numbers = List()
numbers.add(1)
numbers.add(2)
numbers.add(3)
println(numbers.count())    # 3
println(numbers.at(0))      # 1
```

### Iteration

```zebra
for item in items
    println(item)
```

---

## HashMap Methods

Create a HashMap:
```zebra
var map = HashMap()
```

### Basic Operations

```zebra
map.put(key, value)         # Add or update key-value pair
map.fetch(key)              # ValueType?: get value (nil if key not found)
map.contains(key)           # bool: key exists?
map.remove(key)             # Remove key
map.clear()                 # Remove all entries
```

### Iteration

```zebra
map.keys()                  # List(KeyType): all keys
map.values()                # List(ValueType): all values
```

**Example:**
```zebra
var scores = HashMap()
scores.put("Alice", 95)
scores.put("Bob", 87)

if scores.contains("Alice")
    var score = scores.fetch("Alice")  # 95
    if score != nil
        println("Alice: ${score}")
```

---

## Set Methods

Create a Set:
```zebra
var unique = Set()
```

### Basic Operations

```zebra
unique.add(element)         # Add element (no-op if already exists)
unique.remove(element)      # Remove element
unique.contains(element)    # bool: element exists?
unique.clear()              # Remove all elements
```

### Iteration

```zebra
for item in unique
    println(item)
```

**Example:**
```zebra
var colors = Set()
colors.add("red")
colors.add("blue")
colors.add("red")           # No-op, already exists
println(colors.count())     # 2, not 3
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
    println(i)

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
    println(n)
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
System.args()               # List(str): command-line arguments
System.env(name)            # str?: get environment variable (nil if not set)
System.cwd()                # str: current working directory
System.exit(code)           # Exit program with code
System.errln(message)       # Print to standard error
```

**Example:**
```zebra
var args = System.args()
for arg in args
    println("Argument: ${arg}")

var home = System.env("HOME")
if home != nil
    println("Home: ${home}")

println("Current: ${System.cwd()}")
```

---

## File I/O

```zebra
File.read(filename)         # Result(str, str): read entire file
File.write(filename, content)  # Result(bool, str): write file
File.exists(path)           # bool: file exists?
File.delete(path)           # Result(bool, str): delete file
```

**Example:**
```zebra
var result = File.read("data.txt")

if result.isOk()
    var content = result.value()
    println(content)
else
    println("Error: ${result.error()}")

var write_result = File.write("output.txt", "Hello")
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
    println("Valid email")

var numbers = Regex.compile("\\d+")
var matches = numbers.findAll("abc 123 def 456")
# matches = ["123", "456"]
```

---

## Result Type

The `Result(T, E)` type is used for error handling.

```zebra
Result.ok(value)            # Create success result
Result.err(error)           # Create error result
```

**Methods on Result:**

```zebra
var result as Result(int, str) = Result.ok(42)

result.isOk()               # bool: is success?
result.isErr()              # bool: is error?
result.value()              # T: get success value (unsafe if error!)
result.error()              # E: get error value (unsafe if success!)
result.unwrapOr(default)    # T: get value or default if error
```

**Example:**
```zebra
var result = divide(10, 2)

if result.isOk()
    var value = result.value()
    println(value)
else
    println("Error: ${result.error()}")

# Using unwrapOr
var value = result.unwrapOr(0)
```

---

## String Interpolation

Embed expressions in strings using `${}`:

```zebra
var name = "Alice"
var age = 30
println("${name} is ${age} years old")
println("Sum: ${10 + 5}")
println("Upper: ${"hello".upper()}")
```

---

## Collections Initialization

### List

```zebra
var items = List()             # Empty list
```

To initialize with values, add them after creation.

### HashMap

```zebra
var map = HashMap()       # Empty map
```

### Set

```zebra
var unique = Set()             # Empty set
```

---

## Common Type Methods

### All Types

```zebra
value.toString()            # str: convert to string representation
```

### Nullable Types (T?)

```zebra
var x as int? = 42

if x != nil
    # Safe to use x as int here
    println(x)
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
var value as int? = 42

branch value
    on nil
        println("Value is nil")
    on _
        println("Value is ${value}")
```

### Result Pattern Matching

```zebra
var result = operation()

branch result
    on ok(value)
        println("Success: ${value}")
    on err(error)
        println("Error: ${error}")
```

---

## Common Patterns

### Safe Null Checking

```zebra
var x as int? = nil

if x != nil
    println(x + 1)
else
    println("x is nil")
```

### Error Handling

```zebra
var result = File.read("file.txt")

if result.isErr()
    println("Error: ${result.error()}")
    return
    
var content = result.value()
```

### Iteration

```zebra
var items = List()
items.add(1)
items.add(2)

for item in items
    println(item)
```

### Type Conversion

```zebra
var num_str = "42"
var num = num_str.toInt()

if num != nil
    println(num + 1)
```

---

## Important Notes

1. **Nullable Return Values** — Many functions return nullable types (e.g., `str?`, `int?`). Check with `if x != nil` before using.

2. **Result Types** — File I/O and other operations return `Result(T, E)`. Check with `.isOk()` or `.isErr()`.

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

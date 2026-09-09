# Appendix A: Grammar Reference

This appendix is a quick reference for Zebra's syntax. For detailed explanations, refer to the chapter listed for each feature.

---

## Basic Types

### Primitive Types

```zebra
var x: int = 42           # 64-bit integer
var y: float = 3.14       # 64-bit floating point
var b: bool = true        # Boolean
var s: str = "hello"      # Immutable string
var c: char = 'x'         # Single character
```

**References:** Chapter 02 (Values and Types)

### Nullable Types

```zebra
var x: int? = nil         # Can be int or nil
var s: str? = "hello"     # Can be string or nil

if x != nil
    print(x)  # Safe to use x here
```

**References:** Chapter 11 (Nil Tracking and Safety)

### Collection Types

```zebra
var numbers: List(int) = List()
var mapping: HashMap(str, int) = HashMap()

numbers.add(1)
mapping.set("key", 42)
```

**References:** Chapter 03 (Collections)

### Error Handling

```zebra
def parse(text: str): int throws
    if text.len == 0
        raise "Empty input"
    return 42

var value = parse("hello") catch 0

# Multi-statement handling uses a method-level catch clause. The
# caught value's text is `.message` — interpolating it directly
# (`${err}`) fails with `use of undeclared identifier 'err'`.
def attempt()
    var v = parse("")
    print(v)
catch |err|
    print("Error: ${err.message}")
```

**References:** Chapter 12 (Error Handling)

---

## Functions

### Basic Function Definition

```zebra
def greet(name: str): str
    return "Hello, ${name}"

var message = greet("Alice")
```

**References:** Chapter 04 (Functions and Scope)

### Functions with Multiple Parameters

```zebra
def add(a: int, b: int): int
    return a + b

var sum = add(3, 4)
```

### Functions with Optional Parameters

```zebra
def calculate(a: int, b: int, operation: str): int
    if operation == "add"
        return a + b
    else
        return a - b
```

### Returning Multiple Values (via Structure)

```zebra
class Result
    var value: int
    var success: bool

def divide(a: int, b: int): Result
    var result = Result()
    if b != 0
        result.value = a / b
        result.success = true
    else
        result.success = false
    return result
```

---

## Classes

### Basic Class Definition

The constructor keyword is `cue init`, not `def init` — a plain `def
init` collides with the class's auto-generated default constructor and
fails full compile with `error: duplicate struct member name 'init'`
(it passes `zebra -c`, so this one is a checker blind spot):

```zebra
class Person
    var name: str = ""
    var age: int = 0
    
    cue init(name: str, age: int)
        this.name = name
        this.age = age
    
    def describe(): str
        return "${name} is ${age} years old"

var person = Person("Alice", 30)
print(person.describe())
```

**References:** Chapter 07 (Classes and Instances)

### Class with Shared Methods

```zebra
class Math
    static
        def add(a: int, b: int): int
            return a + b

var result = Math.add(2, 3)
```

**References:** Chapter 07 (Classes and Instances)

### Class with Properties

```zebra
class Circle
    var radius: float = 0.0
    
    def area(): float
        return 3.14159 * radius * radius
```

**References:** Chapter 10 (Properties and Computed Values)

### Inheritance

```zebra
interface Animal
    def speak(): str

class Dog implements Animal
    var name: str = ""
    
    def speak(): str
        return "Woof!"

var dog = Dog()
dog.name = "Buddy"
print(dog.speak())  # "Woof!"
```

**References:** Chapter 08 (Interfaces and Protocols)

---

## Interfaces

### Basic Interface Definition

```zebra
interface Shape
    def area(): float
    def perimeter(): float

class Circle implements Shape
    var radius: float = 0.0
    
    def area(): float
        return 3.14159 * radius * radius
    
    def perimeter(): float
        return 2.0 * 3.14159 * radius
```

**References:** Chapter 08 (Interfaces and Protocols)

---

## Control Flow

### If/Else If/Else

There is no `elif` keyword — the middle branch is `else if`:

```zebra
if x > 10
    print("Large")
else if x > 5
    print("Medium")
else
    print("Small")
```

**References:** Chapter 05 (Control Flow)

### While Loop

```zebra
var i = 0
while i < 10
    print(i)
    i = i + 1
```

**References:** Chapter 05 (Control Flow)

### For Loop

```zebra
for item in collection
    print(item)

for i in 0.to(10)
    print(i)  # 0, 1, 2, ..., 9
```

**References:** Chapter 05 (Control Flow)

### Break and Continue

```zebra
var i = 0
while i < 10
    if i == 5
        break            # Exit loop immediately
    
    if i == 2
        i = i + 1
        continue         # Skip to next iteration
    
    print(i)
    i = i + 1
```

**References:** Chapter 05 (Control Flow)

### Branch (Pattern Matching)

`branch` pattern-matches on **union variants** (or struct field
patterns) — it isn't a nil-check dispatcher. `branch` on a plain `T?`
with `on nil` fails full compile with `error: switch on type '?i64'`;
use `if x != nil` / `if x as n` (Nil Safety, above) for optionals
instead:

```zebra
union Shape
    circle: float
    square: float

var s = Shape.circle(5.0)

branch s
    on Shape.circle as r
        print("circle with radius ${r}")
    on Shape.square as side
        print("square with side ${side}")
```

### Error Handling

```zebra
def load(path: str): str throws
    if path.len == 0
        raise "Empty path"
    return "data"

# Inline postfix catch expression
var data = load("") catch "default"

# Method-level catch clause (attaches to a def) — the caught value's
# text is `.message`; interpolating `err` directly is a compile error.
def attempt()
    var d = load("")
    print(d)
catch |err|
    print("Error: ${err.message}")
```

**References:** Chapter 12 (Error Handling)

---

## Operators

### Arithmetic

```zebra
10 + 5          # Addition
10 - 5          # Subtraction
10 * 5          # Multiplication
10 / 5          # Integer division (or float division with floats)
10 % 3          # Modulo (remainder)
```

### Comparison

```zebra
10 > 5          # Greater than
10 < 5          # Less than
10 >= 5         # Greater than or equal
10 <= 5         # Less than or equal
10 == 5         # Equal
10 != 5         # Not equal
```

### Logical

```zebra
true and false      # Logical AND
true or false       # Logical OR
not true            # Logical NOT
```

### String Concatenation

```zebra
"hello" + " " + "world"        # Concatenation
"${variable} text"             # Interpolation
```

**References:** Chapter 06 (Strings and Unicode)

### Assignment

```zebra
var x = 10              # Simple assignment
x = x + 5               # Update
```

There's no comma-separated multi-declaration form (`var x = 10, y = 20`
is a parse error) — declare each variable on its own line.

### Pipelines

The right-hand side of `->` must be a call expression — `a -> f()` passes
`a` as `f`'s first argument. A bare function name (`a -> f`) or a
leading-dot method chain (`a -> .trim()`) both fail at compile time:

```zebra
def double(x: int): int
    return x * 2

var result = 5 -> double()   # same as double(5)
```

**References:** Chapter 15 (Pipelines and Function Composition)

---

## Comments

```zebra
# Single-line comment

# Multi-line comments use multiple # lines
# Like this example here
```

---

## Variables and Scope

### Variable Declaration

```zebra
var x = 42                  # Local variable, inferred type
var x: int = 42          # Local variable, explicit type
```

(As above, there's no comma-separated multi-declaration form — each
`var` declares exactly one name.)

### Scope

```zebra
def example()
    var x = 10
    
    if true
        var y = 20         # y is only visible here
        print(x)  # x is visible (outer scope)
        print(y)  # y is visible
    
    print(x)  # x is visible
    # print y           # ERROR: y is out of scope
```

**References:** Chapter 04 (Functions and Scope)

---

## Generics

### Generic Functions

Zebra's generics are documented — and actually implemented — on
**classes only**. A free-standing top-level `def` that references an
unbound type parameter like `T` compiles under `zebra -c`, but fails
full compile with `error: use of undeclared identifier 'T'`, because
nothing ever binds `T` to a concrete type outside of a `class(T)`
declaration:

```zebra
# NOT SUPPORTED — fails full compile: T is never bound to a type.
# def first(items: List(T)): T?
#     if items.count() > 0
#         return items.at(0)
#     return nil
```

To get the same behavior, put the function on a generic class instead
(see Generic Classes, below) or write one non-generic version per
concrete type you need.

**References:** Chapter 13 (Generics and Type Constraints)

### Generic Classes

```zebra
class Box(T)
    var item: T?
    
    def store(item: T)
        this.item = item
    
    def fetch(): T?
        return this.item

var box = Box(str)()
box.store("Hello")
var value = box.fetch()  # Type is str?
```

**References:** Chapter 13 (Generics and Type Constraints)

### Type Constraints

Constraints are written on the type parameter itself — `T where T
implements InterfaceName` — not as a trailing clause on a `def`, and
there's no `T where T can be X` shorthand:

```zebra
class SortedBox(T where T implements Comparable)
    var item: T?

    def store(item: T)
        this.item = item
```

**References:** Chapter 13 (Generics and Type Constraints)

---

## Error Handling

### Fallible Functions

```zebra
def divide(a: int, b: int): int throws
    if b == 0
        raise "Division by zero"
    return a / b
```

### Catch Expression

There's no inline `catch |e| expr` binding form — a bound `catch |e|`
only exists as the method-level clause below, and it must actually use
`e` (an unused capture is a compile error):

```zebra
# Inline fallback
var value = divide(10, 0) catch 0

# Explicit propagation instead
def caller(): int throws
    return divide(10, 0)?
```

### Method-Level Catch Clause

```zebra
def attempt()
    var value = divide(10, 0)
    print(value)
catch |err|
    print("Error: ${err.message}")

# The `try expr` prefix form and `try ... catch ...` block form were removed
# in 0.15. Use `expr?` for inline propagation, or attach `catch` to a `def`.
```

**References:** Chapter 12 (Error Handling)

---

## Nil Safety

### Null Checking

```zebra
var x: int? = nil

if x != nil
    # Safe to use x as int here
    print(x + 1)

if x == nil
    print("x is nil")
```

### Safe Navigation

```zebra
var x: int? = 42

if x != nil
    var doubled = x * 2  # Safe because x is checked
```

**References:** Chapter 11 (Nil Tracking and Safety)

---

## String Operations

### String Properties

```zebra
var text = "Hello"

text.len            # Length
text.upper()        # Uppercase
text.lower()        # Lowercase
text.trim()         # Remove whitespace
text.contains("ll") # Check substring
```

### String Searching

```zebra
text.indexOf("ll")              # Find position of substring
text.startsWith("He")           # Check prefix
text.endsWith("o")              # Check suffix
```

### String Manipulation

```zebra
text.split(",")                 # Split by delimiter
text.replace("o", "a")          # Replace all occurrences
text.substring(0, 5)            # Extract portion
text.charAt(0)                  # Byte at position (returns `byte`, not `str`)
```

**References:** Chapter 06 (Strings and Unicode), Chapter 19 (Standard Library)

---

## Collections

### List Operations

A bare `List()` with no type argument and no annotated `var` type
compiles under `zebra -c` but fails full compile — give it a type
argument. `.remove()` takes an **index**, not a value — there's no
remove-by-value; filter it out instead:

```zebra
var items: List(str) = List()

items.add("apple")              # Add item
items = items.filter(def(x) = x != "apple")  # Remove by value
items.count()                   # Count items
items.at(0)                     # Get item at index
items.contains("apple")         # Check membership
items.clear()                   # Remove all items

for item in items
    print(item)  # Iterate
```

### HashMap Operations

There's no `.put()` or `.fetch()` — the real accessor names are
`.set()` and `.get()`:

```zebra
var map = HashMap(str, int)()

map.set("a", 1)                 # Add/update
map.get("a")                    # Get value (returns nullable)
map.contains("a")               # Check key exists
map.remove("a")                 # Remove key

for key, value in map
    print("${key} => ${value}")
```

### Deduplication (via HashMap)

```zebra
var seen: HashMap(str, bool) = HashMap()

seen.set("apple", true)         # Track item
seen.contains("apple")          # Check membership

for key, _ in seen
    print(key)  # Iterate unique items
```

**References:** Chapter 03 (Collections)

---

## Type Conversion

```zebra
# String to int — toInt() returns a PLAIN int (0 on bad input), not
# int?. Comparing it to `nil` compiles under `zebra -c` but fails full
# compile with `error: comparison of 'i64' with null`. Use tryInt()
# for a real int? you can nil-check.
var num = "42".tryInt()         # int?

# String to float — same story: toFloat() is plain float, tryFloat() is float?
var decimal = "3.14".tryFloat() # float?

# Int to string
var str = 42.toString()         # str

# Float to string
var str = 3.14.toString()       # str

# Boolean to string
var str = true.toString()       # "true"
```

**References:** Chapter 19 (Standard Library Tour)

---

## Advanced Features

### Contracts

`require` is a block keyword, not an inline statement — the condition(s)
go on their own indented line(s) beneath it, one expression per line, with
no custom message argument:

```zebra
def divide(a: int, b: int): int
    require
        b != 0
    return a / b
```

**References:** Chapter 14 (Contracts and Assertions)

### Assertions

```zebra
assert x > 0, "x must be positive"
```

**References:** Chapter 14 (Contracts and Assertions)

### Mixins

Mixins are pulled in with `adds`, not `implements` — `implements` is
for interfaces. `class Person implements Serializable` compiles under
`zebra -c` but fails full compile with `error: use of undeclared
identifier 'Serializable'`:

```zebra
mixin Serializable
    def to_json(): str
        return "{}"

class Person adds Serializable
    var name: str = ""
```

**References:** Chapter 09 (Composition and Mixins)

---

## Module and Namespace

### Importing

```zebra
use MathUtils
use ast exposing Stmt, Expr, TypeRef

# Access module functionality
var args = sys.args()
```

### Defining Namespaces

```zebra
namespace MyApp.Utils
    def helper_function(): str
        return "Helper"
```

---

## Special Keywords

| Keyword | Purpose | Reference |
|---------|---------|-----------|
| `var` | Declare variable | Chapter 04 |
| `def` | Define function | Chapter 04 |
| `class` | Define class | Chapter 07 |
| `interface` | Define interface | Chapter 08 |
| `is` | Runtime type check (interface conformance / class identity) | Chapter 08 |
| `if`, `else if`, `else` | Conditional (no `elif` keyword) | Chapter 05 |
| `while`, `for` | Loops | Chapter 05 |
| `break`, `continue` | Loop control | Chapter 05 |
| `branch`, `on` | Pattern matching | Chapter 12 |
| `return` | Return from function | Chapter 04 |
| `nil` | Null value | Chapter 11 |
| `true`, `false` | Boolean literals | Chapter 02 |
| `as` | Optional binding / type narrowing (`if x as n`, `if x is T as r`) | Chapter 11 |
| `this` | Reference to current object | Chapter 07 |
| `static` | Static/class-level members (not `shared` — that keyword doesn't exist) | Chapter 07 |
| `require` | Precondition | Chapter 14 |
| `ensure` | Postcondition | Chapter 14 |
| `where` | Type constraint (on a generic class's type parameter) | Chapter 13 |

---

## Operator Precedence (Highest to Lowest)

1. Function calls, array access `()`
2. Unary operators `not`
3. Multiplication, division, modulo `* / %`
4. Addition, subtraction `+ -`
5. Comparison `< > <= >= == !=`
6. Logical AND `and`
7. Logical OR `or`
8. Assignment `=`

---

## Quick Type Reference

| Type | Example | Size | Range |
|------|---------|------|-------|
| `int` | `42` | 64-bit | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 |
| `float` | `3.14` | 64-bit | ±1.7976931348623157e+308 |
| `bool` | `true` | 1-bit | true, false |
| `str` | `"hello"` | Variable | UTF-8 encoded strings |
| `char` | `'x'` | 32-bit | Unicode character |
| `T?` | `42` or `nil` | Depends on T | T or nil |
| `List(T)` | `List(int)()` | Dynamic | Ordered collection |
| `HashMap(K,V)` | `HashMap(str, int)()` | Dynamic | Key-value pairs |
| `struct` | `Point(3, 4)` | Stack | Value type |
| `union` | `Shape.circle(5)` | Stack | Tagged union |

A bare `List()` / `HashMap()` with no type argument and no annotated
`var` type is a checker blind spot: it compiles under `zebra -c` but
fails full compile with `error: expected expression, found 'anytype'`
— always supply the type, as in the examples above.

---

## Common Patterns

### Safe Navigation

```zebra
var x: int? = 42
if x != nil
    print(x + 1)
```

### Null Coalescing (using `orelse`)

There is no `.unwrapOr()` method — the `orelse` operator is the
null-coalescing idiom:

```zebra
var x: int? = nil
var value = x orelse 0  # Use 0 if x is nil
```

### Error Handling Pattern

Zebra has no `Result` type and no `.isErr()` / `.error()` / `.value()`
methods — errors propagate through `throws` functions instead. Use `?`
to propagate, `catch value` for a fallback, or a function-level `catch
|e|` clause to handle the error explicitly:

```zebra
def operation(): int throws
    raise "something went wrong"

def main()
    var result = operation()
    print("Result: ${result}")
catch |e|
    print("Error: ${e.message}")
```

### For-Each Loop

```zebra
for item in collection
    print(item)
```

### String Interpolation

```zebra
var name = "Alice"
var age = 30
print("${name} is ${age} years old")
```

---

For more details on any feature, consult the appropriate chapter listed in the references.

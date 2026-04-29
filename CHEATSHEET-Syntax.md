# Zebra Syntax Cheat Sheet

One-page reference for Zebra syntax. Print this page!

---

## Variables & Types

```zebra
var x = 42                              # int (inferred)
var s = "hello"                         # str
var f = 3.14                            # float
var b = true                            # bool
var c = 'x'                             # char

var x: int = 42                       # explicit type
var y: int? = nil                     # nullable type
```

---

## Functions

```zebra
def add(a: int, b: int): int
    return a + b

var result = add(2, 3)                  # 5

def no_return()
    print "Just print"
```

---

## Classes

```zebra
class Person
    var name: str = ""
    var age: int = 0

    cue init(name: str, age: int)
        this.name = name
        this.age = age

    def describe(): str
        return "${name} is ${age}"

var person = Person("Alice", 30)
```

---

## Interfaces

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

---

## Structs & Unions

```zebra
struct Point
    var x: int
    var y: int

union Value
    int_ as int
    str_ as str
    none_

# Pattern matching
branch v
    on Value.int_ as n
        print n
    on Value.str_ as s
        print s
    else
        pass
```

---

## Composition & Mixins

Zebra has **no class inheritance.**  Reuse via interfaces (Ch 08), mixins
(`adds`), or composition (fields).

```zebra
# Mixin — shared methods pulled into multiple classes:
mixin Loggable
    def log(message: str)
        print "[log] ${message}"

class UserService adds Loggable
    cue init
        pass
    # `log()` is now a method on UserService.

# Composition — has-a, not is-a:
class Storage
    var path: str = ""

class Report
    var storage: Storage      # field-held helper

    cue init(p: str)
        storage = Storage()
        storage.path = p
```

See Chapter 09 for the full picture.

---

## Control Flow

```zebra
# If/Elif/Else
if x > 10
    print "Large"
elif x > 5
    print "Medium"
else
    print "Small"

# While loop
var i = 0
while i < 10
    print i
    i = i + 1

# For loop
for item in items
    print item

for i in 0..10
    print i  # 0, 1, 2, ..., 9

# Break & Continue
while true
    if x == 5
        break
    if x == 2
        x = x + 1
        continue
    print x
    x = x + 1
```

---

## Operators

```zebra
# Arithmetic
10 + 5, 10 - 5, 10 * 5, 10 / 5, 10 % 3

# Comparison
10 > 5, 10 < 5, 10 >= 5, 10 <= 5
10 == 5, 10 != 5

# Logical
true and false
true or false
not true

# String
"hello" + " world"
"Value: ${x}"                           # interpolation
```

---

## Collections

```zebra
# List
var numbers = List(int)()
numbers.add(1)
numbers.add(2)
for num in numbers
    print num
numbers.count()
numbers.at(0)
numbers.contains(1)
numbers.remove(1)

# HashMap
var map = HashMap(str, int)()
map.put("a", 1)
map.fetch("a")                        # retrieve value
map.contains("a")
map.remove("a")
for key, value in map
    print "${key}: ${value}"
```

---

## Strings

```zebra
var text = "Hello, World!"

# Properties & Methods
text.len                                # length
text.upper()                            # uppercase
text.lower()                            # lowercase
text.contains("World")                  # substring search
text.startsWith("Hello")                # prefix check
text.endsWith("!")                      # suffix check
text.split(",")                         # split to List(str)
text.replace("World", "Zebra")          # replace all occurrences
text.trim()                             # remove whitespace
text.indexOf("World")                   # find position (-1 if not found)
text.reverse()                          # reverse string
text.repeat(3)                          # repeat N times

# Type conversion
"42".toInt()                            # int? (nullable)
"3.14".toFloat()                        # float?
42.toString()                           # "42"
```

---

## Error Handling

```zebra
# Functions that can fail use throws
def parse(text: str): int throws
    if text.len == 0
        raise "Empty input"
    return 42

# Catch expression (inline fallback)
var value = parse("abc") catch 0

# Try/catch block
try
    var v = parse("")
    print v
catch |err|
    print "Error: ${err}"

# Catch with binding
var result = parse("x") catch |e| -1
```

---

## Nil Safety

```zebra
var x: int? = 42                      # Can be int or nil
var y: int? = nil                     # Explicitly nil

# Safe check
if x != nil
    var safe_x = x + 1                  # Safe now
```

---

## Generics

```zebra
# Generic function
def first(items: List(T)) as T?
    if items.count() > 0
        return items.at(0)
    return nil

# Generic class
class Box(T)
    var item: T?

    def store(value: T)
        this.item = value

    def retrieve(): T?
        return this.item

var box = Box(str)()
box.store("hello")
```

---

## Pipelines

```zebra
var result = text -> .trim() -> .upper() -> .split(" ")

# Equivalent to:
var trimmed = text.trim()
var upper = trimmed.upper()
var parts = upper.split(" ")
```

---

## File I/O

```zebra
# Read file
var content = File.read("file.txt") catch ""

# Write file
File.write("output.txt", content)

# Check existence
if File.exists("file.txt")
    print "File exists"
```

---

## Regular Expressions

```zebra
var pattern = Regex.compile("[a-z0-9]+@[a-z]+\\.[a-z]+")

pattern.matches("user@example.com")     # bool
pattern.find(text)                      # str? (first match)
pattern.findAll(text)                   # List(str) (all matches)
pattern.replace(text, "X")              # str (replace first)
pattern.replaceAll(text, "X")           # str (replace all)
pattern.split(text)                     # List(str) (split by match)
```

---

## System Access

```zebra
sys.args()                              # List(str): command-line args
sys.exit(code)                          # Exit program
Arg.parse()                             # Structured argument parsing
```

---

## Modules

```zebra
use MathUtils                           # Import module
use ast exposing Stmt, Expr, TypeRef    # Selective import
```

---

## Math Module

```zebra
Math.PI                                 # 3.14159...
Math.E                                  # 2.71828...
Math.sin(x)                             # Trig functions
Math.sqrt(x)                            # Square root
Math.pow(x, y)                          # Power
Math.abs(x)                             # Absolute value
Math.min(a, b)                          # Minimum
Math.max(a, b)                          # Maximum
Math.floor(x)                           # Round down
Math.ceil(x)                            # Round up
```

---

## Static Methods

```zebra
class MathUtils
    static
        def add(a: int, b: int): int
            return a + b

MathUtils.add(2, 3)                     # Call without instance
```

The keyword is `static` (the older `shared` was renamed in 2026-04-19).

---

## Contracts (`require` / `ensure` / `invariant`)

```zebra
class Counter
    var count: int = 0

    invariant
        count >= 0

    def increment(): int
        ensure
            result == old count + 1     # `result` = return value; `old expr` = pre-call snapshot
        count = count + 1
        return count

    def decrement_by(n: int)
        require
            n > 0
            n <= count
        count = count - n
```

Pass `--turbo` to strip all contract checks for production builds.
See Chapter 14.

---

## Reflection — `Reflect.*` / `@reflectable`

```zebra
# Tier 1: static field/type-name arrays:
class User
    var name: str = ""
    var age: int = 0

print Reflect.className(u)              # "User"
for n in Reflect.fieldNames(u)
    print n

# Tier 3: strict JSON deserialization
@reflectable
class User
    var name: str = ""
    var age: int = 0

if Json.parseStrict(User, src) as u
    print u.name
```

Strict semantics: missing key, type mismatch, or extra key → nil.
Scope-1 fields: int / float / bool / str.

---

## Comments

```zebra
# Single-line comment

# Multi-line comments
# are just multiple
# single-line comments
```

---

## Keywords Quick Reference

| Keyword | Use |
|---------|-----|
| `var` | Declare variable |
| `def` | Define function |
| `class` | Define class |
| `struct` | Define value type |
| `union` | Define tagged union |
| `enum` | Define enumeration |
| `interface` | Define interface |
| `is` | Member attribute / type check |
| `implements` | Implement interface |
| `if`, `elif`, `else` | Conditional |
| `while` | While loop |
| `for` | For loop |
| `break` | Exit loop |
| `continue` | Skip iteration |
| `branch` | Pattern matching |
| `on` | Pattern case |
| `return` | Return from function |
| `raise` | Signal an error |
| `throws` | Mark function as fallible |
| `try`, `catch` | Error handling |
| `except` | Struct update copy |
| `nil` | Null value |
| `true`, `false` | Boolean literals |
| `as` | Binding clause (`if x as n`, `branch on V as r`) |
| `static` | Type-associated (class-level) member |
| `mixin` | Declare a reusable bag of methods |
| `adds` | Include a mixin into a class |
| `require` | Precondition contract |
| `ensure` | Postcondition contract |
| `invariant` | Class invariant contract |
| `result` | Return-value reference inside `ensure` |
| `old` | Pre-call snapshot inside `ensure` |
| `assert` | Inline sanity check |
| `arena` | Bounded-scope memory block |
| `to` | Numeric / unwrap operator (`x to int`, `x to!`) |
| `this` | Current object reference |
| `use` | Import module |
| `@reflectable` | Opt class into Tier-3 reflection (`Json.parseStrict`) |
| `exposing` | Selective import |
| `where` | Type constraint |

---

## Quick Type Reference

| Type | Example | Default |
|------|---------|---------|
| `int` | `42` | 0 |
| `float` | `3.14` | 0.0 |
| `bool` | `true` | false |
| `str` | `"hello"` | "" |
| `char` | `'x'` | '' |
| `T?` | `42` or `nil` | nil |
| `List(T)` | `List(int)()` | empty |
| `HashMap(K,V)` | `HashMap(str, int)()` | empty |
| `^T` | `^Node` | heap pointer |

---

## Operator Precedence

1. `()` — function call, array access
2. `not` — logical NOT
3. `*`, `/`, `%` — multiplication, division, modulo
4. `+`, `-` — addition, subtraction
5. `<`, `>`, `<=`, `>=`, `==`, `!=` — comparison
6. `and` — logical AND
7. `or` — logical OR
8. `=` — assignment

---

**Print this page for quick reference!**

For more details, see the full book or use the Troubleshooting guide (Appendix C).

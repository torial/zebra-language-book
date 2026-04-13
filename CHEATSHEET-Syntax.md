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

var x as int = 42                       # explicit type
var y as int? = nil                     # nullable type
```

---

## Functions

```zebra
def add(a as int, b as int) as int
    return a + b

var result = add(2, 3)                  # 5

def no_return()
    print "Just print"
```

---

## Classes

```zebra
class Person
    var name as str = ""
    var age as int = 0

    cue init(name as str, age as int)
        this.name = name
        this.age = age

    def describe() as str
        return "${name} is ${age}"

var person = Person("Alice", 30)
```

---

## Interfaces

```zebra
interface Shape
    def area() as float
    def perimeter() as float

class Circle is Shape
    var radius as float = 0.0

    def area() as float
        return 3.14159 * radius * radius

    def perimeter() as float
        return 2.0 * 3.14159 * radius
```

---

## Structs & Unions

```zebra
struct Point
    var x as int
    var y as int

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

## Inheritance

```zebra
class Animal
    var name as str = ""
    def speak() as str
        return "Sound"

class Dog is Animal
    def speak() as str
        return "Woof!"
```

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

for i in 0.to(10)
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
map.set("a", 1)
map.get("a")                          # returns int? (nullable)
map.contains("a")
map.remove("a")
for entry in map.entries()
    print "${entry.key}: ${entry.value}"
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
text.replace("World", "Zebra")          # replace first
text.replaceAll("l", "L")              # replace all
text.trim()                             # remove whitespace
text.substring(0, 5)                    # extract portion
text.charAt(0)                          # char at position
text.indexOf("World")                   # find position (-1 if not found)

# Type conversion
"42".toInt()                            # int? (nullable)
"3.14".toFloat()                        # float?
42.toString()                           # "42"
```

---

## Error Handling

```zebra
# Functions that can fail use throws
def parse(text as str) as int throws
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
var x as int? = 42                      # Can be int or nil
var y as int? = nil                     # Explicitly nil

# Safe check
if x != nil
    var safe_x = x + 1                  # Safe now
```

---

## Generics

```zebra
# Generic function
def first(items as List(T)) as T?
    if items.count() > 0
        return items.at(0)
    return nil

# Generic class
class Box(T)
    var item as T?

    def set(value as T)
        this.item = value

    def get() as T?
        return this.item

var box = Box(str)()
box.set("hello")
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

## Shared/Static Methods

```zebra
class MathUtils
    shared
        def add(a as int, b as int) as int
            return a + b

MathUtils.add(2, 3)                     # Call without instance
```

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
| `is` | Inherit from class/interface |
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
| `as` | Type annotation |
| `shared` | Static/class member |
| `this` | Current object reference |
| `use` | Import module |
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

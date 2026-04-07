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
    println("Just print")
```

---

## Classes

```zebra
class Person
    var name as str = ""
    var age as int = 0
    
    def init(name as str, age as int)
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
    println("Large")
elif x > 5
    println("Medium")
else
    println("Small")

# While loop
var i = 0
while i < 10
    println(i)
    i = i + 1

# For loop
for item in items
    println(item)

for i in 0.to(10)
    println(i)  # 0, 1, 2, ..., 9

# Break & Continue
while true
    if x == 5
        break
    if x == 2
        x = x + 1
        continue
    println(x)
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
    println(num)
numbers.count()
numbers.at(0)
numbers.contains(1)
numbers.remove(1)

# HashMap
var map = HashMap(str, int)()
map.put("a", 1)
map.fetch("a")                          # returns int? (nullable)
map.contains("a")
map.remove("a")

# Set
var unique = Set(str)()
unique.add("a")
unique.contains("a")
unique.remove("a")
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
text.replaceAll("l", "L")               # replace all
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

## Error Handling with Result

```zebra
# Create Result
Result.ok(value)
Result.err(error_message)

# Check Result
var result = operation()
if result.isOk()
    var value = result.value()
elif result.isErr()
    var error = result.error()

# Unwrap Result
var value = result.unwrapOr(default)    # default if error

# Pattern match
branch result
    on ok(value)
        println(value)
    on err(error)
        println("Error: ${error}")
```

---

## Nil Safety

```zebra
var x as int? = 42                      # Can be int or nil
var y as int? = nil                     # Explicitly nil

# Safe check
if x != nil
    var safe_x = x + 1                  # Safe now

# Safe access with default
var value = x.unwrapOr(0)               # 0 if x is nil
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
var result = File.read("file.txt")
if result.isOk()
    var content = result.value()

# Write file
var write_result = File.write("output.txt", content)

# Check existence
if File.exists("file.txt")
    println("File exists")

# Delete file
File.delete("file.txt")
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
System.args()                           # List(str): command-line args
System.env("HOME")                      # str?: environment variable
System.cwd()                            # str: current directory
System.exit(code)                       # Exit program
```

---

## Type Conversion

```zebra
# String conversions
"42".toInt()                            # int?
"3.14".toFloat()                        # float?
42.toString()                           # "42"
3.14.toString()                         # "3.14"
true.toString()                         # "true"
```

---

## Shared/Static Methods

```zebra
class Math
    shared
        def add(a as int, b as int) as int
            return a + b

Math.add(2, 3)                          # Call without instance
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
| `nil` | Null value |
| `true`, `false` | Boolean literals |
| `as` | Type annotation |
| `shared` | Static/class member |
| `this` | Current object reference |
| `where` | Type constraint |

---

## Common Type Patterns

```zebra
var name as str                         # String variable
var count as int                        # Integer variable
var items as List(str)                  # List of strings
var map as HashMap(str, int)            # Map of str->int
var maybe as str?                       # Nullable string
var result as Result(int, str)          # Result: ok(int) or err(str)
```

---

## Common Patterns

### Safe Null Checking
```zebra
var x as int? = get_value()
if x != nil
    println(x + 1)
```

### Safe File Reading
```zebra
var result = File.read("file.txt")
if result.isErr()
    println("Error: ${result.error()}")
    return
var content = result.value()
```

### Loop Through Collection
```zebra
for item in items
    println(item)
```

### String Interpolation
```zebra
var name = "Alice"
println("Hello, ${name}!")
```

### Build String from List
```zebra
var parts = ["a", "b", "c"]
var joined = parts.join(",")            # "a,b,c"
```

### Handle Error Result
```zebra
branch operation()
    on ok(value)
        println(value)
    on err(error)
        println("Failed: ${error}")
```

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
| `Set(T)` | `Set(str)()` | empty |
| `Result(T,E)` | `Result.ok(42)` | — |

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

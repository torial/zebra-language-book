# Appendix A: Grammar Reference

This appendix is a quick reference for Zebra's syntax. For detailed explanations, refer to the chapter listed for each feature.

---

## Basic Types

### Primitive Types

```zebra
var x as int = 42           # 64-bit integer
var y as float = 3.14       # 64-bit floating point
var b as bool = true        # Boolean
var s as str = "hello"      # Immutable string
var c as char = 'x'         # Single character
```

**References:** Chapter 02 (Values and Types)

### Nullable Types

```zebra
var x as int? = nil         # Can be int or nil
var s as str? = "hello"     # Can be string or nil

if x != nil
    print x              # Safe to use x here
```

**References:** Chapter 11 (Nil Tracking and Safety)

### Collection Types

```zebra
var numbers as List(int) = List()
var mapping as HashMap(str, int) = HashMap()

numbers.add(1)
mapping.set("key", 42)
```

**References:** Chapter 03 (Collections)

### Error Handling

```zebra
def parse(text as str) as int throws
    if text.len == 0
        raise "Empty input"
    return 42

var value = parse("hello") catch 0

try
    var v = parse("")
catch |err|
    print "Error: ${err}"
```

**References:** Chapter 12 (Error Handling)

---

## Functions

### Basic Function Definition

```zebra
def greet(name as str) as str
    return "Hello, ${name}"

var message = greet("Alice")
```

**References:** Chapter 04 (Functions and Scope)

### Functions with Multiple Parameters

```zebra
def add(a as int, b as int) as int
    return a + b

var sum = add(3, 4)
```

### Functions with Optional Parameters

```zebra
def calculate(a as int, b as int, operation as str) as int
    if operation == "add"
        return a + b
    else
        return a - b
```

### Returning Multiple Values (via Structure)

```zebra
class Result
    var value as int
    var success as bool

def divide(a as int, b as int) as Result
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

```zebra
class Person
    var name as str = ""
    var age as int = 0
    
    def init(name as str, age as int)
        this.name = name
        this.age = age
    
    def describe() as str
        return "${name} is ${age} years old"

var person = Person("Alice", 30)
print person.describe()
```

**References:** Chapter 07 (Classes and Instances)

### Class with Shared Methods

```zebra
class Math
    shared
        def add(a as int, b as int) as int
            return a + b

var result = Math.add(2, 3)
```

**References:** Chapter 07 (Classes and Instances)

### Class with Properties

```zebra
class Circle
    var radius as float = 0.0
    
    def area() as float
        return 3.14159 * radius * radius
```

**References:** Chapter 10 (Properties and Computed Values)

### Inheritance

```zebra
class Animal
    var name as str = ""
    
    def speak() as str
        return "Some sound"

class Dog is Animal
    # Inherits name from Animal
    
    def speak() as str
        return "Woof!"

var dog = Dog()
dog.name = "Buddy"
print dog.speak()  # "Woof!"
```

**References:** Chapter 09 (Inheritance and Mixins)

---

## Interfaces

### Basic Interface Definition

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

**References:** Chapter 08 (Interfaces and Protocols)

---

## Control Flow

### If/Elif/Else

```zebra
if x > 10
    print "Large"
elif x > 5
    print "Medium"
else
    print "Small"
```

**References:** Chapter 05 (Control Flow)

### While Loop

```zebra
var i = 0
while i < 10
    print i
    i = i + 1
```

**References:** Chapter 05 (Control Flow)

### For Loop

```zebra
for item in collection
    print item

for i in 0.to(10)
    print i  # 0, 1, 2, ..., 9
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
    
    print i
    i = i + 1
```

**References:** Chapter 05 (Control Flow)

### Branch (Pattern Matching)

```zebra
var value as int? = 42

branch value
    on nil
        print "Value is nil"
    on _
        print "Value is ${value}"

```

### Error Handling

```zebra
def load(path as str) as str throws
    if path.len == 0
        raise "Empty path"
    return "data"

# Catch expression
var data = load("") catch "default"

# Try/catch block
try
    var d = load("")
catch |err|
    print "Error: ${err}"
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
var x = 10, y = 20      # Multiple assignments
```

### Pipelines

```zebra
text -> .trim() -> .upper() -> .split(" ")
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
var x as int = 42          # Local variable, explicit type
var x = 42, y = "hello"    # Multiple declarations
```

### Scope

```zebra
def example()
    var x = 10
    
    if true
        var y = 20         # y is only visible here
        print x         # x is visible (outer scope)
        print y         # y is visible
    
    print x             # x is visible
    # print y           # ERROR: y is out of scope
```

**References:** Chapter 04 (Functions and Scope)

---

## Generics

### Generic Functions

```zebra
def first(items as List(T)) as T?
    if items.count() > 0
        return items.at(0)
    return nil

var nums = List()
nums.add(42)
var first_num = first(nums)  # Type is int?
```

**References:** Chapter 13 (Generics and Type Constraints)

### Generic Classes

```zebra
class Box(T)
    var item as T?
    
    def set(item as T)
        this.item = item
    
    def get() as T?
        return this.item

var box = Box(str)()
box.set("Hello")
var value = box.get()  # Type is str?
```

**References:** Chapter 13 (Generics and Type Constraints)

### Type Constraints

```zebra
def compare(a as T, b as T) as int where T can be Comparable
    # T must implement Comparable interface
    if a < b
        return -1
    elif a > b
        return 1
    else
        return 0
```

**References:** Chapter 13 (Generics and Type Constraints)

---

## Error Handling

### Fallible Functions

```zebra
def divide(a as int, b as int) as int throws
    if b == 0
        raise "Division by zero"
    return a / b
```

### Catch Expression

```zebra
# Inline fallback
var value = divide(10, 0) catch 0

# Catch with binding
var result = divide(10, 0) catch |e| -1
```

### Try/Catch Block

```zebra
try
    var value = divide(10, 0)
    print value
catch |err|
    print "Error: ${err}"
```

**References:** Chapter 12 (Error Handling)

---

## Nil Safety

### Null Checking

```zebra
var x as int? = nil

if x != nil
    # Safe to use x as int here
    print x + 1

if x == nil
    print "x is nil"
```

### Safe Navigation

```zebra
var x as int? = 42

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
text.charAt(0)                  # Get character at position
```

**References:** Chapter 06 (Strings and Unicode), Chapter 19 (Standard Library)

---

## Collections

### List Operations

```zebra
var items = List()

items.add("apple")              # Add item
items.remove("apple")           # Remove item
items.count()                   # Count items
items.at(0)                     # Get item at index
items.contains("apple")         # Check membership
items.clear()                   # Remove all items

for item in items
    print item               # Iterate
```

### HashMap Operations

```zebra
var map = HashMap()

map.set("a", 1)                 # Add/update
map.get("a")                  # Get value (returns nullable)
map.contains("a")               # Check key exists
map.remove("a")                 # Remove key
map.keys()                       # Get all keys

for key in map.keys()
    var value = map.get(key)
    if value != nil
        print "${key} => ${value}"
```

### Deduplication (via HashMap)

```zebra
var seen as HashMap(str, bool) = HashMap()

seen.set("apple", true)         # Track item
seen.contains("apple")          # Check membership

for key in seen.keys()
    print key                # Iterate unique items
```

**References:** Chapter 03 (Collections)

---

## Type Conversion

```zebra
# String to int (returns nullable)
var num = "42".toInt()          # int?

# String to float (returns nullable)
var decimal = "3.14".toFloat()  # float?

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

### Contracts (if supported)

```zebra
def divide(a as int, b as int) as int
    require b != 0, "Divisor cannot be zero"
    return a / b
```

**References:** Chapter 14 (Contracts and Assertions)

### Assertions

```zebra
assert x > 0, "x must be positive"
```

**References:** Chapter 14 (Contracts and Assertions)

### Mixins

```zebra
mixin Serializable
    def to_json() as str
        return "{}"

class Person is Serializable
    var name as str = ""
    
    def to_json() as str
        return "{\"name\": \"${name}\"}"
```

**References:** Chapter 09 (Inheritance and Mixins)

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
    def helper_function() as str
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
| `is` | Inherit from class/interface | Chapter 09 |
| `if`, `elif`, `else` | Conditional | Chapter 05 |
| `while`, `for` | Loops | Chapter 05 |
| `break`, `continue` | Loop control | Chapter 05 |
| `branch`, `on` | Pattern matching | Chapter 12 |
| `return` | Return from function | Chapter 04 |
| `nil` | Null value | Chapter 11 |
| `true`, `false` | Boolean literals | Chapter 02 |
| `as` | Type annotation | Chapter 02 |
| `Result` | Error type | Chapter 12 |
| `shared` | Static/class method | Chapter 07 |
| `this` | Reference to current object | Chapter 07 |
| `require` | Precondition | Chapter 14 |
| `ensure` | Postcondition | Chapter 14 |
| `where` | Type constraint | Chapter 13 |

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
| `List(T)` | `List()` | Dynamic | Ordered collection |
| `HashMap(K,V)` | `HashMap()` | Dynamic | Key-value pairs |
| `struct` | `Point(3, 4)` | Stack | Value type |
| `union` | `Shape.circle(5)` | Stack | Tagged union |

---

## Common Patterns

### Safe Navigation

```zebra
var x as int? = 42
if x != nil
    print x + 1
```

### Null Coalescing (using unwrapOr)

```zebra
var x as int? = nil
var value = x.unwrapOr(0)  # Use 0 if x is nil
```

### Try-Catch Pattern

```zebra
var result = operation()
if result.isErr()
    print "Error: ${result.error(}")
else
    print "Success: ${result.value(}")
```

### For-Each Loop

```zebra
for item in collection
    print item
```

### String Interpolation

```zebra
var name = "Alice"
var age = 30
print "${name} is ${age} years old"
```

---

For more details on any feature, consult the appropriate chapter listed in the references.

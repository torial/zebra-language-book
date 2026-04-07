# Appendix C: Troubleshooting

This appendix helps you debug common Zebra programming errors. Each section shows a problem, its cause, and solution.

---

## Type Errors

### "error: expected type X, got type Y"

**What it means:** You're using a value of one type where another is expected.

**Common causes:**
- String where int expected
- Int where string expected
- Nullable type where non-nullable expected

**Example:**
```zebra
var x = 42          # int
var message = x     # ERROR: trying to assign int to str context
println("Value: " + x)  # ERROR: can't concatenate string + int directly
```

**Solution:**
```zebra
var x = 42
var message = x.toString()      # Convert int to string
println("Value: " + message)    # Now it works

# Or use interpolation
println("Value: ${x}")          # Better approach
```

---

### "error: arithmetic requires numeric type, got 'str'"

**What it means:** You're trying to do math on a string.

**Common cause:** Forgetting to convert string to number.

**Example:**
```zebra
var x = "10"
var y = "5"
var sum = x + y         # ERROR: concatenates "105", not arithmetic sum
var result = x - y      # ERROR: can't subtract strings
```

**Solution:**
```zebra
var x = "10".toInt()
var y = "5".toInt()

if x != nil and y != nil
    var sum = x + y         # 15
    println(sum)
```

**Better:**
```zebra
var result = "10".toInt() and "5".toInt()
if result != nil
    # Handle both being valid
```

---

### "error: type mismatch in collection"

**What it means:** You're adding the wrong type to a collection.

**Example:**
```zebra
var numbers = List(int)()
numbers.add(42)         # OK
numbers.add("hello")    # ERROR: expecting int, got str
```

**Solution:**
Check the collection's declared type and add matching values:
```zebra
var numbers = List(int)()
numbers.add(42)

var names = List(str)()
names.add("hello")
```

---

## Nil and Null Errors

### "error: cannot use nil value as int"

**What it means:** You're using a nullable value where a non-nullable value is required.

**Common cause:** Not checking for nil before using.

**Example:**
```zebra
var x as int? = nil
var result = x + 1      # ERROR: can't add to potentially nil value
```

**Solution:**
```zebra
var x as int? = nil

if x != nil
    var result = x + 1  # Safe—x is definitely int here
else
    println("x is nil")
```

**Alternative:**
```zebra
var x as int? = nil
var value = x.unwrapOr(0)  # Use 0 if x is nil
var result = value + 1
```

---

### "error: cannot use value of type T as nullable type T?"

**What it means:** You're assigning non-nullable to nullable (usually OK) or vice versa (error).

**Example:**
```zebra
var x as int = 42
var y as int? = x       # OK: int can become int?

var z as int = y        # ERROR: int? cannot become int (might be nil!)
```

**Solution:**
```zebra
var y as int? = 42

if y != nil
    var z as int = y    # Safe now—y is definitely int
```

---

### "error: nil pointer dereference"

**What it means:** You're using a nil value when it should have a real value.

**Common causes:**
- Collection index out of bounds
- Unwrapping nil value
- Calling method on nil

**Example:**
```zebra
var x as int? = nil
println(x + 1)          # ERROR if x is nil
```

**Solution:**
```zebra
var x as int? = get_value()

if x != nil
    println(x + 1)
else
    println("Value not found")
```

---

## Collection Errors

### "error: index out of bounds"

**What it means:** You're accessing a list with an invalid index.

**Example:**
```zebra
var items = List(int)()
items.add(42)

var first = items.at(0)     # OK
var second = items.at(1)    # ERROR: index 1 doesn't exist
var third = items.at(-1)    # ERROR: negative index
```

**Solution:**
```zebra
var items = List(int)()
items.add(42)

if items.count() > 0
    var first = items.at(0)  # Safe

for i in 0.to(items.count())
    var item = items.at(i)   # Safe—i is valid
```

**Better:**
```zebra
for item in items
    println(item)            # No index worries
```

---

### "error: cannot remove from empty list"

**What it means:** You're removing from a list with no elements.

**Example:**
```zebra
var items = List(int)()
items.remove(42)        # ERROR: can't remove from empty list
```

**Solution:**
```zebra
var items = List(int)()

if items.count() > 0
    items.remove(42)
```

---

### "error: key not found in HashMap"

**What it means:** You're accessing a HashMap key that doesn't exist.

**Example:**
```zebra
var map = HashMap(str, int)()
var value = map.fetch("key")  # Returns nil, not an error

# But if you don't check nil:
var num = map.fetch("key")
var result = num + 1           # ERROR: num is nil!
```

**Solution:**
```zebra
var map = HashMap(str, int)()
var value = map.fetch("key")

if value != nil
    var result = value + 1
else
    println("Key not found")

# Or use unwrapOr
var value = map.fetch("key").unwrapOr(0)  # 0 if not found
```

---

## String Errors

### "error: string concatenation requires string on left and right"

**What it means:** You're trying to concatenate non-strings.

**Example:**
```zebra
var x = 42
var message = "Value: " + x     # ERROR: can't add string + int
```

**Solution:**
```zebra
var x = 42

# Convert to string
var message = "Value: " + x.toString()

# Or use interpolation (better)
var message = "Value: ${x}"

# Or use concat method
var message = "Value: ".concat(x.toString())
```

---

### "error: string index out of bounds"

**What it means:** You're accessing a character past the end of the string.

**Example:**
```zebra
var text = "hello"
var last = text.charAt(10)      # ERROR: index out of bounds
```

**Solution:**
```zebra
var text = "hello"

if text.len > 10
    var char = text.charAt(10)
else
    println("Index out of range")

// Safe way
var last = text.charAt(text.len - 1)  # Get last character
```

---

### "error: substring indices out of range"

**What it means:** Your substring start/end indices are invalid.

**Example:**
```zebra
var text = "hello"
var part = text.substring(10, 15)   # ERROR: indices out of bounds
var part = text.substring(3, 1)     # ERROR: start > end
```

**Solution:**
```zebra
var text = "hello"

var start = 1
var end = 4

if start >= 0 and end <= text.len and start <= end
    var part = text.substring(start, end)  # "ell"
```

---

## Function Errors

### "error: function expects N parameters, got M"

**What it means:** You're calling a function with wrong number of arguments.

**Example:**
```zebra
def add(a as int, b as int) as int
    return a + b

var sum = add(5)        # ERROR: expects 2, got 1
var sum = add(1, 2, 3)  # ERROR: expects 2, got 3
```

**Solution:**
```zebra
def add(a as int, b as int) as int
    return a + b

var sum = add(1, 2)     # Correct: 2 parameters
```

---

### "error: function parameter type mismatch"

**What it means:** You're passing wrong type to function.

**Example:**
```zebra
def greet(name as str) as str
    return "Hello, ${name}"

greet(42)               # ERROR: expects str, got int
```

**Solution:**
```zebra
def greet(name as str) as str
    return "Hello, ${name}"

greet("Alice")          # Correct: str parameter
greet(42.toString())    # Convert int to str
```

---

### "error: function does not return a value"

**What it means:** Your function says it returns something but doesn't.

**Example:**
```zebra
def get_value() as int
    if true
        return 42
    # Missing return for false case
```

**Solution:**
```zebra
def get_value() as int
    if true
        return 42
    else
        return 0    # Now all paths return

# Or use branch
def get_value() as int
    var result = 0
    if condition
        result = 42
    return result
```

---

## Error Handling Errors

### "error: result must be checked before use"

**What it means:** You're using a Result without checking if it's success or error.

**Example:**
```zebra
var result = File.read("file.txt")
var content = result.value()    # ERROR: might be error!
```

**Solution:**
```zebra
var result = File.read("file.txt")

if result.isOk()
    var content = result.value()
else
    println("Error: ${result.error()}")

# Or use branch
branch result
    on ok(content)
        println(content)
    on err(error)
        println("Error: ${error}")
```

---

### "error: unwrap on error result would panic"

**What it means:** You're calling `.unwrap()` on an error Result.

**Example:**
```zebra
var result = operation()
var value = result.unwrap()     # ERROR if result.isErr()
```

**Solution:**
```zebra
var result = operation()

if result.isOk()
    var value = result.unwrap()  # Safe now

# Or use unwrapOr with default
var value = result.unwrapOr(default_value)
```

---

## Class and Inheritance Errors

### "error: cannot assign to immutable field"

**What it means:** You're trying to modify a readonly/immutable field.

**Example:**
```zebra
class Person
    var name as str = ""

var person = Person()
person.name = "Alice"           # OK if var field

class Circle
    var radius as float = 0.0   # If immutable
    
var circle = Circle()
circle.radius = 5.0             # ERROR if immutable
```

**Solution:**
Ensure fields are declared with `var`:
```zebra
class Person
    var name as str = ""        # Mutable
    var age as int = 0          # Mutable

var person = Person()
person.name = "Alice"           # Now OK
person.age = 30                 # Now OK
```

---

### "error: unimplemented interface method"

**What it means:** Your class doesn't implement all methods required by interface.

**Example:**
```zebra
interface Shape
    def area() as float
    def perimeter() as float

class Circle is Shape
    var radius as float = 0.0
    
    def area() as float
        return 3.14 * radius * radius
    
    # ERROR: missing perimeter() method
```

**Solution:**
```zebra
interface Shape
    def area() as float
    def perimeter() as float

class Circle is Shape
    var radius as float = 0.0
    
    def area() as float
        return 3.14 * radius * radius
    
    def perimeter() as float
        return 2.0 * 3.14 * radius  # Now complete
```

---

### "error: cannot instantiate abstract class"

**What it means:** You're trying to create an instance of a class that can't be instantiated.

**Solution:**
Create a concrete subclass:
```zebra
class Shape          # Abstract-ish
    # ...

class Circle is Shape
    # Provide all implementations
    # ...

var circle = Circle()  # OK
# var shape = Shape()  # ERROR
```

---

## File I/O Errors

### "error: file not found"

**What it means:** You're trying to read a file that doesn't exist.

**Example:**
```zebra
var result = File.read("missing.txt")
# If not handling Result, this fails
```

**Solution:**
```zebra
var result = File.read("missing.txt")

if result.isErr()
    println("File not found: ${result.error()}")
else
    var content = result.value()
    println(content)

# Or check first
if File.exists("missing.txt")
    var result = File.read("missing.txt")
```

---

### "error: permission denied writing file"

**What it means:** You don't have permission to write to a location.

**Solution:**
Check permissions or use a different location:
```zebra
var result = File.write("output.txt", content)

if result.isErr()
    println("Cannot write: ${result.error()}")
    // Try writing to temp directory instead
    var temp_result = File.write("/tmp/output.txt", content)
```

---

## Regex Errors

### "error: invalid regular expression"

**What it means:** Your regex pattern has syntax errors.

**Example:**
```zebra
var pattern = Regex.compile("[a-z")    # ERROR: unclosed bracket
var pattern = Regex.compile("(abc")    # ERROR: unclosed group
```

**Solution:**
Fix the regex syntax:
```zebra
var pattern = Regex.compile("[a-z]")   # Correct
var pattern = Regex.compile("(abc)")   # Correct
```

**Common mistakes:**
- Unmatched brackets: `[a-z`, `[a-z])`
- Unmatched parentheses: `(`, `)`
- Unescaped special characters: `.` should be `\.` for literal dot
- Invalid escape: `\x` (use `\\x` for literal backslash)

---

### "error: regex match failed"

**What it means:** Pattern doesn't match input (not really an error, just didn't match).

**Example:**
```zebra
var pattern = Regex.compile("^hello$")
if not pattern.matches("hello world")
    println("No match")
```

**Solution:**
Make regex more flexible:
```zebra
var pattern = Regex.compile("hello")   # Matches substring
var pattern = Regex.compile("^hello")  # Matches start
var pattern = Regex.compile("hello.*") # Matches hello + anything
```

---

## Performance Issues

### "program runs very slowly"

**Common causes:**
- String concatenation in loops
- Excessive list copying
- HashMap with poor hash function
- Nested loops with high complexity
- Frequent function calls

**Solutions:**

1. **Don't concatenate strings in loops:**
```zebra
# SLOW
var result = ""
for item in items
    result = result + item + ", "

# FAST
var parts = List(str)()
for item in items
    parts.add(item)
var result = parts.join(", ")
```

2. **Avoid copying large structures:**
```zebra
# SLOW
var copy = big_list  # Copies entire list
for item in copy
    process(item)

# FAST
for item in big_list
    process(item)
```

3. **Use HashMap for lookups, not List:**
```zebra
# SLOW: O(n) for each lookup
var found = false
for item in list
    if item == search_key
        found = true

# FAST: O(1) lookup
if set.contains(search_key)
    found = true
```

4. **Watch algorithmic complexity:**
```zebra
# SLOW: O(n²) nested loops
for i in 0.to(items.count())
    for j in 0.to(items.count())
        process(items.at(i), items.at(j))

# FAST: O(n log n) or O(n)
// Use appropriate algorithm
```

---

## Debugging Tips

### Print Debugging

```zebra
var x = 10
println("x = ${x}")          # Check variable value
println("After operation")   # Check execution flow

if condition
    println("Condition true: ${variable}")
```

### Assertion-Based Debugging

```zebra
assert x > 0, "x must be positive"
assert items.count() == 3, "Expected 3 items"
assert result.isOk(), "Operation must succeed"
```

### Type Checking

```zebra
var x = 42
println(x.toString())        # Force type check

var result as Result(int, str) = operation()
// Type annotation makes intent clear
```

### Null Checking

```zebra
var x as int? = get_value()

if x != nil
    println("Value: ${x}")
else
    println("Value is nil")
```

---

## Common Patterns for Error Avoidance

### Safe Navigation

```zebra
var x as int? = get_value()

if x != nil
    var result = x + 1
else
    println("Value not available")
```

### Safe Collection Access

```zebra
var items = List(int)()

for i in 0.to(items.count())
    var item = items.at(i)  # Always safe with this pattern
```

### Safe String Operations

```zebra
var text = "hello"

if text.len > 0
    var first = text.charAt(0)

if text.contains("ll")
    var pos = text.indexOf("ll")
```

### Safe Type Conversion

```zebra
var num_str = "42"
var num = num_str.toInt()

if num != nil
    println(num + 1)
```

### Safe Error Handling

```zebra
var result = risky_operation()

if result.isErr()
    println("Error: ${result.error()}")
    return

var value = result.value()
```

---

## Getting Help

If you encounter an error not listed here:

1. **Read the error message carefully** — It usually tells you exactly what's wrong
2. **Check the relevant chapter** — Use references in main chapters
3. **Review the grammar reference** — Appendix A covers all syntax
4. **Look at examples** — See how features are used in context
5. **Check stdlib reference** — Appendix B covers all built-in functions

Remember: Most errors are type-related (wrong types), nil-related (using nil values), or collection-related (index out of bounds). Check these first.

---

## Error Message Quick Reference

| Error | Chapter | Appendix |
|-------|---------|----------|
| Type errors | 02, 13 | A |
| Nil errors | 11 | A |
| Collection errors | 03 | B |
| String errors | 06 | B |
| Function errors | 04 | A |
| Error handling | 12 | B |
| Class errors | 07, 09 | A |
| File I/O errors | 20 | B |
| Regex errors | 21 | B |

Good luck, and happy Zebra programming!

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
print("Value: " + x)  # ERROR: can't concatenate string + int directly
```

**Solution:**
```zebra
var x = 42
var message = x.toString()      # Convert int to string
print("Value: " + message)  # Now it works

# Or use interpolation
print("Value: ${x}")  # Better approach
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

**Solution:** `toInt()` returns a **plain** `int` (0 on bad input),
which can't be `nil`-checked — comparing it to `nil` compiles under
`zebra -c` but fails full compile (`error: comparison of 'i64' with
null`). Use `tryInt()`, which genuinely returns `int?`:

```zebra
var x = "10".tryInt()
var y = "5".tryInt()

if x != nil and y != nil
    var sum = x + y         # 15
    print(sum)
```

Note that `and`/`or` require `bool` operands — `x != nil and y != nil`
works because each side is a comparison, but `x and y` directly (with
`x`, `y` as `int?`) is a type error, not a way to check "both valid."

---

### "error: type mismatch: expected int, got str"

**What it means:** You're adding the wrong type to a collection. (Note:
this needs an explicitly typed `List(int)` — a bare `List()` with no
type argument is a *different* problem, a checker blind spot that
fails full compile with `expected expression, found 'anytype'` before
you'd ever see the type-mismatch error below.)

**Example:**
```zebra
var numbers: List(int) = List()
numbers.add(42)         # OK
numbers.add("hello")    # ERROR: expecting int, got str
```

**Solution:**
Check the collection's declared type and add matching values:
```zebra
var numbers: List(int) = List()
numbers.add(42)

var names: List(str) = List()
names.add("hello")
```

---

## Nil and Null Errors

### "error: cannot use nil value as int"

**What it means:** You're using a nullable value where a non-nullable value is required.

**Common cause:** Not checking for nil before using.

**Example:**
```zebra
var x: int? = nil
var result = x + 1      # ERROR: can't add to potentially nil value
```

**Solution:**
```zebra
var x: int? = nil

if x != nil
    var result = x + 1  # Safe—x is definitely int here
else
    print("x is nil")
```

**Alternative:** there's no `.unwrapOr()` method — use `orelse`:
```zebra
var x: int? = nil
var value = x orelse 0  # Use 0 if x is nil
var result = value + 1
```

---

### "error: cannot use value of type T as nullable type T?"

**What it means:** You're assigning non-nullable to nullable (usually OK) or vice versa (error).

**Example:**
```zebra
var x: int = 42
var y: int? = x       # OK: int can become int?

var z: int = y        # ERROR: int? cannot become int (might be nil!)
```

**Solution:**
```zebra
var y: int? = 42

if y != nil
    var z: int = y    # Safe now—y is definitely int
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
var x: int? = nil
print(x + 1)  # ERROR if x is nil
```

**Solution:**
```zebra
var x: int? = get_value()

if x != nil
    print(x + 1)
else
    print("Value not found")
```

---

## Collection Errors

### "error: index out of bounds"

**What it means:** You're accessing a list with an invalid index.

**Example:**
```zebra
var items: List(int) = List()
items.add(42)

var first = items.at(0)     # OK
var second = items.at(1)    # ERROR: index 1 doesn't exist
var third = items.at(-1)    # ERROR: negative index
```

**Solution:**
```zebra
var items: List(int) = List()
items.add(42)

if items.count() > 0
    var first = items.at(0)  # Safe

for i in 0.to(items.count())
    var item = items.at(i)   # Safe—i is valid
```

**Better:**
```zebra
for item in items
    print(item)  # No index worries
```

---

### `thread N panic: index out of bounds`

**What it means:** `.remove()` takes an **index**, not a value — there's
no remove-by-value overload — and removing an out-of-range index (an
empty list has none) panics the process rather than raising a
catchable error.

**Example:**
```zebra
var items: List(int) = List()
items.remove(0)        # PANIC: index out of bounds: index 0, len 0
```

**Solution:**
```zebra
var items: List(int) = List()

if items.count() > 0
    items.remove(0)
```

To remove by *value* instead of by index, filter it out:
```zebra
items = items.filter(def(x) = x != 42)
```

---

### "error: key not found in HashMap"

**What it means:** You're accessing a HashMap key that doesn't exist.

**Example:**
```zebra
var map = HashMap(str, int)()
var value = map.get("key")  # Returns nil, not an error

# But if you don't check nil:
var num = map.get("key")
var result = num + 1           # ERROR: num is nil!
```

**Solution:**
```zebra
var map = HashMap(str, int)()
var value = map.get("key")

if value != nil
    var result = value + 1
else
    print("Key not found")
```

Note: there's no `set`/`get` keyword conflict — those **are** the real
accessor names. `.put()` and `.fetch()` don't exist on `HashMap` at all.

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

### "error: index N outside slice of length M"

**What it means:** You're accessing a byte past the end of the string —
this fails at full compile with the message above; there's no
catchable exception, just an out-of-bounds crash.

**Example:**
```zebra
var text = "hello"
var last = text.charAt(10)      # PANIC: index 10 outside slice of length 5
```

**Solution:** guard with `.len` first. Also note `char` is a reserved
word — it can't be used as a variable name:

```zebra
var text = "hello"

if text.len > 10
    var byte_val = text.charAt(10)
    print(byte_val)
else
    print("Index out of range")

# Safe way
var last = text.charAt(text.len - 1)  # Get last byte
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
def add(a: int, b: int): int
    return a + b

var sum = add(5)        # ERROR: expects 2, got 1
var sum = add(1, 2, 3)  # ERROR: expects 2, got 3
```

**Solution:**
```zebra
def add(a: int, b: int): int
    return a + b

var sum = add(1, 2)     # Correct: 2 parameters
```

---

### "error: function parameter type mismatch"

**What it means:** You're passing wrong type to function.

**Example:**
```zebra
def greet(name: str): str
    return "Hello, ${name}"

greet(42)               # ERROR: expects str, got int
```

**Solution:**
```zebra
def greet(name: str): str
    return "Hello, ${name}"

greet("Alice")          # Correct: str parameter
greet(42.toString())    # Convert int to str
```

---

### "error: function does not return a value"

**What it means:** Your function says it returns something but doesn't.

**Example:**
```zebra
def get_value(): int
    if true
        return 42
    # Missing return for false case
```

**Solution:**
```zebra
def get_value(): int
    if true
        return 42
    else
        return 0    # Now all paths return

# Or use branch
def get_value(): int
    var result = 0
    if condition
        result = 42
    return result
```

---

## Error Handling Errors

Zebra has no `Result` type, and no `.isOk()` / `.isErr()` / `.value()`
/ `.unwrap()` / `.unwrapOr()` methods — those don't exist on anything.
Functions that can fail are declared `throws` and their errors
propagate or get handled with `?`, `catch`, or a method-level `catch`
clause.

### "error: expected type 'T', found 'anyerror!T'"

**What it means:** You called a `throws` function and used its result
directly, without propagating or catching the possible error.

**Example:**
```zebra
def operation(): int throws
    raise "fail"

def main()
    var value = operation()    # ERROR: unhandled `anyerror!int`
    print(value)
```

**Solution:** propagate with `?`, supply a fallback with `catch value`,
or attach a method-level `catch |e|` clause:

```zebra
def operation(): int throws
    raise "fail"

# Inline fallback
def main1()
    var value = operation() catch 0
    print(value)

# Propagate to a throws caller
def main2(): int throws
    var value = operation()?
    return value

# Handle explicitly
def main3()
    var value = operation()
    print(value)
catch |e|
    print("Error: ${e.message}")
```

Note that `File.read` / `File.write` are **not** `throws` — see
Chapter 20. Calling `.catch` on them is a different error (`expected
error union type, found 'str'`); guard with `File.exists()` instead.

---

## Class and Inheritance Errors

### "error: cannot assign to immutable field"

**What it means:** You're trying to modify a readonly/immutable field.

**Example:**
```zebra
class Person
    var name: str = ""

var person = Person()
person.name = "Alice"           # OK if var field

class Circle
    var radius: float = 0.0   # If immutable
    
var circle = Circle()
circle.radius = 5.0             # ERROR if immutable
```

**Solution:**
Ensure fields are declared with `var`:
```zebra
class Person
    var name: str = ""        # Mutable
    var age: int = 0          # Mutable

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
    def area(): float
    def perimeter(): float

class Circle implements Shape
    var radius: float = 0.0
    
    def area(): float
        return 3.14 * radius * radius
    
    # ERROR: missing perimeter() method
```

**Solution:**
```zebra
interface Shape
    def area(): float
    def perimeter(): float

class Circle implements Shape
    var radius: float = 0.0
    
    def area(): float
        return 3.14 * radius * radius
    
    def perimeter(): float
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

class Circle implements Shape
    # Provide all implementations
    # ...

var circle = Circle()  # OK
# var shape = Shape()  # ERROR
```

---

## File I/O Errors

### `thread N panic: File.read error`

**What it means:** `File.read` and `File.write` are plain-value calls,
not `throws` — there's no `Result` to check and no `.isErr()` to call.
A missing (or unreadable) file **panics the process outright**. See
Chapter 20 for the full explanation.

**Example:**
```zebra
var content = File.read("missing.txt")  # panics if the file is absent
```

**Solution:** guard with `File.exists()` before reading, or wrap the
call in your own `throws` function if you want `catch`/`?` semantics:

```zebra
if File.exists("missing.txt")
    var content = File.read("missing.txt")
    print(content)
else
    print("File not found")

# Or: wrap it so callers can use catch/?
def read_safely(path: str): str throws
    if not File.exists(path)
        raise "file not found: ${path}"
    return File.read(path)
```

---

### Writing to a location you can't write to

**What it means:** `File.write` panics the same way `File.read` does
if the write fails (e.g. a missing parent directory or a permissions
problem) — there's no return value to inspect.

**Solution:** Check the target directory exists first, or route writes
through your own `throws` wrapper the same way as `read_safely` above,
so a caller can `catch` a failure instead of crashing:

```zebra
def write_safely(path: str, content: str): void throws
    if not Dir.exists(Path.dirname(path))
        raise "directory does not exist: ${Path.dirname(path)}"
    File.write(path, content)
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

There's no `.matches()` method — `.match()` is the whole-string
anchored test (both ends must match), so it rejects "hello world"
against a pattern for just "hello":

```zebra
var pattern = Regex.compile("^hello$")
if not pattern.match("hello world")
    print("No match")
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
var parts: List(str) = List()
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
# Use appropriate algorithm
```

---

## Debugging Tips

### Print Debugging

```zebra
var x = 10
print("x = ${x}")  # Check variable value
print("After operation")  # Check execution flow

if condition
    print("Condition true: ${variable}")
```

### Assertion-Based Debugging

```zebra
assert x > 0, "x must be positive"
assert items.count() == 3, "Expected 3 items"
```

### Type Checking

`throws` is a function modifier, not part of a variable's type — `var
result: int throws = ...` is a parse error. Annotate the variable with
just its value type, and let the function signature carry `throws`:

```zebra
var x = 42
print(x.toString())  # Force type check

def operation(): int throws
    return 42

var result: int = operation() catch 0
```

### Null Checking

```zebra
var x: int? = get_value()

if x != nil
    print("Value: ${x}")
else
    print("Value is nil")
```

---

## Common Patterns for Error Avoidance

### Safe Navigation

```zebra
var x: int? = get_value()

if x != nil
    var result = x + 1
else
    print("Value not available")
```

### Safe Collection Access

```zebra
var items: List(int) = List()

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
var num = num_str.tryInt()   # toInt() is a plain int — can't be nil-checked

if num != nil
    print(num + 1)
```

### Safe Error Handling

```zebra
def risky_operation(): int throws
    return 42

def main()
    var value = risky_operation()
    print(value)
catch |e|
    print("Error: ${e.message}")
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

# Part 5: Ecosystem (Chapters 19-22)

## Chapter 19: Standard Library Tour

**Time:** 90 min | **Prereq:** 01-06

### Overview
Explore what's available before writing your own utilities.

### Core Modules

**String Methods:**
- `.len` — length
- `.upper()`, `.lower()` — case
- `.split()`, `.join()` — partition/combine
- `.trim()`, `.trimLeft()`, `.trimRight()` — whitespace
- `.contains()`, `.startsWith()`, `.endsWith()` — search
- `.replace()`, `.replaceAll()` — substitution
- `.charAt()`, `.substring()`, `.indexOf()` — access
- `.concat()` — combine
- `.reverse()` — flip

**Collection Methods:**
- `List.add()`, `List.remove()`, `List.count()`, `List.at()`
- `HashMap.put()`, `HashMap.fetch()`, `HashMap.contains()`
- `Set.add()`, `Set.remove()`, `Set.contains()`
- Iteration: `for item in collection`

**Math Functions:**
- Arithmetic: +, -, *, /, %
- Comparison: <, >, <=, >=, ==, !=
- Logical: and, or, not
- Type conversion: `.toString()`, `.toInt()`, `.toFloat()`

### Real World
Learning what exists prevents reinventing wheels.

---

## Chapter 20: File I/O and System Access

**Time:** 90 min | **Prereq:** 06, 12

### File Operations

```zebra
class FileIO
    shared
        def read_file(path as str) as Result(str, str)
            # Read entire file
            return Result.ok("content")
        
        def write_file(path as str, content as str) as Result(bool, str)
            # Write file
            return Result.ok(true)
        
        def file_exists(path as str) as bool
            return true
        
        def delete_file(path as str) as Result(bool, str)
            return Result.ok(true)
```

### Line-by-Line Reading

```zebra
class LineReader
    shared
        def process_lines(path as str) as Result(int, str)
            var lines = 0
            var content = read_file(path).unwrapOr("")
            for line in content.split("\n")
                if line.len > 0
                    lines = lines + 1
            return Result.ok(lines)
```

### System Access

```zebra
class System
    shared
        def args as List(str)
            # Command-line arguments
            return List()
        
        def env(name as str) as str?
            # Environment variables
            return nil
        
        def cwd as str
            # Current directory
            return "."
```

### Key Topics
- Text file reading/writing
- Binary files
- Directory operations
- Error handling for file not found
- Line-by-line processing
- CSV/JSON parsing basics

---

## Chapter 21: Regular Expressions (Deep Dive)

**Time:** 90 min | **Prereq:** 06

### Regex Pattern Syntax

**Literals:**
- `hello` — exact match
- `h.llo` — . matches any char
- `h*llo` — * = zero or more
- `h+llo` — + = one or more
- `h?llo` — ? = zero or one

**Classes:**
- `[abc]` — any of a, b, c
- `[a-z]` — range a through z
- `[^abc]` — NOT a, b, c
- `\d` — digit
- `\w` — word char
- `\s` — whitespace

**Anchors:**
- `^hello` — start of line
- `hello$` — end of line
- `\bhello\b` — word boundary

**Groups:**
- `(hello|hi)` — alternation
- `(ab)+` — repeat group

### Common Patterns

```zebra
// Email
var email_re = Regex.compile("[a-z0-9]+@[a-z]+\\.[a-z]+")

// Phone
var phone_re = Regex.compile("\\d{3}-\\d{3}-\\d{4}")

// URL
var url_re = Regex.compile("https?://[a-z0-9]+\\.[a-z]+")
```

### Operations

```zebra
class RegexOps
    shared
        def match(re as Regex, text as str) as bool
            return re.match(text)
        
        def find(re as Regex, text as str) as str?
            return re.find(text)
        
        def findAll(re as Regex, text as str) as List(str)
            var results as List(str) = List()
            # Collect all matches
            return results
        
        def replace(re as Regex, text as str, replacement as str) as str
            return re.replace(text, replacement)
        
        def split(re as Regex, text as str) as List(str)
            return re.split(text)
```

### Real-World Use Cases
- Email/phone validation
- Log parsing
- Data extraction
- Text normalization

---

## Chapter 22: FFI and Interop

**Time:** 90 min | **Prereq:** 02, 07, 12

### Calling C Code

```zebra
class CInterop
    shared
        def c_add(a as int, b as int) as int
            # Call C function
            return a + b
        
        def c_strlen(s as str) as int
            # Call strlen from C stdlib
            return 0
```

### Calling Zig Code

```zebra
class ZigInterop
    shared
        def zig_sqrt(x as float) as float
            # Call Zig function
            return 0.0
        
        def zig_random as int
            # Call Zig's random
            return 0
```

### Type Marshaling

```zebra
// C expects: int foo(const char* str, int* out_len)
// Zebra code:
def call_c_func(input as str)
    var out_len as int = 0
    var result = c_func(input, out_len)
    return out_len
```

### Safety Considerations
- Memory ownership
- Lifetime issues
- Type compatibility
- Error handling across boundaries

### Real-World Applications
- Calling system libraries
- Performance-critical code
- Platform-specific features
- Legacy code integration

---

## Appendices

### Appendix A: Grammar Reference

**Types:**
- Primitives: `int`, `float`, `bool`, `str`, `char`
- Collections: `List(T)`, `HashMap(K,V)`, `Set(T)`
- Nullable: `T?` (can be T or nil)
- Result: `Result(T, E)`

**Classes:**
```zebra
class Name
    var field as Type = default
    shared
        def shared_method
    def instance_method
```

**Interfaces:**
```zebra
interface Name
    def method_signature
```

**Functions:**
```zebra
def function_name(param as Type) as ReturnType
    return value
```

**Control Flow:**
- `if condition ... elif ... else ...`
- `while condition ... break ... continue`
- `for item in collection ...`
- `branch value on case ...`

---

### Appendix B: Built-in Functions and Stdlib

**I/O:**
- `print(value)` — output to console
- `println(value)` — output with newline
- `File.read(path)` — read file
- `File.write(path, content)` — write file

**Type Conversion:**
- `.toString()` — to string
- `.toInt()` — to integer
- `.toFloat()` — to float

**Collections:**
- `List.add()`, `List.remove()`, `List.count()`
- `HashMap.put()`, `HashMap.fetch()`, `HashMap.contains()`
- `Set.add()`, `Set.remove()`, `Set.contains()`

**String Methods:**
(See Chapter 19 for comprehensive list)

**System:**
- `sys.args()` — command-line arguments
- `sys.errln(msg)` — error output
- `File.exists(path)`, `File.delete(path)`

---

### Appendix C: Troubleshooting

**"error: arithmetic requires numeric type, got 'str'"**
→ Can't use `+` with strings. Use `.concat()` or interpolation: `"${var}"`

**"error: use of undefined identifier 'nil'"**
→ Variable type isn't nullable. Use `T?` not `T` if it can be nil.

**"error: cannot assign to immutable value"**
→ Field is read-only. Create setter method or use `var` not `shared var`

**"error: nil pointer"**
→ You unwrapped nil with `to!`. Check before unwrapping: `if x != nil`

**"error: unimplemented interface method"**
→ Your class doesn't implement all interface methods. Add the missing method.

**Performance tips:**
- Use StringBuilder for loop concatenation
- Lazy-load expensive resources
- Cache computed properties
- Avoid deep copying large structures

---

## Quick Reference

**Common Tasks:**

```zebra
// Read file
var content = File.read("file.txt")

// Parse lines
var lines = content.split("\n")

// Count items
for item in items
    count = count + 1

// Search list
for item in items
    if item.contains("search")
        print item

// Convert types
var num = "42".toInt()

// Handle nil
var value as str? = get_value()
if value != nil
    print value

// Handle errors
var result = operation()
if result.isErr()
    print result.errValue()
```

---

## Where to Go Next

- Build the three projects
- Contribute to Zebra itself
- Share projects on GitHub
- Write your own libraries

---

**You've completed the Zebra programming guide. Welcome to the community!**

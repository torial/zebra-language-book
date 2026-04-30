# 12: Error Handling

**Audience:** All  
**Time:** 120 minutes  
**Prerequisites:** 02-Values, 04-Functions, 07-Classes, 11-Nil-Tracking  
**You'll learn:** `throws` annotation, `raise` statement, `try`/`catch` blocks, error propagation, `catch` expressions

---

## The Big Picture

Zebra's primary error model is **exceptions** — `throws`/`raise`/`try`/`catch`.
The shape is inspired by Zig's error-set system (each `throws` function returns
`anyerror!T` in the generated Zig), but enriched: `raise "msg"` carries a
string message, and `raise "msg", obj` attaches a structured details object
via a thread-local `_error_ctx` — strictly more than Zig's payload-less
error enums.

`Result(T)` exists as a secondary error-as-value type for the cases where
that fits better (parser combinators, batch validators), but the
recommended default is `throws`.

Either way, error paths are explicit in the type system: you can see at a
glance which functions may fail and which cannot.

---

## Functions That Can Fail: `throws`

Mark a function with `throws` to indicate it may produce an error:

```zebra
# file: 12_throws_basic.zbr
# teaches: throws annotation
# chapter: 12-Error-Handling

class Validator
    static
        def parse_int(text: str): int throws
            if text.len == 0
                raise "Empty string"
            # Parse and return
            return 42

def main()
    var result = Validator.parse_int("123") catch 0
    print result
```

**Breakdown:**
- `: int throws` — This function returns `int` but may fail
- `raise "Empty string"` — Signal an error with a message
- `catch 0` — If the call fails, use `0` as the fallback value

---

## `raise` — Signaling Errors

Use `raise` to signal that something went wrong:

```zebra
# file: 12_raise.zbr
# teaches: raise statement
# chapter: 12-Error-Handling

class FileLoader
    static
        def load(path: str): str throws
            if path.len == 0
                raise "Path cannot be empty"
            if not path.endsWith(".txt")
                raise "Only .txt files supported"
            return "file contents here"
```

`raise` immediately exits the function and propagates the error to the caller.

---

## `try` / `catch` — Handling Errors

### Block Form

Use `try`/`catch` blocks for structured error handling:

```zebra
# file: 12_try_catch.zbr
# teaches: try/catch blocks
# chapter: 12-Error-Handling

def main()
    try
        var value = Validator.parse_int("")
        print "Got: ${value}"
    catch
        print "Failed to parse"
```

### Catch with Binding

Bind the error value to inspect it:

```zebra
# file: 12_catch_binding.zbr
# teaches: catch with error binding
# chapter: 12-Error-Handling

def main()
    try
        var value = Validator.parse_int("")
        print "Got: ${value}"
    catch |err|
        print "Error: ${err}"
```

### Catch with Type

Specify a type for the error binding:

```zebra
# file: 12_catch_typed.zbr
# teaches: catch with typed error binding
# chapter: 12-Error-Handling

def main()
    try
        var value = Validator.parse_int("")
        print value
    catch |err as str|
        print "String error: ${err}"
```

---

## `catch` Expression — Inline Fallbacks

For simple cases, use `catch` as an expression to provide a default:

```zebra
# file: 12_catch_expr.zbr
# teaches: catch expression for defaults
# chapter: 12-Error-Handling

def main()
    # Provide a default value if the call fails
    var value = Validator.parse_int("abc") catch 0
    print value  # 0

    # Catch with binding
    var msg = Validator.parse_int("") catch |e| "failed: ${e}"
    print msg
```

This is the most common pattern for simple error recovery.

---

## Error Propagation

![Error Propagation Flow](diagrams/05-error-propagation.png)

Functions annotated with `throws` can propagate errors from callees automatically. If a `throws` function calls another `throws` function without catching, the error propagates up:

```zebra
# file: 12_propagation.zbr
# teaches: error propagation
# chapter: 12-Error-Handling

class Parser
    static
        def parse_config(text: str): str throws
            if text.len == 0
                raise "Empty config"
            return "parsed"

class System
    static
        def load_system(config_text: str): str throws
            # If parse_config raises, the error propagates up
            var parsed = Parser.parse_config(config_text)
            return "System loaded with: ${parsed}"

def main()
    var result = System.load_system("data") catch "load failed"
    print result
```

---

## Real World: API Client

```zebra
# file: 12_api_client.zbr
# teaches: realistic error handling
# chapter: 12-Error-Handling

class APIClient
    static
        def fetch_user(user_id: int): str throws
            if user_id <= 0
                raise "Invalid user ID"
            if user_id == 1
                return "Alice"
            raise "User not found"

        def fetch_and_greet(user_id: int): str throws
            var user = fetch_user(user_id)
            return "Hello, ${user}!"

def main()
    # Using catch expression
    var greeting = APIClient.fetch_and_greet(1) catch "Could not greet"
    print greeting  # Hello, Alice!

    # Using try/catch block
    try
        var g2 = APIClient.fetch_and_greet(999)
        print g2
    catch |err|
        print "Error: ${err}"
```

---

## Exercises

### Exercise 1: Safe Division

Write a function `safe_divide(a: int, b: int): int throws` that raises on division by zero.

<details>
<summary>Solution</summary>

```zebra
class MathUtils
    static
        def safe_divide(a: int, b: int): int throws
            if b == 0
                raise "Division by zero"
            return a / b

def main()
    var r1 = MathUtils.safe_divide(10, 2) catch 0
    var r2 = MathUtils.safe_divide(10, 0) catch 0
    print r1  # 5
    print r2  # 0
```

</details>

### Exercise 2: Chained Error Handling

Write two functions that chain: `parse_age(text: str): int throws` and `validate_age(text: str): str throws` (returns "valid" if age is 0-150).

<details>
<summary>Solution</summary>

```zebra
class AgeValidator
    static
        def parse_age(text: str): int throws
            if text.len == 0
                raise "Empty input"
            var age = text.toInt()
            if age == nil
                raise "Not a number"
            return age

        def validate_age(text: str): str throws
            var age = parse_age(text)
            if age < 0
                raise "Age cannot be negative"
            if age > 150
                raise "Age too large"
            return "valid"

def main()
    try
        var result = AgeValidator.validate_age("25")
        print result  # valid
    catch |err|
        print "Error: ${err}"

    var r2 = AgeValidator.validate_age("200") catch "invalid"
    print r2  # invalid
```

</details>

---

## Next Steps

- → **13-Generics** — Type-safe containers
- → **15-Pipelines** — Chain operations gracefully

---

## Key Takeaways

- **`throws`** — Annotates functions that may fail
- **`raise`** — Signals an error, exits the function immediately
- **`try`/`catch`** — Block-form error handling with optional binding
- **`catch` expression** — Inline fallback: `expr catch default`
- **Errors propagate** — A `throws` function can let callee errors bubble up
- **Errors are explicit** — You always know which functions can fail

---

**Next:** Head to **13-Generics** for type-safe abstractions.

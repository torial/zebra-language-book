# 02: Values and Types

**Audience:** All  
**Time:** 90 minutes  
**Prerequisites:** 01-Getting-Started  
**You'll learn:** Zebra's type system, declaring variables, type inference, value vs. reference semantics

--- 

## The Big Picture

Every value in Zebra has a **type**. The type tells you:
- What kind of data it holds
- What operations you can perform on it
- How much memory it uses
- Whether it can be `nil`

Zebra's type system is **your best friend**—it catches mistakes at compile time instead of in production.

![Type Hierarchy Diagram](diagrams/01-type-hierarchy.png)

---

## Basic Types

### Integers

```zebra
# file: 02_integers.zbr
# teaches: integer types, arithmetic
# chapter: 02-Values-and-Types

def main()
    var age = 25
    var population = 8_000_000_000     # Underscores for readability
    var tiny: int8 = 100               # explicit narrow type
    var huge: int64 = 9_223_372_036_854_775_807

    print age
    print population
    print tiny
    print huge
```

**Integer types:**
- `int` — Default integer (usually 64-bit)
- `int8`, `int16`, `int32`, `int64` — Specific sizes
- `uint`, `uint8`, etc. — Unsigned (non-negative) integers

**Arithmetic:**
```zebra
var x = 10
var y = 3
print x + y    # 13
print x - y    # 7
print x * y    # 30
print x / y    # 3 (integer division)
print x % y    # 1 (remainder)
```

### Floating Point

```zebra
# file: 02_floats.zbr
# teaches: float types, precision
# chapter: 02-Values-and-Types

def main()
    var pi = 3.14159
    var precise: float64 = 3.141592653589793

    print pi
    print precise

    # Arithmetic
    var result = pi * 2.0
    print result
```

**Float types:**
- `float` — Default floating point (usually 64-bit)
- `float32`, `float64` — Specific precision

### Booleans

```zebra
# file: 02_bools.zbr
# teaches: boolean values, logic
# chapter: 02-Values-and-Types

def main()
    var is_ready = true
    var is_finished = false

    print is_ready
    print is_finished

    # Logic
    print true and false   # false
    print true or false    # true
    print not true         # false
```

### Strings

```zebra
# file: 02_strings.zbr
# teaches: string type, string operations
# chapter: 02-Values-and-Types

def main()
    var greeting = "Hello"
    var name = "World"

    print greeting
    print greeting.len      # 5
    print greeting.upper()  # HELLO
    print name.lower()      # world

    # Concatenation
    var message = greeting.concat(" ").concat(name)
    print message           # Hello World
```

**String methods** (we'll cover these fully in Chapter 06):
- `.len` — Length
- `.upper()` — Uppercase
- `.lower()` — Lowercase
- `.concat()` — Concatenate
- `.contains()` — Check for substring
- `.split()` — Split by delimiter

---

## Declaring Variables

### Type Inference (the default)

Zebra infers the type from the right-hand side. Most variables don't need an annotation:

```zebra
var age = 25          # Inferred as int
var name = "Alice"    # Inferred as str
var active = true     # Inferred as bool
var pi = 3.14         # Inferred as float
```

### Explicit Types (when they aid the reader)

You can always pin the type explicitly. Reach for this when:
- the right-hand side is a function call whose return type isn't obvious to a reader
- you want a different concrete width (`int8`, `float32`) than inference would pick
- the variable starts as `nil` or `undefined` and inference can't narrow it

```zebra
var age: int = 25                          # redundant; inference would do
var payment_amount: float = compute_total()  # earns its keep — return type isn't visible
var counter: int8 = 0                      # narrower than the default int
var maybeUser: User? = nil                 # required: nil alone has no type
```

The book uses inference by default and adds annotations only where they earn their keep.

### Naming Conventions

Use `snake_case` for variables:

```zebra
var user_id = 42           # ✅ Good
var UserID = 42            # ❌ Avoid (that's for classes)
var user_id_number = 42    # ✅ Clear but verbose
var uid = 42               # ❌ Too abbreviated
```

---

## Comparison and Equality

```zebra
# file: 02_comparisons.zbr
# teaches: comparison operators
# chapter: 02-Values-and-Types

def main()
    var x = 10
    var y = 20

    print x == y    # false (equal)
    print x != y    # true (not equal)
    print x < y     # true (less than)
    print x > y     # false (greater than)
    print x <= y    # true (less or equal)
    print x >= y    # false (greater or equal)

    var name = "Alice"
    print name == "Alice"   # true
    print name == "Bob"     # false
```

---

## Type Conversions

### Implicit Conversion (When Safe)

```zebra
var small: int8 = 100
var big: int = small  # ✅ Fine: int8 → int is always safe
```

### Explicit Conversion

```zebra
# file: 02_conversions.zbr
# teaches: type conversion
# chapter: 02-Values-and-Types

def main()
    var x = 42
    var s = x.toString()      # int → str
    print s

    var pi = 3.14
    var i = pi.toInt()        # float → int (loses decimal)
    print i                   # 3

    var flag = true
    var b = flag.toString()   # bool → str
    print b                   # true
```

---

## Nullable Types (Introduction)

Sometimes a value might not exist. Zebra uses `?` to mark this:

```zebra
# file: 02_nullables.zbr
# teaches: nullable types introduction
# chapter: 02-Values-and-Types

def main()
    var name: str? = "Alice"    # Can hold str or nil
    var empty: str? = nil       # Explicitly nil

    # You must check before using
    if name != nil
        print name              # Safe to use

    if empty != nil
        print empty
    else
        print "Name is empty"
```

**Key point:** `str?` means "string or nil". We'll explore nil tracking fully in Chapter 11.

### If you're new to programming

> A **nullable type** is like an optional value. Sometimes you have it, sometimes you don't.
> Instead of errors when it's missing, Zebra lets you check first.

---

## Type Mismatch Errors

Zebra prevents mixing types unsafely:

```zebra
var x: int = "hello"  # ❌ Error: can't assign str to int
var y: str = 42       # ❌ Error: can't assign int to str
var z: int = 3.14     # ❌ Error: can't assign float to int
```

**Why?** Type safety catches bugs before they happen. You can't accidentally treat a string as a number.

---

## Real World: Processing User Data

```zebra
# file: 02_user_data.zbr
# teaches: realistic variable use
# chapter: 02-Values-and-Types

class User
    var id: int
    var name: str
    var email: str
    var age: int
    var is_active: bool

def main()
    # Create a user
    var user = User()
    user.id = 1
    user.name = "Alice"
    user.email = "alice@example.com"
    user.age = 30
    user.is_active = true

    # Display
    print "User: ${user.name}"
    print "Email: ${user.email}"
    print "Age: ${user.age}"
    print "Active: ${user.is_active}"
```

---

## Common Mistakes

> ❌ **Mistake:** Skipping a type annotation when the right-hand side is opaque
>
> ```zebra
> var result = compute()  # What's the type?
> ```
>
> 💡 **Why it matters:** Inference is fine when the literal makes the type obvious (`var x = 25`). When the RHS is a function call whose return type isn't visible at the call site, an annotation pays for itself in readability.
>
> ✅ **Better:**
> ```zebra
> var result: int = compute()  # Clear: it's an int
> ```

> ❌ **Mistake:** Mixing types in arithmetic
>
> ```zebra
> var x = 10
> var y = 3.14
> print x + y  # ❌ Can't add int + float
> ```
>
> 💡 **Why:** Different types might need different handling.
>
> ✅ **Better:**
> ```zebra
> var x = 10.0
> var y = 3.14
> print x + y  # ✅ Both float
> ```

> ❌ **Mistake:** Using a nullable type without checking
>
> ```zebra
> var name: str? = nil
> print name.upper()  # ❌ Error: nil doesn't have .upper()
> ```
>
> ✅ **Better:**
> ```zebra
> var name: str? = nil
> if name != nil
>     print name.upper()  # Safe
> ```

---

## Exercises

### Exercise 1: Type Conversion

Write a program that:
1. Creates an integer variable
2. Creates a float variable
3. Converts both to strings
4. Prints them

<details>
<summary>Solution</summary>

```zebra
def main()
    var count = 42
    var price = 19.99

    var count_str = count.toString()
    var price_str = price.toString()

    print "Count: ${count_str}"
    print "Price: ${price_str}"
```

**Output:**
```
Count: 42
Price: 19.99
```

</details>

### Exercise 2: Comparisons

Write a program that compares two numbers and prints which is larger:

<details>
<summary>Solution</summary>

```zebra
def main()
    var x = 100
    var y = 75

    if x > y
        print "${x} is larger than ${y}"
    else
        print "${y} is larger than ${x}"
```

**Output:**
```
100 is larger than 75
```

</details>

### Exercise 3: User Profile

Create a data structure to hold user information (name, age, email) and print a profile:

<details>
<summary>Solution</summary>

```zebra
class Person
    var name: str
    var age: int
    var email: str

def main()
    var person = Person()
    person.name = "Carol"
    person.age = 28
    person.email = "carol@example.com"

    print "Name: ${person.name}"
    print "Age: ${person.age}"
    print "Email: ${person.email}"
```

</details>

---

## Next Steps

- → **03-Collections** — Lists and HashMaps
- → **04-Functions** — Write reusable code
- → **11-Nil-Tracking** — Deep dive into nullable types

---

## Key Takeaways

- **Every value has a type** — Integers, floats, booleans, strings, and more
- **Types are checked at compile time** — Catches bugs early
- **Use type inference when obvious, explicit types when clarity matters**
- **Conversions are explicit** — No silent type changes
- **Nullable types use `?`** — `str?` can be string or nil
- **Always check nil before using** — `if value != nil { ... }`

---

**Next:** Head to **03-Collections** to learn Lists and HashMaps.

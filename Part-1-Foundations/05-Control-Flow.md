# 05: Control Flow

**Audience:** All  
**Time:** 90 minutes  
**Prerequisites:** 01-04  
**You'll learn:** if/else, match, for loops, while loops, guards, break/continue

---
 
## The Big Picture

**Control flow** directs which code runs based on conditions. Instead of executing every line in order, you:
- **Skip code** if a condition isn't met (`if`)
- **Repeat code** until done (`for`, `while`)
- **Branch** based on many options (`match`)

---

## If / Else

### Basic If

```zebra
# file: 05_if.zbr
# teaches: conditional execution
# chapter: 05-Control-Flow

def main()
    var age = 18

    if age >= 18
        print "You can vote"
```

### If / Else

```zebra
# file: 05_if_else.zbr
# teaches: if-else branching
# chapter: 05-Control-Flow

def main()
    var score = 75

    if score >= 90
        print "A"
    else if score >= 80
        print "B"
    else if score >= 70
        print "C"
    else
        print "F"
```

**Breakdown:**
- `if condition` — Execute if true
- `else if condition` — Try the next condition (Zebra spells the chain `else if`, two words)
- `else` — Default case (if all above are false)

### Multiple Conditions

```zebra
# file: 05_conditions.zbr
# teaches: boolean logic
# chapter: 05-Control-Flow

def main()
    var age = 25
    var has_license = true

    if age >= 18 and has_license
        print "Can drive"

    if age < 16 or not has_license
        print "Cannot drive"
```

**Operators:**
- `and` — Both must be true
- `or` — At least one must be true
- `not` — Flip the value

---

## Match (Pattern Matching)

**Match** is more powerful than if/else. It handles many cases elegantly.

### Simple Match

```zebra
# file: 05_match.zbr
# teaches: pattern matching
# chapter: 05-Control-Flow

def main()
    var color = "red"

    branch color
        on "red"
            print "Stop"
        on "yellow"
            print "Caution"
        on "green"
            print "Go"
        else
            print "Unknown"
```

### Match With Types

Zebra's idiomatic way to dispatch on "what kind of thing is this" is a
**union** plus `branch`. Each variant of the union carries its own data:

```zebra
# file: 05_match_type.zbr
# teaches: type-based matching with unions
# chapter: 05-Control-Flow

union Pet
    dog: str       # name
    cat: str       # name
    fish: str      # tank-size

def main()
    var pet: Pet = Pet.dog("Rex")

    branch pet
        on Pet.dog as name
            print "${name} says: Woof!"
        on Pet.cat as name
            print "${name} says: Meow!"
        on Pet.fish as size
            print "tank: ${size}"
        else
            pass
```

Zebra has no class inheritance, so dispatching on a class hierarchy isn't
the natural pattern here. See **Chapter 09 (Composition and Mixins)** for
why, and **Chapter 07b (Structs and Unions)** for more on tagged unions.

### If you know Python

```python
# Python
match color:
    case "red":
        print("Stop")
    case "green":
        print("Go")

# Zebra
branch color
    on "red"
        print "Stop"
    on "green"
        print "Go"
```

---

## Loops

### For Loop (Iteration)

```zebra
# file: 05_for.zbr
# teaches: for loop iteration
# chapter: 05-Control-Flow

def main()
    var fruits = List(str)()
    fruits.add("apple")
    fruits.add("banana")
    fruits.add("cherry")

    for fruit in fruits
        var f: str = fruit       # typed local for {s} formatting
        print f

    # Numeric range — n.to(end) is exclusive on `end`.
    var i = 0
    while i < fruits.count()
        print "Item ${i}: ${fruits.at(i)}"
        i = i + 1
```

### While Loop (Condition-Based)

```zebra
# file: 05_while.zbr
# teaches: while loop
# chapter: 05-Control-Flow

def main()
    var count = 0

    while count < 5
        print "Count: ${count}"
        count = count + 1

    print "Done!"
```

### Break and Continue

```zebra
# file: 05_break_continue.zbr
# teaches: loop control
# chapter: 05-Control-Flow

def main()
    # Break: exit loop early
    var i = 0
    while true
        if i == 5
            break
        print i
        i = i + 1

    # Continue: skip to next iteration. Numeric ranges use either `start:end`
    # or the equivalent method form `start.to(end)` — both are exclusive on
    # `end` (so `1.to(11)` yields 1,2,...,10).
    for num in 1.to(11)
        if num % 2 == 0
            continue
        print num  # Prints odd numbers only
```

---

## Guards

**Guards** are conditions that must be true for code to run.

```zebra
# file: 05_guards.zbr
# teaches: guard conditions
# chapter: 05-Control-Flow

def process(name: str)
    # Zebra has a `guard` form for early returns:
    guard name.len > 0, return
    guard name.len <= 100, return

    # Process only if all guards passed
    print "Processing: ${name}"

def main()
    process("")            # Guard fails — returns early
    process("Alice")       # Guards pass — processes
    process("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")  # too long — returns early
```

The `guard cond, return` form reads as "the call must satisfy `cond`; otherwise return now". It's equivalent to `if not cond: return` but states the precondition positively. Block form (`guard cond ... else`) is also available — see QUICKSTART §13.

---

## Real World: Data Validation

```zebra
# file: 05_validation.zbr
# teaches: practical control flow
# chapter: 05-Control-Flow

def validate_email(email: str): bool
    # Check not empty
    if email.len == 0
        return false

    # Check has @
    if not email.contains("@")
        return false

    # Check has domain
    var parts: List(str) = email.split("@")
    if parts.count() != 2
        return false

    var domain: str = parts.at(1)
    if not domain.contains(".")
        return false

    return true

def main()
    var emails = List(str)()
    emails.add("alice@example.com")
    emails.add("invalid.email")
    emails.add("bob@domain.co")

    for email in emails
        var e: str = email
        if validate_email(e)
            print "Valid: ${e}"
        else
            print "Invalid: ${e}"
```

---

## Common Patterns

### Early Return

```zebra
def process_order(order_id: int): bool
    var order = fetch_order(order_id)
    
    if order == nil
        return false
    
    if order.total == 0
        return false
    
    if not order.has_items
        return false
    
    # Do the real processing
    charge_card(order)
    ship_items(order)
    return true
```

### Nested Conditions

```zebra
for user in users
    if user.is_active
        for order in user.orders
            if order.status == "pending"
                process_order(order)
```

### Else-If Chain

```zebra
if age < 13
    category = "child"
else if age < 18
    category = "teen"
else if age < 65
    category = "adult"
else
    category = "senior"
```

---

## Common Mistakes

> ❌ **Mistake:** Forgetting the condition
>
> ```zebra
> if age >= 18  # Missing condition or wrong structure
>     print "Adult"
>     print "Extra"  # Both print regardless
> ```
>
> ✅ **Better:**
> ```zebra
> if age >= 18
>     print "Adult"
> else
>     print "Minor"
> ```

> ❌ **Mistake:** Unreachable code
>
> ```zebra
> if x > 0
>     return true
> else
>     return false
> return false  # ❌ Never reached
> ```
>
> ✅ **Better:**
> ```zebra
> if x > 0
>     return true
> return false
> ```

> ❌ **Mistake:** Mutating collection while iterating
>
> ```zebra
> for fruit in fruits
>     if fruit == "apple"
>         fruits.remove(0)  # ❌ Unsafe — modifying during iteration
> ```
>
> ✅ **Better:**
> ```zebra
> var to_remove = List(int)()           # collect indices
> var idx = 0
> for fruit in fruits
>     if fruit == "apple"
>         to_remove.add(idx)
>     idx = idx + 1
> # Remove in reverse so earlier indices stay valid.
> var k = to_remove.count() - 1
> while k >= 0
>     fruits.remove(to_remove.at(k))
>     k = k - 1
> ```

---

## Exercises

### Exercise 1: Grade Calculator

Write a function that converts numeric scores to letter grades:

<details>
<summary>Solution</summary>

```zebra
def grade_to_letter(score: int): str
    if score >= 90
        return "A"
    else if score >= 80
        return "B"
    else if score >= 70
        return "C"
    else if score >= 60
        return "D"
    else
        return "F"

def main()
    var scores = List(int)()
    scores.add(95)
    scores.add(75)
    scores.add(88)
    scores.add(62)

    for score in scores
        var grade = grade_to_letter(score)
        print "${score} = ${grade}"
```

</details>

### Exercise 2: Find Maximum

Iterate through a list and find the maximum value:

<details>
<summary>Solution</summary>

```zebra
def find_max(nums: List(int)): int
    if nums.count() == 0
        return 0

    var max_val = nums.at(0)
    for num in nums
        if num > max_val
            max_val = num
    return max_val

def main()
    var nums = List(int)()
    nums.add(10)
    nums.add(45)
    nums.add(23)
    nums.add(89)
    nums.add(34)

    var max = find_max(nums)
    print "Max: ${max}"  # 89
```

</details>

### Exercise 3: Filter With Control Flow

Count elements matching a condition:

<details>
<summary>Solution</summary>

```zebra
def count_evens(nums: List(int)): int
    var count = 0
    for num in nums
        if num % 2 == 0
            count = count + 1
    return count

def main()
    var nums = List(int)()
    nums.add(1)
    nums.add(2)
    nums.add(3)
    nums.add(4)
    nums.add(5)
    nums.add(6)

    var even_count = count_evens(nums)
    print "Even numbers: ${even_count}"  # 3
```

</details>

---

## Next Steps

- → **06-Strings-and-Unicode** — Text manipulation
- → **05-Control-Flow** — Combine control flow with strings
- 🏋 **Project-1-CLI-Tool** — Use loops and conditions extensively

---

## Key Takeaways

- **if/else** handles simple binary choices
- **match** (branch) is better for many cases
- **for** loops iterate over collections
- **while** loops repeat based on conditions
- **break** exits loops, **continue** skips iterations
- **Early return** makes functions clearer
- **Guard clauses** prevent "arrow code" (deeply nested if statements)

---

**Next:** Head to **06-Strings-and-Unicode** to work with text.

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

class Main
    static
        def main
            var age: int = 18
            
            if age >= 18
                print "You can vote"
```

### If / Else

```zebra
# file: 05_if_else.zbr
# teaches: if-else branching
# chapter: 05-Control-Flow

class Main
    static
        def main
            var score: int = 75
            
            if score >= 90
                print "A"
            elif score >= 80
                print "B"
            elif score >= 70
                print "C"
            else
                print "F"
```

**Breakdown:**
- `if condition` — Execute if true
- `elif condition` — Else-if (try next condition)
- `else` — Default case (if all above are false)

### Multiple Conditions

```zebra
# file: 05_conditions.zbr
# teaches: boolean logic
# chapter: 05-Control-Flow

class Main
    static
        def main
            var age: int = 25
            var has_license: bool = true
            
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

class Main
    static
        def main
            var color: str = "red"
            
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

class Main
    static
        def main
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

class Main
    static
        def main
            var fruits: List(str) = List()
            fruits.add("apple")
            fruits.add("banana")
            fruits.add("cherry")
            
            for fruit in fruits
                print fruit
            
            # With index (if supported)
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

class Main
    static
        def main
            var count: int = 0
            
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

class Main
    static
        def main
            # Break: exit loop early
            var i = 0
            while true
                if i == 5
                    break
                print i
                i = i + 1
            
            # Continue: skip to next iteration
            for num in 1..10
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

class Main
    static
        def process(name: str)
            # Early return if invalid
            if name.len == 0
                return
            if name.len > 100
                return
            
            # Process only if valid
            print "Processing: ${name}"

        def main
            process("")            # Returns early
            process("Alice")       # Processes
            process("x" * 200)     # Returns early
```

---

## Real World: Data Validation

```zebra
# file: 05_validation.zbr
# teaches: practical control flow
# chapter: 05-Control-Flow

class Email
    var address: str

class Validator
    static
        def validate_email(email: str): bool
            # Check not empty
            if email.len == 0
                return false
            
            # Check has @
            if not email.contains("@")
                return false
            
            # Check has domain
            var parts = email.split("@")
            if parts.count() != 2
                return false
            
            var domain = parts.at(1)
            if not domain.contains(".")
                return false
            
            return true

class Main
    static
        def main
            var emails: List(str) = List()
            emails.add("alice@example.com")
            emails.add("invalid.email")
            emails.add("bob@domain.co")
            
            for email in emails
                if Validator.validate_email(email)
                    print "Valid: ${email}"
                else
                    print "Invalid: ${email}"
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
elif age < 18
    category = "teen"
elif age < 65
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
>         fruits.remove(fruit)  # ❌ Unsafe
> ```
>
> ✅ **Better:**
> ```zebra
> var to_remove: List(str) = List()
> for fruit in fruits
>     if fruit == "apple"
>         to_remove.add(fruit)
> for fruit in to_remove
>     fruits.remove(fruit)
> ```

---

## Exercises

### Exercise 1: Grade Calculator

Write a function that converts numeric scores to letter grades:

<details>
<summary>Solution</summary>

```zebra
class Grader
    static
        def grade_to_letter(score: int): str
            if score >= 90
                return "A"
            elif score >= 80
                return "B"
            elif score >= 70
                return "C"
            elif score >= 60
                return "D"
            else
                return "F"

class Main
    static
        def main
            var scores: List(int) = List()
            scores.add(95)
            scores.add(75)
            scores.add(88)
            scores.add(62)
            
            for score in scores
                var grade = Grader.grade_to_letter(score)
                print "${score} = ${grade}"
```

</details>

### Exercise 2: Find Maximum

Iterate through a list and find the maximum value:

<details>
<summary>Solution</summary>

```zebra
class Finder
    static
        def find_max(nums: List(int)) as int
            if nums.count() == 0
                return 0
            
            var max_val = nums.at(0)
            for num in nums
                if num > max_val
                    max_val = num
            return max_val

class Main
    static
        def main
            var nums: List(int) = List()
            nums.add(10)
            nums.add(45)
            nums.add(23)
            nums.add(89)
            nums.add(34)
            
            var max = Finder.find_max(nums)
            print "Max: ${max}"  # 89
```

</details>

### Exercise 3: Filter With Control Flow

Count elements matching a condition:

<details>
<summary>Solution</summary>

```zebra
class Counter
    static
        def count_evens(nums: List(int)) as int
            var count = 0
            for num in nums
                if num % 2 == 0
                    count = count + 1
            return count

class Main
    static
        def main
            var nums: List(int) = List()
            nums.add(1)
            nums.add(2)
            nums.add(3)
            nums.add(4)
            nums.add(5)
            nums.add(6)
            
            var even_count = Counter.count_evens(nums)
            print "Even numbers: ${even_count}"  # 3
```

</details>

---

## Next Steps

- → **06-Strings-and-Unicode** — Text manipulation
- → **05-Control-Flow** — Combine control flow with strings
- 🏋️ **Project-1-CLI-Tool** — Use loops and conditions extensively

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

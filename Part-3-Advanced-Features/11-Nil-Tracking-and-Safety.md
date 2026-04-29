# 11: Nil Tracking and Safety

**Audience:** All  
**Time:** 120 minutes  
**Prerequisites:** 02-Values, 05-Control-Flow, 07-Classes  
**You'll learn:** Nullable types, nil checking, type narrowing, the `to!` operator, optionals

---

## The Big Picture

**Nil** (null/nothing) is one of the most common sources of bugs. Zebra's **nil tracking** forces you to handle it:

> "A billion-dollar mistake." — Tony Hoare, on inventing the null reference

Zebra says: **Explicit nil is safe. Implicit nil is forbidden.**
 
---

## Nullable Types

### Marking Optionality

```zebra
# file: 11_nullable.zbr
# teaches: nullable types
# chapter: 11-Nil-Tracking-and-Safety

class User
    var name: str      # Can't be nil
    var nickname: str? # Can be nil
    var bio: str?      # Can be nil

class Main
    static
        def main
            var user = User()
            user.name = "Alice"    # ✅ Fine
            user.nickname = nil    # ✅ Allowed (it's str?)
            user.bio = "Developer" # ✅ Can assign string to str?
            
            # This won't compile:
            # var empty: str = nil  # ❌ str can't be nil
```

**Key point:** The `?` mark means "this can be nil or the type."

---

## Nil Checking

### Safe Access Pattern

```zebra
# file: 11_nil_check.zbr
# teaches: nil checking
# chapter: 11-Nil-Tracking-and-Safety

class Main
    static
        def main
            var nickname: str? = "Bobby"
            var empty: str? = nil
            
            # Check before using
            if nickname != nil
                print nickname     # Safe: known to not be nil
            
            if empty == nil
                print "No nickname set"
            else
                print empty
            
            # Two ways to check:
            if nickname != nil
                print "Has nickname"
            
            if nickname == nil
                print "No nickname"
            else
                print "Has: ${nickname}"
```

### Type Narrowing

![Type Narrowing Flow](diagrams/04-type-narrowing.png)

After checking, the type is narrowed:

```zebra
# file: 11_narrowing.zbr
# teaches: type narrowing
# chapter: 11-Nil-Tracking-and-Safety

class Main
    static
        def process_name(input: str?)
            if input == nil
                return  # Exit early if nil
            
            # From here, input is narrowed to str
            print input.len        # ✅ Safe: know it's str
            print input.upper()    # ✅ Safe
```

---

## The `to!` Operator (Unwrap)

**Warning:** Only use when you're absolutely certain the value isn't nil.

```zebra
# file: 11_unwrap.zbr
# teaches: unwrap operator
# chapter: 11-Nil-Tracking-and-Safety

class Main
    static
        def main
            var name: str? = "Alice"
            
            # Unwrap: assert it's not nil
            var safe_name = name to!
            print safe_name        # Now just str
            
            # If it WAS nil, this would crash
            var empty: str? = nil
            # var crash = empty to!  # ❌ Would panic at runtime
```

---

## Unwrap with Fallback

```zebra
# file: 11_unwrap_or.zbr
# teaches: safe unwrapping
# chapter: 11-Nil-Tracking-and-Safety

class Main
    static
        def get_user_name(user_id: int): str?
            if user_id == 1
                return "Alice"
            return nil
        
        def main
            var name = get_user_name(1)
            
            # Option 1: Check and use default
            if name != nil
                print name
            else
                print "Unknown user"
            
            # Option 2: if method exists, unwrapOr
            # var safe_name = name.unwrapOr("Guest")
            # print safe_name
```

---

## Real World: Database Queries

```zebra
# file: 11_database.zbr
# teaches: nil in realistic scenarios
# chapter: 11-Nil-Tracking-and-Safety

class User
    var id: int
    var name: str
    var email: str?

class UserDatabase
    static
        def find_user(user_id: int): User?
            if user_id == 1
                var user = User()
                user.id = 1
                user.name = "Alice"
                user.email = "alice@example.com"
                return user
            return nil
        
        def find_user_email(user_id: int): str?
            var user = find_user(user_id)
            if user == nil
                return nil
            return user.email

class Main
    static
        def main
            var user = UserDatabase.find_user(1)
            if user != nil
                print user.name
                if user.email != nil
                    print user.email
                else
                    print "No email on file"
            else
                print "User not found"
            
            # Chaining nil checks
            var email = UserDatabase.find_user_email(999)
            if email != nil
                print "Email: ${email}"
            else
                print "User not found"
```

---

## Common Patterns

### Optional Chaining

```zebra
def get_user_city(user_id: int): str?
    var user = find_user(user_id)
    if user == nil
        return nil
    var address = get_address(user.id)
    if address == nil
        return nil
    return address.city
```

### Guard Clauses

```zebra
def process(data: str?)
    if data == nil
        return
    if data.len == 0
        return
    # Now process safely
    do_work(data)
```

---

## If you're new to programming

> **Nil** means "nothing" or "no value." Different languages call it null, None, undefined.
>
> Zebra makes you declare which variables **can** be nil with `?`. This prevents accidental crashes.
>
> **Type narrowing** means the compiler recognizes that after you check `if x != nil`, you can safely use `x`.

---

## Common Mistakes

> ❌ **Mistake:** Forgetting to check for nil
>
> ```zebra
> var email: str? = get_email()
> print email.len  # ❌ Crash if email is nil!
> ```
>
> ✅ **Better:**
> ```zebra
> var email: str? = get_email()
> if email != nil
>     print email.len  # ✅ Safe
> ```

> ❌ **Mistake:** Using `to!` without certainty
>
> ```zebra
> var value: str? = get_value()
> print value to!  # ❌ Crashes if value is nil
> ```
>
> ✅ **Better:**
> ```zebra
> var value: str? = get_value()
> if value != nil
>     print value  # ✅ Safe, or use unwrapOr
> ```

> ❌ **Mistake:** Assigning nil to non-nullable
>
> ```zebra
> var name: str = nil  # ❌ str can't be nil
> ```
>
> ✅ **Better:**
> ```zebra
> var name: str? = nil  # ✅ Declares it can be nil
> ```

---

## Exercises

### Exercise 1: Find User Email

Write a function that safely retrieves a user's email:

<details>
<summary>Solution</summary>

```zebra
class User
    var id as int
    var name as str
    var email as str?

class UserDB
    shared
        def find_user(id as int) as User?
            if id == 1
                var user = User()
                user.id = 1
                user.name = "Alice"
                user.email = "alice@example.com"
                return user
            return nil
        
        def get_email(user_id as int) as str?
            var user = find_user(user_id)
            if user == nil
                return nil
            return user.email

class Main
    shared
        def main
            var email = UserDB.get_email(1)
            if email != nil
                print "Email: ${email}"
            else
                print "User not found or no email"
```

</details>

### Exercise 2: Safe Division

Write a division function that returns nil on error:

<details>
<summary>Solution</summary>

```zebra
class Calculator
    static
        def safe_divide(a: float, b: float): float?
            if b == 0.0
                return nil
            return a / b

class Main
    static
        def main
            var result = Calculator.safe_divide(10.0, 2.0)
            if result != nil
                print "Result: ${result}"
            
            var bad = Calculator.safe_divide(10.0, 0.0)
            if bad != nil
                print bad
            else
                print "Cannot divide by zero"
```

</details>

### Exercise 3: Nullable Chain

Write a function that navigates nullable fields:

<details>
<summary>Solution</summary>

```zebra
class Profile
    var name: str
    var bio: str?

class User
    var id: int
    var profile: Profile?

class UserService
    static
        def get_user_bio(user_id: int): str?
            var user = find_user(user_id)
            if user == nil
                return nil
            var profile = user.profile
            if profile == nil
                return nil
            return profile.bio
        
        def find_user(id: int): User?
            if id == 1
                var user = User()
                user.id = 1
                var profile = Profile()
                profile.name = "Alice"
                profile.bio = "Developer"
                user.profile = profile
                return user
            return nil

class Main
    static
        def main
            var bio = UserService.get_user_bio(1)
            if bio != nil
                print "Bio: ${bio}"
            else
                print "No bio found"
```

</details>

---

## Next Steps

- → **12-Error-Handling** — Results for error cases
- → **14-Contracts** — Enforce non-nil invariants
- 🏋️ **Project-2-HTTP-Server** — Handle nil API responses

---

## Key Takeaways

- **`?` marks nullable types** — `str?` can be string or nil
- **Check before using** — `if value != nil { ... }`
- **Type narrowing** — Compiler recognizes after checks
- **`to!` unwraps** — Only when certain it's not nil
- **Guard clauses** — Exit early if nil
- **Nil safety prevents crashes** — It's a feature, not a limitation

---

**Next:** Head to **12-Error-Handling** for Results and error propagation.

# 14: Contracts and Assertions

**Audience:** Experienced programmers  
**Time:** 90 minutes  
**Prerequisites:** 04-Functions-and-Scope, 07-Classes-and-Instances  
**You'll learn:** Design by contract, preconditions, postconditions, invariants, assertions

---

## The Big Picture

**Contracts** are promises you make about your code's behavior:

- **Precondition:** "I promise the input will be valid if you call me this way"
- **Postcondition:** "I promise the output will satisfy this if I complete"
- **Invariant:** "I promise this property stays true throughout execution"

Contracts aren't just comments—they're **executable checks** that prevent bugs early and document intent clearly.

```
def withdraw(amount as int) as Result(bool, str)
    # Precondition: amount > 0
    # Precondition: balance >= amount
    # Postcondition: balance decreased by amount
    # Postcondition: no exception raised
```

This is **Design by Contract** (from Eiffel, a language Zebra inherits from).

---

## Preconditions: Validating Inputs

A **precondition** says "if you call me, the input must be valid":

```zebra
# file: 14_preconditions.zbr
# teaches: precondition checking
# chapter: 14-Contracts-and-Assertions

class Bank
    var balance: int = 100
    
    def withdraw(amount: int): bool throws
        # Precondition: amount must be positive
        if amount <= 0
            raise "Amount must be positive"
        
        # Precondition: sufficient funds
        if balance < amount
            raise "Insufficient funds"
        
        balance = balance - amount
        return true

class Main
    static
        def main
            var bank = Bank()
            
            var r1 = bank.withdraw(50)
            if r1.isOk()
                print "Withdrew 50"
            
            var r2 = bank.withdraw(-10)
            if r2.isErr()
                print "Error: ${r2.errValue()}"
```

Notice: you check preconditions **at the start** of the method. If a precondition fails, return early with an error.

---

## Postconditions: Validating Output

A **postcondition** says "when I return, the output will be valid":

```zebra
# file: 14_postconditions.zbr
# teaches: postcondition checking
# chapter: 14-Contracts-and-Assertions

class List
    var items: List(int) = List()
    var count: int = 0
    
    def add(item: int)
        items.add(item)
        count = count + 1
        
        # Postcondition: count must equal items.count()
        if count != items.count()
            # In a real system, raise an error
            print "ERROR: List invariant broken!"

class Main
    static
        def main
            var list = List()
            list.add(1)
            list.add(2)
            list.add(3)
            # Postcondition: count should be 3
```

Postconditions are checked **before returning**. If a postcondition fails, the method had a bug.

---

## Invariants: Properties That Never Break

An **invariant** is a property that must **always** be true:

```zebra
# file: 14_invariants.zbr
# teaches: class invariants
# chapter: 14-Contracts-and-Assertions

class Account
    var balance: int
    var transaction_count: int = 0
    
    # Invariant: balance >= 0 (can't have negative money)
    # Invariant: transaction_count >= 0
    
    def deposit(amount: int)
        if amount < 0
            return  # Reject negative deposits
        
        balance = balance + amount
        transaction_count = transaction_count + 1
        
        # Check invariants
        if balance < 0
            print "ERROR: Balance negative!"
        if transaction_count < 0
            print "ERROR: Transaction count negative!"
    
    def check_invariants: bool
        return balance >= 0 and transaction_count >= 0

class Main
    static
        def main
            var acct = Account()
            acct.balance = 100
            acct.deposit(50)
            
            if not acct.check_invariants()
                print "Invariant violated!"
```

In complex classes, you might check invariants at the **start and end** of every method.

---

## Assertions: Executable Checks

**Assertions** stop execution if a condition is false. Use them to catch bugs during development:

```zebra
# file: 14_assertions.zbr
# teaches: assertions
# chapter: 14-Contracts-and-Assertions

class Math
    static
        def divide(a: int, b: int): int
            # Assertion: b must not be zero
            if b == 0
                raise "Assertion failed: divide by zero"
            
            var result = a / b
            
            # Assertion: result * b == a (for integer division)
            if result * b != a
                raise "Assertion failed: division check"
            
            return result

class Main
    static
        def main
            var x = Math.divide(10, 2)
            print x  # Output: 5
            
            var y = Math.divide(10, 0)  # Raises
```

**Key:** Assertions should fail **loudly**. If a postcondition fails, something is deeply wrong.

---

## Real World: Sorted List Postcondition

Here's a practical example: verify that a sort function actually sorted the list:

```zebra
# file: 14_sort_postcondition.zbr
# teaches: postcondition in realistic code
# chapter: 14-Contracts-and-Assertions

class Sorter
    static
        def bubble_sort(items: List(int)) as List(int)
            var n = items.count()
            var i = 0
            
            while i < n
                var j = 0
                while j < n - 1
                    var a = items.at(j)
                    var b = items.at(j + 1)
                    if a > b
                        # Swap (simplified - no swap in stdlib)
                        pass
                    j = j + 1
                i = i + 1
            
            # Postcondition: list is sorted
            i = 0
            while i < items.count() - 1
                var a = items.at(i)
                var b = items.at(i + 1)
                if a > b
                    raise "Postcondition failed: list not sorted"
                i = i + 1
            
            return items

class Main
    static
        def main
            var list: List(int) = List()
            list.add(3)
            list.add(1)
            list.add(2)
            
            var sorted = Sorter.bubble_sort(list)
            print "Sorted"
```

---

## Design Patterns with Contracts

### Pattern 1: Guard Clauses (Precondition Pattern)

```zebra
# file: 14_guard_clauses.zbr
# teaches: guard clause pattern
# chapter: 14-Contracts-and-Assertions

class FileProcessor
    static
        def process_file(path: str): str throws
            # Preconditions as guard clauses
            if path == nil or path.len == 0
                raise "Path cannot be empty"
            
            if not path.contains(".")
                raise "Path must have extension"
            
            # Rest of method
            return "Processed"

class Main
    static
        def main
            var r = FileProcessor.process_file("")
            if r.isErr()
                print r.errValue()
```

### Pattern 2: Return Early on Precondition Failure

```zebra
# file: 14_early_return.zbr
# teaches: fail fast principle
# chapter: 14-Contracts-and-Assertions

class Validator
    static
        def validate_email(email: str): bool
            # Check preconditions first
            if email == nil
                return false
            
            if email.len == 0
                return false
            
            if not email.contains("@")
                return false
            
            # If all preconditions pass, do real work
            var parts = email.split("@")
            return parts.count() == 2

class Main
    static
        def main
            var valid = Validator.validate_email("user@example.com")
            print valid
```

### Pattern 3: Dual Verification (Assert Both Sides)

```zebra
# file: 14_dual_verify.zbr
# teaches: verifying both input and output
# chapter: 14-Contracts-and-Assertions

class StringHandler
    static
        def reverse_string(text: str): str
            # Precondition
            if text == nil
                return ""
            
            var original_len = text.len
            
            # Do work
            var result = text.reverse()
            
            # Postcondition: length unchanged
            if result.len != original_len
                raise "Postcondition failed: length changed"
            
            return result

class Main
    static
        def main
            var s = StringHandler.reverse_string("hello")
            print s
```

---

## Common Mistakes

### Mistake 1: Confusing Preconditions with Postconditions

```zebra
# WRONG - checking output before doing work
def add(a: int, b: int): int
    var result = a + b
    if a < 0  # This is a PRECONDITION, not postcondition
        raise "Error"
    return result

# CORRECT
def add(a: int, b: int): int
    if a < 0 or b < 0  # Precondition
        raise "Error: inputs must be non-negative"
    
    var result = a + b
    
    if result < a or result < b  # Postcondition (checking invariant property)
        raise "Error: overflow"
    
    return result
```

### Mistake 2: Silent Failures Instead of Assertions

```zebra
# WRONG - silently ignores contract violation
def process(items: List(int))
    if items.count() == 0
        pass  # Just exit, no indication of problem
    for item in items
        print item

# CORRECT - assert or return error
def process(items: List(int)) as bool throws
    if items.count() == 0
        raise "Cannot process empty list"
    
    for item in items
        print item
    
    return true
```

### Mistake 3: Expensive Assertions in Performance-Critical Code

```zebra
# PROBLEMATIC - expensive check in loop
def hot_path(items: List(int))
    for item in items
        # Checking invariants on every iteration is slow
        if not validate_item(item)
            raise "Invalid item"
        # Do actual work

# BETTER - check precondition once, trust throughout
def hot_path(items: List(int))
    # Single precondition check
    for item in items
        if not validate_item(item)
            raise "Invalid list"
    
    # Now do work without re-checking
    for item in items
        # Process item
        pass
```

### Mistake 4: Assertions That Can't Fail

```zebra
# POINTLESS - this can never be false
if x > 5
    # Postcondition that can't fail
    if x >= 5
        print "OK"

# MEANINGFUL - check for real invariants
if x > 5
    # Check for unexpected state
    if x < 0
        raise "Postcondition failed: negative x after increment"
```

---

## Exercises

### Exercise 1: Bank Account with Contracts

Create a `BankAccount` class with `deposit` and `withdraw` methods. Use preconditions to validate amounts, postconditions to verify the balance changes correctly:

<details>
<summary>Solution</summary>

```zebra
class BankAccount
    var balance: int = 0
    
    def deposit(amount: int): bool throws
        # Precondition: positive amount
        if amount <= 0
            raise "Deposit amount must be positive"
        
        var old_balance = balance
        balance = balance + amount
        
        # Postcondition: balance increased by amount
        if balance != old_balance + amount
            raise "Postcondition failed: balance update"
        
        return true
    
    def withdraw(amount: int): bool throws
        # Precondition: positive amount
        if amount <= 0
            raise "Withdrawal amount must be positive"
        
        # Precondition: sufficient funds
        if balance < amount
            raise "Insufficient funds"
        
        var old_balance = balance
        balance = balance - amount
        
        # Postcondition: balance decreased by amount
        if balance != old_balance - amount
            raise "Postcondition failed: balance update"
        
        return true

class Main
    static
        def main
            var account = BankAccount()
            account.balance = 100
            
            var r1 = account.deposit(50)
            print "Deposit: ${r1.isOk()}"
            
            var r2 = account.withdraw(30)
            print "Withdraw: ${r2.isOk()}"
```

</details>

### Exercise 2: Validated String Parser

Write a `StringParser` that parses input strings with clear pre and postconditions:

<details>
<summary>Solution</summary>

```zebra
class StringParser
    static
        def parse_number(text: str): int throws
            # Precondition: non-empty string
            if text == nil or text.len == 0
                raise "Cannot parse empty string"
            
            # NOTE: This parsing is hardcoded for demonstration. A real implementation
            # would parse the string digits. See Chapter 06 (Strings) for real parsing.
            if text == "42"
                var result = 42
                
                # Postcondition: result can be converted back to string
                if result.toString() != text
                    raise "Postcondition failed"
                
                return result
            
            raise "Not a valid number"

class Main
    static
        def main
            var r = StringParser.parse_number("42")
            if r.isOk()
                print "Parsed: ${r.okValue()}"
```

</details>

### Exercise 3: Invariant Checking List

Create a `ValidatedList(T)` that maintains an invariant that all items are non-nil and match a predicate:

<details>
<summary>Solution</summary>

```zebra
class ValidatedList(T)
    var items: List(T) = List()
    var predicate: T -> bool
    
    def init(predicate: T -> bool)
        this.predicate = predicate
    
    def add(item: T): bool
        # Precondition: item must match predicate
        if not predicate(item)
            return false
        
        items.add(item)
        
        # Postcondition: item is in list
        if not items.contains(item)
            raise "Postcondition failed: item not added"
        
        return true
    
    def check_invariants: bool
        for item in items
            if not predicate(item)
                return false
        return true

class Main
    static
        def main
            var list = ValidatedList()
            list.init({ x in x > 0 })
            
            list.add(5)
            list.add(10)
            
            if list.check_invariants()
                print "All invariants maintained"
```

</details>

---

## Key Takeaways

- **Preconditions validate inputs** — Check assumptions at method start
- **Postconditions verify outputs** — Check that return values are correct
- **Invariants encode properties that must always hold** — Reduce mental load
- **Fail fast with clear errors** — Don't silently continue with invalid state
- **Contracts document intent** — Make assumptions explicit

---

## Next Steps

- → **15-Pipelines** — Clean composition with contracts maintained
- → **Project 1** — Combine contracts with real error handling

---

**Contracts transform debugging from a mystery into a guarantee. Use them to build confidence in your code.**

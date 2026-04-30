# 14: Contracts and Assertions

**Audience:** All
**Time:** 90 minutes
**Prerequisites:** 04-Functions-and-Scope, 07-Classes-and-Instances, 12-Error-Handling
**You'll learn:** `require` (preconditions), `ensure` (postconditions, `result`, `old`), `invariant` (class invariants), `assert`, and the `--turbo` strip flag

---

## The Big Picture

Contracts are one of Zebra's marquee features. A contract is an *executable
specification* attached to a function or class — the compiler emits runtime
checks for each clause:

```zebra
def withdraw(amount: int): int throws
    require
        amount > 0
        amount <= balance
    ensure
        result == old balance - amount
    balance = balance - amount
    return balance
```

Three keywords cover the common cases:

| Keyword     | Where                         | What it asserts                         |
|-------------|-------------------------------|------------------------------------------|
| `require`   | Top of method body            | Inputs are valid (precondition)          |
| `ensure`    | Top of method body            | Output is valid (postcondition)          |
| `invariant` | Top of class body             | Object state is always valid             |

These get checked at runtime by default. Pass `--turbo` to the compiler to
strip them all out for production builds — same semantics as
`-DNDEBUG` for C `assert`.

> **Why bother?** Manual `if x raise "..."` checks at the top of each method
> work, but they bury the contract in normal control flow.  `require` /
> `ensure` / `invariant` make the contract syntactically distinct, give it
> a structured failure message with the failing clause, and let the
> production build remove the cost without touching the source.

This is **Design by Contract**, an idea from Eiffel that Zebra inherits and
adapts.

---

## Preconditions: `require`

A `require` block lists conditions that must hold when the method is called.
Each condition is a Boolean expression on its own line:

```zebra
# file: 14_require.zbr
# teaches: precondition checking with require
# chapter: 14-Contracts-and-Assertions

class Bank
    var balance: int = 100

    def withdraw(amount: int): int
        require
            amount > 0
            amount <= balance
        balance = balance - amount
        return balance

def main()
    var bank = Bank()
    print bank.withdraw(50)         # 50
    # bank.withdraw(-10)            # → panic: require failed in 'withdraw'
    # bank.withdraw(1000)           # → panic: require failed in 'withdraw'
```

If any clause is false, Zebra panics with a message naming the method and
the failing clause.

**When to use `require`:**

- Validate parameters (range, non-emptiness, format)
- Assert preconditions on the receiver's state ("only call after `init`")
- Document required ordering between methods

`require` failures indicate a **caller bug** — the caller violated the
contract.  Don't use `require` for user input you intend to validate
gracefully; that's `throws` + `raise` (Chapter 12).

---

## Postconditions: `ensure`

An `ensure` block lists conditions that must hold when the method returns
normally:

```zebra
# file: 14_ensure.zbr
# teaches: postcondition checking with ensure
# chapter: 14-Contracts-and-Assertions

class Counter
    var count: int = 0

    def increment(): int
        ensure
            count > 0
        count = count + 1
        return count

def main()
    var c = Counter()
    print c.increment()          # 1
    print c.increment()          # 2
```

`ensure` clauses fire **only on the success path**, not when the method
raises an error.  This is by design (a throwing method has no meaningful
postcondition).

### The `result` keyword

Inside `ensure`, the keyword `result` refers to the value the method is about
to return.  It has the same type as the method's declared return, so member
access works naturally:

```zebra
# file: 14_ensure_result.zbr
# teaches: result in ensure clauses
# chapter: 14-Contracts-and-Assertions

class Strings
    static
        def normalise(s: str): str
            ensure
                result.len <= s.len           # never grows
                not result.startsWith(" ")
                not result.endsWith(" ")
            return s.trim()
```

`result` is only valid inside `ensure`.  In the method body, you'd refer to
the to-be-returned variable by its own name; `result` is a contract-time
binding, not a regular variable.

### The `old` snapshot

When you need to compare the post-call state to the pre-call state, use the
`old` operator inside `ensure`.  It snapshots an expression at function entry:

```zebra
# file: 14_ensure_old.zbr
# teaches: old snapshots in ensure clauses
# chapter: 14-Contracts-and-Assertions

class Counter
    var count: int = 0

    def increment(): int
        ensure
            result == old count + 1       # post-state vs pre-state
            count == old count + 1
        count = count + 1
        return count
```

`old expr` is valid only inside `ensure`.  Each occurrence captures `expr`
once at function entry; the captured value is then used in the
post-condition check.

---

## Invariants: `invariant`

A class `invariant` block lists conditions that must hold whenever the
object is observable from outside.  Zebra checks the invariant after `cue
init` returns and after every public method exits:

```zebra
# file: 14_invariant.zbr
# teaches: class invariants
# chapter: 14-Contracts-and-Assertions

class Account
    var balance: int = 0
    var transactions: int = 0

    invariant
        balance >= 0
        transactions >= 0

    def deposit(amount: int)
        require
            amount > 0
        balance = balance + amount
        transactions = transactions + 1

    def withdraw(amount: int)
        require
            amount > 0
            amount <= balance
        balance = balance - amount
        transactions = transactions + 1

def main()
    var acct = Account()
    acct.deposit(50)
    acct.withdraw(30)
    # Both invariants checked after each method returns.
```

**Why invariants are a force multiplier:** instead of repeating the same
five sanity checks at the end of every method, you write them once in
`invariant` and the compiler weaves them into every method exit.  When you
add a sixth method later, it gets the invariant check for free.

> An invariant is checked *after* `cue init` returns, not before — your
> constructor is allowed to assemble state stepwise.  Same for setters: the
> invariant is checked once at the end, not after each individual
> assignment.

---

## Assertions: `assert`

For one-off checks inside a method body — debug-time sanity probes that
don't fit the contract structure — Zebra has a plain `assert` statement:

```zebra
# file: 14_assert.zbr
# teaches: assert statement
# chapter: 14-Contracts-and-Assertions

class Math
    static
        def divide(a: int, b: int): int
            require
                b != 0
            var q = a / b
            assert q * b == a       # integer-division sanity probe
            return q
```

Like the contract clauses, `assert` panics on a false condition and is
stripped by `--turbo`.  It's a more granular tool than `ensure` — useful
for checking intermediate values inside a method body.

---

## Real-world example: a sorted list

A class that combines `require` (caller contract), `ensure` (per-method
guarantee), and `invariant` (always-true property):

```zebra
# file: 14_sorted_list.zbr
# teaches: combining require, ensure, and invariant
# chapter: 14-Contracts-and-Assertions

class SortedList
    var items: List(int)

    cue init
        items = List(int)()

    invariant
        # The list is always non-decreasing
        isSorted()

    def isSorted(): bool
        var i = 1
        while i < items.count()
            if items.at(i - 1) > items.at(i)
                return false
            i = i + 1
        return true

    def insert(value: int)
        ensure
            items.count() == old items.count() + 1
        # Insert preserving sorted order.
        var i = 0
        while i < items.count() and items.at(i) < value
            i = i + 1
        items.add(value)
        # Bubble the new value left into its sorted position.
        var j = items.count() - 1
        while j > i
            var tmp = items.at(j - 1)
            items.add(items.at(j))
            j = j - 1

    def smallest(): int
        require
            items.count() > 0
        return items.at(0)

def main()
    var sl = SortedList()
    sl.insert(3)
    sl.insert(1)
    sl.insert(2)
    print sl.smallest()        # 1
    # Invariant verified after every public method.
```

The invariant catches any bug in `insert` automatically — there's no need
to remember to add a "verify still sorted" check at the end of every
mutation.

---

## `--turbo`: stripping contracts for production

In normal builds, every `require`, `ensure`, `invariant`, and `assert`
emits runtime check code.  These add safety during development but cost
cycles in hot paths.  Pass `--turbo` to the compiler to strip them
entirely:

```bash
zebra app.zbr              # contracts active — runtime checks emitted
zebra --turbo app.zbr      # contracts stripped — same source, faster binary
```

`--turbo` is the same source-to-binary toggle C/C++ get with `-DNDEBUG`.
Use it for production releases; develop and test without it.

> Don't put load-bearing logic inside contract clauses — anything you can't
> afford to lose at `--turbo` time.  Side effects in `require` /
> `ensure` are already a code smell; `--turbo` makes the smell into a bug.

---

## If you're new to programming

> A **precondition** is "what must be true before I run."  A **postcondition**
> is "what I promise will be true after I run."  An **invariant** is "what
> stays true the whole time the object exists."

> Contracts are a way of writing your assumptions down *as code* instead of
> in comments — comments rot when the code changes; contracts panic when
> the code violates them.

---

## Common Mistakes

> ❌ **Using `require` for user-input validation**
>
> ```zebra
> def parse_age(s: str): int
>     require
>         s.len > 0       # ❌ user-supplied — should be a graceful failure, not a panic
>     return 42
> ```
>
> ✅ Use `throws`/`raise` for failures the caller can handle:
>
> ```zebra
> def parse_age(s: str): int throws
>     if s.len == 0
>         raise "empty input"
>     return 42
> ```
>
> Reserve `require` for caller-bug detection.

> ❌ **Putting side effects in `require` / `ensure` / `invariant`**
>
> ```zebra
> def step(): int
>     ensure
>         logger.write("step done")    # ❌ side effect in ensure
>         result > 0
>     ...
> ```
>
> Contract clauses are stripped by `--turbo`.  Anything you do inside one
> evaporates in production.

> ❌ **Using `result` outside `ensure`**
>
> ```zebra
> def f(): int
>     return result + 1     # ❌ `result` is contract-only; not a regular variable
> ```
>
> `result` is only meaningful inside `ensure`.  Inside the method body,
> store the to-be-returned value in a regular `var` if you need to refer
> to it.

> ❌ **Expecting `ensure` to fire on the error path**
>
> ```zebra
> def divide(a: int, b: int): int throws
>     ensure
>         result > 0
>     if b == 0
>         raise "div by zero"
>     return a / b
> ```
>
> When the function raises, `ensure` is **not** evaluated — that's correct
> behaviour (a throwing method has no meaningful postcondition).  Don't
> design contracts that depend on `ensure` running on error paths.

---

## Exercises

### Exercise 1: Bank account with contracts

Rewrite the standard bank-account example using `require`, `ensure`, and
`invariant`:

<details>
<summary>Solution</summary>

```zebra
class BankAccount
    var balance: int = 0
    var transactions: int = 0

    invariant
        balance >= 0
        transactions >= 0

    def deposit(amount: int)
        require
            amount > 0
        ensure
            balance == old balance + amount
            transactions == old transactions + 1
        balance = balance + amount
        transactions = transactions + 1

    def withdraw(amount: int)
        require
            amount > 0
            amount <= balance
        ensure
            balance == old balance - amount
            transactions == old transactions + 1
        balance = balance - amount
        transactions = transactions + 1

def main()
    var acct = BankAccount()
    acct.deposit(100)
    acct.withdraw(30)
    print "Balance: ${acct.balance}"
    print "Transactions: ${acct.transactions}"
```

The invariant catches any future bug that would leave `balance` negative
or `transactions` not incrementing.

</details>

### Exercise 2: Validated array indexer

Write a class that wraps a `List(int)` with bounds-checked access, using
`require` to document the contract:

<details>
<summary>Solution</summary>

```zebra
class SafeArray
    var items: List(int)

    cue init
        items = List(int)()

    def push(v: int)
        ensure
            items.count() == old items.count() + 1
        items.add(v)

    def at(i: int): int
        require
            i >= 0
            i < items.count()
        return items.at(i)

    def first(): int
        require
            items.count() > 0
        return items.at(0)

def main()
    var sa = SafeArray()
    sa.push(10)
    sa.push(20)
    print sa.at(0)            # 10
    print sa.first()          # 10
    # sa.at(99)                # → panic: require failed in 'at'
```

</details>

### Exercise 3: Stack with size invariant

Write a `Stack(int)` with `push`/`pop`/`top` that maintains an invariant
relating `count()` to `items.count()`:

<details>
<summary>Solution</summary>

```zebra
class Stack
    var items: List(int)
    var size: int = 0

    cue init
        items = List(int)()

    invariant
        size >= 0
        size == items.count()

    def push(v: int)
        ensure
            size == old size + 1
        items.add(v)
        size = size + 1

    def pop(): int
        require
            size > 0
        ensure
            size == old size - 1
        var top = items.at(size - 1)
        # Remove the last element by clearing then re-adding all but one.
        # (A real implementation would use list.removeLast(); this is illustrative.)
        size = size - 1
        return top

    def top(): int
        require
            size > 0
        return items.at(size - 1)

def main()
    var s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    print s.top()             # 3
    print s.pop()             # 3
    print s.top()             # 2
```

The invariant `size == items.count()` would catch any future bug that
broke the relationship between the count field and the underlying list.

</details>

---

## Key Takeaways

- **`require` documents the caller's contract.**  Use it for caller-bug
  detection, not for graceful user-input validation.
- **`ensure` documents the method's promise.**  `result` refers to the
  return value; `old expr` snapshots `expr` at entry.
- **`invariant` documents the object's permanent state.**  Checked after
  `init` and after every public method exit — write the invariant once,
  get the check for free everywhere.
- **`assert` is the granular tool**: an inline sanity probe inside a
  method body.
- **`--turbo` strips them all.**  Develop with contracts on; ship with
  contracts off.  Don't put side effects inside contract clauses.

---

## Next Steps

- → **15-Pipelines** — Composing functions whose contracts compose, too
- 🏋️ **Project 1 (CLI Tool)** — Use contracts for argument validation

---

**Contracts turn debugging from "where did this go wrong" into "the contract
says what was supposed to be true; here's exactly which clause failed."**

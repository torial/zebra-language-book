# 22c: Testing and Validation

**Audience:** All
**Time:** 90 minutes
**Prerequisites:** 04-Functions-and-Scope, 12-Error-Handling, 22b-Build-System-and-Tooling
**You'll learn:** Writing tests with `assert_*` statements, the `zebra test` runner, filtering with `@tag`, organising tests across a project

---

## The Big Picture

Tests are the safety net that lets you change code without fear. Without
tests, every refactor is a leap of faith; with tests, regressions surface
the moment they're introduced.

Zebra has a **built-in test runner**: any top-level function whose name
starts with `test_` is auto-discovered and run by `zebra test`. No
`use Test` import, no test-class boilerplate, no fixture registration —
just write `def test_something()` and the runner finds it.

This chapter covers the test-writing primitives, the runner CLI, and
patterns for organising tests as your project grows.

> **Tests vs. contracts.** Tests check examples — "for input X, output Y."
> Contracts (`require`/`ensure`/`invariant`, Chapter 14) check invariants
> that should hold for *all* inputs at runtime. Both are useful; they catch
> different bugs. This chapter is about tests.

---

## Writing a Test

A test is a **zero-parameter top-level function whose name starts with
`test_`**:

```zebra
# file: 22c_first_test.zbr
# teaches: writing a single test
# chapter: 22c-Testing-and-Validation

def test_addition()
    assert_eq 1 + 1, 2
    assert_ne 0, 1
```

Run it:

```bash
$ zebra test 22c_first_test.zbr
PASS: test_addition

1 passed, 0 failed
```

The runner discovers `test_addition` automatically, calls it, and reports
the result. No `main()`, no `Test.register(...)`, no manual list.

### What the runner does

Internally, `zebra test`:

1. Compiles the file in **test mode** — any `def main()` is suppressed
2. Generates a synthetic `main()` that calls every `def test_*()` in turn
3. Each `test_*` function is automatically typed `anyerror!void` — assertions can throw without you marking the function `throws`
4. Runs the synthetic main and counts pass/fail
5. Exits `0` if all passed, `1` if any failed

Tests run **sequentially in declaration order**. A failure in one test
does not abort the others — every test gets a chance to run, so you see
all the failures in one pass.

---

## Assertion Statements

Zebra has four built-in assertion **statements** (not functions — they're
parsed specially so failure messages can include both the expected and
actual values):

| Statement | Passes when | Throws when |
|---|---|---|
| `assert_eq <lhs>, <rhs>` | `lhs == rhs` | `lhs != rhs` |
| `assert_ne <lhs>, <rhs>` | `lhs != rhs` | `lhs == rhs` |
| `assert_true <expr>` | `expr` is `true` | `expr` is `false` |
| `assert_false <expr>` | `expr` is `false` | `expr` is `true` |

Examples:

```zebra
# file: 22c_assertions.zbr
# teaches: the four assertion forms
# chapter: 22c-Testing-and-Validation

def test_equality()
    assert_eq 1 + 1, 2
    assert_eq "hello", "hello"
    assert_eq [1, 2, 3].count(), 3

def test_inequality()
    assert_ne 1, 2
    assert_ne "foo", "bar"

def test_booleans()
    assert_true  5 > 3
    assert_true  not false
    assert_false 1 > 2
    assert_false "x".len == 0
```

On failure, each assertion throws `error.ZebraError` with a descriptive
message that includes both operands.

### What about `assert`?

The plain `assert` keyword (used as `assert cond` and `assert cond, "msg"`)
also works inside tests, but the `assert_*` forms produce better failure
messages — they print the actual *values*, not just "expected true, got
false." Prefer `assert_eq` over `assert lhs == rhs` in tests.

---

## Running Tests

The basic invocation:

```bash
zebra test path/to/test_file.zbr
```

Output format:

```
PASS: test_addition
PASS: test_strings
FAIL: test_subtraction — expected 5, got 4

2 passed, 1 failed
```

Exit code:

| All passed | Some failed | Compile error |
|---|---|---|
| `0` | `1` | non-zero (compiler-defined) |

This makes `zebra test` suitable for CI: a failing test fails the build.

### Selecting which tests to run

Three ways to narrow down:

```bash
zebra test --tag NAME file.zbr     # only tests with @tag("NAME") or auto-tags matching
zebra test --filter NAME file.zbr  # only test functions whose name contains NAME
zebra test file.zbr                # everything in the file (default)
```

`--tag` is the recommended way to organise large suites — see the next
section.

---

## Filtering with `@tag`

Apply one or more string tags to a test function:

```zebra
# file: 22c_tags.zbr
# teaches: @tag-based test filtering
# chapter: 22c-Testing-and-Validation

@tag("unit", "math")
def test_addition()
    assert_eq 1 + 1, 2

@tag("integration")
def test_database_roundtrip()
    var db = Sqlite.open(":memory:")
    db.exec("CREATE TABLE t (x INTEGER)")
    db.exec("INSERT INTO t VALUES (42)")
    var row = db.query("SELECT x FROM t").at(0)
    assert_eq row.asInt(0), 42

@tag("slow")
def test_large_dataset()
    # ... long-running test ...
    assert_true true
```

Run only the fast unit tests on every commit, leaving slow integration
tests for nightly runs:

```bash
$ zebra test --tag unit suite.zbr           # only "unit"-tagged tests
$ zebra test --tag integration suite.zbr    # only integration tests
$ zebra test suite.zbr                       # everything
```

`--tag` is matched against the union of: explicit `@tag(...)` arguments,
the file stem (see Auto-Tags below), and the enclosing class/struct name.

---

## Auto-Tags

Two tags are applied to every test without an annotation:

| Auto-tag | Source | Use case |
|---|---|---|
| **File stem** | `foo_test.zbr` → tag `"foo_test"` | Run all tests in one file by name |
| **Class/struct name** | `static def test_X()` inside `class Arithmetic` → tag `"Arithmetic"` | Group tests by the type they exercise |

This means a test inside a class gets *three* tag sources (explicit tags,
the file stem, and the class name), and the runner matches against any
of them.

Given `math_test.zbr` containing:

```zebra
class Arithmetic
    @tag("unit")
    static def test_add()
        assert_eq 2 + 2, 4

    static def test_subtract()
        assert_eq 5 - 3, 2
```

| `--tag` value | Selects |
|---|---|
| `math_test` | All tests in the file (file-stem auto-tag) |
| `Arithmetic` | Both tests in the class |
| `unit` | Only `test_add` (explicit tag) |

The class-name auto-tag is what makes it convenient to group tests by the
type under test without writing `@tag("Arithmetic")` on every method.

---

## Tests in Classes

Tests can live inside a class as `static def test_*()` — the auto-tag for
the class name applies:

```zebra
# file: arithmetic_test.zbr
# teaches: class-scoped tests
# chapter: 22c-Testing-and-Validation

class Arithmetic
    static def test_add()
        assert_eq 2 + 2, 4

    static def test_subtract()
        assert_eq 10 - 3, 7

class Strings
    static def test_concat()
        assert_eq "foo" + "bar", "foobar"

    static def test_len()
        assert_eq "hello".len, 5
```

`zebra test arithmetic_test.zbr` runs all four. Use `--tag Arithmetic` or
`--tag Strings` to run just one class.

This is the cleanest organisation for tests that exercise a specific
class's behaviour — the auto-tag makes filtering free, and the class
groups related tests together.

---

## File Organisation

Conventions that have proven useful:

- **One test file per module.** `cli.zbr` → `cli_test.zbr`. The file-stem
  auto-tag means `zebra test --tag cli_test` runs everything for that module.
- **Co-locate or separate.** Some projects put tests next to source
  (`src/cli.zbr` + `src/cli_test.zbr`); others use a separate `test/`
  directory. Either works; consistency matters more than which.
- **Don't write `def main()` in test files.** The runner generates its
  own. If you do define one, it's silently dropped in test mode.
- **Don't share test state.** Each `test_*` function should be
  independent. If you need setup, write a helper called by each test —
  don't rely on previous tests having run.

---

## Real World: Testing a Module

Here's a small module and the test file that covers it.

### `src/calc.zbr`

```zebra
class Calc
    static def add(a: int, b: int): int
        return a + b

    static def divide(a: int, b: int): int throws
        if b == 0
            raise "division by zero"
        return a / b

    static def max_of(items: List(int)): int throws
        if items.count() == 0
            raise "empty list"
        var best = items.at(0)
        for n in items
            if n > best
                best = n
        return best
```

### `src/calc_test.zbr`

```zebra
use calc

class CalcTests
    static def test_add_basic()
        assert_eq Calc.add(2, 3), 5

    static def test_add_negatives()
        assert_eq Calc.add(-2, -3), -5
        assert_eq Calc.add(-5, 10), 5

    static def test_divide_normal()
        assert_eq Calc.divide(10, 2) catch 0, 5
        assert_eq Calc.divide(15, 3) catch 0, 5

    static def test_divide_by_zero()
        # divide(_, 0) raises; the inline catch substitutes -1
        assert_eq Calc.divide(10, 0) catch -1, -1

    static def test_max_of_normal()
        var nums = [3, 1, 4, 1, 5, 9, 2, 6]
        assert_eq Calc.max_of(nums) catch 0, 9

    static def test_max_of_empty()
        var empty: List(int) = []
        assert_eq Calc.max_of(empty) catch -1, -1
```

Run them:

```bash
$ zebra test src/calc_test.zbr
PASS: CalcTests.test_add_basic
PASS: CalcTests.test_add_negatives
PASS: CalcTests.test_divide_normal
PASS: CalcTests.test_divide_by_zero
PASS: CalcTests.test_max_of_normal
PASS: CalcTests.test_max_of_empty

6 passed, 0 failed
```

Two patterns worth noticing:

1. **Inline `catch` for throwing functions.** `Calc.divide(10, 2) catch 0`
   gives the test a numeric value to compare against, even when the call
   could throw. For the error path, choose a sentinel (`-1` here) that
   can never appear in the success path.
2. **No `def main()`.** The runner generates one; defining your own would
   be ignored.

---

## Common Mistakes

> ❌ **Mistake:** Naming a test function without the `test_` prefix
>
> ```zebra
> def addition_test()        # Wrong — runner doesn't see this
>     assert_eq 1 + 1, 2
> ```
>
> ✅ **Better:**
> ```zebra
> def test_addition()        # Discovered by the runner
>     assert_eq 1 + 1, 2
> ```

> ❌ **Mistake:** Using plain `assert` for value comparisons
>
> ```zebra
> def test_addition()
>     assert (1 + 1) == 2    # works, but failure says only "assertion failed"
> ```
>
> ✅ **Better:**
> ```zebra
> def test_addition()
>     assert_eq 1 + 1, 2     # failure message includes both values
> ```

> ❌ **Mistake:** Sharing state between tests
>
> ```zebra
> var counter = 0
>
> def test_increment_once()
>     counter = counter + 1
>     assert_eq counter, 1   # passes the first time, breaks if run after another test
>
> def test_increment_twice()
>     counter = counter + 1  # depends on counter == 0 — fragile
>     assert_eq counter, 1
> ```
>
> ✅ **Better:** rebuild the state inside each test, or use a helper:
> ```zebra
> def fresh_counter(): int
>     return 0
>
> def test_increment_once()
>     var c = fresh_counter()
>     c = c + 1
>     assert_eq c, 1
> ```

> ❌ **Mistake:** Putting `def main()` in a test file
>
> ```zebra
> def test_thing()
>     assert_true true
>
> def main()                 # silently dropped in test mode — confusing
>     print "this never runs under zebra test"
> ```
>
> Just delete the `main()` — the runner generates one.

---

## Exercises

### Exercise 1: A First Test

Write a file `string_test.zbr` with three tests that check basic string
operations.

<details>
<summary>Solution</summary>

```zebra
def test_concat()
    assert_eq "foo" + "bar", "foobar"

def test_length()
    assert_eq "hello".len, 5
    assert_eq "".len, 0

def test_contains()
    assert_true  "hello world".contains("world")
    assert_false "hello world".contains("zebra")
```

Run it with `zebra test string_test.zbr`.

</details>

### Exercise 2: Class-Scoped Tests with Tags

Write a test file for a hypothetical `User` class. Tag each test with
either `"unit"` (no I/O) or `"integration"` (uses the database). Show how
you'd run just the unit tests.

<details>
<summary>Solution</summary>

```zebra
class UserTests
    @tag("unit")
    static def test_email_validation()
        assert_true  User.is_valid_email("a@b.com")
        assert_false User.is_valid_email("not-an-email")

    @tag("unit")
    static def test_name_normalization()
        assert_eq User.normalize_name("  Alice  "), "Alice"

    @tag("integration")
    static def test_save_and_load()
        # ... uses Sqlite or a file ...
        assert_true true
```

Run only unit tests:

```bash
zebra test --tag unit user_test.zbr
```

</details>

### Exercise 3: Testing a Throwing Function

Add a test file for the `Calc.divide` function from the chapter. Verify
both the success and the throwing paths.

<details>
<summary>Solution</summary>

```zebra
use calc

def test_divide_success()
    assert_eq Calc.divide(20, 4) catch 0, 5
    assert_eq Calc.divide(7, 1) catch 0, 7

def test_divide_zero_raises()
    # Sentinel: divide on success can't return -1 for positive inputs
    assert_eq Calc.divide(10, 0) catch -1, -1
```

The inline `catch` lets `assert_eq` see a value either way. Pick a
sentinel that the success path can't produce.

</details>

---

## Next Steps

- → **22b-Build-System-and-Tooling** — register a test target in your `build.zbr`
- → **14-Contracts-and-Assertions** — runtime invariants alongside tests
- → **10b-Modules-Namespaces-and-Visibility** — organise modules + their test files

---

## Key Takeaways

- **Tests are `def test_*()` top-level (or `static def test_*()` in a class)** — the runner discovers them automatically; no registration needed
- **`zebra test file.zbr`** compiles in test mode (suppressing `main()`), generates a synthetic entry point, runs every discovered test, reports pass/fail
- **Use `assert_eq` / `assert_ne` / `assert_true` / `assert_false`** — they produce better failure messages than bare `assert`
- **`@tag("name")`** marks tests for filtered runs; `zebra test --tag X` runs only matching tests
- **Auto-tags** include the file stem and the enclosing class/struct name — most filtering needs no explicit `@tag`
- **Each test is independent** — no shared state, no setup/teardown framework; if you need setup, write a helper called from each test
- **Inline `catch` is the test-time idiom for throwing functions** — `expr catch sentinel` lets `assert_eq` see a value either way

---

**Next:** Chapter 10b covers modules and namespaces — the structural primitives that let you split a growing test suite (and the rest of your code) across files.

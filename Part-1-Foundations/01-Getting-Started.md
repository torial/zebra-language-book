# 01: Getting Started

**Audience:** All  
**Time:** 30 minutes  
**Prerequisites:** None  
**You'll learn:** Install Zebra, run your first program, understand the toolchain

---

## The Big Picture

Zebra is a **modern, statically-typed language** that prioritizes **safety, clarity, and correctness**. It combines ideas from Python, C#, Objective-C, and Eiffel into a pragmatic language for building robust systems.

This book teaches you to write Zebra code fluently. By the end, you'll understand:
- How Zebra's type system catches bugs at compile time
- Why nil tracking and error handling are first-class citizens
- How to write clean, expressive code that reads almost like pseudocode

Let's get your environment set up and run your first program.

---

## What is Zebra?

**Short version:** A statically-typed language that feels dynamic, with compile-time safety guarantees that prevent entire categories of bugs.

**Key properties:**
- **Compiled** — Zebra code compiles to Zig (which then compiles to machine code)
- **Strongly typed** — Types are checked at compile time, preventing type mismatches
- **Nil-safe** — You explicitly mark values that can be `nil`, preventing null pointer errors
- **Error-aware** — Errors are values you handle, not exceptions you ignore
- **Expressive** — Clear, readable syntax that emphasizes intent over cleverness

**Who uses it:** People building systems where reliability matters (CLI tools, servers, data processing, embedded systems).

---

## Installation

### macOS and Linux

```bash
# Install Zig first (Zebra compiles to Zig)
# https://ziglang.org/download/
# Then install Zebra
# https://github.com/cobra-language/zebra/releases

# Verify installation
zebra --version
```

### Windows

```cmd
# Download from: https://github.com/cobra-language/zebra/releases
# Extract to a directory
# Add to PATH
# Verify:
zebra --version
```

### From Source

```bash
git clone https://github.com/cobra-language/zebra.git
cd zebra/zig-compiler
zig build
# Binary at: zig-out/bin/zebra
```

---

## Your First Program

Create a file named `hello.zbr`:

```zebra
# file: hello.zbr
# teaches: hello world, print statement
# chapter: 01-Getting-Started

def main()
    print "Hello, Zebra!"
```

Run it:

```bash
zebra hello.zbr
```

**Output:**
```
Hello, Zebra!
```

### What just happened?

1. **`def main()`** — Defined the entry point function. Zebra runs `main` automatically when the program starts.
2. **`print "..."`** — Printed text to the console.
3. **`zebra hello.zbr`** — Compiled and ran the program.

That's the whole program. No class wrapper, no boilerplate.

### If you're new to programming

> A **function** is a reusable block of code. `main` is special — it runs automatically when you start the program.
>
> A **statement** is an instruction. `print "Hello, Zebra!"` is a statement that outputs text.
>
> Larger programs often group related code into **classes** (Chapter 07). Small scripts don't need them.

### If you know Python

```python
# Python
print("Hello, World!")

# Zebra
print "Hello, Zebra!"
```

Where Python's entry point is implicit (top-level statements run at import), Zebra's is explicit (you define `main`). The clarity scales: as programs grow you can group code into classes and modules without reshaping the entry point.

### Verbosity dial — annotations are optional when the type is obvious

Zebra has full type inference. You can write either:

```zebra
def main()
    var name: str = "World"        # explicit — annotation aids the reader
    var age: int = 30
    var pi: float = 3.14159
    print "${name} is ${age}"
```

or, equivalently:

```zebra
def main()
    var name = "World"             # inferred from the literal
    var age = 30
    var pi = 3.14159
    print "${name} is ${age}"
```

Both compile to the same Zig. **Use annotations when they aid the reader** (function signatures, public class fields, hairy generic returns) and **drop them when the right-hand side already makes the type obvious** (literals, named-constructor calls, expressions whose return type is plain). The book mostly uses the inferred form going forward; you'll see explicit annotations where they earn their keep.

You can also still use the class-based entry point if you prefer it (older code does):

```zebra
class Main
    static
        def main
            print "Hello, Zebra!"
```

Both forms work. Bare `def main()` is the recommended default for scripts and small programs.

---

## The Toolchain

Zebra's workflow is:

```
hello.zbr (Zebra code)
    ↓
zebra compiler
    ↓
hello.zig (Zig code)
    ↓
zig compiler
    ↓
hello.exe (Executable)
    ↓
Run: ./hello
```

**Why two steps?** Zebra targets Zig because Zig is:
- Low-level (good for systems programming)
- Safe (catches undefined behavior at compile time)
- Explicit (no hidden magic)
- Fast (compiles to efficient machine code)

As a Zebra programmer, you mostly ignore the Zig step. You write `.zbr`, run `zebra <file>`, and get a fast executable.

---

## Common Commands

```bash
# Compile and run
zebra hello.zbr

# Compile only (leaves hello.exe)
zebra -c hello.zbr

# Run with debug output
zebra -v=2 hello.zbr

# Keep intermediate Zig code for inspection
zebra -kif hello.zbr
```

---

## Your Second Program (A Little Interesting)

```zebra
# file: greet.zbr
# teaches: variables, string interpolation
# chapter: 01-Getting-Started

def main()
    var name = "World"
    print "Hello, ${name}!"
```

**Output:**
```
Hello, World!
```

### What's new?

- **`var name = "World"`** — Declared a variable named `name` and initialized it with `"World"`. The type `str` is inferred from the literal; you could also write `var name: str = "World"` if you wanted to make the type explicit.
- **`"Hello, ${name}!"`** — String interpolation: `${name}` is replaced with the value of `name`.

---

## Understanding Errors

When you make a mistake, Zebra tells you clearly:

```zebra
def main()
    print "Hello " + 5  # ❌ Can't add string + number
```

**Error:**
```
greet.zbr:5:24: error: arithmetic requires numeric type, got 'str'
    print "Hello " + 5
                   ^
```

**What it means:**
- **File and line:** `greet.zbr:5:24` — error at line 5, column 24
- **Error type:** "arithmetic requires numeric type" — you tried math with incompatible types
- **The problem:** `+` expects numbers, but got `"Hello "` (a string)

**Fix:** Use string concatenation:
```zebra
print "Hello ".concat(5.toString())
```

Or use string interpolation:
```zebra
print "Hello ${5}"
```

---

## Project Structure (Thinking Ahead)

As programs grow, organize them:

```
my-project/
├── main.zbr          # Entry point
├── utils.zbr         # Helper functions
├── data.zbr          # Data structures
└── lib/
    └── db.zbr        # Database utilities
```

Later chapters will show how to use multiple files. For now, keep everything in one `.zbr` file.

---

## Using Other Files: `use` and `exposing`

When your program spans multiple files, Zebra's `use` statement imports another module:

```zebra
# file: math_utils.zbr
def square(n: int): int
    return n * n
```

```zebra
# file: main.zbr
use math_utils exposing square

def main()
    var answer = square(5)
    print answer  # 25
```

> **Naming note:** `result` is a reserved keyword in Zebra (it binds the return value inside an `ensure` block — see Chapter 14). Pick another name like `answer` or `total` for ordinary locals.

### Selective Imports with `exposing`

`use math_utils` brings the module into scope as `math_utils.square(5)`. Adding `exposing square` lifts the name in directly so you can call `square(5)` without the prefix. You can expose multiple names at once:

```zebra
use ast exposing Stmt, Expr, TypeRef, DeclVar
```

This keeps your code clean when you use many names from a module. You'll see `use...exposing` extensively in later chapters.

---

## Exercises

### Exercise 1: Customize the Greeting

Modify `hello.zbr` to:
1. Declare a variable for your name
2. Print a greeting using that variable

<details>
<summary>Solution</summary>

```zebra
def main()
    var my_name = "Alice"
    print "Hello! My name is ${my_name}."
```

**Output:**
```
Hello! My name is Alice.
```

**Why this works:** We declared `my_name` (inferred as `str`), then used it in interpolation.

</details>

### Exercise 2: Combine Multiple Variables

Create a program that:
1. Declares three variables: `first_name`, `last_name`, and `age`
2. Prints a sentence combining all three

<details>
<summary>Solution</summary>

```zebra
def main()
    var first_name = "Bob"
    var last_name = "Smith"
    var age = 30
    print "My name is ${first_name} ${last_name} and I'm ${age} years old."
```

**Output:**
```
My name is Bob Smith and I'm 30 years old.
```

**Why this works:** We declared three variables — two strings and one integer, all inferred from their literals — and used all three in a single string interpolation.

</details>

---

## Next Steps

- → **02-Values-and-Types** — Dive into Zebra's type system
- → **03-Collections** — Work with Lists and HashMaps
- 🏋️ **Project-1-CLI-Tool** — Build something real

---

## Key Takeaways

- **Zebra is compiled** — Code becomes fast executables
- **Entry point is explicit** — Every program defines `main` (top-level `def main()`, or `Main.main` inside a class for larger programs)
- **Type annotations are optional** — Use them where they aid the reader; lean on inference when the right-hand side is obvious
- **Strings use interpolation** — `"${variable}"` is easier to read than concatenation
- **Errors are clear** — The compiler helps you fix problems
- **Simple programs are simple** — Print and variables are enough for Hello World

---

## Troubleshooting

**"zebra: command not found"**
→ Zebra isn't in your PATH. Check the installation instructions for your OS.

**"error: file not found: hello.zbr"**
→ Make sure you're in the directory with `hello.zbr`. Try: `ls hello.zbr`

**"error: arithmetic requires numeric type"**
→ You mixed types (like string + number). Use `toString()` or string interpolation instead.

**Program compiles but doesn't run**
→ The executable was created but you need to run it. Try: `./hello` (Unix/Mac) or `hello.exe` (Windows)

---

**Ready?** Head to **02-Values-and-Types** and learn the full type system.

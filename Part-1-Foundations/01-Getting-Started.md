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

class Main
    shared
        def main
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

1. **`class Main`** — Defined a class (we'll explore classes fully in Chapter 07)
2. **`shared`** — Marked a method as belonging to the class itself, not instances
3. **`def main`** — Defined the entry point function (where the program starts)
4. **`print "..."`** — Printed text to the console
5. **`zebra hello.zbr`** — Compiled and ran the program

### If you're new to programming

> A **class** is a blueprint for creating objects. The `Main` class holds our program code.
>
> A **function** (or **method**) is a reusable block of code. `main` is special—it runs automatically when you start the program.
>
> A **statement** is an instruction. `print "Hello, Zebra!"` is a statement that outputs text.

### If you know Python

```python
# Python
print("Hello, World!")

# Zebra
print "Hello, Zebra!"
```

Python's implicit entry point becomes explicit in Zebra: you must define `Main.main`. This clarity helps with larger programs.

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

class Main
    shared
        def main
            var name as str = "World"
            print "Hello, ${name}!"
```

**Output:**
```
Hello, World!
```

### What's new?

- **`var name as str`** — Declared a variable named `name` that holds a string (`str`)
- **`= "World"`** — Initialized it with the value `"World"`
- **`"Hello, ${name}!"`** — String interpolation: `${name}` gets replaced with the value of `name`

---

## Understanding Errors

When you make a mistake, Zebra tells you clearly:

```zebra
class Main
    shared
        def main
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
class MathUtils
    shared
        def square(n as int) as int
            return n * n
```

```zebra
# file: main.zbr
use MathUtils

class Main
    shared
        def main
            var result = MathUtils.square(5)
            print result  # 25
```

### Selective Imports with `exposing`

Use `exposing` to import specific names directly into scope:

```zebra
use MathUtils exposing square

class Main
    shared
        def main
            var result = square(5)  # No MathUtils. prefix needed
            print result
```

You can expose multiple names:

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
class Main
    shared
        def main
            var my_name as str = "Alice"
            print "Hello! My name is ${my_name}."
```

**Output:**
```
Hello! My name is Alice.
```

**Why this works:** We declared `my_name` as a string, then used it in interpolation.

</details>

### Exercise 2: Combine Multiple Variables

Create a program that:
1. Declares three variables: `first_name`, `last_name`, and `age`
2. Prints a sentence combining all three

<details>
<summary>Solution</summary>

```zebra
class Main
    shared
        def main
            var first_name as str = "Bob"
            var last_name as str = "Smith"
            var age as int = 30
            print "My name is ${first_name} ${last_name} and I'm ${age} years old."
```

**Output:**
```
My name is Bob Smith and I'm 30 years old.
```

**Why this works:** We declared three variables (two strings, one integer) and used all three in a single string interpolation.

</details>

---

## Next Steps

- → **02-Values-and-Types** — Dive into Zebra's type system
- → **03-Collections** — Work with Lists and HashMaps
- 🏋️ **Project-1-CLI-Tool** — Build something real

---

## Key Takeaways

- **Zebra is compiled** — Code becomes fast executables
- **Entry point is explicit** — Every program defines `Main.main`
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

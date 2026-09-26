# Zebra: 30 Minutes to Productive

Get from zero to your first working Zebra program in 30 minutes.

---

## Minute 1-3: What is Zebra?

Zebra is a modern programming language combining:
- **Python's simplicity** — readable, clear syntax
- **C#'s power** — strong types, interfaces, generics
- **Nil safety** — prevents null pointer crashes
- **Error handling** — explicit `throws`/`raise`/`catch` instead of hidden exceptions
- **Performance** — compiles to Zig → machine code

You can read your first working program in 2 minutes.

---

## Before You Start: Installing Zebra

One command installs a release — the `zebra` compiler plus the Zig toolchain
it builds with:

```bash
# Windows (PowerShell)
irm https://raw.githubusercontent.com/torial/zebra-language/main/install/install.ps1 | iex

# Linux and macOS
curl -fsSL https://raw.githubusercontent.com/torial/zebra-language/main/install/install.sh | sh
```

On Windows the installer adds Zebra to your `PATH`; on Linux and macOS it prints
the `export PATH=...` line to add to your shell profile. Open a new terminal and
check with `zebra --version`. Windows, Linux and macOS (Apple Silicon,
first-class since 0.9.0-rc2) are all supported, and `zebra up` later updates
an installed release.

Prefer to build from source? With Zig 0.16 on your `PATH`:

```bash
git clone https://github.com/torial/zebra-language
cd zebra-language
zig build                          # produces zig-out/bin/zebra (zebra.exe on Windows)
```

---

## Minute 4-10: Your First Program

Create a file: `hello.zbr`

```zebra
def main()
    print("Hello, World!")
```

Compile and run:
```bash
zebra hello.zbr
```

**That's it!** You just wrote your first Zebra program.

---

## Minute 11-20: The Five Things You Need to Know

### 1. Variables and Types

```zebra
var name = "Alice"              # str
var age = 30                    # int
var pi = 3.14                   # float
var active = true               # bool
```

**Key:** Zebra figures out the type. You don't need to write it.

### 2. Functions

```zebra
def greet(name: str): str
    return "Hello, ${name}!"

var message = greet("Bob")      # "Hello, Bob!"
```

**Key:** Parameters and return types are explicit (safer).

### 3. Collections

```zebra
var fruits = List(str)()        # Create list
fruits.add("apple")
fruits.add("banana")

for fruit in fruits
    print(fruit)
```

**Key:** Lists are for ordered collections. Use `for...in` to loop.

### 4. If/Else and Loops

```zebra
var x = 10

if x > 5
    print("Large")
else
    print("Small")

while x > 0
    print(x)
    x = x - 1
```

**Key:** No parentheses needed. Indentation matters.

### 5. Error Handling

```zebra
# A function that can fail is marked `throws`; `raise` signals the failure
def parse_age(text: str): int throws
    var n = text.tryInt()
    if n == nil
        raise "not a number: ${text}"
    return n!

# Or attach a catch clause to a def for more control (there is no
# standalone `try` block — `catch` always attaches to a def's body)
def show_age(text: str)
    var age = parse_age(text)
    print("Age: ${age}")
catch |err|
    print("Error: ${err}")

def main()
    print(parse_age("42") catch -1)       # 42
    print(parse_age("forty") catch -1)    # -1   (the inline fallback)
    show_age("42")                        # Age: 42
    show_age("forty")                     # Error: not a number: forty
```

**Key:** Functions annotated with `throws` can fail. Use inline `expr catch fallback` for a default value, or a method-level `catch` clause (attached to a `def`, after its body) for structured handling.

---

## Minute 21-25: Build Something Real

Create `count_lines.zbr`:

```zebra
def main()
    var filename = "input.txt"

    # File.read is not `throws` (a missing file stops the program), so check first
    if not File.exists(filename)
        print("Error: could not find ${filename}")
        sys.exit(1)

    var content = File.read(filename)
    var lines = content.split("\n")

    print("File: ${filename}")
    print("Lines: ${lines.count()}")
    print("Total characters: ${content.len}")
```

Run:
```bash
zebra count_lines.zbr
```

**You now have a working file analyzer!**

---

## Minute 26-30: The Pattern to Remember

99% of Zebra code follows this pattern:

```zebra
def do_something(input: str): str throws
    # 1. Validate input
    if input.len == 0
        raise "Input is empty"

    # 2. Do work
    var result = input.trim().upper()

    # 3. Return success
    return result

def try_it()
    var v = do_something("")?
    print(v)
catch |err|
    print("Failed: ${err}")

def main()
    # Use catch for simple fallback
    var value = do_something("data") catch "default"
    print(value)                    # DATA

    # Or a method-level catch clause for error details
    try_it()                        # Failed: Input is empty
```

**This pattern handles errors explicitly. No surprises, no crashes.**

---

## Next Steps (5 More Minutes)

- **Read Chapter 01** (Getting Started) — 15 minute deep dive
- **Try examples** — Every chapter has copy-paste examples
- **Build projects** — Chapters 16-18 show complete projects
- **Reference cheat sheet** — See `CHEATSHEET-Syntax.md` for all syntax

---

## Troubleshooting Your First Program

**"error: file not found"**
-> Make sure your .zbr file exists and the compiler can find it

**"error: expected str, got int"**
-> Use `.toString()` or string interpolation: `"${number}"`

**Program compiles but does nothing**
-> Add a top-level `def main()`, or a `class Main` with `static def main` — one of those is your entry point

---

## Cheat Sheet: Five Commands

```zebra
var x = 5                       # Declare variable
def func(): str               # Define function
for item in list                # Loop over collection
if x > 5                        # Conditional
var v = risky() catch default   # Handle errors
```

---

## You're Ready!

You now understand:
- Variables and types
- Functions
- Collections
- Control flow
- Error handling

Read Chapter 02 next to understand the type system deeper, or jump straight to Chapter 16 to build a real project.

**Welcome to Zebra!**

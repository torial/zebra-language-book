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

## Minute 4-10: Your First Program

Create a file: `hello.zbr`

```zebra
class Main
    shared
        def main
            print "Hello, World!"
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
var name = "Alice"              # String
var age = 30                    # Integer
var pi = 3.14                   # Float
var active = true               # Boolean
```

**Key:** Zebra figures out the type. You don't need to write it.

### 2. Functions

```zebra
def greet(name as str) as str
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
    print fruit
```

**Key:** Lists are for ordered collections. Use `for...in` to loop.

### 4. If/Else and Loops

```zebra
var x = 10

if x > 5
    print "Large"
else
    print "Small"

while x > 0
    print x
    x = x - 1
```

**Key:** No parentheses needed. Indentation matters.

### 5. Error Handling

```zebra
# Functions that can fail use `throws`
var content = File.read("data.txt") catch "could not read"
print content

# Or use try/catch for more control
try
    var data = File.read("data.txt")
    print data
catch |err|
    print "Error: ${err}"
```

**Key:** Functions annotated with `throws` can fail. Use `catch` for fallback or `try`/`catch` for structured handling.

---

## Minute 21-25: Build Something Real

Create `count_lines.zbr`:

```zebra
class Main
    shared
        def main
            var filename = "input.txt"

            var content = File.read(filename) catch ""
            if content.len == 0
                print "Error: could not read file"
                sys.exit(1)

            var lines = content.split("\n")

            print "File: ${filename}"
            print "Lines: ${lines.count()}"
            print "Total characters: ${content.len}"
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
def do_something(input as str) as str throws
    # 1. Validate input
    if input.len == 0
        raise "Input is empty"

    # 2. Do work
    var result = process(input)

    # 3. Return success
    return result

class Main
    shared
        def main
            # Use catch for simple fallback
            var value = do_something("data") catch "default"
            print value

            # Or try/catch for error details
            try
                var v = do_something("")
                print v
            catch |err|
                print "Failed: ${err}"
```

**This pattern handles errors explicitly. No surprises, no crashes.**

---

## Next Steps (5 More Minutes)

- **Read Chapter 01** (Getting Started) — 15 minute deep dive
- **Try examples** — Every chapter has copy-paste examples
- **Build projects** — Chapters 16-18 show complete projects
- **Reference cheat sheet** — See `CHEATSHEET.md` for all syntax

---

## Troubleshooting Your First Program

**"error: file not found"**
-> Make sure your .zbr file exists and the compiler can find it

**"error: expected str, got int"**
-> Use `.toString()` or string interpolation: `"${number}"`

**Program compiles but does nothing**
-> Add a `class Main` with `shared def main` — that's your entry point

---

## Cheat Sheet: Five Commands

```zebra
var x = 5                       # Declare variable
def func() as str               # Define function
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

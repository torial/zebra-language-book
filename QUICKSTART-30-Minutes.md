# Zebra: 30 Minutes to Productive

Get from zero to your first working Zebra program in 30 minutes.

---

## Minute 1-3: What is Zebra?

Zebra is a modern programming language combining:
- **Python's simplicity** — readable, clear syntax
- **C#'s power** — strong types, interfaces, generics
- **Nil safety** — prevents null pointer crashes
- **Error handling** — explicit Result types instead of exceptions
- **Performance** — compiles to Zig/WebAssembly

You can read your first working program in 2 minutes.

---

## Minute 4-10: Your First Program

Create a file: `hello.zbr`

```zebra
def main()
    println("Hello, World!")
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
    println(fruit)
```

**Key:** Lists are for ordered collections. Use `for...in` to loop.

### 4. If/Else and Loops

```zebra
var x = 10

if x > 5
    println("Large")
else
    println("Small")

while x > 0
    println(x)
    x = x - 1
```

**Key:** No parentheses needed. Indentation matters.

### 5. Error Handling with Result

```zebra
var result = File.read("data.txt")

if result.isOk()
    var content = result.value()
    println(content)
else
    println("Error: ${result.error()}")
```

**Key:** Functions return `Result(SuccessType, ErrorType)`. Check with `.isOk()`.

---

## Minute 21-25: Build Something Real

Create `count_lines.zbr`:

```zebra
def main()
    var filename = "input.txt"
    
    var result = File.read(filename)
    
    if result.isErr()
        println("Error: ${result.error()}")
        return
    
    var content = result.value()
    var lines = content.split("\n")
    
    println("File: ${filename}")
    println("Lines: ${lines.count()}")
    println("Total characters: ${content.len}")
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
def do_something(input as InputType) as Result(OutputType, ErrorType)
    # 1. Validate input
    if input.len == 0
        return Result.err("Input is empty")
    
    # 2. Do work
    var result = process(input)
    
    # 3. Return success
    return Result.ok(result)

def main()
    # 1. Call function
    var operation_result = do_something("data")
    
    # 2. Check for errors
    if operation_result.isErr()
        println("Failed: ${operation_result.error()}")
        return
    
    # 3. Use result
    var value = operation_result.value()
    println(value)
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

**"error: unknown function 'println'"**
→ Upgrade your Zebra compiler

**"error: file not found"**
→ Make sure your .zbr file exists and the compiler can find it

**"error: expected str, got int"**
→ Use `.toString()` or string interpolation: `"${number}"`

**Program compiles but does nothing**
→ Add a `def main()` function — that's your entry point

---

## Cheat Sheet: Five Commands

```zebra
var x = 5                       # Declare variable
def func() as str               # Define function
for item in list                # Loop over collection
if x > 5                        # Conditional
Result.ok(value)                # Return success
```

---

## You're Ready!

You now understand:
- ✅ Variables and types
- ✅ Functions
- ✅ Collections
- ✅ Control flow
- ✅ Error handling

Read Chapter 02 next to understand the type system deeper, or jump straight to Chapter 16 to build a real project.

**Welcome to Zebra! 🦓**

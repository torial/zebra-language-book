# Chapter 19: Standard Library Tour

**Time:** 90 min | **Audience:** Intermediate | **Prerequisites:** Chapters 01-06

---

## Learning Outcomes

After this chapter, you will:
- Know the major modules and APIs in Zebra's standard library
- Understand when to use built-in functions vs. writing your own
- Navigate API documentation effectively
- Use string, collection, and math operations fluently
- Recognize patterns you can apply to your own libraries

---

## Overview: What's Already Built

One of Zebra's strengths is a thoughtfully designed standard library that covers common tasks without being bloated. Before writing utilities or helper functions, check what's already available. This chapter is a tour of the major components.

The standard library is organized into logical modules:
- **String Operations** — manipulation and inspection
- **Collection Operations** — Lists, HashMaps, Sets
- **Type Conversions** — converting between types
- **Math Operations** — numeric functions
- **System Access** — arguments, environment, file paths
- **I/O Basics** — console and file operations

---

## String Operations

Strings are the most commonly used type in real-world programs. Zebra's string API is powerful but focused on the most useful operations.

### Basic Properties and Inspection

```zebra
// file: stdlib-string-inspect.zbr
// teaches: string properties and inspection methods
// chapter: 19

def main()
    var text = "Hello, World!"
    
    // Length
    println(text.len)           # 13
    
    // Check if empty
    if text.len == 0
        println("Empty string")
    
    // Character access
    var first_char = text.charAt(0)     # 'H'
    var last_char = text.charAt(text.len - 1)   # '!'
    println(first_char)
    println(last_char)
    
    // Check existence
    if text.contains("World")
        println("Found World")
    
    if text.startsWith("Hello")
        println("Greeting detected")
    
    if text.endsWith("!")
        println("Exclamation found")
```

### Case Conversion

```zebra
// file: stdlib-string-case.zbr
// teaches: case conversion methods
// chapter: 19

def main()
    var text = "Zebra Programming"
    
    // Uppercase
    var upper = text.upper()        # "ZEBRA PROGRAMMING"
    println(upper)
    
    // Lowercase
    var lower = text.lower()        # "zebra programming"
    println(lower)
    
    // Practical example: case-insensitive comparison
    def case_insensitive_equals(a as str, b as str) as bool
        return a.lower() == b.lower()
    
    if case_insensitive_equals("Zebra", "ZEBRA")
        println("Same language, different case")
```

### String Searching and Replacement

```zebra
// file: stdlib-string-search.zbr
// teaches: searching and replacing in strings
// chapter: 19

def main()
    var message = "The quick brown fox jumps over the lazy dog"
    
    // Find first occurrence
    var pos = message.indexOf("fox")  # 16
    if pos >= 0
        println("Found 'fox' at position ${pos}")
    
    // Count occurrences (manual approach)
    var text = "apple apple apple"
    var count = 0
    var search_pos = 0
    while search_pos >= 0
        search_pos = text.indexOf("apple", search_pos)
        if search_pos >= 0
            count = count + 1
            search_pos = search_pos + 1
    println(count)  # 3
    
    // Replace first occurrence
    var replaced = message.replace("fox", "cat")
    println(replaced)  # "The quick brown cat jumps over the lazy dog"
    
    // Replace all occurrences
    var all_replaced = message.replaceAll("the", "a")
    println(all_replaced)
```

### String Splitting and Joining

```zebra
// file: stdlib-string-split-join.zbr
// teaches: splitting and joining strings
// chapter: 19

def main()
    // Split by delimiter
    var csv_line = "John,25,Engineer,San Francisco"
    var fields = csv_line.split(",")
    
    // fields is a List(str)
    println(fields.count())     # 4
    println(fields.at(0))       # "John"
    println(fields.at(1))       # "25"
    
    // Process fields
    var names = List(str)()
    for field in fields
        if field.len > 0
            names.add(field)
    
    // Join with separator
    var rejoined = names.join(" | ")
    println(rejoined)  # "John | 25 | Engineer | San Francisco"
    
    // Multi-character delimiter
    var text = "apple::orange::banana"
    var fruits = text.split("::")
    println(fruits.join(", "))  # "apple, orange, banana"
```

### Whitespace Trimming

```zebra
// file: stdlib-string-trim.zbr
// teaches: removing whitespace from strings
// chapter: 19

def main()
    var input = "  Hello, World!  \n"
    
    // Trim both sides
    var trimmed = input.trim()      # "Hello, World!"
    println("'${trimmed}'")
    
    // Trim left side only
    var right_padded = "  left-trimmed"
    println("'${right_padded.trimLeft()}'")  # "'left-trimmed'"
    
    // Trim right side only
    var left_padded = "right-trimmed  "
    println("'${left_padded.trimRight()}'")  # "'right-trimmed  '"
    
    // Practical use: parsing user input
    def parse_number_from_input(input as str) as int?
        var trimmed = input.trim()
        if trimmed.len == 0
            return nil
        return trimmed.toInt()
    
    var num = parse_number_from_input("  42  ")
    if num != nil
        println("Parsed: ${num}")
```

### String Extraction and Concatenation

```zebra
// file: stdlib-string-extract-concat.zbr
// teaches: substring extraction and string concatenation
// chapter: 19

def main()
    var text = "Hello, World!"
    
    // Extract substring
    var hello = text.substring(0, 5)    # "Hello"
    var world = text.substring(7, 12)   # "World"
    println(hello)
    println(world)
    
    // Concatenate strings
    var greeting = hello.concat(", ").concat(world)
    println(greeting)  # "Hello, World"
    
    // String interpolation (often cleaner)
    var result = "${hello}, ${world}"
    println(result)
    
    // Building strings in loops
    var parts = List(str)()
    for i in 1.to(5)
        parts.add("Item-${i}")
    
    var result_str = parts.join(", ")
    println(result_str)  # "Item-1, Item-2, Item-3, Item-4, Item-5"
```

---

## Collection Operations

Collections are the workhorses of most programs. Zebra provides three main collection types, each with a focused API.

### List Operations

Lists are ordered, mutable collections that grow dynamically. They're your go-to for sequences.

```zebra
// file: stdlib-list-ops.zbr
// teaches: list operations and patterns
// chapter: 19

def main()
    var items = List(str)()
    
    // Add items
    items.add("apple")
    items.add("banana")
    items.add("cherry")
    println(items.count())  # 3
    
    // Access by index
    println(items.at(0))    # "apple"
    println(items.at(2))    # "cherry"
    
    // Check contents
    if items.contains("banana")
        println("Found banana")
    
    // Remove specific item
    items.remove("banana")
    println(items.count())  # 2
    
    // Iterate over list
    for fruit in items
        println("Fruit: ${fruit}")
    
    // Find index of item
    var pos = items.indexOf("apple")  # 0 or -1 if not found
    if pos >= 0
        println("Found at position ${pos}")
    
    // Clear list
    items.clear()
    println(items.count())  # 0
```

### HashMap Operations

HashMaps store key-value pairs. Use them when you need to look up values by name or ID.

```zebra
// file: stdlib-hashmap-ops.zbr
// teaches: hashmap operations and patterns
// chapter: 19

def main()
    var scores = HashMap(str, int)()
    
    // Add key-value pairs
    scores.put("Alice", 95)
    scores.put("Bob", 87)
    scores.put("Charlie", 92)
    
    // Retrieve value
    var alice_score = scores.fetch("Alice")  # 95
    if alice_score != nil
        println("Alice scored: ${alice_score}")
    
    // Check if key exists
    if scores.contains("Bob")
        println("Bob's record found")
    
    // Update value
    scores.put("Bob", 89)  # Overwrites previous
    
    // Remove key
    scores.remove("Charlie")
    
    // Iterate over key-value pairs
    for key in scores.keys()
        var value = scores.fetch(key)
        if value != nil
            println("${key}: ${value}")
    
    // Get all keys
    var all_keys = scores.keys()
    println(all_keys.count())  # 2
```

### Set Operations

Sets store unique items with no duplicates. Use them for membership testing and deduplication.

```zebra
// file: stdlib-set-ops.zbr
// teaches: set operations for uniqueness
// chapter: 19

def main()
    var visited_cities = Set(str)()
    
    // Add items
    visited_cities.add("New York")
    visited_cities.add("London")
    visited_cities.add("Tokyo")
    
    // Try adding duplicate
    visited_cities.add("New York")  # No-op, already exists
    println(visited_cities.count())  # 3
    
    // Check membership
    if visited_cities.contains("Paris")
        println("Been to Paris")
    else
        println("Haven't visited Paris yet")
    
    // Remove item
    visited_cities.remove("Tokyo")
    
    // Iterate over set
    for city in visited_cities
        println("Visited: ${city}")
    
    // Practical: remove duplicates from list
    var numbers = List(int)()
    numbers.add(1)
    numbers.add(2)
    numbers.add(2)
    numbers.add(3)
    numbers.add(3)
    numbers.add(3)
    
    var unique = Set(int)()
    for num in numbers
        unique.add(num)
    
    println(unique.count())  # 3
```

---

## Type Conversions

Zebra's type system is strict—you'll need to convert between types explicitly. The standard library provides straightforward conversion methods.

### String Conversions

```zebra
// file: stdlib-type-conversions.zbr
// teaches: converting between types and strings
// chapter: 19

def main()
    // String to int
    var num_str = "42"
    var num = num_str.toInt()
    println(num)  # 42
    
    // String to float
    var float_str = "3.14"
    var float_val = float_str.toFloat()
    println(float_val)  # 3.14
    
    // Int to string
    var num2 = 100
    var str2 = num2.toString()
    println(str2)  # "100"
    
    // Float to string
    var pi = 3.14159
    var pi_str = pi.toString()
    println(pi_str)  # "3.14159"
    
    // Boolean to string
    var flag = true
    var flag_str = flag.toString()
    println(flag_str)  # "true"
    
    // Error handling for conversions
    var user_input = "not a number"
    var parsed = user_input.toInt()
    if parsed == nil
        println("Invalid number")
    
    // Safe conversions with nil checking
    var value as int? = "123".toInt()
    if value != nil
        println("Parsed successfully: ${value}")
```

---

## Math Operations

Zebra doesn't have a separate "Math" module—arithmetic is built into the language and type system.

```zebra
// file: stdlib-math-operations.zbr
// teaches: basic math operations in Zebra
// chapter: 19

def main()
    // Arithmetic operators
    var a = 10
    var b = 3
    
    println(a + b)      # 13
    println(a - b)      # 7
    println(a * b)      # 30
    println(a / b)      # 3 (integer division)
    println(a % b)      # 1 (modulo/remainder)
    
    // Floating-point math
    var x = 10.5
    var y = 3.2
    
    println(x + y)      # 13.7
    println(x - y)      # 7.3
    println(x * y)      # 33.6
    println(x / y)      # ~3.28
    
    // Comparison operators
    println(a > b)      # true
    println(a < b)      # false
    println(a >= b)     # true
    println(a == b)     # false
    println(a != b)     # true
    
    // Logical operators
    var condition1 = true
    var condition2 = false
    
    println(condition1 and condition2)  # false
    println(condition1 or condition2)   # true
    println(not condition1)             # false
    
    // Common patterns: min/max
    def min(a as int, b as int) as int
        if a < b
            return a
        else
            return b
    
    def max(a as int, b as int) as int
        if a > b
            return a
        else
            return b
    
    println(min(5, 3))  # 3
    println(max(5, 3))  # 5
    
    // Absolute value
    def abs_value(n as int) as int
        if n < 0
            return 0 - n
        else
            return n
    
    println(abs_value(-42))  # 42
```

---

## System Access

Accessing the program's environment, arguments, and current directory is essential for real-world programs.

```zebra
// file: stdlib-system-access.zbr
// teaches: accessing system information
// chapter: 19

def main()
    // Command-line arguments
    var args = System.args()
    println("Argument count: ${args.count()}")
    
    if args.count() > 0
        println("First argument: ${args.at(0)}")
        println("All arguments:")
        for arg in args
            println("  - ${arg}")
    
    // Environment variables
    var home = System.env("HOME")
    if home != nil
        println("Home directory: ${home}")
    
    var path = System.env("PATH")
    if path != nil
        var dirs = path.split(":")  # On Unix; Windows uses ";"
        println("PATH has ${dirs.count()} directories")
    
    // Get current working directory
    var cwd = System.cwd()
    println("Current directory: ${cwd}")
    
    // Practical example: parse arguments
    def parse_arguments(args as List(str)) as HashMap(str, str)?
        var options = HashMap(str, str)()
        var i = 0
        
        while i < args.count()
            var arg = args.at(i)
            
            if arg.startsWith("--")
                var key = arg.substring(2, arg.len)
                var value = ""
                
                if i + 1 < args.count() and not args.at(i + 1).startsWith("--")
                    value = args.at(i + 1)
                    i = i + 1
                
                options.put(key, value)
            
            i = i + 1
        
        return options
```

---

## Console I/O

Basic console operations are fundamental to interactive programs.

```zebra
// file: stdlib-console-io.zbr
// teaches: printing to console
// chapter: 19

def main()
    // Simple output
    print("Hello, ")
    println("World!")  # Adds newline
    
    // Output of different types
    println(42)
    println(3.14)
    println(true)
    
    // String interpolation (covered earlier)
    var name = "Alice"
    var age = 30
    println("${name} is ${age} years old")
    
    // Formatted output
    var price = 19.99
    println("Price: $${price}")
    
    // Error output (if available)
    System.errln("This is an error message")
    
    // Practical: status messages
    def process_items(items as List(str))
        for item in items
            print("Processing ${item}... ")
            // Do work here
            println("Done")
    
    var items = List(str)()
    items.add("file1.txt")
    items.add("file2.txt")
    items.add("file3.txt")
    
    process_items(items)
```

---

## Practical Patterns: Data Processing

Now let's put these pieces together in real scenarios.

```zebra
// file: stdlib-data-processing.zbr
// teaches: combining stdlib functions for data processing
// chapter: 19

def main()
    // Parse CSV and calculate statistics
    var data = "Alice,95,Engineering
Bob,87,Sales
Charlie,92,Engineering
Diana,88,Sales"
    
    var lines = data.split("\n")
    var scores = List(int)()
    var dept_map = HashMap(str, int)()
    
    for line in lines
        var parts = line.split(",")
        if parts.count() == 3
            var name = parts.at(0)
            var score = parts.at(1).toInt()
            var dept = parts.at(2).trim()
            
            if score != nil
                scores.add(score)
            
            // Track count by department
            var current = dept_map.fetch(dept)
            if current != nil
                dept_map.put(dept, current + 1)
            else
                dept_map.put(dept, 1)
    
    // Calculate average
    var total = 0
    for score in scores
        total = total + score
    
    var average = total / scores.count()
    println("Average score: ${average}")
    
    // Report by department
    println("Departments:")
    for dept in dept_map.keys()
        var count = dept_map.fetch(dept)
        println("  ${dept}: ${count} people")
```

---

## Key Takeaways

1. **Know Your Tools** — The standard library covers 80% of common tasks. Check the API before rolling your own.

2. **String Operations** — Master `.split()`, `.join()`, `.contains()`, `.replace()` and type conversions—you'll use them constantly.

3. **Collections First** — Always think: "Should this be a List, HashMap, or Set?" before designing data structures.

4. **Explicit Types** — Zebra's strict type system means conversions are explicit. That's a feature, not a bug.

5. **Read Documentation** — This chapter is a tour, not exhaustive. The full API reference is your friend.

---

## Exercises

1. **Word Frequency Counter** — Read a CSV, split by commas, count unique words with a HashMap
2. **Case Converter** — Read user input, convert to upper/lower/title case based on command-line flag
3. **CSV Validator** — Read CSV file, ensure all rows have same number of columns, report errors
4. **Text Processor** — Read text, remove duplicates, sort alphabetically, print report

---

## What's Next

You now understand what's available in the standard library. Chapter 20 covers extending that capability with file I/O and system access for real-world programs.

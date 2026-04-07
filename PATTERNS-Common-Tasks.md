# Zebra: Common Patterns Reference

Copy-paste patterns for typical programming tasks.

---

## File Operations

### Read Entire File Safely

```zebra
var filename = "data.txt"
var result = File.read(filename)

if result.isErr()
    println("Cannot read file: ${result.error()}")
    return

var content = result.value()
# Use content...
```

### Write File Safely

```zebra
var filename = "output.txt"
var content = "File contents here"

var result = File.write(filename, content)

if result.isErr()
    println("Cannot write file: ${result.error()}")
    return

println("File written successfully")
```

### Process File Line by Line

```zebra
var result = File.read("file.txt")

if result.isErr()
    return

var content = result.value()
var lines = content.split("\n")

for line in lines
    if line.trim().len == 0
        continue  # Skip empty lines
    
    # Process line...
    println(line)
```

### Read CSV File

```zebra
var result = File.read("data.csv")
if result.isErr()
    return

var content = result.value()
var lines = content.split("\n")
var records = List(List(str))()

for line in lines
    if line.trim().len == 0
        continue
    
    var fields = line.split(",")
    records.add(fields)

for record in records
    println(record)  # Each field: record.at(0), record.at(1), etc.
```

---

## String Processing

### Split and Process Words

```zebra
var text = "one two three four five"
var words = text.split(" ")

for word in words
    println("Word: ${word}")
```

### Build String from Parts

```zebra
var parts = List(str)()
parts.add("hello")
parts.add("world")
parts.add("from")
parts.add("zebra")

var message = parts.join(" ")      # "hello world from zebra"
```

### Find and Replace

```zebra
var text = "Hello World Hello"

# Replace first occurrence
var result1 = text.replace("Hello", "Hi")   # "Hi World Hello"

# Replace all occurrences
var result2 = text.replaceAll("Hello", "Hi")  # "Hi World Hi"

# Find position
var pos = text.indexOf("World")
if pos >= 0
    println("Found at position ${pos}")
```

### Extract Substring

```zebra
var text = "Hello, World!"

var greeting = text.substring(0, 5)      # "Hello"
var after_comma = text.substring(7, 12)  # "World"
```

### Clean Input

```zebra
var user_input = "  hello world  \n"
var clean = user_input.trim()            # "hello world"
```

### Case Conversion

```zebra
var text = "Hello World"

var upper = text.upper()                 # "HELLO WORLD"
var lower = text.lower()                 # "hello world"
```

---

## Collections & Lists

### Create and Populate List

```zebra
var numbers = List(int)()
numbers.add(1)
numbers.add(2)
numbers.add(3)
```

### Loop Over List

```zebra
for item in items
    println(item)

# With index
for i in 0.to(items.count())
    println("${i}: ${items.at(i)}")
```

### Find Item in List

```zebra
var target = "apple"

for item in items
    if item == target
        println("Found it!")
        break
```

### Filter List

```zebra
var numbers = List(int)()
numbers.add(1)
numbers.add(2)
numbers.add(3)
numbers.add(4)
numbers.add(5)

var evens = List(int)()
for num in numbers
    if num % 2 == 0
        evens.add(num)

# evens = [2, 4]
```

### Transform List

```zebra
var numbers = List(int)()
numbers.add(1)
numbers.add(2)
numbers.add(3)

var doubled = List(int)()
for num in numbers
    doubled.add(num * 2)

# doubled = [2, 4, 6]
```

### Remove Duplicates

```zebra
var items = List(str)()
items.add("apple")
items.add("banana")
items.add("apple")
items.add("cherry")

var unique = Set(str)()
for item in items
    unique.add(item)

# unique has: apple, banana, cherry (duplicates removed)
```

### Count Occurrences

```zebra
var items = List(str)()
items.add("apple")
items.add("apple")
items.add("banana")

var count = 0
for item in items
    if item == "apple"
        count = count + 1

println(count)  # 2
```

---

## Dictionaries & Maps

### Create and Use HashMap

```zebra
var scores = HashMap(str, int)()

scores.put("Alice", 95)
scores.put("Bob", 87)
scores.put("Charlie", 92)

var alice_score = scores.fetch("Alice")
if alice_score != nil
    println("Alice: ${alice_score}")
```

### Loop Over HashMap

```zebra
for key in scores.keys()
    var value = scores.fetch(key)
    if value != nil
        println("${key}: ${value}")
```

### Check if Key Exists

```zebra
if scores.contains("Alice")
    println("Alice found")
else
    println("Alice not found")
```

### Count by Category

```zebra
var items = List(str)()
items.add("red")
items.add("blue")
items.add("red")
items.add("blue")
items.add("red")

var counts = HashMap(str, int)()

for item in items
    var current = counts.fetch(item)
    if current != nil
        counts.put(item, current + 1)
    else
        counts.put(item, 1)

# counts: red->3, blue->2
```

---

## Error Handling

### Safe Function that Can Fail

```zebra
def divide(a as int, b as int) as Result(int, str)
    if b == 0
        return Result.err("Cannot divide by zero")
    
    return Result.ok(a / b)

def main()
    var result = divide(10, 2)
    
    if result.isErr()
        println("Error: ${result.error()}")
        return
    
    var value = result.value()
    println("Result: ${value}")
```

### Propagate Errors Up

```zebra
def process_file(filename as str) as Result(int, str)
    var read_result = File.read(filename)
    
    if read_result.isErr()
        return Result.err(read_result.error())
    
    var content = read_result.value()
    var line_count = content.split("\n").count()
    
    return Result.ok(line_count)
```

### Handle Multiple Errors

```zebra
def calculate(a_str as str, b_str as str) as Result(int, str)
    var a = a_str.toInt()
    if a == nil
        return Result.err("Invalid first number")
    
    var b = b_str.toInt()
    if b == nil
        return Result.err("Invalid second number")
    
    return Result.ok(a + b)
```

### Try Multiple Operations

```zebra
def process_data() as Result(bool, str)
    # Step 1
    var read_result = File.read("input.txt")
    if read_result.isErr()
        return Result.err("Cannot read input")
    var input = read_result.value()
    
    # Step 2: Process
    var processed = input.upper()
    
    # Step 3
    var write_result = File.write("output.txt", processed)
    if write_result.isErr()
        return Result.err("Cannot write output")
    
    return Result.ok(true)
```

---

## Null Safety

### Safe Null Check

```zebra
var x as int? = get_value()

if x != nil
    println("Value: ${x}")
else
    println("No value")
```

### Use Default Value

```zebra
var x as int? = get_value()
var value = x.unwrapOr(0)  # Use 0 if nil
println(value)
```

### Optional Chain

```zebra
var user as User? = get_user()

if user != nil
    if user.address != nil
        println(user.address)
```

### Nested Null Checks

```zebra
var data as Data? = fetch_data()

if data != nil
    var items = data.items
    if items != nil
        for item in items
            println(item)
```

---

## Type Conversions

### String to Number

```zebra
var num_str = "42"
var num = num_str.toInt()

if num != nil
    println(num + 1)
else
    println("Invalid number")
```

### Number to String

```zebra
var num = 42
var text = num.toString()
var message = "The answer is ${text}"
```

### String Interpolation (Preferred)

```zebra
var num = 42
println("The answer is ${num}")
```

### Type Checking

```zebra
var value = 42

# Check if it's an int
var as_str = value.toString()  # Force conversion

# Check compatibility
if value > 0
    println("Positive")
```

---

## Classes & Objects

### Create Class with Constructor

```zebra
class Person
    var name as str = ""
    var age as int = 0
    
    def init(name as str, age as int)
        this.name = name
        this.age = age
    
    def describe() as str
        return "${name} is ${age} years old"

var person = Person("Alice", 30)
println(person.describe())
```

### Use Inheritance

```zebra
class Animal
    var name as str = ""
    
    def speak() as str
        return "Some sound"

class Dog is Animal
    def speak() as str
        return "Woof!"

var dog = Dog()
dog.name = "Buddy"
println(dog.speak())
```

### Implement Interface

```zebra
interface Shape
    def area() as float

class Circle is Shape
    var radius as float = 0.0
    
    def area() as float
        return 3.14159 * radius * radius

var circle = Circle()
circle.radius = 5.0
println(circle.area())
```

### Static Methods

```zebra
class Math
    shared
        def add(a as int, b as int) as int
            return a + b

var result = Math.add(2, 3)  # 5
```

---

## Regular Expressions

### Validate Pattern

```zebra
var email_pattern = Regex.compile("[a-z0-9]+@[a-z]+\\.[a-z]+")

if email_pattern.matches("user@example.com")
    println("Valid email")
```

### Find Matches

```zebra
var numbers = Regex.compile("\\d+")
var text = "I have 3 apples and 7 oranges"

var matches = numbers.findAll(text)
# matches = ["3", "7"]

for match in matches
    println(match)
```

### Split by Pattern

```zebra
var delimiter = Regex.compile("\\s+")  # One or more spaces
var text = "one  two   three"
var words = delimiter.split(text)
# words = ["one", "two", "three"]
```

### Replace Pattern

```zebra
var pattern = Regex.compile("\\d+")
var text = "Version 2.3.1"

var replaced = pattern.replaceAll(text, "X")
# replaced = "Version X.X.X"
```

---

## Command-Line Arguments

### Read Arguments

```zebra
def main()
    var args = System.args()
    
    if args.count() > 0
        println("Arguments:")
        for arg in args
            println("  - ${arg}")
    else
        println("No arguments provided")
```

### Parse Flags

```zebra
def main()
    var args = System.args()
    var verbose = false
    var input_file = ""
    
    for arg in args
        if arg == "-v" or arg == "--verbose"
            verbose = true
        elif arg.startsWith("--input=")
            input_file = arg.substring(8, arg.len)
    
    println("Verbose: ${verbose}")
    println("Input: ${input_file}")
```

---

## Environment Variables

### Read Environment Variables

```zebra
var home = System.env("HOME")
if home != nil
    println("Home: ${home}")
else
    println("HOME not set")

var path = System.env("PATH")
```

### Check Required Variables

```zebra
var api_key = System.env("API_KEY")

if api_key == nil
    println("Error: API_KEY environment variable not set")
    System.exit(1)

println("Using API key: ${api_key}")
```

---

## Loops & Iteration

### Count Loop

```zebra
for i in 0.to(10)
    println(i)  # 0, 1, 2, ..., 9
```

### While Loop

```zebra
var i = 0
while i < 10
    println(i)
    i = i + 1
```

### Loop Until Condition

```zebra
var count = 0
while count < 5
    println(count)
    count = count + 1
```

### Early Exit

```zebra
for item in items
    if item == target
        println("Found!")
        break

while condition
    if error_detected
        break
```

### Skip Iteration

```zebra
for item in items
    if item == skip_value
        continue
    
    println(item)
```

---

## Practical Patterns

### CSV Reader

```zebra
def read_csv(filename as str) as Result(List(List(str)), str)
    var result = File.read(filename)
    
    if result.isErr()
        return Result.err(result.error())
    
    var content = result.value()
    var lines = content.split("\n")
    var records = List(List(str))()
    
    for line in lines
        if line.trim().len == 0
            continue
        
        var fields = line.split(",")
        records.add(fields)
    
    return Result.ok(records)
```

### Word Counter

```zebra
def count_words(filename as str) as Result(HashMap(str, int), str)
    var result = File.read(filename)
    
    if result.isErr()
        return Result.err(result.error())
    
    var content = result.value()
    var text = content.lower()
    var words = text.split(" ")
    var counts = HashMap(str, int)()
    
    for word in words
        var clean = word.trim()
        if clean.len > 0
            var current = counts.fetch(clean)
            if current != nil
                counts.put(clean, current + 1)
            else
                counts.put(clean, 1)
    
    return Result.ok(counts)
```

### Pipeline Processing

```zebra
var input = "  hello world  from zebra  "

var result = input
    -> .trim()
    -> .lower()
    -> .split(" ")

# result is List(str) = ["hello", "world", "from", "zebra"]
```

---

## Quick Debugging

### Print Variable Value

```zebra
var x = 42
println("x = ${x}")
```

### Check Collection Size

```zebra
var items = List(int)()
items.add(1)
items.add(2)
println("Count: ${items.count()}")
```

### Trace Execution

```zebra
def function()
    println("Start")
    # ... code ...
    println("After step 1")
    # ... code ...
    println("Done")
```

### Assert Conditions

```zebra
assert x > 0, "x must be positive"
assert items.count() > 0, "list must not be empty"
```

---

**Save this page and copy patterns as needed!**

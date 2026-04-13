# Zebra: Common Patterns Reference

Copy-paste patterns for typical programming tasks.

---

## File Operations

### Read Entire File Safely

```zebra
var content = File.read("data.txt") catch ""
if content.len == 0
    print "Cannot read file"
    return
# Use content...
```

### Write File Safely

```zebra
try
    File.write("output.txt", "File contents here")
    print "File written successfully"
catch |err|
    print "Cannot write file: ${err}"
```

### Process File Line by Line

```zebra
var content = File.read("file.txt") catch ""
var lines = content.split("\n")

for line in lines
    if line.trim().len == 0
        continue  # Skip empty lines

    # Process line...
    print line
```

### Read CSV File

```zebra
var content = File.read("data.csv") catch ""
var lines = content.split("\n")
var records = List(List(str))()

for line in lines
    if line.trim().len == 0
        continue

    var fields = line.split(",")
    records.add(fields)

for record in records
    print record  # Each field: record.at(0), record.at(1), etc.
```

---

## String Processing

### Split and Process Words

```zebra
var text = "one two three four five"
var words = text.split(" ")

for word in words
    print "Word: ${word}"
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
    print "Found at position ${pos}"
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
    print item

# With index
for i in 0.to(items.count())
    print "${i}: ${items.at(i}")
```

### Find Item in List

```zebra
var target = "apple"

for item in items
    if item == target
        print "Found it!"
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

var seen = HashMap(str, bool)()
var unique = List(str)()
for item in items
    if not seen.contains(item)
        seen.set(item, true)
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

print count  # 2
```

---

## Dictionaries & Maps

### Create and Use HashMap

```zebra
var scores = HashMap(str, int)()

scores.set("Alice", 95)
scores.set("Bob", 87)
scores.set("Charlie", 92)

var alice_score = scores.get("Alice")
if alice_score != nil
    print "Alice: ${alice_score}"
```

### Loop Over HashMap

```zebra
for key in scores.keys()
    var value = scores.get(key)
    if value != nil
        print "${key}: ${value}"
```

### Check if Key Exists

```zebra
if scores.contains("Alice")
    print "Alice found"
else
    print "Alice not found"
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
    var current = counts.get(item)
    if current != nil
        counts.set(item, current + 1)
    else
        counts.set(item, 1)

# counts: red->3, blue->2
```

---

## Error Handling

### Safe Function that Can Fail

```zebra
def divide(a as int, b as int) as int throws
    if b == 0
        raise "Cannot divide by zero"
    return a / b

class Main
    shared
        def main
            var value = divide(10, 2) catch 0
            print "Result: ${value}"

            try
                var v = divide(10, 0)
                print v
            catch |err|
                print "Error: ${err}"
```

### Propagate Errors Up

```zebra
def process_file(filename as str) as int throws
    var content = File.read(filename)
    var line_count = content.split("\n").count()
    return line_count
```

### Handle Multiple Errors

```zebra
def calculate(a_str as str, b_str as str) as int throws
    var a = a_str.toInt()
    if a == nil
        raise "Invalid first number"

    var b = b_str.toInt()
    if b == nil
        raise "Invalid second number"

    return a + b
```

### Try Multiple Operations

```zebra
def process_data() throws
    # Step 1
    var input = File.read("input.txt")

    # Step 2: Process
    var processed = input.upper()

    # Step 3
    File.write("output.txt", processed)
```

---

## Null Safety

### Safe Null Check

```zebra
var x as int? = get_value()

if x != nil
    print "Value: ${x}"
else
    print "No value"
```

### Use Default Value

```zebra
var x as int? = get_value()
var value = x.unwrapOr(0)  # Use 0 if nil
print value
```

### Optional Chain

```zebra
var user as User? = get_user()

if user != nil
    if user.address != nil
        print user.address
```

### Nested Null Checks

```zebra
var data as Data? = fetch_data()

if data != nil
    var items = data.items
    if items != nil
        for item in items
            print item
```

---

## Type Conversions

### String to Number

```zebra
var num_str = "42"
var num = num_str.toInt()

if num != nil
    print num + 1
else
    print "Invalid number"
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
print "The answer is ${num}"
```

### Type Checking

```zebra
var value = 42

# Check if it's an int
var as_str = value.toString()  # Force conversion

# Check compatibility
if value > 0
    print "Positive"
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
print person.describe()
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
print dog.speak()
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
print circle.area()
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
    print "Valid email"
```

### Find Matches

```zebra
var numbers = Regex.compile("\\d+")
var text = "I have 3 apples and 7 oranges"

var matches = numbers.findAll(text)
# matches = ["3", "7"]

for match in matches
    print match
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
class Main
    shared
        def main
            var args = sys.args()

            if args.count() > 0
                print "Arguments:"
                for arg in args
                    print "  - ${arg}"
            else
                print "No arguments provided"
```

### Parse Flags

```zebra
class Main
    shared
        def main
            var args = sys.args()
            var verbose = false
            var input_file = ""

            for arg in args
                if arg == "-v" or arg == "--verbose"
                    verbose = true
                elif arg.startsWith("--input=")
                    input_file = arg.substring(8, arg.len)

            print "Verbose: ${verbose}"
            print "Input: ${input_file}"
```

---

## Environment Variables

### Environment and Exit

```zebra
# Exit with status code
sys.exit(1)

# Use Arg for structured argument parsing
var result = Arg.parse()
```

---

## Loops & Iteration

### Count Loop

```zebra
for i in 0.to(10)
    print i  # 0, 1, 2, ..., 9
```

### While Loop

```zebra
var i = 0
while i < 10
    print i
    i = i + 1
```

### Loop Until Condition

```zebra
var count = 0
while count < 5
    print count
    count = count + 1
```

### Early Exit

```zebra
for item in items
    if item == target
        print "Found!"
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
    
    print item
```

---

## Practical Patterns

### CSV Reader

```zebra
def read_csv(filename as str) as List(List(str)) throws
    var content = File.read(filename)
    var lines = content.split("\n")
    var records = List(List(str))()

    for line in lines
        if line.trim().len == 0
            continue

        var fields = line.split(",")
        records.add(fields)

    return records
```

### Word Counter

```zebra
def count_words(filename as str) as HashMap(str, int) throws
    var content = File.read(filename)
    var text = content.lower()
    var words = text.split(" ")
    var counts = HashMap(str, int)()

    for word in words
        var clean = word.trim()
        if clean.len > 0
            var current = counts.get(clean)
            if current != nil
                counts.set(clean, current + 1)
            else
                counts.set(clean, 1)

    return counts
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
print "x = ${x}"
```

### Check Collection Size

```zebra
var items = List(int)()
items.add(1)
items.add(2)
print "Count: ${items.count(}")
```

### Trace Execution

```zebra
def function()
    print "Start"
    # ... code ...
    print "After step 1"
    # ... code ...
    print "Done"
```

### Assert Conditions

```zebra
assert x > 0, "x must be positive"
assert items.count() > 0, "list must not be empty"
```

---

**Save this page and copy patterns as needed!**

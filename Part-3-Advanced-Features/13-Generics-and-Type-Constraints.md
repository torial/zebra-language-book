# 13: Generics and Type Constraints

**Audience:** Experienced programmers  
**Time:** 120 minutes  
**Prerequisites:** 02-Values-and-Types, 07-Classes-and-Instances, 08-Interfaces-and-Protocols  
**You'll learn:** Generic types, type parameters, constraints, practical uses, common pitfalls

---

## The Big Picture

So far, you've written code that works with specific types: a `List(int)`, a `HashMap(str, int)`. But what if you want a function that works with **any type**? That's where **generics** come in.

Generics let you write code that's *type-safe* but *reusable* across different types:

```zebra
class Container(T)
    var item: T
    
    def get: T
        return item
```

`Container(int)` holds integers. `Container(str)` holds strings. Same code, different types. This is safer than using `object` or `any`, because the type checker still verifies you don't mix types.

---

## Generic Classes

![Generics Instantiation](diagrams/06-generics-instantiation.png)

The simplest generic is a **container that holds a single value**:

```zebra
# file: 13_generic_container.zbr
# teaches: generic class definition
# chapter: 13-Generics-and-Type-Constraints

class Container(T)
    var item: T
    
    def store(value: T)
        item = value
    
    def retrieve: T
        return item

def main()
    var int_box = Container(int)()
    int_box.store(42)
    print int_box.retrieve()  # Output: 42
    
    var str_box = Container(str)()
    str_box.store("hello")
    print str_box.retrieve()  # Output: hello
```

Notice the syntax:
- `Container(T)` — `T` is a **type parameter**
- `Container(int)()` — substitute `int` for `T`, then create an instance
- Inside the class, `T` can be used like any other type

You can have **multiple type parameters**:

```zebra
# file: 13_generic_pair.zbr
# teaches: multiple type parameters
# chapter: 13-Generics-and-Type-Constraints

class Pair(K, V)
    var key: K
    var value: V
    
    def set_key(k: K)
        key = k
    
    def set_value(v: V)
        value = v
    
    def get_key: K
        return key
    
    def get_value: V
        return value

def main()
    var p = Pair(str, int)()
    p.set_key("count")
    p.set_value(42)
    print "Key: ${p.get_key()}, Value: ${p.get_value()}"
```

---

## Generic Methods

You can also write **generic methods** within regular classes:

```zebra
# file: 13_generic_methods.zbr
# teaches: generic methods
# chapter: 13-Generics-and-Type-Constraints

class Utils
    static
        def identity(value: T): T
            return value
        
        def first_of_three(a: T, b: T, c: T): T
            return a

def main()
    var x = Utils.identity(42)
    print x  # Output: 42
    
    var y = Utils.identity("hello")
    print y  # Output: hello
    
    var z = Utils.first_of_three(1, 2, 3)
    print z  # Output: 1
```

The type parameter `T` is inferred from the arguments you pass.

---

## Generic Collections

You already use generics implicitly with `List` and `HashMap`:

```zebra
# file: 13_generic_collections.zbr
# teaches: using generic stdlib types
# chapter: 13-Generics-and-Type-Constraints

def main()
    var numbers: List(int) = List()
    numbers.add(1)
    numbers.add(2)
    numbers.add(3)
    
    for n in numbers
        print n
    
    var ages: HashMap(str, int) = HashMap()
    ages.put("Alice", 30)
    ages.put("Bob", 25)
    
    for name, age in ages
        print "${name}: ${age}"
```

These are all generic types. The standard library provides them pre-built.

---

## Type Constraints

Sometimes you want a generic that works with **any type that implements an interface**:

```zebra
# file: 13_type_constraints.zbr
# teaches: interface constraints
# chapter: 13-Generics-and-Type-Constraints

interface Printable
    def display: str

class Dog
    implements Printable
        def display: str
            return "Woof!"

class Cat
    implements Printable
        def display: str
            return "Meow!"

class Printer
    static
        def print_item(item: Printable)
            print item.display()

def main()
    var dog = Dog()
    var cat = Cat()
    
    Printer.print_item(dog)  # Output: Woof!
    Printer.print_item(cat)  # Output: Meow!
```

Here, `Printer.print_item` accepts **any type** that implements `Printable`. This is a **constraint**: "T must implement interface Printable".

More advanced: constraints on generic methods:

```zebra
# file: 13_generic_constraints_advanced.zbr
# teaches: constraints in generic methods
# chapter: 13-Generics-and-Type-Constraints

interface Comparable
    def compare_to(other: this): int

class ComparableList(T)
    var items: List(T) = List()
    
    def add(item: T)
        items.add(item)
    
    def find_max: T?
        if items.count() == 0
            return nil
        var max = items.at(0)
        var i = 1
        while i < items.count()
            var item = items.at(i)
            # Here, T must implement Comparable
            if item.compare_to(max) > 0
                max = item
            i = i + 1
        return max

def main()
    var list = ComparableList()
    list.add(10)
    list.add(5)
    list.add(20)
    var max = list.find_max()
    if max != nil
        print "Max: ${max}"
```

---

## Real World: Generic Cache

A practical example: a **cache that works with any type**:

```zebra
# file: 13_generic_cache.zbr
# teaches: realistic generic class
# chapter: 13-Generics-and-Type-Constraints

class Cache(K, V)
    var data: HashMap(K, V) = HashMap()
    var max_size: int
    
    def init(max_size: int)
        this.max_size = max_size
    
    def put(key: K, value: V)
        if data.count() >= max_size and not data.contains(key)
            # Evict first key (simplistic LRU simulation)
            # In real code, track access order
            pass
        data.put(key, value)
    
    def lookup(key: K): V?
        if data.contains(key)
            return data.fetch(key)
        return nil
    
    def clear
        data = HashMap()

def main()
    var cache = Cache(str, int)()
    cache.init(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    
    var val = cache.lookup("b")
    if val != nil
        print "Got: ${val}"
```

---

## Common Mistakes

### Mistake 1: Forgetting to Instantiate Generic Parameters

```zebra
# WRONG
var box = Container()  # Error: T not specified
box.store(42)

# CORRECT
var box = Container(int)()
box.store(42)
```

### Mistake 2: Mixing Types in a Generic Container

```zebra
# WRONG
var box = Container(int)()
box.store("hello")  # Error: Expected int, got str

# CORRECT
var box = Container(str)()
box.store("hello")
```

### Mistake 3: Using Constraints Incorrectly

```zebra
# WRONG - method doesn't actually require Comparable
def find_max(items: List(T)): T
    var max = items.at(0)
    var item = items.at(1)
    if item > max  # Error: > not defined for all T
        max = item
    return max

# CORRECT - either don't use >, or require Comparable interface
def find_max(items: List(T)): T
    var max = items.at(0)
    for item in items
        if item.toString() > max.toString()  # Convert to string for comparison
            max = item
    return max
```

### Mistake 4: Type Erasure at Runtime

```zebra
# DANGER - at runtime, type information is lost
def process(items: List(T))
    for item in items
        if item isa int  # This may not work as expected
            print item + 10
```

In Zebra, type parameters are **erased** during code generation to Zig. Use interfaces to encode types you need at runtime.

---

## Exercises

### Exercise 1: Generic Stack

Implement a `Stack(T)` class with `push`, `pop`, and `is_empty` methods:

<details>
<summary>Solution</summary>

```zebra
class Stack(T)
    var items: List(T) = List()
    
    def push(value: T)
        items.add(value)
    
    def pop: T?
        if items.count() == 0
            return nil
        var value = items.at(items.count() - 1)
        # Remove last item (simplified - no remove method)
        return value
    
    def is_empty: bool
        return items.count() == 0

def main()
    var stack = Stack(int)()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    
    var val = stack.pop()
    if val != nil
        print "Popped: ${val}"
```

</details>

### Exercise 2: Generic Filter Function

Write a function that filters a list based on a predicate (function that returns bool):

<details>
<summary>Solution</summary>

```zebra
class ListUtils
    static
        def filter(items: List(T), predicate as T -> bool): List(T)
            var result: List(T) = List()
            for item in items
                if predicate(item)
                    result.add(item)
            return result

def main()
    var numbers: List(int) = List()
    numbers.add(1)
    numbers.add(2)
    numbers.add(3)
    numbers.add(4)
    
    var is_even: T -> bool = { x in x % 2 == 0 }
    var evens = ListUtils.filter(numbers, is_even)
    
    for e in evens
        print e
```

</details>

### Exercise 3: Generic Wrapper with Validation

Create a `ValidatedBox(T)` that only accepts values passing a validation function:

<details>
<summary>Solution</summary>

```zebra
class ValidatedBox(T)
    var item: T?
    var validator: T -> bool
    
    def init(validator: T -> bool)
        this.validator = validator
    
    def set(value: T): bool
        if validator(value)
            item = value
            return true
        return false
    
    def get: T?
        return item

def main()
    var age_box = ValidatedBox(int)()
    age_box.init({ x in x >= 0 and x <= 150 })
    
    if age_box.store(25)
        print "Valid age: ${age_box.retrieve()}"
    
    if not age_box.store(200)
        print "Invalid age"
```

</details>

---

## Key Takeaways

- **Generics enable type-safe reusable code** — Write once, use with many types
- **Type parameters are like function parameters** — `Container(T)` where T is filled in at use time
- **Collections are generics** — `List(T)`, `HashMap(K, V)` work with any type
- **Constraints limit generics** — Use interfaces to require specific capabilities
- **Type erasure happens at compile time** — Don't rely on runtime type information

---

## Next Steps

- → **14-Contracts** — Express what generics must provide
- → **15-Pipelines** — Chain generic operations cleanly
- → **Project 1** — Use generics in real code

---

**Generics are the bridge between flexibility and safety. Master them, and your code scales.**

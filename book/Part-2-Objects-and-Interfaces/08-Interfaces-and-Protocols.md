# 08: Interfaces and Protocols

**Audience:** All  
**Time:** 120 minutes  
**Prerequisites:** 07-Classes-and-Instances  
**You'll learn:** Define interfaces, implement contracts, polymorphism, real-world patterns

---

## The Big Picture

**Interfaces** define contracts—promises about what an object can do, without specifying how. Instead of depending on concrete classes, you depend on interfaces. This enables:
- **Swappable implementations** — Change how something works without changing callers
- **Polymorphism** — Treat different objects the same way
- **Testing** — Mock implementations easily
- **Flexibility** — Add new implementations without modifying existing code
 
---

## Defining Interfaces

### Simple Interface

```zebra
# file: 08_interface_basic.zbr
# teaches: interface definition
# chapter: 08-Interfaces-and-Protocols

interface Animal
    def speak(): str
    def move()

class Dog
    implements Animal
        def speak(): str
            return "Woof!"

        def move()
            print "Running on four legs"

class Bird
    implements Animal
        def speak(): str
            return "Tweet!"

        def move()
            print "Flying through the air"

def main()
    var dog: Animal = Dog()
    print dog.speak()      # Woof!
    dog.move()             # Running on four legs

    var bird: Animal = Bird()
    print bird.speak()     # Tweet!
    bird.move()            # Flying through the air
```

**Key points:**
- `interface Animal` — Define what any animal must do
- `implements Animal` — Promise to implement all methods
- Treat objects as their interface type (`var dog: Animal`)

### Multiple Methods

```zebra
# file: 08_interface_methods.zbr
# teaches: interface with multiple methods
# chapter: 08-Interfaces-and-Protocols

interface PaymentProcessor
    def process(amount: float): bool
    def refund(transaction_id: str): bool
    def get_status(transaction_id: str): str

class CreditCardProcessor
    implements PaymentProcessor
        def process(amount: float): bool
            print "Processing credit card: ${amount}"
            return true
        
        def refund(transaction_id: str): bool
            print "Refunding transaction: ${transaction_id}"
            return true
        
        def get_status(transaction_id: str): str
            return "completed"

class PayPalProcessor
    implements PaymentProcessor
        def process(amount: float): bool
            print "Processing PayPal: ${amount}"
            return true
        
        def refund(transaction_id: str): bool
            print "PayPal refund: ${transaction_id}"
            return true
        
        def get_status(transaction_id: str): str
            return "pending"
```

---

## Polymorphism in Action

### Using Different Implementations

```zebra
# file: 08_polymorphism.zbr
# teaches: polymorphic behavior
# chapter: 08-Interfaces-and-Protocols

def process_payment(processor: PaymentProcessor, amount: float)
    if processor.process(amount)
        print "Payment successful"
    else
        print "Payment failed"

def main()
    var cc_processor = CreditCardProcessor()
    var paypal_processor = PayPalProcessor()

    # Same code, different behavior
    process_payment(cc_processor, 99.99)
    process_payment(paypal_processor, 49.99)
```

### Collections of Interface Types

```zebra
# file: 08_collection_interface.zbr
# teaches: storing different implementations
# chapter: 08-Interfaces-and-Protocols

class Zoo
    var animals: List(Animal) = List(Animal)()

    def add_animal(animal: Animal)
        this.animals.add(animal)

    def make_them_speak()
        for animal in this.animals
            print animal.speak()

    def exercise_all()
        for animal in this.animals
            animal.move()

def main()
    var zoo = Zoo()
    zoo.add_animal(Dog())
    zoo.add_animal(Bird())
    zoo.add_animal(Dog())

    zoo.make_them_speak()
    zoo.exercise_all()
```

---

## Real World: Logging System

```zebra
# file: 08_logger_system.zbr
# teaches: realistic interface use
# chapter: 08-Interfaces-and-Protocols

interface Logger
    def debug(message: str)
    def info(message: str)
    def warn(message: str)
    def error(message: str)

class ConsoleLogger
    implements Logger
        def debug(message: str)
            print "[DEBUG] ${message}"
        
        def info(message: str)
            print "[INFO] ${message}"
        
        def warn(message: str)
            print "[WARN] ${message}"
        
        def error(message: str)
            print "[ERROR] ${message}"

class FileLogger
    implements Logger
        def debug(message: str)
            # Write to file: [DEBUG] message
        
        def info(message: str)
            # Write to file: [INFO] message
        
        def warn(message: str)
            # Write to file: [WARN] message
        
        def error(message: str)
            # Write to file: [ERROR] message

class Application
    var logger: Logger

    def set_logger(l: Logger)
        this.logger = l

    def do_work()
        this.logger.info("Starting work")
        # Do work
        this.logger.info("Work complete")

def main()
    var app = Application()

    # Use console logger
    app.set_logger(ConsoleLogger())
    app.do_work()

    # Switch to file logger (same code, different output)
    app.set_logger(FileLogger())
    app.do_work()
```

---

## Common Patterns

### Strategy Pattern

```zebra
interface SortStrategy
    def sort(items: List(int))

class AscendingSort
    implements SortStrategy
        def sort(items: List(int))
            # Sort ascending

class DescendingSort
    implements SortStrategy
        def sort(items: List(int))
            # Sort descending

class Sorter
    var strategy: SortStrategy

    def set_strategy(s: SortStrategy)
        this.strategy = s

    def sort(items: List(int))
        this.strategy.sort(items)
```

### Adapter Pattern

```zebra
interface NewSystem
    def process(data: str)

class OldSystem
    def old_process(input: str)
        # Old implementation
        pass

class OldSystemAdapter
    implements NewSystem
        var old_system: OldSystem = OldSystem()

        def process(data: str)
            # Adapt new interface to old system
            this.old_system.old_process(data)
```

---

## If you're new to programming

> An **interface** is like a promise or contract. When you say a class "implements" an interface, you promise that it has all the methods the interface requires.
>
> This lets you write code that works with **any** object that implements that interface, without knowing exactly which class it is.
>
> **Polymorphism** means "many forms"—the same code can work with different types of objects.

### If you know Python

```python
# Python (using duck typing)
class Dog:
    def speak(self):
        return "Woof!"

class Bird:
    def speak(self):
        return "Tweet!"

def get_sound(animal):
    return animal.speak()
```

```zebra
# Zebra (using interfaces)
interface Animal
    def speak(): str

class Dog implements Animal
    def speak(): str
        return "Woof!"

class Bird implements Animal
    def speak(): str
        return "Tweet!"

def get_sound(animal: Animal): str
    return animal.speak()
```

Python relies on duck typing ("if it quacks like a duck"). Zebra makes the contract explicit with interfaces.

---

## Common Mistakes

> ❌ **Mistake:** Not implementing all interface methods
>
> ```zebra
> interface Animal
>     def speak(): str
>     def move()
>
> class Dog
>     implements Animal
>         def speak(): str
>             return "Woof!"
>         # ❌ Missing: def move
> ```
>
> 💡 **Why:** The compiler requires all methods. You're breaking the contract.
>
> ✅ **Better:**
> ```zebra
> class Dog
>     implements Animal
>         def speak(): str
>             return "Woof!"
>         def move()
>             print "Running"
> ```

> ❌ **Mistake:** Wrong method signature
>
> ```zebra
> interface PaymentProcessor
>     def process(amount: float): bool
>
> class CreditCard
>     implements PaymentProcessor
>         def process(amount: int): bool  # ❌ int, not float
>             return true
> ```
>
> ✅ **Better:**
> ```zebra
> class CreditCard
>     implements PaymentProcessor
>         def process(amount: float): bool  # ✅ Matches interface
>             return true
> ```

> ❌ **Mistake:** Forgetting to declare implementation
>
> ```zebra
> class Dog  # ❌ Doesn't say implements Animal
>     def speak(): str
>         return "Woof!"
> ```
>
> ✅ **Better:**
> ```zebra
> class Dog
>     implements Animal  # ✅ Explicit contract
>         def speak(): str
>             return "Woof!"
> ```

---

## Exercises

### Exercise 1: Shape Interface

Create an interface for shapes and multiple implementations:

<details>
<summary>Solution</summary>

```zebra
interface Shape
    def area(): float
    def perimeter(): float

class Circle
    var radius: float = 0.0
    implements Shape
        def area(): float
            return 3.14 * this.radius * this.radius
        def perimeter(): float
            return 2.0 * 3.14 * this.radius

class Rectangle
    var width: float = 0.0
    var height: float = 0.0
    implements Shape
        def area(): float
            return this.width * this.height
        def perimeter(): float
            return 2.0 * (this.width + this.height)

def print_shape_info(shape: Shape)
    print "Area: ${shape.area()}"
    print "Perimeter: ${shape.perimeter()}"

def main()
    var circle = Circle()
    circle.radius = 5.0
    print_shape_info(circle)

    var rect = Rectangle()
    rect.width = 10.0
    rect.height = 5.0
    print_shape_info(rect)
```

</details>

### Exercise 2: Database Interface

Create a database interface with multiple implementations:

<details>
<summary>Solution</summary>

```zebra
interface Database
    def save(key: str, value: str): bool
    def load(key: str): str?
    def delete(key: str): bool

class MemoryDatabase
    var data: HashMap(str, str) = HashMap(str, str)()
    implements Database
        def save(key: str, value: str): bool
            this.data.put(key, value)
            return true
        def load(key: str): str?
            return this.data.get(key)
        def delete(key: str): bool
            this.data.remove(key)
            return true

def main()
    var db: Database = MemoryDatabase()
    db.save("user1", "Alice")
    db.save("user2", "Bob")

    if db.load("user1") as user
        print "Found: ${user}"

    db.delete("user1")
```

</details>

### Exercise 3: Document Processor

Create an interface for document processors:

<details>
<summary>Solution</summary>

```zebra
interface DocumentProcessor
    def process(content: str): str
    def validate(content: str): bool

class MarkdownProcessor
    implements DocumentProcessor
        def process(content: str): str
            # Convert markdown to HTML
            return "<html>${content}</html>"
        def validate(content: str): bool
            return content.len > 0

class JSONValidator
    implements DocumentProcessor
        def process(content: str): str
            return content  # Already valid JSON
        def validate(content: str): bool
            return content.contains("{") and content.contains("}")

def process_document(processor: DocumentProcessor, doc: str)
    if processor.validate(doc)
        var processed = processor.process(doc)
        print "Processed: ${processed}"
    else
        print "Invalid document"

def main()
    var md = MarkdownProcessor()
    process_document(md, "# Hello")

    var json = JSONValidator()
    process_document(json, "{}")
```

</details>

---

## Next Steps

- → **09-Composition-and-Mixins** — Sharing behaviour without inheritance
- → **14-Contracts** — More complex interfaces
- 🏋 **Project-2-HTTP-Server** — Interfaces for handlers and middleware

---

## Key Takeaways

- **Interfaces define contracts** — What methods must exist, not how they work
- **Polymorphism** lets you write code once, work with many types
- **Swap implementations** without changing callers
- **Testing is easier** — Mock implementations implement the interface
- **Makes code flexible** — Add new implementations without modifying existing code
- **Forces clear design** — Interfaces make relationships explicit

---

**Next:** Head to **09-Composition-and-Mixins** for code reuse without classical inheritance.

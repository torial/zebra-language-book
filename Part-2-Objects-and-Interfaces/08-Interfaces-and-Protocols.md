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
// file: 08_interface_basic.zbr
// teaches: interface definition
// chapter: 08-Interfaces-and-Protocols

interface Animal
    def speak as str
    def move

class Dog
    implements Animal
        def speak as str
            return "Woof!"
        
        def move
            print "Running on four legs"

class Bird
    implements Animal
        def speak as str
            return "Tweet!"
        
        def move
            print "Flying through the air"

class Main
    shared
        def main
            var dog as Animal = Dog()
            print dog.speak()      // Woof!
            dog.move()             // Running on four legs
            
            var bird as Animal = Bird()
            print bird.speak()     // Tweet!
            bird.move()            // Flying through the air
```

**Key points:**
- `interface Animal` — Define what any animal must do
- `implements Animal` — Promise to implement all methods
- Treat objects as their interface type (`var dog as Animal`)

### Multiple Methods

```zebra
// file: 08_interface_methods.zbr
// teaches: interface with multiple methods
// chapter: 08-Interfaces-and-Protocols

interface PaymentProcessor
    def process(amount as float) as bool
    def refund(transaction_id as str) as bool
    def get_status(transaction_id as str) as str

class CreditCardProcessor
    implements PaymentProcessor
        def process(amount as float) as bool
            print "Processing credit card: ${amount}"
            return true
        
        def refund(transaction_id as str) as bool
            print "Refunding transaction: ${transaction_id}"
            return true
        
        def get_status(transaction_id as str) as str
            return "completed"

class PayPalProcessor
    implements PaymentProcessor
        def process(amount as float) as bool
            print "Processing PayPal: ${amount}"
            return true
        
        def refund(transaction_id as str) as bool
            print "PayPal refund: ${transaction_id}"
            return true
        
        def get_status(transaction_id as str) as str
            return "pending"
```

---

## Polymorphism in Action

### Using Different Implementations

```zebra
// file: 08_polymorphism.zbr
// teaches: polymorphic behavior
// chapter: 08-Interfaces-and-Protocols

class Store
    shared
        def process_payment(processor as PaymentProcessor, amount as float)
            if processor.process(amount)
                print "Payment successful"
            else
                print "Payment failed"

class Main
    shared
        def main
            var cc_processor = CreditCardProcessor()
            var paypal_processor = PayPalProcessor()
            
            // Same code, different behavior
            Store.process_payment(cc_processor, 99.99)
            Store.process_payment(paypal_processor, 49.99)
```

### Collections of Interface Types

```zebra
// file: 08_collection_interface.zbr
// teaches: storing different implementations
// chapter: 08-Interfaces-and-Protocols

class Zoo
    var animals as List(Animal) = List()
    
    def add_animal(animal as Animal)
        animals.add(animal)
    
    def make_them_speak
        for animal in animals
            print animal.speak()
    
    def exercise_all
        for animal in animals
            animal.move()

class Main
    shared
        def main
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
// file: 08_logger_system.zbr
// teaches: realistic interface use
// chapter: 08-Interfaces-and-Protocols

interface Logger
    def debug(message as str)
    def info(message as str)
    def warn(message as str)
    def error(message as str)

class ConsoleLogger
    implements Logger
        def debug(message as str)
            print "[DEBUG] ${message}"
        
        def info(message as str)
            print "[INFO] ${message}"
        
        def warn(message as str)
            print "[WARN] ${message}"
        
        def error(message as str)
            print "[ERROR] ${message}"

class FileLogger
    implements Logger
        def debug(message as str)
            # Write to file: [DEBUG] message
        
        def info(message as str)
            # Write to file: [INFO] message
        
        def warn(message as str)
            # Write to file: [WARN] message
        
        def error(message as str)
            # Write to file: [ERROR] message

class Application
    var logger as Logger
    
    def set_logger(l as Logger)
        logger = l
    
    def do_work
        logger.info("Starting work")
        # Do work
        logger.info("Work complete")

class Main
    shared
        def main
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
    def sort(items as List(int))

class AscendingSort
    implements SortStrategy
        def sort(items as List(int))
            # Sort ascending

class DescendingSort
    implements SortStrategy
        def sort(items as List(int))
            # Sort descending

class Sorter
    var strategy as SortStrategy
    
    def set_strategy(s as SortStrategy)
        strategy = s
    
    def sort(items as List(int))
        strategy.sort(items)
```

### Adapter Pattern

```zebra
interface NewSystem
    def process(data as str)

class OldSystem
    def old_process(input as str)
        # Old implementation

class OldSystemAdapter
    implements NewSystem
        var old_system as OldSystem = OldSystem()
        
        def process(data as str)
            // Adapt new interface to old system
            old_system.old_process(data)
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

# Zebra (using interfaces)
interface Animal
    def speak as str

class Dog
    implements Animal
        def speak as str
            return "Woof!"

class Bird
    implements Animal
        def speak as str
            return "Tweet!"

class Main
    shared
        def get_sound(animal as Animal) as str
            return animal.speak()
```

Python relies on duck typing ("if it quacks like a duck"). Zebra makes the contract explicit with interfaces.

---

## Common Mistakes

> ❌ **Mistake:** Not implementing all interface methods
>
> ```zebra
> interface Animal
>     def speak as str
>     def move
>
> class Dog
>     implements Animal
>         def speak as str
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
>         def speak as str
>             return "Woof!"
>         def move
>             print "Running"
> ```

> ❌ **Mistake:** Wrong method signature
>
> ```zebra
> interface PaymentProcessor
>     def process(amount as float) as bool
>
> class CreditCard
>     implements PaymentProcessor
>         def process(amount as int) as bool  # ❌ int, not float
>             return true
> ```
>
> ✅ **Better:**
> ```zebra
> class CreditCard
>     implements PaymentProcessor
>         def process(amount as float) as bool  # ✅ Matches interface
>             return true
> ```

> ❌ **Mistake:** Forgetting to declare implementation
>
> ```zebra
> class Dog  # ❌ Doesn't say implements Animal
>     def speak as str
>         return "Woof!"
> ```
>
> ✅ **Better:**
> ```zebra
> class Dog
>     implements Animal  # ✅ Explicit contract
>         def speak as str
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
    def area as float
    def perimeter as float

class Circle
    var radius as float = 0.0
    implements Shape
        def area as float
            return 3.14 * radius * radius
        def perimeter as float
            return 2.0 * 3.14 * radius

class Rectangle
    var width as float = 0.0
    var height as float = 0.0
    implements Shape
        def area as float
            return width * height
        def perimeter as float
            return 2.0 * (width + height)

class Main
    shared
        def print_shape_info(shape as Shape)
            print "Area: ${shape.area()}"
            print "Perimeter: ${shape.perimeter()}"
        
        def main
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
    def save(key as str, value as str) as bool
    def load(key as str) as str?
    def delete(key as str) as bool

class MemoryDatabase
    var data as HashMap(str, str) = HashMap()
    implements Database
        def save(key as str, value as str) as bool
            data.put(key, value)
            return true
        def load(key as str) as str?
            if data.contains(key)
                return data.fetch(key)
            return nil
        def delete(key as str) as bool
            data.remove(key)
            return true

class Main
    shared
        def main
            var db as Database = MemoryDatabase()
            db.save("user1", "Alice")
            db.save("user2", "Bob")
            
            var user = db.load("user1")
            if user != nil
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
    def process(content as str) as str
    def validate(content as str) as bool

class MarkdownProcessor
    implements DocumentProcessor
        def process(content as str) as str
            # Convert markdown to HTML
            return "<html>${content}</html>"
        def validate(content as str) as bool
            return content.len > 0

class JSONValidator
    implements DocumentProcessor
        def process(content as str) as str
            return content  # Already valid JSON
        def validate(content as str) as bool
            return content.contains("{") and content.contains("}")

class Main
    shared
        def process_document(processor as DocumentProcessor, doc as str)
            if processor.validate(doc)
                var result = processor.process(doc)
                print "Processed: ${result}"
            else
                print "Invalid document"
        
        def main
            var md = MarkdownProcessor()
            process_document(md, "# Hello")
            
            var json = JSONValidator()
            process_document(json, "{}")
```

</details>

---

## Next Steps

- → **09-Inheritance** — Extending classes
- → **14-Contracts** — More complex interfaces
- 🏋️ **Project-2-HTTP-Server** — Interfaces for handlers and middleware

---

## Key Takeaways

- **Interfaces define contracts** — What methods must exist, not how they work
- **Polymorphism** lets you write code once, work with many types
- **Swap implementations** without changing callers
- **Testing is easier** — Mock implementations implement the interface
- **Makes code flexible** — Add new implementations without modifying existing code
- **Forces clear design** — Interfaces make relationships explicit

---

**Next:** Head to **09-Inheritance** to extend classes and share code across hierarchies.

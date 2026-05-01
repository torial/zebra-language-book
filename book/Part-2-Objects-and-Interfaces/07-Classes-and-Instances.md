# 07: Classes and Instances

**Audience:** All (with beginner sidebar)  
**Time:** 120 minutes  
**Prerequisites:** 01-06  
**You'll learn:** Define classes, instantiate objects, instance methods, fields, initialization

---

## The Big Picture

**Classes** are blueprints for objects. Instead of a loose collection of variables, a class groups related data and behavior together.

```
Real world: A car has properties (color, speed) and behaviors (accelerate, brake)
Code: A Car class has fields (color, speed) and methods (accelerate, brake)
```

---

## Defining Classes

![Class Structure](diagrams/12-class-structure.png)

### Simple Class

```zebra
# file: 07_class_basic.zbr
# teaches: class definition, cue init
# chapter: 07-Classes-and-Instances

class Person
    var name: str
    var age: int

    cue init(name: str, age: int)
        this.name = name
        this.age = age

    def greet()
        print "Hi, I'm ${this.name}"

def main()
    var person = Person("Alice", 30)
    person.greet()  # Hi, I'm Alice
```

**Breakdown:**
- `class Person` — Define a class named Person.
- `var name: str` — Field (property) of the class.
- `cue init(name, age)` — Constructor. `this.name = name` initialises the field from the argument of the same name (using `this.` to disambiguate).
- `def greet()` — Method of the class.
- `Person("Alice", 30)` — Create an instance, passing constructor args.

> The class fields don't need defaults when `cue init` always sets them. The "field default" form (`var name: str = ""`) shines when you want to allow construction without specifying every field — see "Fields and Initialization" below.

### Fields and Initialization

```zebra
# file: 07_init.zbr
# teaches: field defaults vs. explicit init
# chapter: 07-Classes-and-Instances

class Rectangle
    var width: int = 0      # Defaults — class is constructible with `Rectangle()`
    var height: int = 0

    def area(): int
        return this.width * this.height

def main()
    var rect = Rectangle()
    rect.width = 10
    rect.height = 5
    print rect.area()  # 50
```

> Field defaults make a class **bare-constructible** (`Rectangle()` works) and let callers fill in only the fields they care about. Adding `cue init(width: int, height: int)` would make construction strict and let you drop the defaults — both styles compose.

### Instance Methods

```zebra
# file: 07_methods.zbr
# teaches: instance methods
# chapter: 07-Classes-and-Instances

class Counter
    var count: int = 0

    def increment()
        this.count = this.count + 1

    def decrement()
        this.count = this.count - 1

    def reset()
        this.count = 0

    def get_count(): int
        return this.count

def main()
    var counter = Counter()
    counter.increment()
    counter.increment()
    counter.increment()
    print counter.get_count()  # 3
    counter.reset()
    print counter.get_count()  # 0
```

### Static Methods (Class Methods)

```zebra
# file: 07_static.zbr
# teaches: static (class-level) methods
# chapter: 07-Classes-and-Instances

class MathUtil
    static
        def abs(x: int): int
            if x < 0
                return 0 - x
            return x

        def max_of(a: int, b: int): int
            if a > b
                return a
            return b

def main()
    print MathUtil.abs(-5)      # 5
    print MathUtil.max_of(10, 20)  # 20
```

> When the methods are pure and don't share state, you have a choice: group them on a class for namespacing (as above) or write them as plain top-level `def`s in a module. Pick the form that reads better at the call site. Top-level `def` keeps the call as `abs(-5)`; the class form makes `MathUtil.abs(-5)` self-documenting at a distance.

### If you're new to programming

> A **class** is like a template. When you create an instance (with `Person()`), you're making a specific copy from that template.
>
> **Fields** are the properties (like `name`, `age`)
>
> **Methods** are the behaviors (like `greet()`)
>
> **Instance methods** work on a specific object (`person.greet()`)
>
> **Static methods** belong to the class itself (`MathUtil.abs()`)

---

## Real World: User Management

```zebra
# file: 07_user_system.zbr
# teaches: realistic class design
# chapter: 07-Classes-and-Instances

class User
    var username: str = ""
    var email: str = ""
    var created_at: str = ""
    var is_active: bool = true

    def is_valid(): bool
        return this.username.len > 0 and this.email.contains("@")

    def deactivate()
        this.is_active = false

    def display_profile()
        print "User: ${this.username}"
        print "Email: ${this.email}"
        print "Active: ${this.is_active}"

class UserManager
    static
        var users: List(User) = List(User)()

        def add_user(user: User): bool
            if not user.is_valid()
                return false
            UserManager.users.add(user)
            return true

        def find_user(username: str): User?
            for user in UserManager.users
                if user.username == username
                    return user
            return nil

        def user_count(): int
            return UserManager.users.count()

def main()
    var user1 = User()
    user1.username = "alice"
    user1.email = "alice@example.com"

    if UserManager.add_user(user1)
        print "User added"

    if UserManager.find_user("alice") as found
        found.display_profile()
```

---

## Common Patterns

### Value Object

```zebra
class Point
    var x: int = 0
    var y: int = 0

    def distance_from_origin(): float
        return 0.0  # sqrt(x*x + y*y) once you have a sqrt to call
```

### Service Class

```zebra
class EmailService
    static
        def send(to: str, subject: str, body: str): bool
            # Implementation
            return true
```

### Builder Pattern

```zebra
class UserBuilder
    var username: str = ""
    var email: str = ""
    var age: int = 0

    def with_username(name: str)
        this.username = name

    def with_email(addr: str)
        this.email = addr

    def build(): User
        var user = User()
        user.username = this.username
        user.email = this.email
        return user
```

---

## Common Mistakes

> ❌ **Mistake:** Forgetting to initialize fields
>
> ```zebra
> class Person
>     var name: str  # No default value
> var p = Person()
> print p.name  # ❌ Uninitialized!
> ```
>
> ✅ **Better:**
> ```zebra
> class Person
>     var name: str = ""  # Has default
> ```

> ❌ **Mistake:** Modifying shared fields unintentionally
>
> ```zebra
> class Counter
>     static var count: int = 0
>     
>     def reset
>         count = 0  # Affects ALL instances!
> ```
>
> ✅ **Better:**
> ```zebra
> class Counter
>     var count: int = 0  # Instance field
>     
>     def reset
>         count = 0  # Only this instance
> ```

---

## Exercises

### Exercise 1: Bank Account

Create a BankAccount class with deposit and withdraw methods:

<details>
<summary>Solution</summary>

```zebra
class BankAccount
    var balance: float = 0.0
    var account_number: str = ""

    def deposit(amount: float)
        this.balance = this.balance + amount

    def withdraw(amount: float): bool
        if amount > this.balance
            return false
        this.balance = this.balance - amount
        return true

    def get_balance(): float
        return this.balance

def main()
    var account = BankAccount()
    account.account_number = "1234567890"
    account.deposit(1000.0)
    print "Balance: ${account.get_balance()}"
    account.withdraw(100.0)
    print "Balance: ${account.get_balance()}"
```

</details>

### Exercise 2: Product Catalog

Create a Product class and a simple store:

<details>
<summary>Solution</summary>

```zebra
class Product
    var name: str = ""
    var price: float = 0.0
    var quantity: int = 0

    def total_value(): float
        return this.price * @as(f64, @floatFromInt(this.quantity))

class Store
    var products: List(Product) = List(Product)()

    def add_product(product: Product)
        this.products.add(product)

    def total_inventory_value(): float
        var total = 0.0
        for product in this.products
            total = total + product.total_value()
        return total

def main()
    var store = Store()

    var apple = Product()
    apple.name = "Apple"
    apple.price = 0.50
    apple.quantity = 100
    store.add_product(apple)

    var orange = Product()
    orange.name = "Orange"
    orange.price = 0.75
    orange.quantity = 80
    store.add_product(orange)

    print "Total value: ${store.total_inventory_value()}"
```

> The `@as(f64, @floatFromInt(this.quantity))` is a temporary float-from-int cast — Zebra's `int * float` doesn't auto-promote (mixed-type arithmetic is rejected, by design). Once a typed `float(int)` builtin lands, that escape hatch becomes a clean conversion.

</details>

---

## Next Steps

- → **08-Interfaces** — Contracts for classes
- → **09-Inheritance** — Class hierarchies
- 🏋 **Project-2-HTTP-Server** — Use classes extensively

---

## Key Takeaways

- **Classes group data and behavior** — Fields + methods
- **Instances are copies** — Each `Person()` is independent
- **Instance methods** work on specific objects
- **Shared methods** belong to the class, not instances
- **Initialize fields** — Don't leave them undefined
- **Methods should have clear names** — `deposit()` not `d()`

---

**Next:** Head to **08-Interfaces** to define contracts between classes.

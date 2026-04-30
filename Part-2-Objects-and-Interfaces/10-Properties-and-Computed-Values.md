# 10: Properties and Computed Values

**Audience:** All  
**Time:** 90 minutes  
**Prerequisites:** 07-Classes  
**You'll learn:** Getters, setters, computed properties, lazy initialization, encapsulation

---

## The Big Picture

**Properties** let you control how fields are accessed and modified. Instead of letting code directly access `person.age`, you can:
- **Validate** on assignment (no negative ages)
- **Calculate** on access (compute age from birth year)
- **Cache** computed values
- **Log** access for debugging

---

## Getters

### Simple Getter

```zebra
# file: 10_getter.zbr
# teaches: computed properties
# chapter: 10-Properties-and-Computed-Values

class Person
    var birth_year: int = 2000
    
    def age: int
        return 2024 - birth_year
    
    def name_length: int
        var name = "Alice"
        return name.len

def main()
    var person = Person()
    person.birth_year = 1990
    print person.age()         # 34
    print person.name_length() # 5
```

### Derived Properties

```zebra
# file: 10_derived.zbr
# teaches: deriving values from fields
# chapter: 10-Properties-and-Computed-Values

class Rectangle
    var width: int = 0
    var height: int = 0
    
    def area: int
        return width * height
    
    def perimeter: int
        return 2 * (width + height)
    
    def is_square: bool
        return width == height

def main()
    var rect = Rectangle()
    rect.width = 10
    rect.height = 10

    print "Area: ${rect.area()}"           # 100
    print "Perimeter: ${rect.perimeter()}" # 40
    print "Square: ${rect.is_square()}"    # true
```

---

## Setters (Validation)

### Controlling Field Assignment

```zebra
# file: 10_setter_validation.zbr
# teaches: setters with validation
# chapter: 10-Properties-and-Computed-Values

class Account
    var balance: float = 0.0
    
    def deposit(amount: float): bool
        if amount <= 0.0
            return false
        balance = balance + amount
        return true
    
    def withdraw(amount: float): bool
        if amount <= 0.0
            return false
        if amount > balance
            return false
        balance = balance - amount
        return true
    
    def get_balance: float
        return balance

def main()
    var account = Account()
    account.deposit(100.0)
    print account.get_balance()    # 100

    account.withdraw(25.0)
    print account.get_balance()    # 75

    account.withdraw(100.0)  # Fails (not enough balance)
    print account.get_balance()    # 75 (unchanged)
```

### Setter with Side Effects

```zebra
# file: 10_setter_effects.zbr
# teaches: setters with side effects
# chapter: 10-Properties-and-Computed-Values

class User
    var username: str = ""
    var email: str = ""
    var last_modified: str = ""
    
    def set_username(new_name: str): bool
        if new_name.len < 3
            return false
        username = new_name
        last_modified = "2024-01-01"  # Update timestamp
        return true
    
    def set_email(new_email: str): bool
        if not new_email.contains("@")
            return false
        email = new_email
        last_modified = "2024-01-01"  # Update timestamp
        return true

def main()
    var user = User()
    if user.set_username("alice")
        print "Username set"

    if user.set_email("alice@example.com")
        print "Email set"
        print "Last modified: ${user.last_modified}"
```

---

## Computed Properties

```zebra
# file: 10_computed.zbr
# teaches: expensive computed properties
# chapter: 10-Properties-and-Computed-Values

class DataSet
    var numbers: List(int) = List()
    
    def sum: int
        var total = 0
        for num in numbers
            total = total + num
        return total
    
    def average: float
        if numbers.count() == 0
            return 0.0
        return sum / numbers.count()
    
    def min_value: int
        var min = numbers.at(0)
        for num in numbers
            if num < min
                min = num
        return min
    
    def max_value: int
        var max = numbers.at(0)
        for num in numbers
            if num > max
                max = num
        return max

def main()
    var data = DataSet()
    data.numbers.add(10)
    data.numbers.add(20)
    data.numbers.add(30)
    data.numbers.add(40)

    print "Sum: ${data.sum()}"           # 100
    print "Average: ${data.average()}"   # 25
    print "Min: ${data.min_value()}"     # 10
    print "Max: ${data.max_value()}"     # 40
```

---

## Lazy Initialization

```zebra
# file: 10_lazy_init.zbr
# teaches: lazy initialization
# chapter: 10-Properties-and-Computed-Values

class Database
    var connection: str?   = nil
    var is_connected: bool = false
    
    def get_connection: str
        if connection == nil
            # Expensive operation: only when needed
            connection = "Connected to DB"
            is_connected = true
        return connection

def main()
    var db = Database()

    # Connection not created yet
    print "Is connected: ${db.is_connected}"  # false

    # Access connection (now it's created)
    if db.get_connection() as conn
        print conn                            # Connected to DB

    # Already exists
    if db.get_connection() as conn2
        print conn2                           # Connected to DB
```

---

## Real World: Temperature Converter

```zebra
# file: 10_temperature.zbr
# teaches: properties in realistic scenarios
# chapter: 10-Properties-and-Computed-Values

class Temperature
    var celsius: float = 0.0
    
    def fahrenheit: float
        return celsius * 9.0 / 5.0 + 32.0
    
    def kelvin: float
        return celsius + 273.15
    
    def set_from_fahrenheit(f: float)
        celsius = (f - 32.0) * 5.0 / 9.0
    
    def set_from_kelvin(k: float)
        celsius = k - 273.15
    
    def is_freezing: bool
        return celsius <= 0.0
    
    def is_boiling: bool
        return celsius >= 100.0

def main()
    var temp = Temperature()
    temp.celsius = 25.0

    print "Celsius: ${temp.celsius}"
    print "Fahrenheit: ${temp.fahrenheit()}"
    print "Kelvin: ${temp.kelvin()}"
    print "Freezing: ${temp.is_freezing()}"
    print "Boiling: ${temp.is_boiling()}"

    temp.set_from_fahrenheit(98.6)
    print "Body temp in Celsius: ${temp.celsius}"
```

---

## Real World: Configuration

```zebra
# file: 10_config.zbr
# teaches: configuration management
# chapter: 10-Properties-and-Computed-Values

class Config
    var host: str = "localhost"
    var port: int = 8080
    var debug: bool = false
    
    def set_host(h: str): bool
        if h.len == 0
            return false
        host = h
        return true
    
    def set_port(p: int): bool
        if p < 1 or p > 65535
            return false
        port = p
        return true
    
    def get_url: str
        return "http://${host}:${port}"
    
    def set_debug(d: bool)
        debug = d

def main()
    var config = Config()
    config.set_host("example.com")
    config.set_port(443)
    config.set_debug(true)

    print config.get_url()           # http://example.com:443
    print "Debug: ${config.debug}"   # true
```

---

## Common Patterns

### Read-Only Properties

```zebra
class BankAccount
    var balance: float = 0.0
    
    def get_balance: float
        return balance  # Can read
    
    def deposit(amount: float)
        balance = balance + amount  # Can modify only via methods
    
    # No setter: direct assignment not allowed
```

### Write-Only Properties

```zebra
class Password
    var encrypted_password: str = ""
    
    def set_password(plain: str)
        # Encrypt and store
        encrypted_password = "encrypted:" + plain
    
    # No getter: can't read it back
```

---

## If you're new to programming

> A **getter** is a method that retrieves a value (often computing it on the fly).
>
> A **setter** is a method that stores a value (often with validation).
>
> **Computed properties** are values you calculate rather than store. Like `age` = current_year - birth_year.
>
> **Lazy initialization** means "don't create something expensive until someone actually asks for it."

---

## Common Mistakes

> ❌ **Mistake:** Exposing internal fields directly
>
> ```zebra
> class User
>     var age: int = 0
> var user = User()
> user.age = -5  # ❌ No validation!
> ```
>
> ✅ **Better:**
> ```zebra
> class User
>     var age: int = 0
>     def set_age(new_age: int): bool
>         if new_age < 0
>             return false
>         age = new_age
>         return true
> ```

> ❌ **Mistake:** Computing expensive properties every time
>
> ```zebra
> class DataSet
>     var numbers: List(int) = List()
>     
>     def sum: int  # Recalculates every call
>         var total = 0
>         for num in numbers
>             total = total + num
>         return total  # O(n) every time!
> ```
>
> ✅ **Better (if called often):**
> ```zebra
> class DataSet
>     var numbers: List(int) = List()
>     var cached_sum: int? = nil
>     
>     def sum: int
>         if cached_sum == nil
>             var total = 0
>             for num in numbers
>                 total = total + num
>             cached_sum = total
>         return cached_sum
>     
>     def add_number(num: int)
>         numbers.add(num)
>         cached_sum = nil  # Invalidate cache
> ```

> ❌ **Mistake:** Side effects in getters
>
> ```zebra
> class Logger
>     var count: int = 0
>     
>     def get_count: int
>         count = count + 1  # ❌ Has side effect!
>         return count
> ```
>
> ✅ **Better:**
> ```zebra
> class Logger
>     var count: int = 0
>     
>     def get_count: int
>         return count  # ✅ Pure getter, no side effects
>     
>     def log_access
>         count = count + 1  # Explicit method for side effects
> ```

---

## Exercises

### Exercise 1: Bank Account Properties

Create a bank account with validated setters:

<details>
<summary>Solution</summary>

```zebra
class BankAccount
    var owner: str = ""
    var balance: float = 0.0
    var interest_rate: float = 0.02
    
    def set_owner(name: str): bool
        if name.len < 2
            return false
        owner = name
        return true
    
    def deposit(amount: float): bool
        if amount <= 0.0
            return false
        balance = balance + amount
        return true
    
    def withdraw(amount: float): bool
        if amount > balance
            return false
        balance = balance - amount
        return true
    
    def apply_interest
        var interest = balance * interest_rate
        balance = balance + interest
    
    def get_balance: float
        return balance

def main()
    var account = BankAccount()
    account.set_owner("Alice")
    account.deposit(1000.0)
    account.apply_interest()
    print "Balance: ${account.get_balance()}"
```

</details>

### Exercise 2: Circle Properties

Create a circle class with radius and diameter properties:

<details>
<summary>Solution</summary>

```zebra
class Circle
    var radius: float = 0.0
    
    def set_radius(r: float): bool
        if r <= 0.0
            return false
        radius = r
        return true
    
    def diameter: float
        return radius * 2.0
    
    def set_diameter(d: float): bool
        if d <= 0.0
            return false
        radius = d / 2.0
        return true
    
    def area: float
        return 3.14159 * radius * radius
    
    def circumference: float
        return 2.0 * 3.14159 * radius

def main()
    var circle = Circle()
    circle.set_radius(5.0)

    print "Radius: ${circle.radius}"
    print "Diameter: ${circle.diameter()}"
    print "Area: ${circle.area()}"
    print "Circumference: ${circle.circumference()}"

    circle.set_diameter(20.0)
    print "New radius: ${circle.radius}"
```

</details>

### Exercise 3: User Profile with Validation

Create a user profile with validated properties:

<details>
<summary>Solution</summary>

```zebra
class UserProfile
    var username: str = ""
    var email: str = ""
    var age: int = 0
    
    def set_username(name: str): bool
        if name.len < 3 or name.len > 20
            return false
        username = name
        return true
    
    def set_email(addr: str): bool
        if not addr.contains("@") or not addr.contains(".")
            return false
        email = addr
        return true
    
    def set_age(a: int): bool
        if a < 13 or a > 120
            return false
        age = a
        return true
    
    def is_adult: bool
        return age >= 18
    
    def is_valid: bool
        return username.len > 0 and email.contains("@") and age > 0

def main()
    var user = UserProfile()
    if user.set_username("alice_wonder")
        print "Username set"
    if user.set_email("alice@example.com")
        print "Email set"
    if user.set_age(25)
        print "Age set"

    print "Is adult: ${user.is_adult()}"
    print "Is valid: ${user.is_valid()}"
```

</details>

---

## Next Steps

- → **11-Nil-Tracking** — Advanced safety with properties
- → **14-Contracts** — Enforce property invariants
- 🏋️ **Project-1-CLI-Tool** — Use configuration properties

---

## Key Takeaways

- **Getters compute** values from fields
- **Setters validate** before storing
- **Computed properties** derive from other data
- **Lazy initialization** defers expensive work
- **Control access** to prevent invalid states
- **Encapsulation** protects class invariants

---

**Next:** Head to **Part 3** and **11-Nil-Tracking** for Zebra's safety features.

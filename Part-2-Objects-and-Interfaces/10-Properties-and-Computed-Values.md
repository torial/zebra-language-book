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
    var birth_year as int = 2000
    
    def age as int
        return 2024 - birth_year
    
    def name_length as int
        var name = "Alice"
        return name.len

class Main
    shared
        def main
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
    var width as int = 0
    var height as int = 0
    
    def area as int
        return width * height
    
    def perimeter as int
        return 2 * (width + height)
    
    def is_square as bool
        return width == height

class Main
    shared
        def main
            var rect = Rectangle()
            rect.width = 10
            rect.height = 10
            
            print "Area: ${rect.area()}"         # 100
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
    var balance as float = 0.0
    
    def deposit(amount as float) as bool
        if amount <= 0.0
            return false
        balance = balance + amount
        return true
    
    def withdraw(amount as float) as bool
        if amount <= 0.0
            return false
        if amount > balance
            return false
        balance = balance - amount
        return true
    
    def get_balance as float
        return balance

class Main
    shared
        def main
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
    var username as str = ""
    var email as str = ""
    var last_modified as str = ""
    
    def set_username(new_name as str) as bool
        if new_name.len < 3
            return false
        username = new_name
        last_modified = "2024-01-01"  # Update timestamp
        return true
    
    def set_email(new_email as str) as bool
        if not new_email.contains("@")
            return false
        email = new_email
        last_modified = "2024-01-01"  # Update timestamp
        return true

class Main
    shared
        def main
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
    var numbers as List(int) = List()
    
    def sum as int
        var total = 0
        for num in numbers
            total = total + num
        return total
    
    def average as float
        if numbers.count() == 0
            return 0.0
        return sum / numbers.count()
    
    def min_value as int
        var min = numbers.at(0)
        for num in numbers
            if num < min
                min = num
        return min
    
    def max_value as int
        var max = numbers.at(0)
        for num in numbers
            if num > max
                max = num
        return max

class Main
    shared
        def main
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
    var connection as str?   = nil
    var is_connected as bool = false
    
    def get_connection as str
        if connection == nil
            # Expensive operation: only when needed
            connection = "Connected to DB"
            is_connected = true
        return connection

class Main
    shared
        def main
            var db = Database()
            
            # Connection not created yet
            print "Is connected: ${db.is_connected()}"  # false
            
            # Access connection (now it's created)
            var conn = db.get_connection()
            print conn                                  # Connected to DB
            
            # Already exists
            var conn2 = db.get_connection()
            print conn2                                 # Connected to DB
```

---

## Real World: Temperature Converter

```zebra
# file: 10_temperature.zbr
# teaches: properties in realistic scenarios
# chapter: 10-Properties-and-Computed-Values

class Temperature
    var celsius as float = 0.0
    
    def fahrenheit as float
        return celsius * 9.0 / 5.0 + 32.0
    
    def kelvin as float
        return celsius + 273.15
    
    def set_from_fahrenheit(f as float)
        celsius = (f - 32.0) * 5.0 / 9.0
    
    def set_from_kelvin(k as float)
        celsius = k - 273.15
    
    def is_freezing as bool
        return celsius <= 0.0
    
    def is_boiling as bool
        return celsius >= 100.0

class Main
    shared
        def main
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
    var host as str = "localhost"
    var port as int = 8080
    var debug as bool = false
    
    def set_host(h as str) as bool
        if h.len == 0
            return false
        host = h
        return true
    
    def set_port(p as int) as bool
        if p < 1 or p > 65535
            return false
        port = p
        return true
    
    def get_url as str
        return "http://${host}:${port}"
    
    def set_debug(d as bool)
        debug = d

class Main
    shared
        def main
            var config = Config()
            config.set_host("example.com")
            config.set_port(443)
            config.set_debug(true)
            
            print config.get_url()     // http://example.com:443
            print "Debug: ${config.debug}"  # true
```

---

## Common Patterns

### Read-Only Properties

```zebra
class BankAccount
    var balance as float = 0.0
    
    def get_balance as float
        return balance  # Can read
    
    def deposit(amount as float)
        balance = balance + amount  # Can modify only via methods
    
    # No setter: direct assignment not allowed
```

### Write-Only Properties

```zebra
class Password
    var encrypted_password as str = ""
    
    def set_password(plain as str)
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
>     var age as int = 0
> var user = User()
> user.age = -5  # ❌ No validation!
> ```
>
> ✅ **Better:**
> ```zebra
> class User
>     var age as int = 0
>     def set_age(new_age as int) as bool
>         if new_age < 0
>             return false
>         age = new_age
>         return true
> ```

> ❌ **Mistake:** Computing expensive properties every time
>
> ```zebra
> class DataSet
>     var numbers as List(int) = List()
>     
>     def sum as int  # Recalculates every call
>         var total = 0
>         for num in numbers
>             total = total + num
>         return total  # O(n) every time!
> ```
>
> ✅ **Better (if called often):**
> ```zebra
> class DataSet
>     var numbers as List(int) = List()
>     var cached_sum as int? = nil
>     
>     def sum as int
>         if cached_sum == nil
>             var total = 0
>             for num in numbers
>                 total = total + num
>             cached_sum = total
>         return cached_sum
>     
>     def add_number(num as int)
>         numbers.add(num)
>         cached_sum = nil  # Invalidate cache
> ```

> ❌ **Mistake:** Side effects in getters
>
> ```zebra
> class Logger
>     var count as int = 0
>     
>     def get_count as int
>         count = count + 1  # ❌ Has side effect!
>         return count
> ```
>
> ✅ **Better:**
> ```zebra
> class Logger
>     var count as int = 0
>     
>     def get_count as int
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
    var owner as str = ""
    var balance as float = 0.0
    var interest_rate as float = 0.02
    
    def set_owner(name as str) as bool
        if name.len < 2
            return false
        owner = name
        return true
    
    def deposit(amount as float) as bool
        if amount <= 0.0
            return false
        balance = balance + amount
        return true
    
    def withdraw(amount as float) as bool
        if amount > balance
            return false
        balance = balance - amount
        return true
    
    def apply_interest
        var interest = balance * interest_rate
        balance = balance + interest
    
    def get_balance as float
        return balance

class Main
    shared
        def main
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
    var radius as float = 0.0
    
    def set_radius(r as float) as bool
        if r <= 0.0
            return false
        radius = r
        return true
    
    def diameter as float
        return radius * 2.0
    
    def set_diameter(d as float) as bool
        if d <= 0.0
            return false
        radius = d / 2.0
        return true
    
    def area as float
        return 3.14159 * radius * radius
    
    def circumference as float
        return 2.0 * 3.14159 * radius

class Main
    shared
        def main
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
    var username as str = ""
    var email as str = ""
    var age as int = 0
    
    def set_username(name as str) as bool
        if name.len < 3 or name.len > 20
            return false
        username = name
        return true
    
    def set_email(addr as str) as bool
        if not addr.contains("@") or not addr.contains(".")
            return false
        email = addr
        return true
    
    def set_age(a as int) as bool
        if a < 13 or a > 120
            return false
        age = a
        return true
    
    def is_adult as bool
        return age >= 18
    
    def is_valid as bool
        return username.len > 0 and email.contains("@") and age > 0

class Main
    shared
        def main
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

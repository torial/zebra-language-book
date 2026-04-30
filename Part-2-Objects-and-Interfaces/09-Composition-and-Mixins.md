# 09: Composition and Mixins

**Audience:** All
**Time:** 90 minutes
**Prerequisites:** 07-Classes, 08-Interfaces
**You'll learn:** Why Zebra rejects class inheritance, how to share behaviour with **mixins**, and how to combine smaller classes via **composition**

---

## Why no inheritance?

Zebra deliberately omits class inheritance. There is no `extends`, no `super`,
no parent class.

Decades of inheritance experience surfaced known problems: the fragile
base-class problem (a change in the parent silently breaks subclasses), diamond
inheritance ambiguity, surprising method-resolution order, and tight coupling
between base and derived classes. Languages like Go and Rust have shown that
large systems can be built without ever needing inheritance.

Zebra leans on **three reuse primitives**, each with a clear role:

| Primitive    | Purpose                                            | Keyword                       |
|--------------|----------------------------------------------------|-------------------------------|
| Interface    | Polymorphism — "X plays the role of Drawable"      | `implements` (Chapter 08)     |
| Mixin        | Behaviour reuse — "X has the methods of Logger"    | `adds`                        |
| Composition  | "X has-a Logger"                                   | normal field                  |

This chapter covers **mixins** (`adds`) and **composition** (field-holding).
Interfaces were covered in Chapter 08.

---

## Mixins — sharing methods across classes

A **mixin** is a named bag of methods that a class can pull in. Declare it
with `mixin`:

```zebra
# file: 09_mixin_basic.zbr
# teaches: declaring and using mixins
# chapter: 09-Composition-and-Mixins

mixin Loggable
    def log(message: str)
        print "[log] ${message}"

mixin Cacheable
    var _cache: HashMap(str, str)

    cue init
        _cache = HashMap(str, str)()

    def cache_get(key: str): str?
        return _cache.get(key)

    def cache_set(key: str, value: str)
        _cache.set(key, value)
```

Then use `adds` on the class:

```zebra
class UserService adds Loggable, Cacheable
    cue init
        _cache = HashMap(str, str)()

    def lookup(id: str): str
        var hit = cache_get(id)
        if hit as found
            return found
        log("cache miss for ${id}")
        var fetched = "user-${id}"
        cache_set(id, fetched)
        return fetched

def main()
    var svc = UserService()
    print svc.lookup("42")    # logs "cache miss for 42", returns "user-42"
    print svc.lookup("42")    # silent cache hit, returns "user-42"
```

**Key points:**

- A mixin is declared with `mixin`, not `class`. It can't be instantiated on
  its own.
- `class C adds M1, M2, M3` includes `M1`'s, `M2`'s, and `M3`'s methods (and
  fields) into `C` as if they were declared on `C` directly.
- All mixin methods are accessible on the class without any dotted prefix.
  `svc.log(...)` and `svc.cache_get(...)` look identical to native methods.
- No method-resolution magic: if two mixins define a method with the same
  name, that's a compile error — pick one or rename one.

---

## Composition — has-a, not is-a

When a class needs the *services* of another class but isn't conceptually
the same kind of thing, hold an instance as a field:

```zebra
# file: 09_composition.zbr
# teaches: composition with helper classes
# chapter: 09-Composition-and-Mixins

class FileWriter
    var path: str = ""

    cue init(p: str)
        path = p

    def write(content: str)
        File.write(path, content)

class AuditedReport
    var writer: FileWriter
    var entries: List(str)

    cue init(p: str)
        this.writer = FileWriter(p)
        this.entries = List(str)()

    def add_entry(line: str)
        this.entries.add(line)

    def publish()
        var content = this.entries.join("\n")
        this.writer.write(content)

def main()
    var r = AuditedReport("/tmp/audit.log")
    r.add_entry("user logged in")
    r.add_entry("user updated profile")
    r.publish()
```

`AuditedReport` *uses* `FileWriter`; it isn't a `FileWriter`. The same idea
inheritance-heavy languages call "favouring composition over inheritance."
In Zebra it's just the natural pattern.

---

## Mixin vs. composition — when to use each

| Use a **mixin** when…                                                  | Use **composition** when…                                                |
|------------------------------------------------------------------------|--------------------------------------------------------------------------|
| The shared behaviour is part of the class's identity ("X is also Loggable") | The class *uses* a helper but isn't the helper ("X has a FileWriter")    |
| The mixin's state should be flat with the class's state                | You want the helper to have its own lifecycle                            |
| The behaviour doesn't need its own configuration or replaceable identity | You want the helper independently testable, mockable, or swappable     |

A reasonable default order: reach for **interfaces** first (when you only need
a contract), **composition** second (when you need a helper), **mixins** last
(when the same exact methods need to be reused verbatim across multiple classes).

---

## Multiple mixins — building richer classes

A class can combine several mixins:

```zebra
# file: 09_multiple_mixins.zbr
# teaches: combining multiple mixins
# chapter: 09-Composition-and-Mixins

mixin Timestamped
    var created_at_ms: int = 0

    def stamp_now()
        this.created_at_ms = DateTime.now().epochMs

mixin Tagged
    var tags: List(str)

    cue init()
        this.tags = List(str)()

    def tag(t: str)
        this.tags.add(t)

class BlogPost adds Timestamped, Tagged
    var title: str = ""
    var body: str = ""

    cue init(t: str, b: str)
        this.title = t
        this.body = b
        this.tags = List(str)()
        this.stamp_now()

def main()
    var p = BlogPost("Hello", "First post body")
    p.tag("intro")
    p.tag("zebra")
    print "${p.title} — ${p.tags.count()} tags @ ${p.created_at_ms} ms"
```

The class picks up `created_at_ms`, `tags`, `stamp_now()`, and `tag(...)`
as if they were declared directly on `BlogPost`.

---

## Polymorphism — reach for interfaces (Chapter 08)

When you want a function that works on "anything that can do X," use an
interface — not a hierarchy:

```zebra
# file: 09_polymorphism.zbr
# teaches: interface-based polymorphism (instead of inheritance)
# chapter: 09-Composition-and-Mixins

interface Sounding
    def sound(): str

class Dog implements Sounding
    var name: str = ""

    cue init(n: str)
        this.name = n

    def sound(): str
        return "${this.name}: Woof!"

class Cat implements Sounding
    var name: str = ""

    cue init(n: str)
        this.name = n

    def sound(): str
        return "${this.name}: Meow!"

def main()
    var animals: List(Sounding) = List(Sounding)()
    animals.add(Dog("Rex"))
    animals.add(Cat("Whiskers"))

    for a in animals
        print a.sound()
```

Both `Dog` and `Cat` `implements Sounding`. Code that wants any sounding thing
accepts a `Sounding`; the underlying class can be anything. This is the
polymorphism inheritance offers — without coupling `Dog` or `Cat` to a shared
base implementation.

---

## Real world: a document with capabilities

A realistic example combining interface + mixin + field composition:

```zebra
# file: 09_document_capabilities.zbr
# teaches: combining interface + mixin + composition
# chapter: 09-Composition-and-Mixins

interface Publishable
    def publish()

mixin Versioned
    var version: int = 0

    def bump()
        this.version = this.version + 1

class Storage
    var path: str = ""

    cue init(p: str)
        path = p

    def write(content: str)
        File.write(path, content)

class BlogPost implements Publishable adds Versioned
    var title: str = ""
    var body: str = ""
    var storage: Storage

    cue init(t: str, store_path: str)
        title = t
        storage = Storage(store_path)

    def publish()
        this.bump()                              # mixin method
        var content = "${this.title} v${this.version}\n\n${this.body}"
        this.storage.write(content)              # composition

def main()
    var post = BlogPost("Hello", "/tmp/hello.txt")
    post.body = "First post"
    post.publish()                       # writes v1
    post.body = "First post (revised)"
    post.publish()                       # writes v2
```

`BlogPost` plays the role of a `Publishable` (interface), gains version-tracking
(mixin), and uses a `Storage` helper (field). Three orthogonal capabilities,
none of them coupled into a fragile inheritance chain.

---

## If you're new to programming

> Inheritance is a popular but easy-to-misuse feature. The mental shift Zebra
> asks of you is: instead of "Dog **is a** kind of Animal," ask "what does Dog
> need to **do**?" and pull those abilities in piece by piece.

> A useful default: start with no mixins. When two classes share a contract,
> declare an `interface` and have both `implements` it. When one class needs
> another class's services, hold an instance as a field. When two classes
> need exactly the same methods, factor those methods into a `mixin` and have
> both `adds` it.

---

## Common mistakes

> ❌ **Reaching for class hierarchies you can't have**
>
> ```zebra
> class Dog inherits Animal       # ❌ `inherits` doesn't exist in Zebra
>     def bark
>         print "${name} says: Woof!"
> ```
>
> ✅ Use a mixin or an interface:
>
> ```zebra
> mixin Named
>     var name: str = ""
>
> class Dog adds Named
>     def bark
>         print "${name} says: Woof!"
> ```

> ❌ **Calling `super` to chain into a "parent"**
>
> ```zebra
> def accelerate
>     super.accelerate()           # ❌ no `super` in Zebra
> ```
>
> ✅ Express the shared behaviour as a method on a mixin and call it directly:
>
> ```zebra
> mixin Acceleratable
>     var speed: int = 0
>
>     def base_accelerate
>         speed = speed + 10
>
> class Car adds Acceleratable
>     def accelerate
>         base_accelerate()
>         print "Car cruising at ${speed} mph"
> ```

> ❌ **Two mixins declaring the same method name**
>
> ```zebra
> mixin A
>     def hello
>         print "A"
>
> mixin B
>     def hello
>         print "B"
>
> class C adds A, B               # ❌ ambiguous: which hello()?
> ```
>
> ✅ Rename one or pick the canonical mixin:
>
> ```zebra
> mixin A
>     def hello_a
>         print "A"
>
> mixin B
>     def hello_b
>         print "B"
>
> class C adds A, B
> ```

> ❌ **Modelling a "kind-of" relationship with a mixin**
>
> A `mixin` is for shared *methods*, not for "is-a" modelling. If you find
> yourself reaching for inheritance because Dog is a kind of Animal, the
> right answer is usually an `interface` for the shared contract, with each
> concrete class implementing it independently.

---

## Exercises

### Exercise 1: Vehicle behaviours

Build three vehicle types (`Car`, `Motorcycle`, `Truck`) that share
starting/stopping behaviour via a mixin, but each has a distinct `describe()`
method.

<details>
<summary>Solution</summary>

```zebra
mixin Engine
    var running: bool = false

    def start
        running = true
        print "Engine started"

    def stop
        running = false
        print "Engine stopped"

class Car adds Engine
    var brand: str = ""
    var doors: int = 4

    cue init(b: str)
        brand = b

    def describe: str
        return "${brand} car with ${doors} doors"

class Motorcycle adds Engine
    var brand: str = ""

    cue init(b: str)
        brand = b

    def describe: str
        return "${brand} motorcycle"

class Truck adds Engine
    var brand: str = ""
    var payload_kg: int = 0

    cue init(b: str, p: int)
        brand = b
        payload_kg = p

    def describe: str
        return "${brand} truck (${payload_kg}kg payload)"

def main()
    var car = Car("Toyota")
    car.start()
    print car.describe()
    car.stop()
```

</details>

### Exercise 2: Employees and managers — without inheritance

Model `Employee`, `Manager`, and `Director` without any "kind-of" relationship.
Use a mixin for shared salary/name behaviour, and composition for the
manager's reporting structure.

<details>
<summary>Solution</summary>

```zebra
mixin Compensated
    var name: str = ""
    var salary: float = 0.0

    def info: str
        return "${name} (${salary})"

class Employee adds Compensated
    cue init(n: str, s: float)
        name = n
        salary = s

class Manager adds Compensated
    var team: List(Employee)

    cue init(n: str, s: float)
        name = n
        salary = s
        team = List(Employee)()

    def add_report(e: Employee)
        team.add(e)

    def info: str
        return "${name} (${salary}, manages ${team.count()})"

class Director adds Compensated
    var managers: List(Manager)
    var budget: float = 0.0

    cue init(n: str, s: float, b: float)
        name = n
        salary = s
        budget = b
        managers = List(Manager)()

    def info: str
        return "${name} (${salary}, budget ${budget})"
```

`Manager` and `Director` aren't subclasses of `Employee` — they each `adds
Compensated` independently. Where a manager needs to know its reports, it
holds them by composition (`team: List(Employee)`).

</details>

### Exercise 3: Shapes implementing a common interface

Use the `Shape` interface from Chapter 08 with three independent classes —
no shared base, no inheritance.

<details>
<summary>Solution</summary>

```zebra
interface Shape
    def area: float
    def perimeter: float

class Circle implements Shape
    var radius: float = 0.0

    cue init(r: float)
        radius = r

    def area: float
        return 3.14 * radius * radius

    def perimeter: float
        return 2.0 * 3.14 * radius

class Rectangle implements Shape
    var width: float = 0.0
    var height: float = 0.0

    cue init(w: float, h: float)
        width = w
        height = h

    def area: float
        return width * height

    def perimeter: float
        return 2.0 * (width + height)

class Triangle implements Shape
    var base: float = 0.0
    var height: float = 0.0
    var hypotenuse: float = 0.0

    cue init(b: float, h: float, hy: float)
        base = b
        height = h
        hypotenuse = hy

    def area: float
        return 0.5 * base * height

    def perimeter: float
        return base + height + hypotenuse

def main()
    var shapes: List(Shape) = List(Shape)()
    shapes.add(Circle(5.0))
    shapes.add(Rectangle(4.0, 6.0))
    shapes.add(Triangle(3.0, 4.0, 5.0))

    for s in shapes
        print "area=${s.area()} perim=${s.perimeter()}"
```

</details>

---

## Next Steps

- → **10-Properties** — Field access patterns and getter idioms
- → **14-Contracts** — Enforce invariants across composed types
- 🏋️ **Project-1-CLI-Tool** — Use mixins for cross-cutting concerns
  (logging, configuration)

---

## Key Takeaways

- **Zebra has no inheritance.** No `extends`, no `super`, no parent class.
  This is by design.
- **Three reuse primitives**: interfaces (`implements` — polymorphism),
  mixins (`adds` — behaviour reuse), composition (fields — has-a).
- **Reach for interfaces first**, composition second, mixins last.
- **Mixins are flat** — their methods become part of the class as if
  declared directly.
- **Conflicting mixin methods are a compile error** — no method-resolution
  magic, no diamond ambiguity.

---

**Next:** Head to **10-Properties** for getter idioms and computed-value
patterns.

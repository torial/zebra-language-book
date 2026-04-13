# 7b: Structs, Unions, and Value Types

**Audience:** All  
**Time:** 120 minutes  
**Prerequisites:** 02-Values, 04-Functions, 07-Classes  
**You'll learn:** Structs (value types), unions (tagged unions), `^T` heap indirection, `except` for struct updates, `branch` pattern matching on unions

---

## The Big Picture

Zebra has three kinds of composite types:

| Type | Semantics | Assignment copies... | Allocated on... |
|------|-----------|---------------------|-----------------|
| `class` | Reference | The pointer | Heap |
| `struct` | Value | The whole value | Stack |
| `union` | Tagged union | The whole value | Stack |

You already know classes (Chapter 07). This chapter covers the other two — and they're essential for writing efficient, safe Zebra code.

---

## Structs: Value Types

A struct is like a class, but with **value semantics**. When you assign a struct variable, the entire value is copied.

```zebra
# file: 07b_struct_basic.zbr
# teaches: struct definition and value semantics
# chapter: 07b-Structs-Unions

struct Point
    var x as int
    var y as int

    cue init(x as int, y as int)
        this.x = x
        this.y = y

    def distSq() as int
        return x * x + y * y

class Main
    shared def main()
        var a = Point(3, 4)
        var b = a              # copies the entire Point
        print a.distSq()      # 25
        print b.x              # 3
```

### When to use struct vs class

- **Struct:** Small, short-lived values. Config objects, coordinates, tokens, AST nodes.
- **Class:** Long-lived objects with identity. Collections, services, shared mutable state.

Rule of thumb: if you'd never ask "is this the *same* object?", use a struct.

---

## `except` — Struct Update Copies

The `except` keyword creates a copy of a struct with specific fields overridden. This is the primary idiom for immutable-style struct manipulation:

```zebra
# file: 07b_except.zbr
# teaches: except struct update syntax
# chapter: 07b-Structs-Unions

struct Config
    var indent as int
    var owner as str
    var verbose as bool

    cue init(indent as int, owner as str, verbose as bool)
        this.indent = indent
        this.owner = owner
        this.verbose = verbose

    def indented() as Config
        var c = this except
            indent = indent + 1
        return c

    def withOwner(name as str) as Config
        var c = this except
            owner = name
        return c

class Main
    shared def main()
        var base = Config(0, "nobody", false)
        var inner = base.indented()
        var owned = inner.withOwner("Alice")
        print owned.indent      # 1
        print owned.owner       # Alice
        print owned.verbose     # false (unchanged)
```

### Critical rule: no method chaining on temporaries

```zebra
# WRONG — temporary struct can't be mutated:
# var c = makeConfig().indented().withOwner("Foo")

# RIGHT — use intermediate variables:
var c0 = makeConfig()
var c1 = c0.indented()
var c = c1.withOwner("Foo")
```

---

## Enums

Enums define a fixed set of named constants:

```zebra
# file: 07b_enum.zbr
# teaches: enum types
# chapter: 07b-Structs-Unions

enum Color
    red
    green
    blue

enum Status(int)
    ok = 0
    err = 1

class Main
    shared def main()
        var c = Color.red
        var s = Status.ok
        print s     # 0
```

Use `branch` (see below) to match on enum values.

---

## Unions: Tagged Unions

A union is a type that can hold **one of several variants**, each with its own payload type. Think of it as a type-safe alternative to "this could be an int OR a string OR nothing."

```zebra
# file: 07b_union_basic.zbr
# teaches: union definition and construction
# chapter: 07b-Structs-Unions

union Value
    int_ as int
    str_ as str
    bool_ as bool
    none_

class Main
    shared def main()
        var v1 = Value.int_(42)
        var v2 = Value.str_("hello")
        var v3 = Value.none_()
```

**Naming convention:** Variants that collide with Zebra keywords get a trailing underscore: `int_`, `str_`, `bool_`, `none_`.

---

## `branch` — Pattern Matching on Unions

Use `branch` to inspect which variant a union holds:

```zebra
# file: 07b_branch.zbr
# teaches: branch pattern matching
# chapter: 07b-Structs-Unions

union Shape
    circle as float         # radius
    rect as Dims            # width/height struct
    point                   # no payload

struct Dims
    var w as float
    var h as float
    cue init(w as float, h as float)
        this.w = w
        this.h = h

def describe(s as Shape) as str
    branch s
        on Shape.circle as r
            return "Circle with radius ${r}"
        on Shape.rect as d
            return "Rectangle ${d.w} x ${d.h}"
        on Shape.point
            return "Point"
        else
            pass
    return "unknown"

class Main
    shared def main()
        var c = Shape.circle(3.14)
        var r = Shape.rect(Dims(10.0, 5.0))
        print describe(c)    # Circle with radius 3.14
        print describe(r)    # Rectangle 10.0 x 5.0
```

**Rules:**
- Each `on` arm binds the variant's payload to a name (`as r`, `as d`)
- `else` with `pass` is required for non-exhaustive branches
- Payload-less variants (`point`) don't need `as` binding

### Branch on enums and strings

`branch` also works on enums and strings:

```zebra
branch color
    on Color.red
        print "Stop"
    on Color.green
        print "Go"
    else
        print "Unknown"

branch command
    on "quit"
        sys.exit(0)
    on "help"
        print "Available commands: quit, help"
    else
        print "Unknown command"
```

---

## `^T` — Heap Indirection for Recursive Types

Structs and unions live on the stack. But what if a type needs to reference itself? A `Node` with a `next` field that's also a `Node` would be infinitely sized.

`^T` solves this — it's a heap-allocated pointer to `T`:

```zebra
# file: 07b_heap_indirect.zbr
# teaches: ^T heap indirection
# chapter: 07b-Structs-Unions

struct Node
    var value as int
    var next as ^Node?     # optional heap pointer to another Node

    cue init(value as int, next as ^Node?)
        this.value = value
        this.next = next

class Main
    shared def main()
        var a = Node(1, nil)
        var b = Node(2, nil)
        a.next = b              # auto-boxes: copies b to the heap
        print a.value           # 1
```

**Key points:**
- `^T` in field type → `*T` in Zig (a pointer)
- `^T?` → `?*T` (an optional pointer)
- Assignment to a `^T` field **auto-boxes**: allocates a heap copy
- Inside `branch`, `^T` payloads are transparent — the binding has type `T`, not `*T`

### Where you see `^T` in practice

The Zebra compiler's own AST uses `^T` heavily:

```zebra
union Expr
    int_ as int
    str_ as str
    binary as ^ExprBinary     # recursive: contains two sub-Exprs
    call as ^ExprCall

struct ExprBinary
    var left as ^Expr
    var op as BinaryOp
    var right as ^Expr
```

---

## Putting It All Together: A Small AST

```zebra
# file: 07b_mini_ast.zbr
# teaches: combining structs, unions, and ^T
# chapter: 07b-Structs-Unions

union Expr
    num as int
    add as ^BinExpr
    neg as ^Expr

struct BinExpr
    var left as ^Expr
    var right as ^Expr

    cue init(left as ^Expr, right as ^Expr)
        this.left = left
        this.right = right

def eval(e as Expr) as int
    branch e
        on Expr.num as n
            return n
        on Expr.add as b
            return eval(b.left) + eval(b.right)
        on Expr.neg as inner
            return 0 - eval(inner)
        else
            pass
    return 0

class Main
    shared def main()
        # 3 + (neg 2) = 1
        var three = Expr.num(3)
        var two = Expr.neg(Expr.num(2))
        var sum = Expr.add(BinExpr(three, two))
        print eval(sum)     # 1
```

---

## Exercises

### Exercise 1: RGB Color Struct

Define a `Color` struct with `r`, `g`, `b` fields (all `int`). Add a `mix` method that averages two colors using `except`.

<details>
<summary>Solution</summary>

```zebra
struct Color
    var r as int
    var g as int
    var b as int

    cue init(r as int, g as int, b as int)
        this.r = r
        this.g = g
        this.b = b

    def mix(other as Color) as Color
        var c = this except
            r = (r + other.r) / 2
            g = (g + other.g) / 2
            b = (b + other.b) / 2
        return c

class Main
    shared def main()
        var red = Color(255, 0, 0)
        var blue = Color(0, 0, 255)
        var purple = red.mix(blue)
        print purple.r      # 127
        print purple.b      # 127
```

</details>

### Exercise 2: Expression Evaluator

Extend the mini AST to support multiplication. Add a `mul` variant and handle it in `eval`.

---

## Key Takeaways

- **`struct`** = value type; assignment copies the whole value
- **`union`** = tagged union; holds one variant at a time
- **`branch`** = pattern matching on unions, enums, and strings
- **`except`** = create a struct copy with specific fields overridden
- **`^T`** = heap-indirection pointer; breaks recursive type cycles
- **Use structs for small config/data objects, classes for stateful services**

---

**Next:** Head to **08-Interfaces** for polymorphism without inheritance.

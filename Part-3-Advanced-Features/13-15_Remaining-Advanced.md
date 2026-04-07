# Part 3 Remaining Chapters (13-15)

Due to space, these are comprehensive outlines with key examples. Follow the template from completed chapters for full expansion.

---

## Chapter 13: Generics and Type Constraints

**Time:** 120 min | **Prereq:** 02, 08

### Overview
Generic types let you write reusable code that works with any type while maintaining type safety.

### Key Topics

**Generic Classes:**
```zebra
class Container(T)
    var item as T
    
    def get as T
        return item
    
    def set(value as T)
        item = value

class Main
    shared
        def main
            var int_container = Container(int)()
            int_container.set(42)
            print int_container.get()
            
            var str_container = Container(str)()
            str_container.set("hello")
            print str_container.get()
```

**Generic Functions:**
```zebra
class Utils
    shared
        def print_all(items as List(T)) as str
            var result = ""
            for item in items
                result = result.concat(item.toString())
                result = result.concat(", ")
            return result
```

**Constraints:**
```zebra
class Comparable(T)
    def compare(a as T, b as T) as int
        return 0
```

### Real World
- Generic List, HashMap, Set implementations
- Type-safe wrappers
- Reusable algorithms that work with any type

### Common Mistakes
- Forgetting type parameters
- Overconstrained generics
- Type erasure at runtime

### Exercises
1. Create a generic Pair class
2. Write a generic search function
3. Build a generic cache with size limit

---

## Chapter 14: Contracts and Assertions

**Time:** 90 min | **Prereq:** 04, 07

### Overview
Contracts document and enforce assumptions about code behavior.

### Preconditions
```zebra
class Math
    shared
        def divide(a as int, b as int) as int
            # Precondition: b must not be zero
            if b == 0
                raise "Division by zero"
            return a / b
```

### Postconditions
```zebra
class List
    def add(item as str)
        var old_count = count()
        # Add item
        # Postcondition: count should increase by 1
        if count() != old_count + 1
            raise "List.add failed invariant"
```

### Assertions
```zebra
class Process
    shared
        def process(data as str)
            # Assert precondition
            if data.len == 0
                return
            # Do work
            # Assert postcondition
```

### Real World
- API contract enforcement
- Algorithm correctness verification
- Invariant maintenance

### Exercises
1. Add contracts to bank account
2. Verify sorting postcondition
3. Check data structure invariants

---

## Chapter 15: Pipelines and Function Composition

**Time:** 90 min | **Prereq:** 04

### Overview
The pipeline operator `->` chains operations for readability.

### Pipeline Basics
```zebra
class Main
    shared
        def main
            var text = "HELLO WORLD"
            var result = text.lower().split(" ").at(0)
            
            # Same thing with pipeline (more readable):
            var result2 = text
                -> .lower()
                -> .split(" ")
                -> .at(0)
```

### Function Composition
```zebra
class Transform
    shared
        def double(x as int) as int
            return x * 2
        
        def add_ten(x as int) as int
            return x + 10
        
        def compose_and_run(x as int) as int
            return x -> double() -> add_ten()

class Main
    shared
        def main
            print Transform.compose_and_run(5)  # (5 * 2) + 10 = 20
```

### Real World
- Data transformation pipelines
- Builder patterns
- Functional composition

### Exercises
1. Build a text processing pipeline
2. Create a number transformation chain
3. Compose multiple string operations

---

## Completion Guidance

Each of these chapters should follow the proven template:
1. Opening (audience, time, prereq, objectives)
2. Big picture (why it matters)
3. Intuition first (with analogies)
4. Problem-first examples (2-3 realistic scenarios)
5. Deeper patterns (3-4 approaches)
6. Real world (actual use cases)
7. Common mistakes (3-5 with fixes)
8. Exercises (3-4 with solutions)
9. Key takeaways (3-5 bullets)
10. Next steps (related chapters, projects)

Use the completed chapters (01-12) as style and structure reference.

---

**To expand these chapters:**
1. Copy structure from chapters 01-06 (Part 1 Foundations)
2. Write each section fully (300-500 words each)
3. Create 8-10 runnable examples per chapter
4. Write 3-4 exercises with solutions
5. Test all code examples: `zebra examples/13_*.zbr`

---

**Estimated completion:** 3-4 hours per chapter with full elaboration.

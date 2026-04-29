# Zebra Book — Chapter Templates & Remaining Outline

This document provides the structure and detailed outlines for the remaining chapters. Each chapter follows the same proven template established in Part 1.

---

## PART 2: Objects & Interfaces (Chapters 08-10)

### Chapter 08: Interfaces and Protocols
**Time:** 120 min | **Prereq:** 07

**Topics:**
- Defining interfaces (abstract contracts)
- Implementing interfaces (conformance)
- Polymorphism (treating objects as their interface type)
- Real world: Payment processors, loggers, validators
- Common patterns: Strategy, Observer-like patterns
- Mistakes: Not implementing all methods, wrong signatures
- Exercises: Database interface, shape hierarchy

**Code Examples:**
```zebra
interface Drawable
    def draw
    def get_bounds: Rectangle

class Circle
    implements Drawable
        def draw
            print "Drawing circle"
        def get_bounds: Rectangle
            return Rectangle()
```

---

### Chapter 09: Inheritance and Mixins
**Time:** 120 min | **Prereq:** 07-08

**Topics:**
- Class inheritance (extending base classes)
- Method overriding (replacing behavior)
- Super calls (calling parent implementation)
- Abstract classes and methods
- Mixins (composing behavior from multiple traits)
- Real world: Animal hierarchy, UI components
- Common mistakes: Deep inheritance chains, forgetting super
- Exercises: Vehicle hierarchy, game characters

**Code Examples:**
```zebra
class Animal
    var name: str

class Dog
    inherits Animal
        def speak
            print "Woof: ${name}"

class Cat
    inherits Animal
        def speak
            print "Meow: ${name}"
```

---

### Chapter 10: Properties and Computed Values
**Time:** 90 min | **Prereq:** 07

**Topics:**
- Getters and setters (controlled access)
- Computed properties (derived values)
- Lazy initialization (defer calculation)
- Real world: User profiles, configuration
- Common patterns: Validation on set, caching on get
- Mistakes: Side effects in getters, infinite recursion
- Exercises: Temperature converter, age calculator

**Code Examples:**
```zebra
class Person
    var birth_year: int = 2000
    
    def age: int
        return 2024 - birth_year
    
    def set_age(new_age: int)
        birth_year = 2024 - new_age
```

---

## PART 3: Advanced Features (Chapters 11-15)

### Chapter 11: Nil Tracking and Safety
**Time:** 120 min | **Prereq:** 01-06

**Topics:**
- Nullable types (`?` syntax)
- Nil checks and narrowing
- Unwrap operator (`to!`)
- Optional chaining (safe navigation)
- Real world: Database queries, user input, API responses
- Common mistakes: Forgetting nil checks, unwrapping unsafely
- Exercises: Safe string parsing, null-safe navigation

---

### Chapter 12: Error Handling with Results
**Time:** 120 min | **Prereq:** 11

**Topics:**
- Result type (Ok/Err pattern)
- Error propagation
- Chaining operations
- vs. Exceptions (why Zebra uses Results)
- Real world: API clients, file operations, validation
- Common mistakes: Ignoring errors, nested unwrapping
- Exercises: Division with error handling, CSV parsing with validation

---

### Chapter 13: Generics and Type Constraints
**Time:** 120 min | **Prereq:** 02-08

**Topics:**
- Generic types and methods
- Type parameters
- Constraints (ensuring type compatibility)
- Variance (covariance, contravariance)
- Real world: Collections, data structures, algorithms
- Common mistakes: Forgetting type parameters, overconstrained types
- Exercises: Generic queue, generic sort

---

### Chapter 14: Contracts and Assertions
**Time:** 90 min | **Prereq:** 04

**Topics:**
- Preconditions (what must be true before)
- Postconditions (what must be true after)
- Invariants (always true)
- Assertions for debugging
- Real world: API contracts, algorithm correctness
- Common mistakes: Expensive assertions, unclear messages
- Exercises: Validated types, guaranteed invariants

---

### Chapter 15: Pipelines and Function Composition
**Time:** 90 min | **Prereq:** 04

**Topics:**
- Pipeline operator (`->`)
- Function composition
- Method chaining
- Real world: Data transformation, processing chains
- Common mistakes: Overly nested pipelines, unclear intent
- Exercises: Text processing pipeline, data analysis chain

---

## PART 4: Practical Projects (Chapters 16-18)

### Project 1: Command-Line Tool (Text Processing)
**Time:** 3-4 hours | **Prereq:** 01-09

**Build:** A file processing tool (word count, grep-lite, CSV tool)

**Learning:**
- Command-line argument parsing
- File I/O (reading, writing)
- Collections for data processing
- Error handling (file not found, invalid format)
- Classes for organizing logic

**Chapters of implementation:**
1. Project setup and basic structure
2. Parsing arguments
3. Reading files and processing
4. Output formatting
5. Handling errors gracefully

---

### Project 2: HTTP Server
**Time:** 4-5 hours | **Prereq:** 01-12

**Build:** A simple REST API server (JSON responses, routing, error handling)

**Learning:**
- Networking basics (TCP, HTTP)
- Error handling (Result type heavily used)
- Structs for request/response
- Interfaces for handlers
- Nil tracking in real systems

**Chapters:**
1. Server setup and listening
2. Parsing HTTP requests
3. Routing to handlers
4. JSON serialization
5. Error handling and status codes

---

### Project 3: Data Analysis
**Time:** 3-4 hours | **Prereq:** 01-09

**Build:** Analyze text data (n-grams, word frequencies, similarity)

**Learning:**
- Collections mastery (List, HashMap, Set)
- Algorithms (sorting, filtering, aggregation)
- String processing and regex
- Results for error handling

**Chapters:**
1. Loading and parsing data
2. N-gram analysis
3. Frequency computation
4. Sorting and ranking
5. Reporting results

---

## PART 5: Ecosystem (Chapters 19-22)

### Chapter 19: Standard Library Tour
**Time:** 90 min | **Prereq:** 01-06

**Topics:**
- Core data structures (List, HashMap, Set methods)
- String manipulation library
- Math functions
- Type conversion utilities
- Real world: What's available before rolling your own
- Exercises: Use stdlib functions effectively

---

### Chapter 20: File I/O and System Access
**Time:** 90 min | **Prereq:** 06, 12

**Topics:**
- Reading files
- Writing files
- Directory operations
- System information (args, environment)
- Error handling (File not found, permission denied)
- Real world: Config files, logging, data export
- Exercises: CSV reader, log analyzer

---

### Chapter 21: Regular Expressions (Deep Dive)
**Time:** 90 min | **Prereq:** 06

**Topics:**
- Pattern syntax (literals, classes, quantifiers)
- Groups and capturing
- Common patterns (email, URL, phone)
- Performance (avoiding catastrophic backtracking)
- Real world: Validation, parsing, searching
- Exercises: Email validator, phone number parser, log analyzer

---

### Chapter 22: FFI and Interop
**Time:** 90 min | **Prereq:** 02, 07, 12

**Topics:**
- Calling C functions
- Calling Zig code
- Type marshaling
- Callbacks from native code
- Safety considerations
- Real world: Accessing system libraries, performance-critical code
- Exercises: Call C math functions, wrap a library

---

## APPENDICES (A-C)

### Appendix A: Grammar Reference
**Content:**
- Lexical structure
- Type syntax
- Expression syntax
- Statement syntax
- Class/Interface/Function syntax
- Quick reference tables

---

### Appendix B: Built-in Functions
**Content:**
- print, println, input
- Type conversion functions
- Standard library overview
- Math functions
- Collection operations
- String methods

---

### Appendix C: Troubleshooting
**Content:**
- "Error: arithmetic requires numeric type, got 'str'" → Explanation + fix
- Common compilation errors
- Runtime errors
- Performance tips
- Where to find help

---

## Writing Checklist for Each Chapter

Every chapter should include:

- [ ] Opening: Audience, time, prerequisites, learning objectives
- [ ] Big picture: Why this matters, real-world relevance
- [ ] Intuition first: Visual explanation, analogies
- [ ] Problem-first examples: Real scenarios
- [ ] Deeper patterns: 2-3 different approaches
- [ ] Real world code: From actual use cases
- [ ] Common mistakes: 3-5 with fixes
- [ ] Exercises: 3-4 with solutions
- [ ] Key takeaways: 3-5 bullet points
- [ ] Next steps: Links to related chapters, projects
- [ ] All code examples: Runnable, tagged, in `/examples/`

---

## Example: How to Write Chapter X

When you sit down to write Chapter X:

1. **Create file:** `Part-N/0X-Title.md`
2. **Copy template:** Start with the outline from _BOOK_CHAPTERS_TEMPLATE.md
3. **Write sections:**
   - Introduction (150 words)
   - Big Picture (200 words)
   - Intuition First (300 words + diagram)
   - Problem-First Examples (400 words + 3 examples)
   - Deeper Patterns (500 words + 4 examples)
   - Real World (300 words + 1 large example)
   - Common Mistakes (300 words + 3 mistakes)
   - Exercises (400 words + 3 exercises with solutions)
   - Next Steps (100 words)
   - Key Takeaways (100 words)
4. **Extract code:** Tag each example with `// file:`, `// teaches:`, `// chapter:`
5. **Test examples:** Run `zebra <file>.zbr` for each
6. **Review:** Check against checklist above
7. **Commit:** Save to git with chapter number and title

---

## Estimated Writing Time

**Full Book:**
- Part 1: 6 chapters × 2-3 hours = 12-18 hours (✅ DONE)
- Part 2: 4 chapters × 2-3 hours = 8-12 hours
- Part 3: 5 chapters × 2-3 hours = 10-15 hours
- Part 4: 3 projects × 3-4 hours = 9-12 hours
- Part 5: 4 chapters × 1-2 hours = 4-8 hours
- Appendices: 3 sections × 1-2 hours = 3-6 hours

**Total: 46-71 hours of focused writing**

**Per week (10 hours/week):** Complete in 5-7 weeks

---

## Next Steps

1. ✅ Part 1 (Chapters 01-06) — COMPLETE
2. → Complete Part 2 (Chapters 08-10) — Use template structure
3. → Write Part 3 (Chapters 11-15) — Use template structure
4. → Build Part 4 (3 Projects) — Write step-by-step implementations
5. → Write Part 5 (Chapters 19-22) — Use template structure
6. → Write Appendices (A-C) — Compress into reference format
7. → Build Python tools (extract, validate, build HTML/PDF)
8. → Test build system with `make build`

---

**Strategy for completion:**
- Each chapter takes 2-3 focused writing sessions
- Start with outlines (this document) → fill in content
- Test examples immediately after writing
- Iterate on prose after all chapters are drafted


# Zebra Code Examples Index

A complete guide to 250+ code examples extracted from the Zebra Programming Book.

---

## Quick Start

**New to Zebra?** Start here:
1. [Hello World](#hello-world) — Your first program
2. [Variables & Types](#variables-and-types) — Understand Zebra's type system
3. [Functions](#functions) — Writing reusable code
4. [Loops & Control Flow](#loops-and-control-flow) — Program flow
5. [Collections](#collections) — Working with data

---

## Browse by Difficulty Level

### Beginner (Basics)
Essential concepts for all Zebra programmers:
- [Hello World & Basic Output](#hello-world)
- [Variables & Types](#variables-and-types)
- [Operators & Arithmetic](#operators-and-arithmetic)
- [String Basics](#string-basics)
- [Simple Functions](#functions)
- [Loops & Conditionals](#loops-and-control-flow)

### Intermediate (Core Language)
Foundation of practical Zebra programs:
- [Collections (List, HashMap, Set)](#collections)
- [Classes & Objects](#classes-and-objects)
- [Interfaces & Protocols](#interfaces-and-protocols)
- [Error Handling](#error-handling)
- [File I/O](#file-io)
- [String Processing](#string-processing)

### Advanced (Professional Code)
Building production systems:
- [Generics & Type Constraints](#generics)
- [Regular Expressions](#regular-expressions)
- [Inheritance & Mixins](#inheritance-and-mixins)
- [Pipelines](#pipelines)
- [Contracts & Assertions](#contracts-and-assertions)
- [FFI & Interop](#ffi-and-interop)

---

## Browse by Topic

### Hello World
Entry point for all learners.

**Files:**
- `01-getting-started/hello.zbr` — Print text to console
- `01-getting-started/hello_advanced.zbr` — Enhanced greeting
- `01-getting-started/main_function.zbr` — Understanding entry point

**Run it:**
```bash
zebra 01-getting-started/hello.zbr
```

---

### Variables and Types

Understanding Zebra's type system.

**Beginner:**
- `02-values-types/simple_variables.zbr` — Declare variables
- `02-values-types/type_inference.zbr` — Let Zebra figure out types
- `02-values-types/explicit_types.zbr` — Specify types explicitly

**Intermediate:**
- `02-values-types/nullable_types.zbr` — Handle potentially nil values
- `02-values-types/type_conversion.zbr` — Convert between types
- `02-values-types/type_narrowing.zbr` — Refine types safely

**Key Concepts:**
- `int` — 64-bit integers
- `float` — Floating-point numbers
- `str` — Text strings (immutable)
- `bool` — True/false values
- `T?` — Nullable types

---

### Operators and Arithmetic

Basic math and logical operations.

**Files:**
- `02-values-types/arithmetic.zbr` — Add, subtract, multiply, divide
- `02-values-types/comparison.zbr` — Compare values
- `02-values-types/logical_operators.zbr` — and, or, not operations
- `02-values-types/operator_precedence.zbr` — Order of operations

---

### String Basics

Working with text.

**Beginner:**
- `06-strings/string_literals.zbr` — Create strings
- `06-strings/string_length.zbr` — Get string length
- `06-strings/string_concatenation.zbr` — Join strings

**Intermediate:**
- `06-strings/string_interpolation.zbr` — Embed values in strings
- `06-strings/string_methods.zbr` — upper(), lower(), contains()
- `06-strings/string_search.zbr` — Find substrings
- `06-strings/string_split_join.zbr` — Split and rejoin text

**Advanced:**
- `06-strings/unicode_handling.zbr` — UTF-8 and international text
- `06-strings/string_builder.zbr` — Efficient string building

---

### Functions

Reusable blocks of code.

**Beginner:**
- `04-functions/simple_function.zbr` — Define and call functions
- `04-functions/function_parameters.zbr` — Pass data to functions
- `04-functions/function_return.zbr` — Return values from functions

**Intermediate:**
- `04-functions/function_overloading.zbr` — Multiple functions, same name
- `04-functions/function_scope.zbr` — Variable visibility
- `04-functions/recursive_functions.zbr` — Functions that call themselves

**Advanced:**
- `04-functions/higher_order_functions.zbr` — Functions as values
- `04-functions/tail_recursion.zbr` — Optimized recursion

---

### Loops and Control Flow

Program flow and repetition.

**Beginner:**
- `05-control-flow/if_else.zbr` — Conditional execution
- `05-control-flow/while_loop.zbr` — Repeat while condition true
- `05-control-flow/for_loop.zbr` — Iterate over ranges

**Intermediate:**
- `05-control-flow/for_each_loop.zbr` — Loop through collections
- `05-control-flow/break_continue.zbr` — Control loop flow
- `05-control-flow/nested_loops.zbr` — Loops within loops

**Advanced:**
- `05-control-flow/pattern_matching.zbr` — Branch on values
- `05-control-flow/guard_clauses.zbr` — Early returns and guards

---

### Collections

Storing and organizing data.

**List Examples:**
- `03-collections/list_creation.zbr` — Create lists
- `03-collections/list_operations.zbr` — add(), remove(), at()
- `03-collections/list_iteration.zbr` — Loop through lists
- `03-collections/list_filtering.zbr` — Select items
- `03-collections/list_transformation.zbr` — Transform elements

**HashMap Examples:**
- `03-collections/hashmap_creation.zbr` — Create key-value maps
- `03-collections/hashmap_operations.zbr` — put(), fetch(), contains()
- `03-collections/hashmap_iteration.zbr` — Loop through entries
- `03-collections/count_by_category.zbr` — Group and count

**Set Examples:**
- `03-collections/set_creation.zbr` — Create unique item sets
- `03-collections/set_operations.zbr` — add(), remove(), contains()
- `03-collections/set_deduplication.zbr` — Remove duplicates

---

### Classes and Objects

Object-oriented programming.

**Beginner:**
- `07-classes/class_definition.zbr` — Create a class
- `07-classes/constructor.zbr` — Initialize objects
- `07-classes/instance_methods.zbr` — Methods on objects
- `07-classes/instance_variables.zbr` — Store object data

**Intermediate:**
- `07-classes/static_methods.zbr` — Methods without instances
- `07-classes/property_access.zbr` — Get and set data
- `07-classes/class_vs_instance.zbr` — Shared vs instance members

**Advanced:**
- `07-classes/method_overloading.zbr` — Same name, different signatures

---

### Interfaces and Protocols

Contracts and polymorphism.

**Files:**
- `08-interfaces/interface_definition.zbr` — Define an interface
- `08-interfaces/interface_implementation.zbr` — Implement interface
- `08-interfaces/interface_polymorphism.zbr` — Use interfaces polymorphically
- `08-interfaces/multiple_interfaces.zbr` — Implement multiple interfaces

---

### Composition and Mixins

Code reuse via mixins (`adds`) and composition (helper instances as fields).
Zebra has no class inheritance — see Chapter 09 for the rationale.

**Beginner:**
- `09-inheritance/basic_inheritance.zbr` — Extend a class
- `09-inheritance/method_override.zbr` — Replace parent methods
- `09-inheritance/super_call.zbr` — Call parent implementations

**Advanced:**
- `09-inheritance/mixin_composition.zbr` — Share behavior via mixins
- `09-inheritance/trait_implementation.zbr` — Multiple inheritance patterns

---

### Nil Tracking and Safety

Prevent null pointer errors.

**Beginner:**
- `11-nil-tracking/nullable_types.zbr` — Understand T?
- `11-nil-tracking/null_checks.zbr` — if x != nil pattern
- `11-nil-tracking/safe_navigation.zbr` — Safe value access

**Intermediate:**
- `11-nil-tracking/nil_coalescing.zbr` — Default values with unwrapOr()
- `11-nil-tracking/exhaustive_checking.zbr` — Handle all cases

---

### Error Handling

Handle problems gracefully.

**Beginner:**
- `12-error-handling/result_type.zbr` — Success or error
- `12-error-handling/result_checking.zbr` — if result.isOk() pattern
- `12-error-handling/result_unwrapping.zbr` — Extract values safely

**Intermediate:**
- `12-error-handling/result_propagation.zbr` — Pass errors up
- `12-error-handling/error_branches.zbr` — branch result on ok/err
- `12-error-handling/custom_errors.zbr` — Define error types

**Advanced:**
- `12-error-handling/error_chaining.zbr` — Compose operations

---

### Generics

Write flexible, type-safe code.

**Beginner:**
- `13-generics/generic_function.zbr` — Functions with type parameters
- `13-generics/generic_class.zbr` — Classes with type parameters
- `13-generics/generic_constraints.zbr` — Constrain type parameters

**Advanced:**
- `13-generics/variance.zbr` — Covariance and contravariance
- `13-generics/multiple_type_params.zbr` — Multiple type parameters

---

### File I/O

Read and write files.

**Beginner:**
- `20-file-io/read_file.zbr` — Load file contents
- `20-file-io/write_file.zbr` — Save data to file
- `20-file-io/file_exists.zbr` — Check if file exists

**Intermediate:**
- `20-file-io/read_lines.zbr` — Process line by line
- `20-file-io/csv_reading.zbr` — Parse CSV files
- `20-file-io/file_operations.zbr` — Delete, copy operations

**Advanced:**
- `20-file-io/batch_processing.zbr` — Process multiple files
- `20-file-io/streaming.zbr` — Handle large files

---

### String Processing

Advanced text manipulation.

**Beginner:**
- `19-stdlib/string_case.zbr` — upper(), lower()
- `19-stdlib/string_search.zbr` — contains(), indexOf()
- `19-stdlib/string_split.zbr` — split(), join()

**Intermediate:**
- `19-stdlib/string_replace.zbr` — Find and replace
- `19-stdlib/string_formatting.zbr` — Format output
- `19-stdlib/string_extraction.zbr` — substring operations

**Advanced:**
- `19-stdlib/string_builder.zbr` — Efficient building
- `19-stdlib/text_analysis.zbr` — Word counts, statistics

---

### Regular Expressions

Pattern matching in text.

**Beginner:**
- `21-regex/regex_match.zbr` — Test if pattern matches
- `21-regex/regex_find.zbr` — Find matches in text
- `21-regex/simple_patterns.zbr` — Basic patterns

**Intermediate:**
- `21-regex/character_classes.zbr` — [a-z], \d, \w, \s
- `21-regex/quantifiers.zbr` — *, +, ?, {n,m}
- `21-regex/groups.zbr` — () and | alternation

**Advanced:**
- `21-regex/email_validation.zbr` — Email pattern
- `21-regex/url_extraction.zbr` — Extract URLs
- `21-regex/log_parsing.zbr` — Parse log files

---

### Pipelines

Functional composition and data flow.

**Files:**
- `15-pipelines/simple_pipeline.zbr` — Chain operations
- `15-pipelines/pipeline_flow.zbr` — Data through multiple steps
- `15-pipelines/custom_pipeline.zbr` — Define pipeline operators

---

### Contracts and Assertions

Validate assumptions.

**Files:**
- `14-contracts/precondition.zbr` — Require before execution
- `14-contracts/postcondition.zbr` — Ensure after execution
- `14-contracts/assertions.zbr` — Check conditions

---

### FFI and Interop

Call code from other languages.

**Files:**
- `22-ffi/c_function_call.zbr` — Call C code
- `22-ffi/zig_interop.zbr` — Call Zig code
- `22-ffi/type_marshaling.zbr` — Convert types across boundaries
- `22-ffi/error_handling.zbr` — Handle errors from C

---

## Browse by Chapter

### Part 1: Foundations

- **Chapter 1:** Getting Started
  - File: `01-getting-started/`
  - Topics: hello world, main function, compilation

- **Chapter 2:** Values and Types
  - Files: `02-values-types/`
  - Topics: int, float, str, bool, type inference

- **Chapter 3:** Collections
  - Files: `03-collections/`
  - Topics: List, HashMap, Set

- **Chapter 4:** Functions and Scope
  - Files: `04-functions/`
  - Topics: defining functions, parameters, return types, scope

- **Chapter 5:** Control Flow
  - Files: `05-control-flow/`
  - Topics: if/elif/else, while, for, break, continue

- **Chapter 6:** Strings and Unicode
  - Files: `06-strings/`
  - Topics: string operations, UTF-8, internationalization

### Part 2: Objects and Interfaces

- **Chapter 7:** Classes and Instances
  - Files: `07-classes/`
  - Topics: class definition, constructor, instance methods

- **Chapter 8:** Interfaces and Protocols
  - Files: `08-interfaces/`
  - Topics: interface definition, implementation, polymorphism

- **Chapter 9:** Composition and Mixins
  - Files: `09-inheritance/` (directory still pre-rewrite — see README.md note)
  - Topics: mixins (`adds`), composition (fields), interface-based polymorphism

- **Chapter 10:** Properties and Computed Values
  - Files: `10-properties/`
  - Topics: getters, setters, computed properties

### Part 3: Advanced Features

- **Chapter 11:** Nil Tracking and Safety
  - Files: `11-nil-tracking/`
  - Topics: nullable types, null checks, safe navigation

- **Chapter 12:** Error Handling with Results
  - Files: `12-error-handling/`
  - Topics: Result type, error propagation, recovery

- **Chapter 13:** Generics and Type Constraints
  - Files: `13-generics/`
  - Topics: generic functions, generic classes, constraints

- **Chapter 14:** Contracts and Assertions
  - Files: `14-contracts/`
  - Topics: preconditions, postconditions, assertions

- **Chapter 15:** Pipelines and Function Composition
  - Files: `15-pipelines/`
  - Topics: pipeline operator, data flow, composition

### Part 4: Practical Projects

- **Chapter 16:** Project 1 - CLI Tool
  - Files: `16-project-cli/`
  - Topics: command-line args, file operations, user interaction

- **Chapters 17-18:** Projects 2-3 - Web and Analysis
  - Files: `17-18-projects/`
  - Topics: HTTP, networking, data analysis

### Part 5: Ecosystem

- **Chapter 19:** Standard Library Tour
  - Files: `19-stdlib/`
  - Topics: built-in functions, collections, conversions

- **Chapter 20:** File I/O and System Access
  - Files: `20-file-io/`
  - Topics: reading, writing, directory operations

- **Chapter 21:** Regular Expressions
  - Files: `21-regex/`
  - Topics: pattern matching, validation, extraction

- **Chapter 22:** FFI and Interop
  - Files: `22-ffi/`
  - Topics: calling C, Zig interop, marshaling

---

## How to Use These Examples

### Run an Example

```bash
zebra path/to/example.zbr
```

### Study an Example

Each example file has:
- Clear purpose statement in comments
- Minimal, focused code
- Typical 5-50 lines
- Copy-paste ready

### Find Examples by Task

Looking for: **"How do I read a file?"**

Search strategy:
1. Look in chapter index (Chapter 20: File I/O)
2. Find relevant file in `20-file-io/`
3. Look for `read_file.zbr` or `file_operations.zbr`
4. Copy and adapt to your use case

### Progress Path

**Recommended learning order:**

1. **Week 1:** Basics
   - `hello.zbr` → `simple_variables.zbr` → `arithmetic.zbr` → `string_basics.zbr` → `simple_function.zbr`

2. **Week 2:** Control Flow
   - `if_else.zbr` → `while_loop.zbr` → `for_loop.zbr` → `list_creation.zbr` → `list_iteration.zbr`

3. **Week 3:** Objects
   - `class_definition.zbr` → `constructor.zbr` → `interface_definition.zbr` → `basic_inheritance.zbr`

4. **Week 4:** Error Handling & Files
   - `result_type.zbr` → `result_checking.zbr` → `read_file.zbr` → `write_file.zbr`

5. **Week 5+:** Advanced Topics & Projects
   - Pick examples relevant to your project needs

---

## Example Metadata

Each example includes:

- **File:** Location and name
- **Time:** Estimated reading time (1-5 minutes)
- **Topic:** What it teaches
- **Difficulty:** Beginner, Intermediate, or Advanced
- **Dependencies:** Other concepts you should know first
- **Output:** What you should see when run
- **Variations:** Ideas for modification

---

## Quick Reference by Task

### "How do I...?"

| Task | Look in | Example |
|------|----------|---------|
| Print to console? | Chapter 1 | `01-getting-started/hello.zbr` |
| Use variables? | Chapter 2 | `02-values-types/simple_variables.zbr` |
| Create a list? | Chapter 3 | `03-collections/list_creation.zbr` |
| Write a function? | Chapter 4 | `04-functions/simple_function.zbr` |
| Loop through items? | Chapter 5 | `05-control-flow/for_each_loop.zbr` |
| Work with strings? | Chapter 6 | `06-strings/string_interpolation.zbr` |
| Create a class? | Chapter 7 | `07-classes/class_definition.zbr` |
| Use an interface? | Chapter 8 | `08-interfaces/interface_implementation.zbr` |
| Handle errors? | Chapter 12 | `12-error-handling/result_checking.zbr` |
| Read a file? | Chapter 20 | `20-file-io/read_file.zbr` |
| Use regex? | Chapter 21 | `21-regex/regex_match.zbr` |

---

## Contributing Examples

Found a cool pattern? Created a useful example?

1. Add file to appropriate chapter directory
2. Follow naming convention: `descriptive_name.zbr`
3. Add metadata comment at top
4. Test that it compiles and runs
5. Submit to the project

---

## Statistics

- **Total Examples:** 250+
- **Lines of Code:** ~15,000
- **Topics Covered:** 50+
- **Difficulty Levels:** 3 (Beginner, Intermediate, Advanced)
- **Estimated Reading Time:** 30-50 hours for all examples

---

## See Also

- **Main Book:** Read the full chapters for detailed explanations
- **Cheat Sheet:** `CHEATSHEET-Syntax.md` for quick syntax reference
- **Patterns Guide:** `PATTERNS-Common-Tasks.md` for copy-paste solutions
- **Quick Start:** `QUICKSTART-30-Minutes.md` for 30-minute intro

---

Happy learning! 🦓

Questions? Check the Troubleshooting guide (Appendix C in the main book).

# The Zebra Book — Master Outline

## Complete Chapter List & Dependencies

```
PART 1: FOUNDATIONS (6 chapters, ~12 hours)
├─ 01-Getting-Started.md ............................ (30 min)
├─ 02-Values-and-Types.md .......................... (90 min)
├─ 03-Collections.md ............................... (120 min)
├─ 04-Functions-and-Scope.md ....................... (120 min)
├─ 05-Control-Flow.md .............................. (90 min)
└─ 06-Strings-and-Unicode.md ....................... (90 min)

PART 2: OBJECTS & INTERFACES (4 chapters, ~8 hours)
├─ 07-Classes-and-Instances.md (requires: 01,02,04,05)
├─ 08-Interfaces-and-Protocols.md (requires: 07)
├─ 09-Inheritance-and-Mixins.md (requires: 08)
└─ 10-Properties-and-Computed-Values.md (requires: 07)

PART 3: ADVANCED FEATURES (5 chapters, ~10 hours)
├─ 11-Nil-Tracking-and-Safety.md (requires: 02,05,07)
├─ 12-Error-Handling-with-Results.md (requires: 02,11)
├─ 13-Generics-and-Type-Constraints.md (requires: 02,08)
├─ 14-Contracts-and-Assertions.md (requires: 04)
└─ 15-Pipelines-and-Function-Composition.md (requires: 04,05)

PART 4: PRACTICAL PROJECTS (3 chapters, ~12 hours)
├─ Project-1-CLI-Tool.md (requires: 01-06, 21)
├─ Project-2-HTTP-Server.md (requires: 01-12, 20)
└─ Project-3-Data-Analysis.md (requires: 01-06, 13)

PART 5: ECOSYSTEM (4 chapters, ~6 hours)
├─ 16-Standard-Library-Tour.md (requires: 01-06)
├─ 17-File-IO-and-System-Access.md (requires: 02,05,06)
├─ 18-Regular-Expressions.md (requires: 06)
└─ 19-FFI-and-Interop.md (requires: 02,07)

APPENDICES (3 chapters, reference)
├─ A-Grammar-Reference.md
├─ B-Built-in-Functions.md
└─ C-Troubleshooting.md
```

## Reading Paths

### Path A: Complete Linear (for learning from start to finish)
**Duration:** 50-60 hours | **Best for:** Building comprehensive understanding

```
01 → 02 → 03 → 04 → 05 → 06
       ↓
       07 → 08 → 09 → 10
            ↓
            11 → 12 → 13 → 14 → 15
                           ↓
                      (Projects 1-3)
                           ↓
                      16 → 17 → 18 → 19
```

### Path B: Quick Start to Shipping (focus on practical output)
**Duration:** 25-30 hours | **Best for:** Building something immediately

```
01 → 02 → 03 → 04 → 05 → 06 → 07 → 11
              ↓
              16 → 17 → Project-2-HTTP-Server
```

### Path C: Safety-First (understand Zebra's unique features)
**Duration:** 15-20 hours | **Best for:** Understanding what makes Zebra different

```
01 → 02 → 04 → 05 → 07 → 11 → 12 → 14
              ↓
              13 (if you want generics too)
```

### Path D: Object-Oriented Deep Dive (classes, inheritance, polymorphism)
**Duration:** 20-25 hours | **Best for:** OOP enthusiasts

```
01 → 02 → 04 → 05 → 07 → 08 → 09 → 10 → 13
              ↓
              Project-1-CLI-Tool
```

### Path E: Data & Scripting (collections, algorithms, I/O)
**Duration:** 20-25 hours | **Best for:** Data analysis, system tools

```
01 → 02 → 03 → 04 → 05 → 06 → 16 → 17 → 18
              ↓
              Project-3-Data-Analysis
```

## Chapter Topics at a Glance

### Part 1: Foundations

| Chapter | Covers | Projects |
|---------|--------|----------|
| **01** | Installation, tooling, first program | None |
| **02** | Types (int, float, bool, str), variables, type inference | Simple values |
| **03** | List, HashMap, Set, iteration, indexing | Collections |
| **04** | Functions, parameters, return values, closures, captures | Utilities |
| **05** | if/else, match, for, while, break, continue, guards | Control logic |
| **06** | String literals, interpolation, methods, Unicode, regex intro | Text processing |

### Part 2: Objects & Interfaces

| Chapter | Covers | Projects |
|---------|--------|----------|
| **07** | Class definition, instantiation, methods, shared members | OOP basics |
| **08** | Interface definition, protocol conformance, polymorphism | Contracts |
| **09** | Inheritance, mixins, super, abstract methods | Hierarchies |
| **10** | Properties, getters/setters, computed properties, lazy init | Encapsulation |

### Part 3: Advanced Features

| Chapter | Covers | Projects |
|---------|--------|----------|
| **11** | Nilable types (?), nil checks, narrowing, to! operator | Safety |
| **12** | Result type, ok/err, unwrapOr, error propagation | Error handling |
| **13** | Generics, constraints, variance, type parameters | Reusability |
| **14** | Contracts (pre/post), assertions, invariants | Correctness |
| **15** | Pipeline operator (->), composition, functional patterns | Style |

### Part 4: Projects

| Project | Goal | Learn |
|---------|------|-------|
| **1** | Build a file processor CLI (wc, grep-lite, csv tool) | Args, files, collections, control flow |
| **2** | Build an HTTP server (JSON API, routing, error handling) | Networking, error handling, structs, interfaces |
| **3** | Analyze data (n-grams, frequency, sorting, output) | Collections, regex, algorithms, results |

### Part 5: Ecosystem

| Chapter | Covers | Projects |
|---------|--------|----------|
| **16** | String methods, List methods, HashMap methods, math | Practical stdlib |
| **17** | File reading/writing, directories, system calls, args | I/O |
| **18** | Thompson NFA regex, matching, groups, split, replace | Text |
| **19** | C FFI, Zig FFI, calling native functions, callbacks | Systems |

## Time Estimates

**Minimum (just the chapters, no exercises):** 30 hours
**Standard (chapters + exercises, no projects):** 40 hours
**Full (everything):** 60 hours

Per chapter:
- Reading: 20-30 min
- Understanding the "why": 20-30 min
- Exercises: 20-40 min
- Playing around on your own: 30-60 min

## What's Assumed

✅ You know: variables, functions, loops, if/else, basic types  
✅ You've programmed before (Python, Java, Go, Rust, C, etc.)  
✅ You can install and run programs  

❌ You don't need: compiler internals, language design theory, Zig knowledge (bonus if you have it)

## How Examples Work

Every code example is:
1. **In the text** (for reading)
2. **In a file** under `examples/` (for running)
3. **Tagged with metadata:**
   ```
   // file: 02_hello.zbr
   // teaches: hello world, print
   // chapter: 01-Getting-Started
   ```
4. **Validated by make build** (must compile and run correctly)

To run an example:
```bash
zebra examples/01_hello.zbr
```

## Notes on Iteration

This book is a **living document**:

- Chapters will improve through multiple drafts
- Examples will update as Zebra evolves
- New chapters may be added as the language grows
- Feedback will shape future versions

**Current focus areas for iteration:**
- Balancing depth vs. breadth
- Making sure projects feel real and useful
- Validating all examples work end-to-end
- Polishing prose and visual explanations

---

**Start reading:** Pick a path above, then dive into the first chapter.

**Contributing?** See CONTRIBUTING.md for how to suggest improvements.

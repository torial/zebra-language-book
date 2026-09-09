# Zebra Programming Book - Diagrams Embedded

**Status:** ✅ All 13 diagrams embedded in chapters

This document tracks where each SVG diagram has been embedded in the Zebra Programming Book.

---

## Part 1: Foundations

### Chapter 02: Values and Types
- **Location:** After "The Big Picture" section, before "Basic Types"
- **Diagram:** `01-type-hierarchy.svg`
- **Purpose:** Visual overview of Zebra's type system (primitives, collections, nullable, Result)

### Chapter 03: Collections
- **Location:** After "The Big Picture" section, before "Lists"
- **Diagram:** `02-collections-comparison.svg`
- **Purpose:** Side-by-side comparison of List, HashMap, Set with memory layout and iteration patterns

### Chapter 04: Functions and Scope
- **Location:** In "## Scope" section, before "### Local Scope"
- **Diagram:** `03-scope-and-lifetime.svg`
- **Purpose:** Variable scope boundaries, lifetime, and closure capture mechanics

### Chapter 06: Strings and Unicode
- **Location:** In "## Unicode and Internationalization" section, before "### Unicode Basics"
- **Diagram:** `13-unicode-representation.svg`
- **Purpose:** UTF-8 encoding, ASCII vs multi-byte characters, string method operations

---

## Part 2: Objects & Interfaces

### Chapter 07: Classes and Instances
- **Location:** After "## Defining Classes", before "### Simple Class"
- **Diagram:** `12-class-structure.svg`
- **Purpose:** Class anatomy with fields, methods, instance vs shared (static) members, memory layout

### Chapter 09: Composition and Mixins
- **Status:** Diagram outdated — was a class-hierarchy chart; the chapter
  no longer teaches hierarchies (Zebra has no inheritance).  Replace with
  a diagram showing the three reuse primitives (interface / mixin / composition)
  side-by-side.  Tracked as Phase B follow-up.
- **Old diagram:** `10-class-hierarchy.svg` (now stale)

---

## Part 3: Advanced Features

### Chapter 11: Nil Tracking and Safety
- **Location:** In "### Type Narrowing" section, before code examples
- **Diagram:** `04-type-narrowing.svg`
- **Purpose:** Nil check flow, type narrowing before/after, compile-time guarantees

### Chapter 12: Error Handling with Results
- **Location:** In "## Error Propagation" section, before code examples
- **Diagram:** `05-error-propagation.svg`
- **Purpose:** How errors propagate through Result types, success vs error paths

### Chapter 13: Generics and Type Constraints
- **Location:** After "## Generic Classes", before "### Simple Class" code
- **Diagram:** `06-generics-instantiation.svg`
- **Purpose:** Generic template instantiation, type parameter substitution, concrete type creation

### Chapter 15: Pipelines and Function Composition
- **Location:** After "## Basic Pipeline Syntax", before code examples
- **Diagram:** `07-pipeline-flow.svg`
- **Purpose:** Data flow through pipelines, nested vs pipeline readability, step-by-step execution

---

## Part 4: Practical Projects

### Chapter 16: Project 1 - CLI Tool
- **Location:** After "## Project Overview", before "## Step 1"
- **Diagram:** `08-project1-modules.svg`
- **Purpose:** Module architecture and dependencies (cli_args, file_processor, pattern_search, main)

### Chapter 17-18: Project 2 - HTTP Server
- **Location:** After learning outcomes, before "### Step 1: HTTP Request/Response Types"
- **Diagram:** `09-http-cycle.svg`
- **Purpose:** HTTP request/response cycle, router dispatch, handler processing, client-server flow

### Chapter 17-18: Project 3 - Text Data Analysis
- **Location:** After learning outcomes, before "### Step 1: Frequency Analysis"
- **Diagram:** `11-analysis-pipeline.svg`
- **Purpose:** Data analysis pipeline steps, frequency analysis, n-grams, similarity metrics

---

## Diagram Statistics

| Metric | Count |
|--------|-------|
| Total diagrams | 13 |
| Embedded in chapters | 13 |
| Coverage | 100% |

### By Topic
- Fundamentals: 4 diagrams
- OOP: 2 diagrams
- Advanced Features: 4 diagrams
- Projects: 3 diagrams

### By Content Type
- Type system: 3 diagrams (types, collections, generics)
- Control flow & scope: 3 diagrams (scope, type narrowing, error propagation)
- Data structures: 1 diagram (Unicode)
- Classes & inheritance: 2 diagrams (class structure, hierarchy)
- Operators & composition: 1 diagram (pipelines)
- Architecture & design: 3 diagrams (3 projects)

---

## Visual Consistency

All diagrams use a unified design system:

### Color Scheme
- **Blue (#0284c7):** Primary/main elements, data structures
- **Green (#16a34a):** Output, success states, instance data
- **Purple (#4f46e5):** Processing steps, methods
- **Amber (#d97706):** Warnings, special cases, notes
- **Red (#dc2626):** Base/parent elements, errors

### Typography
- **Sans-serif (Arial):** Labels, titles
- **Monospace (Monaco):** Code, keywords, example data

### Accessibility
- High contrast text on backgrounds
- Clear labels on all elements
- Descriptive captions
- No pure decorative elements

---

## Usage in Rendered Output

### HTML/Web
SVGs render natively in modern browsers:
```html
<img src="diagrams/01-type-hierarchy.svg" alt="Type Hierarchy">
```

### PDF
SVGs convert cleanly to PDF when rendering with Pandoc or similar tools:
```bash
pandoc chapter.md -o chapter.pdf --include-in-header style.css
```

### Markdown Preview
GitHub, GitLab, and most markdown viewers display SVGs inline.

### Print
SVGs are vector-based and print at any resolution without pixelation.

---

## Maintaining Diagrams

If you need to update diagrams:

1. **Edit SVGs** — Open in Inkscape, Adobe Illustrator, or text editor
2. **Keep color scheme** — Maintain consistent palette across all diagrams
3. **Update DIAGRAMS_EMBEDDED.md** — Document any location changes
4. **Test rendering** — Verify in browser, PDF, and print preview
5. **Verify consistency** — Ensure style matches other diagrams

---

## Future Enhancements

Diagrams that could be added:

- Memory layout with garbage collection
- Concurrency model (if added to Zebra)
- Performance characteristics charts
- More detailed module dependency graphs
- Common error patterns flow charts
- Compile-time vs runtime behavior comparison

---

**Last Updated:** April 7, 2026  
**Status:** Complete and embedded  
**Format:** SVG (Scalable Vector Graphics)

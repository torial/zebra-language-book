# The Zebra Programming Language

A guide to Zebra from fundamentals through advanced patterns, for experienced
programmers learning a new language.

Zebra is a statically-typed, compiled language with Python-flavoured syntax
(by way of Cobra). It compiles to Zig, and from there to native code. The
language and compiler live at
[github.com/torial/zebra-language](https://github.com/torial/zebra-language);
this book's source is at
[github.com/torial/zebra-language-book](https://github.com/torial/zebra-language-book).

## How the book is organised

| Part | What it covers |
|---|---|
| **Part 1: Foundations** | Installing the toolchain, values and types, collections, functions, control flow, strings. |
| **Part 2: Objects and Interfaces** | Classes, structs and unions, interfaces, composition and mixins, properties, modules. |
| **Part 3: Advanced Features** | Nil tracking, `Result`-based error handling, generics, contracts, memory and lifetimes, concurrency, pipelines. |
| **Part 4: Practical Projects** | Three worked projects (a CLI tool, an HTTP server, a text-analysis tool) plus GUI applications. |
| **Part 5: Ecosystem** | Standard library tour, file I/O, regular expressions, FFI, the build system, testing. |
| **Appendices** | Grammar, standard library, troubleshooting, and attribute references. |
| **Quick References** | A 30-minute quickstart, a one-page syntax cheat sheet, and copy-paste patterns for common tasks. |

## Where to start

- **New to Zebra?** Start with [01: Getting Started](Part-1-Foundations/01-Getting-Started.md)
  and read Part 1 in order.
- **In a hurry?** Read the [30-Minute Quickstart](reference/quickstart.md), then keep the
  [Syntax Cheat Sheet](reference/cheatsheet.md) open while you work.
- **Coming from an OOP language?** Chapters 07–10b, then 11 and 12.
- **Interested in safety features?** Chapters 11 (nil tracking), 12 (results), 14 (contracts), 14b (lifetimes).

Use the sidebar (or the `←` / `→` keys) to move between chapters, and the search icon
(or `S`) to search the whole book.

## Status

The chapters are re-verified against the current Zebra compiler on a rolling basis;
`validate-examples.py` in the repository is the source of truth for which code examples
compile. Found a mistake? See
[CONTRIBUTING.md](https://github.com/torial/zebra-language-book/blob/main/CONTRIBUTING.md).

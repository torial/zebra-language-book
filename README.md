# The Zebra Programming Language Book

A comprehensive guide to Zebra from fundamentals through advanced patterns. Written for experienced programmers learning a new language.

## Quick Start

```bash
# Read the master outline and choose your path
cat _outline.md

# Build and validate all examples compile
make build

# Generate HTML
make html

# Generate PDF
make pdf
```

## About This Book

**Audience:** Experienced programmers (you know loops, functions, types)  
**Scope:** Intro to intermediate Zebra  
**Length:** ~400-500 pages (when printed)  
**Time:** 40-60 hours active learning (chapters + exercises + projects)

### Three Teaching Styles Blended In

1. **Head First** — Visual, intuitive, "aha!" moments
2. **Problem-First** — Solve real problems, learn the tools you need
3. **Practical** — Apply it immediately in working code

Each chapter uses all three approaches, so you get intuition, understanding, and hands-on skill.

## Structure

- **Part 1: Foundations** — Values, types, functions, control flow, strings
- **Part 2: Objects & Interfaces** — Classes, inheritance, mixins, protocols
- **Part 3: Advanced Features** — Nil tracking, Results, generics, contracts, pipes
- **Part 4: Practical Projects** — Build real tools: CLI, HTTP server, data analysis
- **Part 5: Ecosystem** — Standard library, I/O, regex, FFI
- **Appendices** — Reference, troubleshooting, grammar

## Reading Paths

### "I want to learn Zebra end-to-end"
Part 1 → Part 2 → Part 3 → Part 5 → Part 4 projects

### "I want to build a server quickly"
01-Getting-Started → 02-Values → 03-Collections → 04-Functions → 05-Control-Flow → 07-Classes → 11-Nil-Tracking → 12-Error-Handling → 20-File-IO → Project-2-HTTP-Server

### "I want to understand Zebra's safety features"
02-Values → 11-Nil-Tracking → 12-Error-Handling → 14-Contracts → 09-Generics

### "I'm coming from Python"
Each chapter has "If you know Python" sidebars showing equivalents

## What You'll Build

By the end of this book, you'll have:
- ✅ Solid understanding of Zebra fundamentals
- ✅ Three real projects (CLI tool, HTTP server, data analysis)
- ✅ Knowledge of Zebra's unique safety features
- ✅ Ability to write idiomatic Zebra code
- ✅ Understanding of when to use advanced features

## Examples

All examples are:
- ✅ **Runnable** — You can `zebra run examples/<chapter>_<name>.zbr`
- ✅ **Validated** — Part of the build system (if they don't compile, the book fails to build)
- ✅ **Progressive** — Start simple, get more complex
- ✅ **With Solutions** — Exercises include solutions

## Living Document

This book is a living document. It will:
- Update with new Zebra features
- Improve based on reader feedback
- Fix examples when compiler changes
- Add new chapters as the language evolves

**Zig 0.16+ breaking changes?** We'll update the book.

## Contributing

Found an error? Want to suggest a better example? See `CONTRIBUTING.md`.

## Credits

**Book Content & Examples:** Claude Haiku 4.5 (prior session)
- All 22 chapters, appendices, and 180+ code examples
- Architecture and curriculum design
- Real-world project walkthroughs

**Diagrams:** 13 SVG illustrations  
**Build System & Infrastructure:** Claude Haiku 4.5 (current session)
- PDF generation pipeline (Pandoc + MiKTeX + xelatex)
- SVG to PNG conversion at 300 DPI
- Environment variable management
- Build automation and path fixing

**Project Coordination:** Sean McKay

---

**Last Updated:** 2026-04-07  
**For Zebra:** Latest (zig_backend branch)  
**Status:** Complete first draft ready for iteration

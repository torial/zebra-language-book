# Diagram audit, 2026-09-21

Thirteen SVGs under `book/diagrams/`, checked against the language as it is (zebra-language
`f596eba`: QUICKSTART, SURFACE.md, CHANGELOG, the test corpus), every `<text>` element read;
disputed snippets were RUN through the compiler (marked **[ran]**). Done by a subagent at
Sean's request, relayed and checked by Fable 5.1. Nothing here is fixed yet; this is the
worklist.

## Cross-cutting (every embedded diagram)

1. The chapters embed `../diagrams/NN-name.png`; the PNGs exist locally (generated from the
   SVGs by `convert-svg-to-png.bat`) but `.gitignore` keeps them out of the repo (`*.png`; the
   `!diagrams/*.png` exception does not match `book/diagrams/`), so the PUBLISHED book shows
   broken images unless the Pages build regenerates them. Check the deployed site; either
   track the PNGs or embed the SVGs (`diagrams/README.md` says to embed the SVGs).
2. `name as Type` annotations in 03, 04, 05, 06, 10, 12 -- the syntax is `: Type`; `as` is a
   binding clause. **[ran]** `def process(name as str)` is a parse error.
3. Paren-less `def name as T` in 06, 10, 12 -- must be `def name(): T`.
4. Bare `print x` in 02, 04, 13 -- `print` is a function. **[ran]** parse error.
5. `Result(T, E)` / `.isOk()` / `.okValue()` / `.isErr()` / `Result.ok()` in 01, 04, 05, 08 --
   the type does not exist; errors are `throws` / `raise` / `expr?` / `catch` (QUICKSTART
   §12). Chapter 12 itself says the Result type was removed.
6. `diagrams/README.md` labels 10 as "Chapter 9: Inheritance"; chapter 9 is Composition and
   Mixins, and Zebra has no class inheritance.

## Per diagram

| Diagram | Embedded in | Verdict | Definite errors |
|---|---|---|---|
| 01-type-hierarchy | ch 02 | wrong: Result box; `int` "value or error"; `int?` "value, nil, or error" | 3 |
| 02-collections-comparison | ch 03 | wrong: `List()`/`HashMap()`/`Set()` need type args **[ran]**; six bare prints. (Diagram is RIGHT that generic `Set` exists; chapter 3 line 16 saying only `StrSet` exists is the stale one.) | 9 |
| 03-scope-and-lifetime | ch 04 | wrong: `as` params; the closure panel (`var closure = capture` + nested def) is not a Zebra form **[ran]**; `capture` copies once, it does not keep the outer variable alive | 3 |
| 04-type-narrowing | ch 11 | wrong: `as`; `print name # ERROR!` -- printing an optional is legal and prints `nil` **[ran]**; Example 2 (`parse_int`, `Result`, `.okValue()`, "narrowed to Ok") does not exist. Chapter-side: the `if input == nil: return` then `input.len` example under the embed does NOT compile **[ran]** (§11: only the `!= nil` shape narrows) | 7 |
| 05-error-propagation | ch 12 | wrong: every line of the code block (`as`, `Result`, `File.read` "returns Result" -- it returns `str`, `parse_json` -- it is `Json.parse`); contradicts the chapter that embeds it | 8 |
| 06-generics-instantiation | ch 13 | minor: `var item as T` / `def get as T` (×3 each) **[ran]** | 6 sites, one class |
| 07-pipeline-flow | ch 15 | wrong: multi-line pipeline without parens **[ran]**; `-> double(.)` placeholder does not exist (it is `-> double()`) **[ran]**; untyped helper defs **[ran]**; "Nested Calls" panel is method chaining; the custom-function panel is truncated and its step panel starts from a different input | 4 |
| 08-project1-modules | ch 16 | minor: "Standard Library: File, CommandLine, Result" -- `CommandLine` is not a namespace (`sys.args()` / `Arg.parse()`), Result does not exist. Module map matches the chapter -- which is itself stale the same way (`CommandLine.args()`, `.isErr()`, `elif`, `def run: bool throws`) | 2 |
| 09-http-cycle | ch 17 | accurate vs the language (no code); does not match the chapter's SIMULATED server (no socket, one fabricated `/health`, array body, no Content-Type). Real Zebra has `Http.serve` -- neither uses it | 0 |
| 10-class-hierarchy | not embedded | wrong in premise: `extends`, `super.speak()`, inherited members, bodiless `def speak as str` -- **[ran]** "Zebra has no class inheritance"; delete or redraw as interface + mixin + composition | whole diagram |
| 11-analysis-pipeline | ch 18 | accurate vs the language; "Cosine … angle between word vectors" describes a formula the chapter calls a simplified ratio (and "range 0 to 1" fails for repeated words); the sample report does not match `print_report` | 0 |
| 12-class-structure | ch 07 | wrong: `shared var` / `shared def` (keyword is `static`) **[ran]**; `as` everywhere; `def check_balance as float`; `next_id` undeclared (should be `next_account_id`); `owner` never assigned yet shown as "Alice"; bare `BankAccount()` needs field defaults. Static-vs-instance semantics and memory panel are right | 11 |
| 13-unicode-representation | ch 06 | wrong: `charAt(0)` shown as `"H"` -- it returns a `byte`, prints `72` **[ran]**, and the diagram's own label says "byte"; bare prints; `var str` shadows the type. Byte counts, hex bytes, code points, `substring` all right; omits `codePointCount()`, the chapter's point | 6 |

## Prioritised fixes

1. Make the images reach readers (cross-cutting #1).
2. Delete or redraw 10-class-hierarchy as interface + mixin + composition; fix README.
3. Redraw 05-error-propagation around `throws` / `raise` / `expr?` / `catch`.
4. Remove Result from 01 and 04; fix 04's "print name # ERROR!".
5. Mechanical syntax sweep across 02/03/04/06/10/12/13 (`as T` -> `: T`, `def f as T` ->
   `def f(): T`, `print x` -> `print(x)`, `shared` -> `static`, typed constructors).
6. 07: parens, `double()`, typed defs, retitle, finish or drop the truncated panel.
7. 13: `charAt` output, `var str` rename, add `codePointCount()`.
8. 12: `next_id`, defaults or `cue init`, set `owner`.
9. 08: the stdlib line; chapter 16 needs the same overhaul.
10. 09 and 11: align with what the chapters' code does, or upgrade the chapters to `Http.serve`.

Chapter-side defects found on the way: chapter 3 line 16 (only `StrSet` exists -- false);
chapter 11's narrowing example under the diagram does not compile; chapter 16 uses the
removed Result API and `CommandLine`; the book validation run of 2026-09-21 shows 22
regressions from recent compiler changes (assert_* freed, closed method tables).

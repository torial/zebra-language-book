# The Zebra Programming Language Book

**Read it online: <https://torial.github.io/zebra-language-book/>**

A guide to Zebra from fundamentals through advanced patterns, for experienced
programmers learning a new language. Twenty-two chapters plus additions
(structs/unions, modules, memory and lifetimes, concurrency, GUI apps, build
tooling, testing) across five parts, plus appendices.

## Chapters

See [`_outline.md`](_outline.md) for the full chapter list, per-chapter topic
summaries, and several suggested reading paths (linear, quick-start, safety-
focused, OOP-focused, data/scripting-focused).

The source lives under `book/Part-1-Foundations/` through
`book/Part-5-Ecosystem/`, plus `book/Part-5-Ecosystem/Appendix-*.md`. The
reading order for the website is `book/SUMMARY.md`; add new chapters there.

## Building

See [`BUILD.md`](BUILD.md) for the full pipeline (extract examples → lint →
validate → HTML → PDF), required tools, and platform notes. Short version:

```bash
make all      # everything
make quick    # extract + validate only, fast sanity check
make serve    # live preview of the website (needs mdbook)
```

The website is built with [mdBook](https://rust-lang.github.io/mdBook/) from
`book.toml` + `book/SUMMARY.md` and deployed to GitHub Pages by
`.github/workflows/pages.yml` on every push to `main`.

## Status

The chapters were re-verified against the current Zebra compiler on
2026-09-09. `validate-examples.py` is the source of truth for which code
examples actually compile — it gates on regression against
`validation-baseline.txt`; run it yourself rather than trusting any
percentage or completion claim in prose (including older status notes in
this repo, which predate this pass and may be stale).

## Contributing

Found an error, or want to suggest a better example? See
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Credits

**Book content & examples:** Claude Haiku 4.5 (prior session) — chapters,
appendices, code examples, curriculum design, project walkthroughs.

**Build system & infrastructure:** Claude Haiku 4.5 (prior session) — PDF and
HTML generation pipeline, example extraction and validation, build
automation.

**Project coordination:** Sean McKay

# 22b: Build System and Tooling

**Audience:** All — required for any multi-file project
**Time:** 120 minutes
**Prerequisites:** 01-Hello-World, 04-Functions-and-Scope
**You'll learn:** The `zebra` compiler's subcommands, the project build system (`zebra build` + `Build` module), the REPL, dead-code analysis, and the DAP debugger

---

## The Big Picture

Up to this point every example has been a **single `.zbr` file** run with
`zebra hello.zbr`. That works for examples and small tools. Real projects need:

- **Multi-file builds** — `src/main.zbr` plus a dozen modules, all compiled into one binary
- **Cross-compilation** — build a Linux binary from your Windows machine
- **Optimization flags** — `Debug` for development, `ReleaseSafe` for ship
- **Library targets** — produce a `.dll` / `.so` for plugin use
- **A REPL** — try a snippet without writing a file
- **A debugger** — set breakpoints, inspect variables
- **Dead-code analysis** — find functions and union arms you forgot to remove

This chapter covers the tooling that turns Zebra from a scripting language
into a project-shaped language.

---

## Compiler Subcommands

`zebra` is a single binary with several subcommands. Run `zebra --help` for
the full list; the everyday ones:

| Command | What it does |
|---|---|
| `zebra file.zbr` | Compile and run a single file |
| `zebra build` | Project build — reads `build.zbr` (see below) |
| `zebra repl` | Launch the interactive REPL |
| `zebra test file.zbr` | Run the test suite in `file.zbr` (see Chapter 22c) |
| `zebra check file.zbr` | Dead-code analysis — unused functions and union arms |
| `zebra debug file.zbr` | Launch under `lldb-dap` for breakpoint debugging |
| `zebra --emit-zig file.zbr` | Emit the generated Zig source instead of compiling |

The default subcommand (no flag) is "compile and run." Almost all your
day-to-day work goes through this or `zebra build`.

---

## Single-File Workflow

For a single file, `zebra` does everything in one step:

```bash
$ zebra hello.zbr
Hello, world!
```

Under the hood the compiler:
1. **Parses** `hello.zbr` into an AST
2. **Resolves** identifiers and types
3. **Type-checks** the program
4. **Emits Zig source** to a temp directory
5. **Invokes `zig build-exe`** on the generated Zig
6. **Runs the resulting binary**

If you want to inspect the intermediate Zig, use `--emit-zig`:

```bash
$ zebra --emit-zig hello.zbr > hello.zig
$ head -20 hello.zig
const std = @import("std");
const _allocator = std.heap.page_allocator;
...
```

Or `--output-dir DIR` to keep the generated files in a project directory:

```bash
$ zebra --output-dir build/ hello.zbr
# generates build/hello.zig + build/zig-out/bin/hello[.exe]
```

The output directory becomes a normal Zig project — useful if you want to
hand-tune the build or audit what got generated.

---

## The REPL

Launch with `zebra repl`. Enter Zebra statements one at a time:

```
$ zebra repl
Zebra REPL 0.15 — type :help for commands
>>> var x = 10 + 5
>>> print x
15
>>> def double(n: int): int
...     return n * 2
>>> double(x)
30
```

The REPL uses an **accumulation model** — each input is appended to a
running session, recompiled, and re-run. Redefining a function or variable
runs the redefined version, but doesn't remove the old line from history.
Use `:clear` to start over.

### REPL commands

All REPL commands begin with `:`.

| Command | Action |
|---|---|
| `:help` | List all REPL commands |
| `:clear` | Reset the accumulated session — start fresh |
| `:history` | Print everything entered so far |
| `:load <file>` | Read a `.zbr` file into the REPL environment |
| `:save <file>` | Save the current session to a file |
| `:exit` (or Ctrl-D) | Quit |

### Multi-line input

When a line ends with an indent-starting construct (like `def`, `class`,
`if`, `while`), the REPL switches to multi-line mode and shows `...`:

```
>>> def factorial(n: int): int
...     if n <= 1
...         return 1
...     return n * factorial(n - 1)
...
>>> factorial(6)
720
```

End the block with a blank line, or with a dedented line that completes
the parse.

### When the REPL helps

The REPL is great for:
- Trying syntax you're not sure about ("does this expression parse?")
- Exploring a module's API interactively
- Quick math or one-off computations
- Demonstrating language features to others

It's not a replacement for `.zbr` files for real work. There's no
incremental compilation yet — each new input recompiles the entire
accumulated session. Long sessions get slow.

---

## Project Builds: `zebra build`

For anything bigger than a single file, write a `build.zbr` file in your
project root and run `zebra build`. The `build.zbr` file is a regular
Zebra program; its `main()` function declares the build targets.

```zebra
# file: build.zbr
# A minimal build script

def main()
    var b = Build.new()
    b.exe("myapp", "src/main.zbr")
```

That's the whole build script. Run it from the project root:

```bash
$ zebra build
# compiles src/main.zbr → zig-out/bin/myapp[.exe]
```

The `Build` module is **built-in** — no `use` import is needed.

### Why a Zebra file for builds?

Many languages use a custom DSL (Make, CMake, package.json) for builds. Zig
uses Zig itself for `build.zig`. Zebra follows Zig's lead: your `build.zbr`
is real Zebra, so you can compute target names, loop over files, and call
helper functions — anything you'd do in a regular program.

---

## The Build Module API

The `Build.new()` call returns a build context. Add targets with `b.exe()`
and `b.lib()`. Each target supports method chaining:

```zebra
# file: build.zbr
# teaches: imperative-style build script
# chapter: 22b-Build-System-and-Tooling

def main()
    var b = Build.new()

    # exe(name, entry_source) → BuildTarget
    var app = b.exe("myapp", "src/main.zbr")
    app.platform("x86_64-linux")       # cross-compilation target
    app.option("optimize", "Debug")    # passed through to zig build-exe

    # lib(name, entry_source) → BuildTarget (stub for now)
    var support = b.lib("support", "src/support.zbr")

    # linkLib records a dependency edge
    app.linkLib(support)

    # b.run() — compile all exe targets
    b.run()
```

### BuildTarget chain methods

All chain methods return the target, so you can fluently chain:

```zebra
b.exe("app", "src/main.zbr")
    .platform("aarch64-linux")
    .option("optimize", "ReleaseSafe")
```

| Method | Effect |
|---|---|
| `b.exe(name, entry)` | Add an executable target |
| `b.lib(name, entry)` | Add a library target (stub — prints a placeholder message at build time) |
| `b.run()` | Compile all registered exe targets |
| `target.platform(str)` | Set a cross-compilation triple (e.g. `"aarch64-linux"`, `"x86_64-windows"`) |
| `target.option(key, val)` | Pass a key/value through to `zig build-exe` |
| `target.linkLib(other)` | Record a dependency on another target |
| `b.dependency(name, ver)` | Reserve a package-manager dependency (post-1.0 stub) |

### How `b.run()` works

For each `exe` target, `b.run()`:
1. Runs `zebra --emit-zig <entry>` to produce a `.zig` source file
2. Runs `zig build-exe <zig_file> -femit-bin=zig-out/bin/<name>`
3. Threads `platform`/`option` arguments through to step 2

`lib` and `test_` targets are stubs — they print a "not yet implemented"
message. Library output is on the post-1.0 roadmap.

### `b.dependency()` — package manager stub

```zebra
b.dependency("some-pkg", "0.1.0")
```

This is a no-op today. It records the request so a future package manager
can read it from your `build.zbr`. Including it now keeps your scripts
future-compatible.

---

## Declarative Style (Recommended)

Omit the `b.run()` call entirely. `zebra build` automatically calls it
after `main()` returns:

```zebra
# file: build.zbr
# teaches: declarative-style build script
# chapter: 22b-Build-System-and-Tooling

def main()
    var b = Build.new()
    b.exe("myapp", "src/main.zbr").option("optimize", "ReleaseSafe")
    # no b.run() needed — zebra build calls it automatically
```

The auto-run is a no-op if you also called `b.run()` explicitly, so both
styles work. **Prefer declarative** — it matches Zig's `build.zig`
convention and reads more like a manifest.

---

## Compiler Flags

These flags apply to `zebra file.zbr` (the single-file form). The
project-build equivalent goes through `target.option(key, val)`.

| Flag | Effect |
|---|---|
| `--emit-zig` | Write generated Zig source to stdout instead of compiling |
| `--output-dir DIR` | Write generated Zig files to `DIR/` (project-style output) |
| `--turbo` | Strip all contract checks (`require`/`ensure`/`invariant`) — see Ch14 |
| `--cpu=VALUE` | Pass `-mcpu=VALUE` to Zig (e.g. `native`, `x86_64+avx2`) |
| `--gui-backend=libui_ng` | Use native OS controls (Win32/GTK3/Cocoa) |
| `--gui-backend=tui` | Use the ZigZag terminal-UI backend |
| `--gui-backend=glfw` | Use Dear ImGui (OpenGL + GLFW) |
| `--zig-backend file.zbr` | Delegate to `zebra-bootstrap.exe` (Zig-implemented compiler) |
| `--listen PORT` | Debug mode: expose DAP on `PORT` instead of launching the IDE |

`--turbo` and `--gui-backend` are the two you'll touch most often. `--cpu`
matters for SIMD (Chapter 19 covers SIMD vector types).

---

## Dead-Code Analysis: `zebra check`

`zebra check file.zbr` walks your module graph and reports:

- **Unused union arms** — variants that no `branch` ever matches
- **Unreachable functions** — top-level `def` declarations never called

```bash
$ zebra check src/codegen.zbr
warning: union arm 'Type_.str_slice' never matched
warning: def 'genDebugPrint' never called
```

Output is one warning per line on stdout. Exit code is `0` whether or not
warnings were emitted — `zebra check` is informational, not a gate.

**Use it before refactors.** Dead code can hide subtle bugs (a function
you thought was being called isn't) and bloats the binary. Running
`zebra check` over your module catches both.

**Limitations:**
- Doesn't detect unused class methods (only top-level `def`)
- Doesn't detect unused fields
- Doesn't detect unused parameters

Future versions may extend coverage.

---

## Debugging: `zebra debug`

`zebra debug file.zbr` compiles the program and launches it under
`lldb-dap`, exposing the Debug Adapter Protocol on a local socket. IDE
clients connect to the socket for:

- **Breakpoints** at any `.zbr` source line
- **Stepping** (step over / into / out)
- **Variable inspection** at the current frame
- **Stack traces** with proper `.zbr` file:line mapping

The compiler emits `// zbr:file:line` markers in the generated Zig, so the
DAP proxy translates lldb-dap's `.zig` locations back to your `.zbr` source
automatically.

### IDE setup

VS Code: install the [LLDB-DAP extension] and add to `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [{
        "type": "zebra",
        "request": "launch",
        "name": "Debug",
        "program": "${workspaceFolder}/src/main.zbr"
    }]
}
```

ZebraIDE has a **Debug** button in the toolbar that wires this up
automatically — see `docs/DEBUGGING.md` for full details.

### Standalone DAP

If you want to connect from a custom tool, run:

```bash
zebra debug --listen 4711 src/main.zbr
# Waits for a DAP client to connect to localhost:4711
```

The compiler will block until the connection arrives, then forward DAP
messages between your client and lldb-dap.

### Prerequisites

You need `lldb-dap` installed and on `PATH`. On Windows, the LLVM installer
includes it. The compiler emits a clear error message if it can't find it.

---

## Real World: A Multi-Module Project

Here's a realistic project layout for a CLI tool that uses three modules:

```
my-tool/
├── build.zbr                  # build script
├── src/
│   ├── main.zbr               # entry point
│   ├── cli.zbr                # argument parsing
│   └── work.zbr               # core logic
└── test/
    └── work_test.zbr          # tests for work.zbr
```

### `src/main.zbr`

```zebra
use cli
use work

def main()
    var opts = cli.parse_args(sys.args())
    work.run(opts)
```

### `src/cli.zbr`

```zebra
class Options
    var verbose: bool = false
    var input_path: str = ""

def parse_args(args: List(str)): Options
    var opts = Options()
    # ... parse args ...
    return opts
```

### `src/work.zbr`

```zebra
use cli

def run(opts: cli.Options)
    if opts.verbose
        print("Processing ${opts.input_path}")
    # ... do work ...
```

### `build.zbr`

```zebra
def main()
    var b = Build.new()
    b.exe("my-tool", "src/main.zbr").option("optimize", "ReleaseSafe")
```

Run it:

```bash
$ zebra build
$ zig-out/bin/my-tool --verbose somefile.txt
Processing somefile.txt
```

The compiler resolves `use cli` by looking for `cli.zbr` next to the
importing file — `src/cli.zbr` is found relative to `src/main.zbr`.

### Adding a debug target

For a side-by-side debug build, register two exe targets:

```zebra
def main()
    var b = Build.new()
    b.exe("my-tool",       "src/main.zbr").option("optimize", "ReleaseSafe")
    b.exe("my-tool-debug", "src/main.zbr").option("optimize", "Debug")
```

`zebra build` produces both binaries. Use the debug one with
`zebra debug src/main.zbr` for breakpoint sessions.

---

## Common Mistakes

> ❌ **Mistake:** Forgetting that `Build` is built-in
>
> ```zebra
> use Build   # Wrong — Build is not a user module
>
> def main()
>     var b = Build.new()
> ```
>
> ✅ **Better:**
> ```zebra
> def main()
>     var b = Build.new()   # Build is built-in; no use needed
> ```

> ❌ **Mistake:** Calling `b.run()` AND relying on auto-run
>
> Both work, but mixing styles makes scripts confusing for readers.
> Pick one: declarative (no `b.run()`) or imperative (explicit `b.run()`).

> ❌ **Mistake:** Using `b.lib()` and expecting an actual `.so` / `.dll`
>
> The `lib` target is a stub. Use `@export class` + `zebra --shared file.zbr`
> for the DynLib plugin path (see Chapter 22 / FFI). `b.lib()` exists to
> reserve the API shape.

> ❌ **Mistake:** Running `zebra repl` for production-shaped work
>
> The REPL recompiles the accumulated session on every input. After ~50
> statements it gets slow. For exploratory work that turns into "I'm
> building something," promote to a `.zbr` file and run with `zebra`.

---

## Exercises

### Exercise 1: Two-Target Build

Write a `build.zbr` that produces both a debug and a release build of the
same source file under different binary names.

<details>
<summary>Solution</summary>

```zebra
def main()
    var b = Build.new()
    b.exe("app-debug",   "src/main.zbr").option("optimize", "Debug")
    b.exe("app-release", "src/main.zbr").option("optimize", "ReleaseSafe")
```

</details>

### Exercise 2: Cross-Compilation

Modify Exercise 1 so the release build targets `aarch64-linux` instead of
the host platform.

<details>
<summary>Solution</summary>

```zebra
def main()
    var b = Build.new()
    b.exe("app-debug",   "src/main.zbr").option("optimize", "Debug")
    b.exe("app-release", "src/main.zbr")
        .option("optimize", "ReleaseSafe")
        .platform("aarch64-linux")
```

</details>

### Exercise 3: REPL Workflow

Open `zebra repl` and do the following without writing any `.zbr` file:

1. Define `fib(n: int): int` that returns the n-th Fibonacci number
2. Call it with `n = 10` and print the result
3. Save your session to `fib_session.zbr`
4. Open the saved file and check that running it as `zebra fib_session.zbr` produces the same output

This exercise has no programmatic solution — its goal is to build muscle
memory for the REPL's accumulate-and-save loop. Try it.

---

## Next Steps

- → **22c-Testing-and-Validation** — write tests for your build targets
- → **10b-Modules-Namespaces-and-Visibility** — structure a multi-file project
- → **22-FFI-and-Interop** — produce shared libraries with `@export class`

---

## Key Takeaways

- **`zebra file.zbr`** runs a single file end-to-end; everything else builds on this
- **`zebra build`** reads `build.zbr` (a regular Zebra program) and produces project binaries
- **The `Build` module is built-in** — no `use` import; `Build.new()` returns a context, `b.exe(name, entry)` adds targets
- **Declarative style is recommended** — drop `b.run()` and let `zebra build` auto-invoke it
- **`zebra repl`** is for exploration, not production work; use `:save` to promote a session to a file
- **`zebra check`** finds dead union arms and unreachable functions — run it before refactors
- **`zebra debug`** launches under `lldb-dap` for breakpoint debugging with proper `.zbr` source mapping
- **`--turbo` strips contract checks** for release builds; `--gui-backend` selects the GUI renderer; `--cpu` enables SIMD targets

---

**Next:** Chapter 22c covers testing — how to write, run, and organize tests with the `Test` stdlib module and `zebra test` subcommand.

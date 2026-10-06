# Chapter 22: FFI and Interop

**Time:** 90 min | **Audience:** Advanced | **Prerequisites:** Chapters 02, 07, 12

---

## Learning Outcomes

After this chapter, you will:
- Understand Foreign Function Interface (FFI) concepts
- Call C functions — from the C library, your own `.c` files, and prebuilt libraries
- Call Zig code directly
- Marshal numbers, strings and pointers between Zebra and C
- Turn C-style error codes into Zebra errors
- Build Zebra plugins that other programs load at runtime
- Know the performance and safety tradeoffs

---

## Overview: Calling External Code

Not all code is Zebra. Sometimes you need to call:
- **C libraries** — system libraries, legacy code, performance-critical code
- **Zig code** — for optimal control or performance
- **Platform APIs** — Windows, Linux, macOS system functions

FFI (Foreign Function Interface) lets you call these from Zebra. Every route goes through
one of two pieces of syntax: **`extern def`**, which declares a function that lives
outside Zebra, and **`use`**, which finds the file that supplies it and builds it into
your program. There is no build script and no linker flag to write — one `zebra` command
compiles the C, links the library and runs the result.

| What you have | What you write |
|---|---|
| a function in the C standard library | `extern def` |
| a `.c` file | `use name` + `extern def` for each function |
| a `.c` file **with a `.h`** | `use name`, then call `name.function(...)` |
| a prebuilt `.lib` / `.a` / `.so` | `use name` + `extern def` |
| a `.zig` file | `use name`, then call `name.function(...)` |
| a Zebra library to load at runtime | `DynLib` (end of chapter) |

The supporting `.c`, `.h` and `.zig` files shown below sit beside the examples in
`examples/22-ffi-and-interop/`, so every program here runs as written.

---

## Calling C Functions

### C Standard Library Functions

The simplest case: a function the C library already provides.

```zebra
# file: ffi-c-simple.zbr
# teaches: calling C standard library functions with extern def
# chapter: 22

# Declarations only: no body, and the C name IS the Zebra name.
# The C library is always linked, so these need nothing else.
extern def sqrt(x: float64): float64
extern def pow(base: float64, exponent: float64): float64
extern def abs(n: int32): int32

def main()
    print(sqrt(16.0))        # 4.0
    print(pow(2.0, 8.0))     # 256.0
    print(abs(0 - 42))       # 42
```

Output:

```text
4.0
256.0
42
```

`extern def` has no body. The compiler emits a plain Zig `extern fn` and calls it
directly — there is no wrapper or marshaling layer between your call and the C function.

### Your Own C File

Put a `.c` file beside your program and `use` it by name. The compiler finds
`temperature.c`, hands it to `zig` to compile, and links the result:

```c
/* temperature.c -- no header, so the Zebra side declares each function */

double celsius_to_fahrenheit(double c) {
    return c * 9.0 / 5.0 + 32.0;
}

int clamp_int(int value, int lo, int hi) {
    if (value < lo) return lo;
    if (value > hi) return hi;
    return value;
}
```

```zebra
# file: ffi-c-source.zbr
# teaches: compiling and calling your own C file
# chapter: 22

# Finds temperature.c beside this file, compiles it with zig, and links it.
use temperature

extern def celsius_to_fahrenheit(c: float64): float64
extern def clamp_int(value: int32, lo: int32, hi: int32): int32

def main()
    print(celsius_to_fahrenheit(100.0))   # 212.0
    print(celsius_to_fahrenheit(-40.0))   # -40.0
    print(clamp_int(150, 0, 100))         # 100
    print(clamp_int(0 - 5, 0, 100))       # 0
```

Output:

```text
212.0
-40.0
100
0
```

### With a Header: No Declarations Needed

If the C file has a matching `.h`, the compiler imports the header instead, and its
functions are reached **through the module name** — no `extern def` lines at all:

```c
/* geometry.h -- the header makes `use geometry` import these declarations */
#pragma once

double hypotenuse(double a, double b);
long long area_of_rect(long long w, long long h);
```

```c
/* geometry.c -- compiled and linked by `use geometry` */
#include <math.h>
#include "geometry.h"

double hypotenuse(double a, double b) {
    return sqrt(a * a + b * b);
}

long long area_of_rect(long long w, long long h) {
    return w * h;
}
```

```zebra
# file: ffi-c-header.zbr
# teaches: a C file with a header -- no extern def needed
# chapter: 22

use geometry

def main()
    # The header's declarations are reached through the module name
    print(geometry.hypotenuse(3.0, 4.0))     # 5.0
    print(geometry.area_of_rect(6, 7))       # 42
```

Output:

```text
5.0
42
```

The header route reads the C types from the header itself, so `long long` arrives as
Zebra's 64-bit `int` and `double` as `float`. The `extern def` route trusts *your*
declaration instead — which is why the next section matters.

---

## The ABI Rule: Use Sized Types

**Zebra's `int` is 64-bit; C's `int` is 32-bit.** If those were allowed to meet, a call
would link cleanly and then read half of its answer from the wrong place — a green build
and a wrong program. So `extern def` refuses the ambiguous types and asks which one you
meant. Declaring `extern def abs(n: int): int` gives:

```text
`int` is ambiguous in an `extern` signature (return type of `abs`): Zebra's `int` is 64-bit, C's `int` is 32-bit. Write `int32` for C `int`, or `int64` for C `long long`/`int64_t`.
```

Use the explicitly sized types, which map straight onto the C ones:

| C | Zebra |
|---|---|
| `int` | `int32` |
| `long long` / `int64_t` | `int64` |
| `unsigned int` / `uint32_t` | `uint32` |
| `unsigned char` | `uint8` |
| `float` / `double` | `float32` / `float64` |
| `char *` / `void *` / any pointer | `^byte` |

`str` is refused the same way, because a Zebra `str` is a slice — a pointer **and** a
length — and C has no such type. Declaring `extern def strlen(s: str): uint64` gives:

```text
`str` is not a C-ABI type in an `extern` signature (parameter `s` of `strlen`): Zebra's `str` is a slice (pointer + length) and C has no such type. Write `^byte` for a C `char*`, then `zig"std.mem.span(...)"` to read it back as a str.
```

---

## Strings: `^byte`

A C function that takes or returns a `char *` is declared with `^byte`. Converting
between `^byte` and `str` takes one line of Zig each, through the `zig"…"` escape hatch
(an expression written in Zig, whose value comes back into Zebra). Copy these two helpers
into any program that talks to C strings:

```c
/* textlib.c -- C functions that take and return C strings (char*) */

/* Count the vowels in a NUL-terminated string. */
int count_vowels(const char *s) {
    int n = 0;
    for (; *s; s++) {
        char c = *s;
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') n++;
    }
    return n;
}

/* Return a pointer to a static, NUL-terminated string. C owns it. */
const char *library_name(void) {
    return "textlib 1.0";
}
```

```zebra
# file: ffi-c-strings.zbr
# teaches: passing strings to and from C with ^byte
# chapter: 22

use textlib

extern def count_vowels(s: ^byte): int32
extern def library_name(): ^byte

# str -> char*. A Zebra str has a length but no terminator, so append a
# NUL byte (${0:c}), then hand C a pointer to the first byte.
def to_c_string(s: str): ^byte
    var z = s + "${0:c}"
    return zig"@ptrCast(@constCast(z.ptr))"

# char* -> str. Measures up to the NUL; the bytes still belong to C.
def from_c_string(p: ^byte): str
    return zig"std.mem.span(@as([*:0]const u8, @ptrCast(p)))"

def main()
    print(count_vowels(to_c_string("programming language")))   # 7
    print(from_c_string(library_name()))                       # textlib 1.0
```

Output:

```text
7
textlib 1.0
```

Two ownership facts sit behind those helpers:

- **`to_c_string` makes a copy** with the terminator on the end. The copy lives as long
  as the rest of your program's strings, so C may read it during the call; C must not
  free it, and should not keep the pointer for later.
- **`from_c_string` does not copy.** The resulting `str` points at C's bytes. That is
  right for a static string like `library_name()`'s; if C hands you a buffer it will
  reuse or free, copy it into a Zebra string first — concatenation always builds a new
  string, so `from_c_string(p) + ""` is enough.

### Bytes With a Length

Many C APIs take a pointer **and** a length instead of a terminated string. Then no copy
is needed — a `str` already *is* a pointer and a length. This is a real CRC-32 in C,
wrapped so Zebra callers never see a pointer:

```c
/* checksum.c -- a small C library: CRC-32 (the zlib/PNG polynomial) */

/* The checksum of `len` bytes at `data`. The bytes need no terminator. */
unsigned int crc32_bytes(const unsigned char *data, long long len) {
    unsigned int crc = 0xFFFFFFFFu;
    for (long long i = 0; i < len; i++) {
        crc ^= data[i];
        for (int k = 0; k < 8; k++)
            crc = (crc >> 1) ^ (0xEDB88320u & (0u - (crc & 1u)));
    }
    return ~crc;
}
```

```zebra
# file: ffi-checksum.zbr
# teaches: wrapping a C library function behind a Zebra function
# chapter: 22

use checksum

extern def crc32_bytes(data: ^byte, len: int64): uint32

# The Zebra-facing API: takes a str, hides the pointer and the length
def crc32(text: str): uint32
    var data: ^byte = zig"@ptrCast(@constCast(text.ptr))"
    return crc32_bytes(data, text.len)

def main()
    var msg = "The quick brown fox jumps over the lazy dog"
    print("${crc32(msg):08x}")    # 414fa339
    print("${crc32(""):08x}")     # 00000000

    # A changed byte changes the checksum
    if crc32(msg) != crc32(msg.replace("dog", "cog"))
        print("tampering detected")
```

Output:

```text
414fa339
00000000
tampering detected
```

(`414fa339` is the standard CRC-32 of that sentence, so the C code, the call and the
string all line up.) The length is declared `int64` / `long long` on purpose, so that
`text.len`, a Zebra `int`, passes straight through.

> **Current limitation:** passing an `int` where an `extern def` declares `uint64` passes
> `zebra -c` but fails to build ("expected type 'u64', found 'i64'"). Declare lengths as
> `int64` on both sides, as here.

---

## Pointers and Ownership: Opaque Handles

When C keeps state between calls, the usual C answer is an **opaque handle**: C allocates
a struct, gives you a pointer, and you pass that pointer back to every function. Zebra
carries it as a `^byte` and never looks inside:

```c
/* stats.c -- an opaque handle: C allocates the object, C frees it */
#include <stdlib.h>

typedef struct {
    long long count;
    double sum;
    double min;
    double max;
} Stats;

Stats *stats_new(void) {
    Stats *s = malloc(sizeof(Stats));
    if (s) { s->count = 0; s->sum = 0.0; s->min = 0.0; s->max = 0.0; }
    return s;
}

void stats_add(Stats *s, double x) {
    if (s->count == 0 || x < s->min) s->min = x;
    if (s->count == 0 || x > s->max) s->max = x;
    s->count++;
    s->sum += x;
}

long long stats_count(const Stats *s) { return s->count; }
double stats_mean(const Stats *s) { return s->count ? s->sum / s->count : 0.0; }
double stats_max(const Stats *s) { return s->max; }

void stats_free(Stats *s) { free(s); }
```

```zebra
# file: ffi-c-handles.zbr
# teaches: opaque C handles and who frees them
# chapter: 22

use stats

# Zebra never looks inside a Stats; it only carries the pointer around.
extern def stats_new(): ^byte
extern def stats_add(s: ^byte, x: float64)
extern def stats_count(s: ^byte): int64
extern def stats_mean(s: ^byte): float64
extern def stats_max(s: ^byte): float64
extern def stats_free(s: ^byte)

def main()
    var s = stats_new()            # C allocates...

    for reading in [12.5, 9.0, 17.25, 11.0]
        stats_add(s, reading)

    print("count: ${stats_count(s)}")   # count: 4
    print("mean:  ${stats_mean(s)}")    # mean:  12.4375
    print("max:   ${stats_max(s)}")     # max:   17.25

    stats_free(s)                  # ...so C frees. s is dangling from here on.
```

Output:

```text
count: 4
mean:  12.4375
max:   17.25
```

The rules that keep this safe are the ones you would follow in C:

- **Whoever allocates, frees.** `stats_new` allocates with `malloc`, so `stats_free`
  frees with `free`. Zebra's memory management never touches the struct.
- **One free, and nothing after it.** Zebra cannot tell that `s` is dangling after
  `stats_free(s)`; calling `stats_add(s, ...)` there is undefined behaviour, exactly as
  in C.
- **A handle is not checked.** Passing a pointer from one library to another library's
  function compiles fine. Keep each kind of handle inside a small Zebra wrapper class if
  you pass them around a large program.

---

## Error Handling Across Boundaries

### Return Code Patterns

C functions don't raise errors; they return codes. Wrap the call in a `throws` function
that turns the codes into errors, and the rest of your program never sees the C
convention:

```c
/* portparse.c -- C-style error reporting: the return value is the status */

/* Parse a decimal TCP port.
 * Returns the port (1..65535), or a negative error code:
 *   -1  empty or not a number      -2  out of range */
int parse_port(const char *s) {
    if (*s == '\0') return -1;
    long value = 0;
    for (; *s; s++) {
        if (*s < '0' || *s > '9') return -1;
        value = value * 10 + (*s - '0');
        if (value > 65535) return -2;
    }
    if (value == 0) return -2;
    return (int)value;
}
```

```zebra
# file: ffi-error-codes.zbr
# teaches: turning C error codes into Zebra errors
# chapter: 22

use portparse

extern def parse_port(s: ^byte): int32

def to_c_string(s: str): ^byte
    var z = s + "${0:c}"
    return zig"@ptrCast(@constCast(z.ptr))"

# The wrapper is the only place that knows the C convention. Callers see an
# ordinary `throws` function: a port, or an error with a message.
def port_from(text: str): int throws
    var code = parse_port(to_c_string(text))
    if code == -1
        raise "not a number: ${text}"
    if code == -2
        raise "port out of range: ${text}"
    return code

def main()
    print(port_from("8080"))
    print(port_from("http"))
    print("not reached")
catch |e|
    print("Error: ${e.message}")
```

Output:

```text
8080
Error: not a number: http
```

The first call returns normally; the second raises, which skips the rest of `main` and
lands in its `catch`.

### Exception-Like Patterns

Some C libraries signal failure with `setjmp`/`longjmp`, or C++ libraries with
exceptions. Neither may cross into Zebra: jumping or unwinding through Zebra frames is
not supported. Write a small C (or C++) shim that catches the failure on its own side and
returns a status code, then wrap the shim exactly as above.

---

## Linking a Prebuilt Library

Most real dependencies are not source you compile — they are a binary someone else built.
`use` finds those too: put `name.lib` (Windows), `libname.a` / `name.a`, or a `.so` /
`.dylib` beside your program, or on `--module-path`, and it is linked in.

To try it, turn `checksum.c` into a library in a separate directory, and copy only the
library beside `ffi-checksum.zbr`:

```bash
mkdir vendor app
cp checksum.c vendor/
cp ffi-checksum.zbr app/
cd vendor
zig build-lib checksum.c      # writes checksum.lib on Windows, libchecksum.a elsewhere
cp checksum.lib ../app/       # (or libchecksum.a)
cd ../app
zebra ffi-checksum.zbr        # same program, same output: 414fa339 ...
```

The Zebra program is unchanged — the same `use checksum` and the same `extern def` — and
it prints the same three lines. Remove the library and the compiler names what it looked
for:

```text
`use checksum`: module not found -- no checksum.zbr (or .c / .lib / .a / .so / .dylib, libchecksum.a/.so/.dylib, .zig) in the current directory
```

If both `checksum.c` and `checksum.lib` are present, the `.c` source wins.

---

## Calling Zig Code

Zig is closer to Zebra, making interop more ergonomic. A `.zig` file beside your program
is imported by `use`, and every `pub fn` in it is callable through the module name. No
`extern def` is needed, and **strings need no conversion**: a Zig `[]const u8` is exactly
what a Zebra `str` is.

```zig
// zigmath.zig -- every `pub fn` is callable as zigmath.<name>(...) after `use zigmath`
const std = @import("std");

pub fn gcd(a: i64, b: i64) i64 {
    var x = a;
    var y = b;
    while (y != 0) {
        const t = @mod(x, y);
        x = y;
        y = t;
    }
    return x;
}

pub fn isPrime(n: i64) bool {
    if (n < 2) return false;
    var d: i64 = 2;
    while (d * d <= n) : (d += 1) {
        if (@mod(n, d) == 0) return false;
    }
    return true;
}

// A Zig []const u8 IS a Zebra str, so strings cross with no conversion.
pub fn countOf(haystack: []const u8, needle: []const u8) i64 {
    return @intCast(std.mem.count(u8, haystack, needle));
}
```

```zebra
# file: ffi-zig-basic.zbr
# teaches: calling Zig functions from Zebra
# chapter: 22

use zigmath

def main()
    print(zigmath.gcd(48, 18))   # 6

    if zigmath.isPrime(17)
        print("17 is prime")
    else
        print("17 is not prime")

    # str passes straight through as a Zig []const u8
    print(zigmath.countOf("mississippi", "ss"))   # 2
```

Output:

```text
6
17 is prime
2
```

Zebra's `int` is Zig's `i64` and `float` is `f64`, so a Zig function written with those
types needs nothing on the Zebra side at all.

---

## Platform-Specific Code

Different platforms have different APIs. Keep the difference on the C side, where the
preprocessor can choose, and give Zebra one signature:

```c
/* platform.c -- the platform difference lives in C, behind one signature */

const char *platform_name(void) {
#if defined(_WIN32)
    return "windows";
#elif defined(__APPLE__)
    return "macos";
#elif defined(__linux__)
    return "linux";
#else
    return "unknown";
#endif
}

const char *path_separator(void) {
#if defined(_WIN32)
    return "\\";
#else
    return "/";
#endif
}
```

```zebra
# file: ffi-platform-specific.zbr
# teaches: keeping platform differences on the C side
# chapter: 22

use platform

extern def platform_name(): ^byte
extern def path_separator(): ^byte

def from_c_string(p: ^byte): str
    return zig"std.mem.span(@as([*:0]const u8, @ptrCast(p)))"

def main()
    # One Zebra program; the C preprocessor picked the answer at build time
    print("platform:  ${from_c_string(platform_name())}")
    print("separator: ${from_c_string(path_separator())}")
```

Output on Windows (Linux prints `linux` and `/`; macOS prints `macos` and `/`):

```text
platform:  windows
separator: \
```

Before reaching for C here, check the standard library: `sys` and `File` (Chapter 20)
already cover environment variables, paths and file sizes on every platform.

---

## What Does Not Cross the Boundary

- **No structs by value.** Pass a handle (above), or pass the fields as separate
  arguments.
- **No arrays or `List`s.** A `List` is not a C array. Keep the collection on one side —
  build it in C behind a handle, as `stats.c` does, or loop in Zebra and pass one value
  per call.
- **No varargs.** `printf` and friends cannot be declared; write a fixed-argument C
  wrapper.
- **No renaming.** The C symbol name is the Zebra name, so a C function whose name is not
  a legal Zebra identifier cannot be reached without a C wrapper.
- **Libraries are found beside the source or on `--module-path`** — there is no system
  library search path and no `-l` flag.
- **`extern` applies to `def` only**, not to variables, types or classes.

---

## Performance Considerations

An `extern` call compiles to a direct call — the same cost as calling the function from C.
What costs time is the **conversion around** the call:

- `to_c_string` allocates and copies the whole string, every time. In a loop, convert
  once and reuse the `^byte`.
- A pointer-and-length API (`checksum.c`) needs no copy at all; prefer it when you write
  the C side yourself.
- A handle API lets C keep its data in its own format between calls, so nothing is
  converted back and forth — `stats.c` never turns its running totals into Zebra values
  until you ask for one.

---

## DynLib — Dynamic Library Plugins

The other direction of FFI: instead of *calling* an existing C library
from Zebra, **producing a shared library** (`.dll` / `.so` / `.dylib`)
that other programs load at runtime. This is Zebra's plugin/extension
point — the pattern an IDE uses to load user-supplied add-ons, or a
server uses to load behaviour modules without restarting.

Two halves: the **producer** (who declares the plugin) and the
**consumer** (who loads it).

### Producer: `@export class`

The producer declares an interface and a class that implements it,
attributed with `@export("symbol")`:

```zebra
# file: greeter.zbr
# compile with:  zebra --shared greeter.zbr
# teaches: @export class for DynLib plugins
# chapter: 22-FFI-and-Interop

interface IGreeter
    def greet(name: str): str
    def version(): int

@export("greeter")
class HelloGreeter implements IGreeter
    def greet(name: str): str
        return "Hello, " + name

    def version(): int
        return 1
```

Compile with `zebra --shared greeter.zbr` to produce `greeter.dll`
(Windows), `libgreeter.so` (Linux), or `libgreeter.dylib` (macOS). The
compiler emits a factory function `pub export fn greeter() *IGreeter`
that wraps a module-static `HelloGreeter` instance in the interface
fat-pointer.

**Producer requirements:**

- The class must implement **at least one interface** — the factory wraps the first listed interface.
- The class `init` must take **no arguments** — the factory calls `ClassName.init()` internally.
- The exported symbol name (`"greeter"` above) is what the consumer passes to `lib.lookup`.

### Producer: `export def` for simple C-callable functions

For individual functions with C-compatible signatures, use `export def`:

```zebra
export def addOne(x: int): int
    return x + 1
```

Emits `pub export fn addOne(x: i64) i64` — callable from C or any
language with FFI support. **C-compatible types only**: primitives are
fine; `str` is a Zig slice (not a C pointer), so `str` parameters and
return types are not directly C-callable. Use `@export class` when you
need richer types.

Any language with a C FFI can call it. Built with `zebra --shared addone.zbr` and loaded
from Python's `ctypes` (Zebra's `int` is a C `long long`):

```python
import ctypes, os
lib = ctypes.CDLL(os.path.abspath("addone.dll"))
lib.addOne.restype = ctypes.c_longlong
lib.addOne.argtypes = [ctypes.c_longlong]
print("addOne(41) via ctypes =", lib.addOne(41))
```

```text
addOne(41) via ctypes = 42
```

### Consumer: loading and calling the plugin

The consumer declares the same interface and loads the library:

```zebra
# file: greeter_host.zbr
# teaches: DynLib.open + lookup
# chapter: 22-FFI-and-Interop

interface IGreeter
    def greet(name: str): str
    def version(): int

def main()
    var lib = DynLib.open("greeter.dll")           # path follows OS convention
    var g = lib.lookup(IGreeter, "greeter")        # factory symbol name

    print(g.greet("World"))  # "Hello, World"
    print(g.version())  # 1

    lib.close()
```

Run after `zebra --shared greeter.zbr` on Windows, it prints:

```text
Hello, World
1
```

`lib.lookup(IFace, "sym")` looks up `sym` as a factory function `fn() *IFace`,
calls it, and returns the resulting fat-pointer. From the consumer's
perspective the returned value is just an `IGreeter` — call its methods
with normal `.method()` syntax. The dispatch happens through the
fat-pointer vtable; the consumer doesn't need to know which class is
behind the interface.

### Real World: Extensible IDE

A natural use: an IDE that loads syntax-highlighting extensions or custom panels at
runtime. Every plugin implements one shared interface — say `IPlugin`, with `name()`,
`on_load()` and `on_file_open(path)` — and is a separate `.zbr` file compiled with
`--shared`. At startup the IDE lists its `plugins/` directory, calls `DynLib.open` on
each library it finds, and calls `lib.lookup(IPlugin, symbol)` using a naming convention
it documents (for example, the file name without its extension as the symbol). It keeps
the returned `IPlugin` values in a list and calls their methods when files open.

The IDE doesn't recompile to add a plugin — drop a new library into `plugins/`, restart,
and the new behaviour appears. `greeter.zbr` and `greeter_host.zbr` above are the whole
mechanism; a plugin system is that pair plus a loop over a directory.

### Notes and gotchas

- **`DynLib.open` panics on failure.** Wrap in a `throws` helper if you
  need graceful "plugin not found" handling.
- **Path conventions vary by OS.** Windows expects `name.dll`; Linux
  expects `libname.so`; macOS expects `libname.dylib`. Pick one
  convention for your application and document it.
- **Plugin and host must agree on the interface.** A version skew (host
  expects `def render(text: str)`, plugin defines `def render(text:
  str, opts: Options)`) is a runtime crash, not a compile error — the
  fat-pointer doesn't carry type information.
- **The exported symbol name is global.** Two plugins with the same
  `@export("name")` cannot coexist in the same host process. Prefix
  with your project's namespace if you ship plugins as a library.

---

## Key Takeaways

1. **`extern def` + `use`** — Declare the function, `use` the file or library that supplies it; one command builds everything.

2. **Sized Types at the Boundary** — `int32` for C `int`, `int64` for `long long`, `^byte` for any pointer. The compiler refuses `int` and `str` in an `extern` signature.

3. **Wrap the C Convention** — Error codes become `raise` inside one `throws` wrapper; C errors do not turn into Zebra errors on their own.

4. **Document Ownership** — Who allocates frees. Handles go back to the library that made them.

5. **Zig Is the Easy Case** — `use` a `.zig` file and call its `pub fn`s; `str` passes straight through.

6. **Test Thoroughly** — FFI bugs are subtle and platform-specific, and the compiler cannot check the C side of a declaration.

---

## When NOT to Use FFI

- **Pure Zebra solution exists** — Use it instead
- **Performance critical loop** — Consider rewriting the loop in C/Zig
- **Simple algorithm** — Zebra is fast enough for most things
- **Unclear memory ownership** — Wrap in C to clarify

---

## Exercises

1. **Hash Function Wrapper** — Wrap OpenSSL's SHA256 safely
2. **Random Number Generator** — Call the C library's `rand`/`srand` via FFI and wrap it in a Zebra class
3. **JSON Parser** — Integrate a C JSON library behind an opaque handle, with error codes turned into `raise`
4. **Text Processing** — Write a C function that takes a pointer and a length (like `checksum.c`) and counts words
5. **System Information** — Retrieve CPU count, memory, etc. via platform APIs, with the `#ifdef`s on the C side

---

## What's Next

You've reached the end of the language itself. What follows are the appendices—grammar reference, standard library summary, and troubleshooting.

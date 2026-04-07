# Chapter 22: FFI and Interop

**Time:** 90 min | **Audience:** Advanced | **Prerequisites:** Chapters 02, 07, 12

---

## Learning Outcomes

After this chapter, you will:
- Understand Foreign Function Interface (FFI) concepts
- Call C functions safely from Zebra
- Marshal data between Zebra and C
- Handle errors and exceptions across language boundaries
- Know the performance and safety tradeoffs

---

## Overview: Calling External Code

Not all code is Zebra. Sometimes you need to call:
- **C libraries** — system libraries, legacy code, performance-critical code
- **Zig code** — for optimal control or performance
- **Platform APIs** — Windows, Linux, macOS system functions

FFI (Foreign Function Interface) lets you call these from Zebra. This chapter covers the patterns, safety considerations, and common pitfalls.

---

## Calling C Functions

### Simple C Function Calls

The simplest case: C functions with primitive types.

```zebra
// file: ffi-c-simple.zbr
// teaches: calling basic C functions
// chapter: 22

// Declare C function signature
// Note: This example assumes the function is available at link time
shared class Math
    shared
        def sqrt(x as float) as float
            # This would be implemented in C
            return 0.0
        
        def pow(base as float, exponent as float) as float
            # C function: double pow(double, double)
            return 0.0

def main()
    var result = Math.sqrt(16.0)
    println(result)  # 4.0
    
    var power = Math.pow(2.0, 8.0)
    println(power)  # 256.0
```

### String Marshaling

Strings require special care because Zebra and C have different string representations.

```zebra
// file: ffi-c-strings.zbr
// teaches: passing strings to C functions
// chapter: 22

shared class CString
    shared
        # C strlen: int strlen(const char* s)
        def strlen(s as str) as int
            # Native C implementation
            return 0
        
        # C strcmp: int strcmp(const char* a, const char* b)
        def strcmp(a as str, b as str) as int
            # Returns: 0 if equal, <0 if a<b, >0 if a>b
            return 0
        
        # C strcpy: char* strcpy(char* dest, const char* src)
        # WARNING: strcpy is dangerous! Buffer overflow risk!
        # Better to use strncpy or avoid it entirely

def main()
    var text = "Hello, World!"
    var length = CString.strlen(text)
    println("Length: ${length}")
    
    var cmp = CString.strcmp("apple", "apple")
    if cmp == 0
        println("Strings are equal")
    
    cmp = CString.strcmp("apple", "banana")
    if cmp < 0
        println("apple comes before banana")
```

### Working with Arrays

Arrays are commonly passed to C functions.

```zebra
// file: ffi-c-arrays.zbr
// teaches: passing arrays to C functions
// chapter: 22

shared class CArray
    shared
        # C qsort: void qsort(void* base, size_t nmemb, size_t size, int (*compar)(const void*, const void*))
        # This is complex to use in Zebra—better to sort in Zebra
        
        # Example: sum array (simplified C function)
        def sum_array(numbers as List(int)) as int
            # In real C: int sum_array(int* arr, int len)
            var total = 0
            for num in numbers
                total = total + num
            return total
        
        # Example: find maximum
        def max_array(numbers as List(int)) as int
            var max_val = numbers.at(0)
            for num in numbers
                if num > max_val
                    max_val = num
            return max_val

def main()
    var numbers = List()
    numbers.add(10)
    numbers.add(20)
    numbers.add(15)
    
    var sum = CArray.sum_array(numbers)
    println("Sum: ${sum}")  # 45
    
    var max_val = CArray.max_array(numbers)
    println("Max: ${max_val}")  # 20
```

### Pointers and Memory Management

This is where FFI gets dangerous.

```zebra
// file: ffi-c-pointers.zbr
// teaches: handling pointers in FFI
// chapter: 22

shared class CMemory
    shared
        # C malloc: void* malloc(size_t size)
        # C free: void free(void* ptr)
        # These are low-level and error-prone
        
        # Better: allocate in Zebra, pass to C
        def process_buffer(data as str) as Result(int, str)
            # Zebra owns the memory, C just reads it
            # Safe! C cannot deallocate
            return Result.ok(data.len)

def main()
    var my_data = "Important data"
    
    # Pass to C function for processing
    var result = CMemory.process_buffer(my_data)
    
    if result.isOk()
        println("Processed: ${result.value()} bytes")
    else
        println("Error: ${result.error()}")
    
    # Zebra's scoping ensures my_data is cleaned up automatically
```

---

## Calling Zig Functions

Zig is closer to Zebra, making interop more ergonomic.

### Basic Zig Interop

```zebra
// file: ffi-zig-basic.zbr
// teaches: calling Zig functions from Zebra
// chapter: 22

shared class ZigMath
    shared
        # Zig function: pub fn gcd(a: i64, b: i64) -> i64
        def gcd(a as int, b as int) as int
            # Implementation in Zig
            return 0
        
        # Zig function: pub fn is_prime(n: u64) -> bool
        def is_prime(n as int) as bool
            return false

def main()
    var result = ZigMath.gcd(48, 18)
    println(result)  # 6
    
    if ZigMath.is_prime(17)
        println("17 is prime")
    else
        println("17 is not prime")
```

### Zig String Handling

Zig's string handling is different from C's.

```zebra
// file: ffi-zig-strings.zbr
// teaches: Zig string interop
// chapter: 22

shared class ZigString
    shared
        # Zig function with slices
        # pub fn string_length(s: []const u8) -> usize
        def string_length(s as str) as int
            return 0
        
        # Case conversion
        # pub fn to_uppercase(allocator: Allocator, s: []const u8) -> ![]u8
        def to_uppercase(s as str) as str
            return ""
        
        # String validation
        # pub fn is_valid_utf8(s: []const u8) -> bool
        def is_valid_utf8(data as str) as bool
            return true

def main()
    var text = "Hello, Zig!"
    var len = ZigString.string_length(text)
    println("Length: ${len}")
    
    var upper = ZigString.to_uppercase(text)
    println("Uppercase: ${upper}")
```

---

## Error Handling Across Boundaries

### Return Code Patterns

Many C functions return error codes rather than throwing exceptions.

```zebra
// file: ffi-error-codes.zbr
// teaches: handling C-style error codes
// chapter: 22

shared class CFile
    shared
        # C fopen: FILE* fopen(const char* filename, const char* mode)
        # Returns NULL on error
        def open_file(filename as str, mode as str) as Result(int, str)
            # In real C, this returns FILE* (opaque pointer)
            # For now, return 0 to indicate error
            var file_handle = 0  # Attempt to open
            
            if file_handle == 0
                return Result.err("Cannot open file: ${filename}")
            else
                return Result.ok(file_handle)
        
        # C close: int fclose(FILE* f)
        # Returns 0 on success, EOF on error
        def close_file(file_handle as int) as Result(bool, str)
            var status = 0  # Attempt to close
            
            if status == 0
                return Result.ok(true)
            else
                return Result.err("Error closing file")

def main()
    var result = CFile.open_file("data.txt", "r")
    
    branch result
        on ok(handle)
            println("File opened: ${handle}")
            
            var close_result = CFile.close_file(handle)
            if close_result.isOk()
                println("File closed")
        on err(error)
            println("Error: ${error}")
```

### Exception-Like Patterns

Some C libraries use setjmp/longjmp for exceptions. These are complex to use from Zebra—consider wrapping in a C shim.

```zebra
// file: ffi-error-wrapper.zbr
// teaches: wrapping C error handling in Zebra
// chapter: 22

# Example: C library with exception-like behavior
# Rather than exposing this complexity to Zebra code,
# wrap it in a simpler Zebra interface

shared class SafeLibrary
    shared
        # C function might throw (via setjmp/longjmp)
        def risky_operation(input as str) as Result(str, str)
            # Wrapper function (in C or Zig) handles exceptions
            # and returns a Result to Zebra
            return Result.err("Operation failed")

def main()
    var result = SafeLibrary.risky_operation("data")
    
    if result.isErr()
        println("Operation failed safely")
```

---

## Type Marshaling

### Numeric Types

Most numeric types map directly:

```zebra
// file: ffi-numeric-types.zbr
// teaches: numeric type marshaling
// chapter: 22

shared class Numeric
    shared
        # Zebra int (64-bit) → C int32_t (32-bit)
        # Be careful with overflow!
        def c_int32_function(n as int) as int
            return 0
        
        # Zebra float → C float or double
        def c_double_function(x as float) as float
            return 0.0
        
        # Boolean: Zebra bool → C bool (or int 0/1)
        def c_bool_function(flag as bool) as bool
            return false

def main()
    # Small numbers are safe
    var result = Numeric.c_int32_function(100)
    println(result)
    
    # Large numbers may overflow in C int32
    # Be careful!
    var large_num = 2147483647 + 1  # Exceeds int32 max
    # Don't pass to C int32 functions!
```

### Collections and Structures

Collections require more care:

```zebra
// file: ffi-structures.zbr
// teaches: passing structures across FFI boundary
// chapter: 22

class Point
    var x as float
    var y as float
    
    def init(x as float, y as float)
        this.x = x
        this.y = y

shared class Geometry
    shared
        # C function: float distance(struct Point a, struct Point b)
        # Assuming C expects Point with fields x, y
        def distance(p1 as Point, p2 as Point) as float
            # Implementation
            var dx = p2.x - p1.x
            var dy = p2.y - p1.y
            return 0.0  # sqrt(dx*dx + dy*dy)

def main()
    var p1 = Point(0.0, 0.0)
    var p2 = Point(3.0, 4.0)
    
    var dist = Geometry.distance(p1, p2)
    println(dist)  # ~5.0 (3-4-5 triangle)
```

---

## Platform-Specific Code

### Windows vs. Unix

Different platforms have different APIs.

```zebra
// file: ffi-platform-specific.zbr
// teaches: handling platform differences
// chapter: 22

shared class Platform
    shared
        # Windows: GetFileSize
        # Unix: stat
        def get_file_size(filename as str) as Result(int, str)
            # Implementation varies by platform
            return Result.ok(0)
        
        def get_environment_variable(name as str) as str?
            # Implemented via getenv (Unix) or GetEnvironmentVariable (Windows)
            return nil
        
        def sleep_milliseconds(ms as int)
            # Windows: Sleep()
            # Unix: usleep()
            pass

def main()
    var size_result = Platform.get_file_size("data.txt")
    
    if size_result.isOk()
        println("File size: ${size_result.value()} bytes")
```

### Conditional Compilation

```zebra
// file: ffi-conditional.zbr
// teaches: platform-specific compilation
// chapter: 22

shared class OSSpecific
    shared
        def platform_name() as str
            # This might vary based on compilation target
            return "Unknown"
        
        def file_separator() as str
            # Windows: \, Unix: /
            return "/"

def main()
    println("Platform: ${OSSpecific.platform_name()}")
    println("Separator: ${OSSpecific.file_separator()}")
```

---

## Safety Considerations

### Memory Safety

The biggest FFI risk: memory management.

```zebra
// file: ffi-safety-memory.zbr
// teaches: FFI memory safety
// chapter: 22

# SAFE: Zebra owns memory
def safe_pattern(data as str) as int
    # Zebra created the string
    # Pass it to C for reading only
    # C should NOT modify or deallocate
    return data.len

# UNSAFE: C allocates memory Zebra must free
# shared class Unsafe
#     shared
#         def allocate_buffer() as str
#             # C allocates memory with malloc
#             # Zebra must call free
#             # This is error-prone! Don't do this.
#             return ""

# BETTER: Provide deallocation function
shared class BetterAlloc
    shared
        # C allocates
        def create_buffer(size as int) as int
            return 0  # Returns opaque handle
        
        # Zebra must call this to free
        def destroy_buffer(handle as int)
            pass

def main()
    var buf = BetterAlloc.create_buffer(1024)
    # Use buffer...
    BetterAlloc.destroy_buffer(buf)
    # buf is now invalid! Don't use it again.
```

### Type Safety

Type mismatches can cause crashes.

```zebra
// file: ffi-safety-types.zbr
// teaches: type safety across FFI boundaries
// chapter: 22

shared class TypeSafety
    shared
        # C expects: void process_array(int* arr, int len)
        def process_array(arr as List(int))
            # Must match! List(str) would be wrong.
            pass
        
        # C expects: int sum(float* values, int count)
        def sum(values as List(float)) as int
            # Values must be floats, not ints
            return 0

def main()
    # Correct usage
    var ints = List()
    ints.add(1)
    ints.add(2)
    ints.add(3)
    # process_array(ints)  # Would need implementation
    
    var floats = List()
    floats.add(1.5)
    floats.add(2.5)
    # var total = sum(floats)  # Correct
    
    # WRONG: Would cause problems
    # var total = sum(ints)  # Type mismatch!
```

### Lifetime Issues

Pointers can outlive their targets.

```zebra
// file: ffi-safety-lifetime.zbr
// teaches: avoiding pointer lifetime issues
// chapter: 22

# UNSAFE: Reference to local variable
# def dangerous() as int
#     var local = 42
#     var ptr = address_of(local)  # Get pointer
#     # local goes out of scope here
#     # ptr now points to garbage!
#     return 0

# SAFE: Return value, not reference
def safe_return(n as int) as int
    var result = n * 2
    # result is copied into return value
    # No dangling pointers
    return result

# SAFE: Use parameters
def safe_parameter(numbers as List(int)) as int
    # List is passed by reference, lives in caller's scope
    # Safe to use while caller owns it
    return numbers.at(0)

def main()
    var my_list = List()
    my_list.add(42)
    
    # Safe—my_list is still alive
    var first = safe_parameter(my_list)
    # After main returns, my_list is cleaned up
```

---

## Practical Example: Crypto Library Integration

```zebra
// file: ffi-crypto-example.zbr
// teaches: practical FFI example with crypto
// chapter: 22

shared class Crypto
    shared
        # OpenSSL/BoringSSL: compute SHA256
        def sha256(input as str) as str
            # C function: 
            # void SHA256(const unsigned char* d, size_t n, unsigned char* md)
            return ""
        
        # Verify hash matches expected value
        def verify_sha256(input as str, expected_hash as str) as bool
            var computed = sha256(input)
            return computed == expected_hash

def main()
    var message = "Secret password"
    var hash = Crypto.sha256(message)
    println("SHA256: ${hash}")
    
    # Verify integrity
    var stored_hash = "a665a45920422f9d417e4867efdc4fb8a04a1d3a4ff2d42bfa0f1db5e2ce9ba"
    
    if Crypto.verify_sha256(message, stored_hash)
        println("Hash verified!")
    else
        println("Hash mismatch!")
```

---

## Performance Considerations

### Call Overhead

FFI calls have overhead:

```zebra
// file: ffi-performance.zbr
// teaches: FFI performance tradeoffs
// chapter: 22

def main()
    # FFI calls are expensive compared to Zebra calls
    # If you're calling an FFI function in a tight loop,
    # consider moving the loop into C
    
    # BAD: Loop in Zebra, FFI call per iteration
    var sum = 0
    for i in 0.to(1000000)
        sum = sum + expensive_c_function(i)
    
    # BETTER: Pass the whole array to C
    var nums = List()
    for i in 0.to(1000000)
        nums.add(i)
    
    sum = sum_all(nums)  # Single FFI call

def expensive_c_function(n as int) as int
    return n * 2

def sum_all(nums as List(int)) as int
    var total = 0
    for num in nums
        total = total + num
    return total
```

### Batching Operations

```zebra
// file: ffi-batching.zbr
// teaches: batching FFI operations
// chapter: 22

shared class Batch
    shared
        # Process one item (slow)
        def process_item(item as str) as str
            return item.upper()
        
        # Process many items (fast)
        def process_batch(items as List(str)) as List(str)
            # Single FFI call for all items
            return items

def main()
    var items = List()
    for i in 0.to(100)
        items.add("item-${i}")
    
    # GOOD: Batch processing
    var results = Batch.process_batch(items)
    
    # BAD: Individual calls
    # for item in items
    #     var result = Batch.process_item(item)  # 100 FFI calls!
```

---

## Key Takeaways

1. **Safety First** — Memory management is dangerous. Prefer Zebra ownership.

2. **Use Result Types** — C errors become Zebra Result types automatically.

3. **Type Carefully** — Type mismatches can cause crashes.

4. **Batch Calls** — Multiple small FFI calls are slower than one big call.

5. **Document Ownership** — Who owns allocated memory? Make it clear.

6. **Test Thoroughly** — FFI bugs are subtle and platform-specific.

---

## When NOT to Use FFI

- **Pure Zebra solution exists** — Use it instead
- **Performance critical loop** — Consider rewriting the loop in C/Zig
- **Simple algorithm** — Zebra is fast enough for most things
- **Unclear memory ownership** — Wrap in C to clarify

---

## Exercises

1. **Hash Function Wrapper** — Wrap OpenSSL's SHA256 safely
2. **Random Number Generator** — Call system random via FFI
3. **JSON Parser** — Integrate a C JSON library with error handling
4. **Text Processing** — Call ICU for Unicode operations
5. **System Information** — Retrieve CPU count, memory, etc. via platform APIs

---

## What's Next

You've reached the end of the language itself. What follows are the appendices—grammar reference, standard library summary, and troubleshooting.

# Zebra Programming Book - Code Examples

This directory contains 180 runnable code examples extracted from the Zebra Programming Book.

## Organization

Examples are organized by chapter:

```
examples/
├── 01-getting-started/
├── 02-values-and-types/
├── 03-collections/
├── ...
└── manifest.json
```

## Running Examples

Each `.zbr` file is a complete, runnable program:

```bash
zebra examples/01-getting-started/01_hello_world.zbr
```

## Example Manifest

See `manifest.json` for a complete index of all examples with metadata:
- Chapter name
- What concept each example teaches
- Associated project (if any)

## Testing All Examples

Run the validation script:

```bash
python3 ../validate-examples.py
```

This compiles and tests each example to ensure correctness.

## By the Numbers

- **Total Examples:** 180
- **Chapters Covered:** 21
- **Topics:** 179

## Quick Reference

### Examples by Chapter


### 01-Getting-Started (2 examples)
- `hello.zbr` — hello world, print statement
- `greet.zbr` — variables, string interpolation

### 02-Values-and-Types (8 examples)
- `02_integers.zbr` — integer types, arithmetic
- `02_floats.zbr` — float types, precision
- `02_bools.zbr` — boolean values, logic
- `02_strings.zbr` — string type, string operations
- `02_comparisons.zbr` — comparison operators
- `02_conversions.zbr` — type conversion
- `02_nullables.zbr` — nullable types introduction
- `02_user_data.zbr` — realistic variable use

### 03-Collections (8 examples)
- `03_lists.zbr` — list creation and access
- `03_list_ops.zbr` — list manipulation
- `03_iteration.zbr` — different iteration styles
- `03_hashmaps.zbr` — hashmap creation and access
- `03_hashmap_ops.zbr` — hashmap manipulation
- `03_sets.zbr` — sets for uniqueness
- `03_real_world.zbr` — collections in realistic scenarios
- `03_patterns.zbr` — collection patterns

### 04-Functions-and-Scope (9 examples)
- `04_functions.zbr` — function definition and calling
- `04_multi_params.zbr` — multiple parameters
- `04_void.zbr` — functions that don't return values
- `04_scope.zbr` — variable scope
- `04_closures.zbr` — closures and variable capture
- `04_capture.zbr` — capture blocks
- `04_utilities.zbr` — practical function use
- `04_patterns.zbr` — early return pattern
- `04_higher_order.zbr` — functions as arguments

### 05-Control-Flow (10 examples)
- `05_if.zbr` — conditional execution
- `05_if_else.zbr` — if-else branching
- `05_conditions.zbr` — boolean logic
- `05_match.zbr` — pattern matching
- `05_match_type.zbr` — type-based matching
- `05_for.zbr` — for loop iteration
- `05_while.zbr` — while loop
- `05_break_continue.zbr` — loop control
- `05_guards.zbr` — guard conditions
- `05_validation.zbr` — practical control flow

### 06-Strings-and-Unicode (11 examples)
- `06_string_basics.zbr` — string creation
- `06_string_props.zbr` — string properties and methods
- `06_interpolation.zbr` — string interpolation
- `06_search.zbr` — searching in strings
- `06_split_join.zbr` — splitting and joining strings
- `06_trim_pad.zbr` — trimming and padding
- `06_replace.zbr` — string replacement
- `06_unicode.zbr` — unicode support
- `06_char_iter.zbr` — iterating over characters
- `06_regex_intro.zbr` — regular expressions introduction
- `06_text_processing.zbr` — practical text operations

### 07-Classes-and-Instances (5 examples)
- `07_class_basic.zbr` — class definition
- `07_init.zbr` — field initialization
- `07_methods.zbr` — instance methods
- `07_shared.zbr` — shared (class) methods
- `07_user_system.zbr` — realistic class design

### 08-Interfaces-and-Protocols (5 examples)
- `08_interface_basic.zbr` — interface definition
- `08_interface_methods.zbr` — interface with multiple methods
- `08_polymorphism.zbr` — polymorphic behavior
- `08_collection_interface.zbr` — storing different implementations
- `08_logger_system.zbr` — realistic interface use

### 09-Inheritance-and-Mixins (7 examples)
- `09_inheritance_basic.zbr` — class inheritance
- `09_override.zbr` — overriding parent methods
- `09_super.zbr` — calling parent implementation
- `09_hierarchy.zbr` — inheritance hierarchies
- `09_polymorphic_hierarchy.zbr` — treating children as parents
- `09_mixins.zbr` — mixin composition
- `09_document_hierarchy.zbr` — realistic inheritance use

### 10-Properties-and-Computed-Values (8 examples)
- `10_getter.zbr` — computed properties
- `10_derived.zbr` — deriving values from fields
- `10_setter_validation.zbr` — setters with validation
- `10_setter_effects.zbr` — setters with side effects
- `10_computed.zbr` — expensive computed properties
- `10_lazy_init.zbr` — lazy initialization
- `10_temperature.zbr` — properties in realistic scenarios
- `10_config.zbr` — configuration management

### 11-Nil-Tracking-and-Safety (6 examples)
- `11_nullable.zbr` — nullable types
- `11_nil_check.zbr` — nil checking
- `11_narrowing.zbr` — type narrowing
- `11_unwrap.zbr` — unwrap operator
- `11_unwrap_or.zbr` — safe unwrapping
- `11_database.zbr` — nil in realistic scenarios

### 12-Error-Handling-with-Results (4 examples)
- `12_result_basic.zbr` — result type
- `12_result_unwrap.zbr` — result unwrapping
- `12_error_propagation.zbr` — propagating errors
- `12_api_client.zbr` — results in realistic code

### 13-Generics-and-Type-Constraints (7 examples)
- `13_generic_container.zbr` — generic class definition
- `13_generic_pair.zbr` — multiple type parameters
- `13_generic_methods.zbr` — generic methods
- `13_generic_collections.zbr` — using generic stdlib types
- `13_type_constraints.zbr` — interface constraints
- `13_generic_constraints_advanced.zbr` — constraints in generic methods
- `13_generic_cache.zbr` — realistic generic class

### 14-Contracts-and-Assertions (8 examples)
- `14_preconditions.zbr` — precondition checking
- `14_postconditions.zbr` — postcondition checking
- `14_invariants.zbr` — class invariants
- `14_assertions.zbr` — assertions
- `14_sort_postcondition.zbr` — postcondition in realistic code
- `14_guard_clauses.zbr` — guard clause pattern
- `14_early_return.zbr` — fail fast principle
- `14_dual_verify.zbr` — verifying both input and output

### 15-Pipelines-and-Function-Composition (7 examples)
- `15_pipeline_basics.zbr` — pipeline operator
- `15_pipeline_chain.zbr` — chaining operations
- `15_pipeline_collections.zbr` — piping through collections
- `15_pipeline_custom.zbr` — custom functions in pipelines
- `15_pipeline_real_world.zbr` — realistic pipeline
- `15_function_composition.zbr` — composing functions
- `15_pipeline_results.zbr` — pipelines with error handling

### 16-Project-1-CLI-Tool (4 examples)
- `cli_args.zbr` — argument parsing
- `file_processor.zbr` — file I/O and text processing
- `pattern_search.zbr` — pattern matching and filtering
- `project1_main.zbr` — orchestrating modules

### 17-18_Projects-2-3 (7 examples)
- `http_types.zbr` — protocol data structures
- `router.zbr` — request routing and dispatching
- `http_server.zbr` — network server programming
- `frequency_analysis.zbr` — frequency counting and sorting
- `ngram_analysis.zbr` — n-gram extraction and pattern detection
- `similarity_analysis.zbr` — similarity metrics and comparison
- `analysis_main.zbr` — combining analysis modules

### 19-Standard-Library-Tour (14 examples)
- `stdlib-string-inspect.zbr` — string properties and inspection methods
- `stdlib-string-case.zbr` — case conversion methods
- `stdlib-string-search.zbr` — searching and replacing in strings
- `stdlib-string-split-join.zbr` — splitting and joining strings
- `stdlib-string-trim.zbr` — removing whitespace from strings
- `stdlib-string-extract-concat.zbr` — substring extraction and string concatenation
- `stdlib-list-ops.zbr` — list operations and patterns
- `stdlib-hashmap-ops.zbr` — hashmap operations and patterns
- `stdlib-set-ops.zbr` — set operations for uniqueness
- `stdlib-type-conversions.zbr` — converting between types and strings
- `stdlib-math-operations.zbr` — basic math operations in Zebra
- `stdlib-system-access.zbr` — accessing system information
- `stdlib-console-io.zbr` — printing to console
- `stdlib-data-processing.zbr` — combining stdlib functions for data processing

### 20-File-IO-and-System-Access (15 examples)
- `file-read-simple.zbr` — simple file reading with error handling
- `file-read-unwrap.zbr` — safe error handling for file reads
- `file-read-lines.zbr` — efficient line-by-line file reading
- `file-analyze.zbr` — analyzing file contents
- `file-write-simple.zbr` — basic file writing
- `file-write-building.zbr` — efficiently building and writing file content
- `file-append.zbr` — appending content to existing files
- `file-batch-process.zbr` — processing multiple files
- `file-convert.zbr` — reading one format and writing another
- `file-exists.zbr` — checking if files exist
- `file-delete.zbr` — safely deleting files
- `file-paths.zbr` — path operations and directory access
- `file-config-management.zbr` — loading and parsing configuration files
- `file-logging.zbr` — generating timestamped log files
- `file-data-import.zbr` — importing and exporting structured data

### 21-Regular-Expressions (17 examples)
- `regex-literals.zbr` — basic regex literal matching
- `regex-dot.zbr` — dot wildcard in regex patterns
- `regex-character-classes.zbr` — character classes and ranges
- `regex-shortcuts.zbr` — common regex shortcuts
- `regex-quantifiers.zbr` — repetition quantifiers
- `regex-anchors.zbr` — position anchors in regex
- `regex-groups.zbr` — grouping and alternation patterns
- `regex-email.zbr` — email validation pattern (simplified)
- `regex-phone.zbr` — phone number pattern matching
- `regex-url.zbr` — URL pattern matching
- `regex-finding.zbr` — finding matches within text
- `regex-extract-structured.zbr` — extracting data from formatted text
- `regex-replace.zbr` — pattern-based text replacement
- `regex-transform.zbr` — using regex for data transformation
- `regex-greedy.zbr` — understanding greedy matching
- `regex-escaping.zbr` — escaping special characters
- `regex-log-analysis.zbr` — using regex for real log analysis

### 22-FFI-and-Interop (18 examples)
- `ffi-c-simple.zbr` — calling basic C functions
- `ffi-c-strings.zbr` — passing strings to C functions
- `ffi-c-arrays.zbr` — passing arrays to C functions
- `ffi-c-pointers.zbr` — handling pointers in FFI
- `ffi-zig-basic.zbr` — calling Zig functions from Zebra
- `ffi-zig-strings.zbr` — Zig string interop
- `ffi-error-codes.zbr` — handling C-style error codes
- `ffi-error-wrapper.zbr` — wrapping C error handling in Zebra
- `ffi-numeric-types.zbr` — numeric type marshaling
- `ffi-structures.zbr` — passing structures across FFI boundary
- `ffi-platform-specific.zbr` — handling platform differences
- `ffi-conditional.zbr` — platform-specific compilation
- `ffi-safety-memory.zbr` — FFI memory safety
- `ffi-safety-types.zbr` — type safety across FFI boundaries
- `ffi-safety-lifetime.zbr` — avoiding pointer lifetime issues
- `ffi-crypto-example.zbr` — practical FFI example with crypto
- `ffi-performance.zbr` — FFI performance tradeoffs
- `ffi-batching.zbr` — batching FFI operations

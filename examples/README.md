# Zebra Programming Book - Code Examples

This directory contains 686 runnable code examples extracted from the Zebra Programming Book.

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

- **Total Examples:** 686
- **Chapters Covered:** 32
- **Topics:** 210

## Quick Reference

### Examples by Chapter


### 01-Getting-Started (13 examples)
- `hello.zbr` — hello world, the print function
- `01-getting-started_001.zbr` — basic example
- `01-getting-started_002.zbr` — basic example
- `01-getting-started_003.zbr` — basic example
- `greet.zbr` — variables, string interpolation
- `01-getting-started_005.zbr` — basic example
- `01-getting-started_006.zbr` — basic example
- `01-getting-started_007.zbr` — basic example
- `math_utils.zbr` — basic example
- `main.zbr` — basic example
- `01-getting-started_010.zbr` — basic example
- `01-getting-started_011.zbr` — basic example
- `01-getting-started_012.zbr` — basic example

### 02-Values-and-Types (24 examples)
- `02_integers.zbr` — integer types, arithmetic
- `02-values-and-types_001.zbr` — basic example
- `02_floats.zbr` — float types, precision
- `02_bools.zbr` — boolean values, logic
- `02_strings.zbr` — string type, string operations
- `02_tuples.zbr` — tuple types, literals, destructuring, and indexing
- `02-values-and-types_006.zbr` — basic example
- `02-values-and-types_007.zbr` — basic example
- `02-values-and-types_008.zbr` — basic example
- `02_comparisons.zbr` — comparison operators
- `02-values-and-types_010.zbr` — basic example
- `02_conversions.zbr` — type conversion
- `02_nullables.zbr` — nullable types introduction
- `02-values-and-types_013.zbr` — basic example
- `02_user_data.zbr` — realistic variable use
- `02-values-and-types_015.zbr` — basic example
- `02-values-and-types_016.zbr` — basic example
- `02-values-and-types_017.zbr` — basic example
- `02-values-and-types_018.zbr` — basic example
- `02-values-and-types_019.zbr` — basic example
- `02-values-and-types_020.zbr` — basic example
- `02-values-and-types_021.zbr` — basic example
- `02-values-and-types_022.zbr` — basic example
- `02-values-and-types_023.zbr` — basic example

### 03-Collections (17 examples)
- `03_lists.zbr` — list creation and access
- `03_list_ops.zbr` — list manipulation
- `03_iteration.zbr` — different iteration styles
- `03_hashmaps.zbr` — hashmap creation and access
- `03_hashmap_ops.zbr` — hashmap manipulation
- `03_dedup.zbr` — using HashMap for uniqueness
- `03_real_world.zbr` — collections in realistic scenarios
- `03_patterns.zbr` — collection patterns
- `03-collections_008.zbr` — basic example
- `03-collections_009.zbr` — basic example
- `03-collections_010.zbr` — basic example
- `03-collections_011.zbr` — basic example
- `03-collections_012.zbr` — basic example
- `03-collections_013.zbr` — basic example
- `03-collections_014.zbr` — basic example
- `03-collections_015.zbr` — basic example
- `03-collections_016.zbr` — basic example

### 04-Functions-and-Scope (26 examples)
- `04_functions.zbr` — function definition and calling
- `04_multi_params.zbr` — multiple parameters
- `04_void.zbr` — functions that don't return values
- `04_scope.zbr` — variable scope
- `04-functions-and-scope_004.zbr` — basic example
- `04_closures.zbr` — closures and variable capture
- `04_capture.zbr` — capture blocks
- `04_utilities.zbr` — practical function use
- `04_patterns.zbr` — early return pattern
- `04-functions-and-scope_009.zbr` — basic example
- `04-functions-and-scope_010.zbr` — basic example
- `04_higher_order.zbr` — functions as arguments
- `04_sig.zbr` — named function types with sig
- `04-functions-and-scope_013.zbr` — basic example
- `04-functions-and-scope_014.zbr` — basic example
- `04_lambda_arg.zbr` — lambda as call argument (statement-body form)
- `04_nested_lambda.zbr` — nested lambda as argument
- `04-functions-and-scope_017.zbr` — basic example
- `04-functions-and-scope_018.zbr` — basic example
- `04-functions-and-scope_019.zbr` — basic example
- `04-functions-and-scope_020.zbr` — basic example
- `04-functions-and-scope_021.zbr` — basic example
- `04-functions-and-scope_022.zbr` — basic example
- `04-functions-and-scope_023.zbr` — basic example
- `04-functions-and-scope_024.zbr` — basic example
- `04-functions-and-scope_025.zbr` — basic example

### 05-Control-Flow (24 examples)
- `05_if.zbr` — conditional execution
- `05_if_else.zbr` — if-else branching
- `05_conditions.zbr` — boolean logic
- `05_inline_if.zbr` — one-line if statement
- `05_if_expr.zbr` — if-expression
- `05_match.zbr` — pattern matching
- `05_match_type.zbr` — type-based matching with unions
- `05_for.zbr` — for loop iteration
- `05_while.zbr` — while loop
- `05_break_continue.zbr` — loop control
- `05_guards.zbr` — guard conditions
- `05_validation.zbr` — practical control flow
- `05-control-flow_012.zbr` — basic example
- `05-control-flow_013.zbr` — basic example
- `05-control-flow_014.zbr` — basic example
- `05-control-flow_015.zbr` — basic example
- `05-control-flow_016.zbr` — basic example
- `05-control-flow_017.zbr` — basic example
- `05-control-flow_018.zbr` — basic example
- `05-control-flow_019.zbr` — basic example
- `05-control-flow_020.zbr` — basic example
- `05-control-flow_021.zbr` — basic example
- `05-control-flow_022.zbr` — basic example
- `05-control-flow_023.zbr` — basic example

### 06-Strings-and-Unicode (23 examples)
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
- `06-strings-and-unicode_011.zbr` — basic example
- `06-strings-and-unicode_012.zbr` — basic example
- `06-strings-and-unicode_013.zbr` — basic example
- `06-strings-and-unicode_014.zbr` — basic example
- `06-strings-and-unicode_015.zbr` — basic example
- `06-strings-and-unicode_016.zbr` — basic example
- `06-strings-and-unicode_017.zbr` — basic example
- `06-strings-and-unicode_018.zbr` — basic example
- `06-strings-and-unicode_019.zbr` — basic example
- `06-strings-and-unicode_020.zbr` — basic example
- `06-strings-and-unicode_021.zbr` — basic example
- `06-strings-and-unicode_022.zbr` — basic example

### 07-Classes-and-Instances (17 examples)
- `07_class_basic.zbr` — class definition, cue init
- `07_init.zbr` — field defaults vs. explicit init
- `07_methods.zbr` — instance methods
- `07_static.zbr` — static (class-level) methods
- `07-classes-and-instances_004.zbr` — basic example
- `07-classes-and-instances_005.zbr` — basic example
- `07-classes-and-instances_006.zbr` — basic example
- `07_user_system.zbr` — realistic class design
- `07-classes-and-instances_008.zbr` — basic example
- `07-classes-and-instances_009.zbr` — basic example
- `07-classes-and-instances_010.zbr` — basic example
- `07-classes-and-instances_011.zbr` — basic example
- `07-classes-and-instances_012.zbr` — basic example
- `07-classes-and-instances_013.zbr` — basic example
- `07-classes-and-instances_014.zbr` — basic example
- `07-classes-and-instances_015.zbr` — basic example
- `07-classes-and-instances_016.zbr` — basic example

### 07b-Structs-Unions-and-Value-Types (11 examples)
- `07b_struct_basic.zbr` — struct definition and value semantics
- `07b_except.zbr` — except struct update syntax
- `07b-structs-unions-and-value-types_002.zbr` — basic example
- `07b_enum.zbr` — enum types
- `07b_union_basic.zbr` — union definition and construction
- `07b_branch.zbr` — branch pattern matching
- `07b-structs-unions-and-value-types_006.zbr` — basic example
- `07b_heap_indirect.zbr` — ^T heap indirection
- `07b-structs-unions-and-value-types_008.zbr` — basic example
- `07b_mini_ast.zbr` — combining structs, unions, and ^T
- `07b-structs-unions-and-value-types_010.zbr` — basic example

### 08-Interfaces-and-Protocols (17 examples)
- `08_interface_basic.zbr` — interface definition
- `08_interface_methods.zbr` — interface with multiple methods
- `08_polymorphism.zbr` — polymorphic behavior
- `08_collection_interface.zbr` — storing different implementations
- `08_logger_system.zbr` — realistic interface use
- `08-interfaces-and-protocols_005.zbr` — basic example
- `08-interfaces-and-protocols_006.zbr` — basic example
- `08-interfaces-and-protocols_007.zbr` — basic example
- `08-interfaces-and-protocols_008.zbr` — basic example
- `08-interfaces-and-protocols_009.zbr` — basic example
- `08-interfaces-and-protocols_010.zbr` — basic example
- `08-interfaces-and-protocols_011.zbr` — basic example
- `08-interfaces-and-protocols_012.zbr` — basic example
- `08-interfaces-and-protocols_013.zbr` — basic example
- `08-interfaces-and-protocols_014.zbr` — basic example
- `08-interfaces-and-protocols_015.zbr` — basic example
- `08-interfaces-and-protocols_016.zbr` — basic example

### 09-Composition-and-Mixins (15 examples)
- `09_mixin_basic.zbr` — declaring and using mixins
- `09-composition-and-mixins_001.zbr` — basic example
- `09_composition.zbr` — composition with helper classes
- `09_multiple_mixins.zbr` — combining multiple mixins
- `09_polymorphism.zbr` — interface-based polymorphism (instead of inheritance)
- `09_document_capabilities.zbr` — combining interface + mixin + composition
- `09-composition-and-mixins_006.zbr` — basic example
- `09-composition-and-mixins_007.zbr` — basic example
- `09-composition-and-mixins_008.zbr` — basic example
- `09-composition-and-mixins_009.zbr` — basic example
- `09-composition-and-mixins_010.zbr` — basic example
- `09-composition-and-mixins_011.zbr` — basic example
- `09-composition-and-mixins_012.zbr` — basic example
- `09-composition-and-mixins_013.zbr` — basic example
- `09-composition-and-mixins_014.zbr` — basic example

### 10-Properties-and-Computed-Values (19 examples)
- `10_getter.zbr` — computed properties
- `10_derived.zbr` — deriving values from fields
- `10_setter_validation.zbr` — setters with validation
- `10_setter_effects.zbr` — setters with side effects
- `10_computed.zbr` — expensive computed properties
- `10_lazy_init.zbr` — lazy initialization
- `10_temperature.zbr` — properties in realistic scenarios
- `10_config.zbr` — configuration management
- `10-properties-and-computed-values_008.zbr` — basic example
- `10-properties-and-computed-values_009.zbr` — basic example
- `10-properties-and-computed-values_010.zbr` — basic example
- `10-properties-and-computed-values_011.zbr` — basic example
- `10-properties-and-computed-values_012.zbr` — basic example
- `10-properties-and-computed-values_013.zbr` — basic example
- `10-properties-and-computed-values_014.zbr` — basic example
- `10-properties-and-computed-values_015.zbr` — basic example
- `10-properties-and-computed-values_016.zbr` — basic example
- `10-properties-and-computed-values_017.zbr` — basic example
- `10-properties-and-computed-values_018.zbr` — basic example

### 10b-Modules-Namespaces-and-Visibility (36 examples)
- `math_utils.zbr` — basic example
- `main.zbr` — basic example
- `main.zbr` — basic example
- `10b-modules-namespaces-and-visibility_003.zbr` — basic example
- `10b-modules-namespaces-and-visibility_004.zbr` — basic example
- `10b-modules-namespaces-and-visibility_005.zbr` — basic example
- `wallet.zbr` — basic example
- `main.zbr` — basic example
- `colors.zbr` — basic example
- `10b-modules-namespaces-and-visibility_009.zbr` — basic example
- `10b-modules-namespaces-and-visibility_010.zbr` — basic example
- `10b-modules-namespaces-and-visibility_011.zbr` — basic example
- `10b-modules-namespaces-and-visibility_012.zbr` — basic example
- `10b-modules-namespaces-and-visibility_013.zbr` — basic example
- `10b-modules-namespaces-and-visibility_014.zbr` — basic example
- `helpers.zbr` — basic example
- `main.zbr` — basic example
- `Wallet.zbr  (primary)` — basic example
- `Wallet.transactions.zbr  (partial — merges into Wallet)` — basic example
- `10b-modules-namespaces-and-visibility_019.zbr` — basic example
- `10b-modules-namespaces-and-visibility_020.zbr` — basic example
- `10b-modules-namespaces-and-visibility_021.zbr` — basic example
- `10b-modules-namespaces-and-visibility_022.zbr` — basic example
- `10b-modules-namespaces-and-visibility_023.zbr` — basic example
- `10b-modules-namespaces-and-visibility_024.zbr` — basic example
- `10b-modules-namespaces-and-visibility_025.zbr` — basic example
- `10b-modules-namespaces-and-visibility_026.zbr` — basic example
- `10b-modules-namespaces-and-visibility_027.zbr` — basic example
- `10b-modules-namespaces-and-visibility_028.zbr` — basic example
- `10b-modules-namespaces-and-visibility_029.zbr` — basic example
- `10b-modules-namespaces-and-visibility_030.zbr` — basic example
- `10b-modules-namespaces-and-visibility_031.zbr` — basic example
- `10b-modules-namespaces-and-visibility_032.zbr` — basic example
- `10b-modules-namespaces-and-visibility_033.zbr` — basic example
- `10b-modules-namespaces-and-visibility_034.zbr` — basic example
- `10b-modules-namespaces-and-visibility_035.zbr` — basic example

### 11-Nil-Tracking-and-Safety (19 examples)
- `11_nullable.zbr` — nullable types
- `11_nil_check.zbr` — nil checking
- `11_narrowing.zbr` — type narrowing
- `11_if_as.zbr` — optional unwrap binding form
- `11-nil-tracking-and-safety_004.zbr` — basic example
- `11_unwrap.zbr` — unwrap operator
- `11_unwrap_or.zbr` — safe unwrapping
- `11_database.zbr` — nil in realistic scenarios
- `11-nil-tracking-and-safety_008.zbr` — basic example
- `11-nil-tracking-and-safety_009.zbr` — basic example
- `11-nil-tracking-and-safety_010.zbr` — basic example
- `11-nil-tracking-and-safety_011.zbr` — basic example
- `11-nil-tracking-and-safety_012.zbr` — basic example
- `11-nil-tracking-and-safety_013.zbr` — basic example
- `11-nil-tracking-and-safety_014.zbr` — basic example
- `11-nil-tracking-and-safety_015.zbr` — basic example
- `11-nil-tracking-and-safety_016.zbr` — basic example
- `11-nil-tracking-and-safety_017.zbr` — basic example
- `11-nil-tracking-and-safety_018.zbr` — basic example

### 12-Error-Handling-with-Results (10 examples)
- `12_throws_basic.zbr` — throws annotation
- `12_raise.zbr` — raise statement
- `12_method_catch.zbr` — method-level catch clause
- `12_catch_binding.zbr` — catch with error binding
- `12_catch_typed.zbr` — catch with typed error binding
- `12_catch_expr.zbr` — catch expression for defaults
- `12_propagation.zbr` — error propagation
- `12_api_client.zbr` — realistic error handling
- `12-error-handling-with-results_008.zbr` — basic example
- `12-error-handling-with-results_009.zbr` — basic example

### 13-Generics-and-Type-Constraints (19 examples)
- `13-generics-and-type-constraints_000.zbr` — basic example
- `13_generic_container.zbr` — generic class definition
- `13_generic_pair.zbr` — multiple type parameters
- `13_generic_methods.zbr` — generic methods
- `13_generic_function.zbr` — top-level generic function declaration
- `13_generic_collections.zbr` — using generic stdlib types
- `13_type_constraints.zbr` — interface constraints
- `13_generic_constraints_advanced.zbr` — constraints in generic methods
- `13_type_aliases.zbr` — type aliases with constraints
- `13_refinement_types.zbr` — parametric refinement types
- `13-generics-and-type-constraints_010.zbr` — basic example
- `13_generic_cache.zbr` — realistic generic class
- `13-generics-and-type-constraints_012.zbr` — basic example
- `13-generics-and-type-constraints_013.zbr` — basic example
- `13-generics-and-type-constraints_014.zbr` — basic example
- `13-generics-and-type-constraints_015.zbr` — basic example
- `13-generics-and-type-constraints_016.zbr` — basic example
- `13-generics-and-type-constraints_017.zbr` — basic example
- `13-generics-and-type-constraints_018.zbr` — basic example

### 14-Contracts-and-Assertions (16 examples)
- `14-contracts-and-assertions_000.zbr` — basic example
- `14_require.zbr` — precondition checking with require
- `14_ensure.zbr` — postcondition checking with ensure
- `14_ensure_result.zbr` — result in ensure clauses
- `14_ensure_old.zbr` — old snapshots in ensure clauses
- `14_invariant.zbr` — class invariants
- `14_assert.zbr` — assert statement
- `14_sorted_list.zbr` — combining require, ensure, and invariant
- `14-contracts-and-assertions_008.zbr` — basic example
- `14-contracts-and-assertions_009.zbr` — basic example
- `14-contracts-and-assertions_010.zbr` — basic example
- `14-contracts-and-assertions_011.zbr` — basic example
- `14-contracts-and-assertions_012.zbr` — basic example
- `14-contracts-and-assertions_013.zbr` — basic example
- `14-contracts-and-assertions_014.zbr` — basic example
- `14-contracts-and-assertions_015.zbr` — basic example

### 14b-Memory-Management-and-Lifetimes (26 examples)
- `14b-memory-management-and-lifetimes_000.zbr` — basic example
- `14b-memory-management-and-lifetimes_001.zbr` — basic example
- `14b-memory-management-and-lifetimes_002.zbr` — basic example
- `14b-memory-management-and-lifetimes_003.zbr` — basic example
- `14b-memory-management-and-lifetimes_004.zbr` — basic example
- `14b-memory-management-and-lifetimes_005.zbr` — basic example
- `14b-memory-management-and-lifetimes_006.zbr` — basic example
- `14b-memory-management-and-lifetimes_007.zbr` — basic example
- `14b-memory-management-and-lifetimes_008.zbr` — basic example
- `14b-memory-management-and-lifetimes_009.zbr` — basic example
- `14b-memory-management-and-lifetimes_010.zbr` — basic example
- `14b-memory-management-and-lifetimes_011.zbr` — basic example
- `14b-memory-management-and-lifetimes_012.zbr` — basic example
- `14b_streaming_processor.zbr` — allocate + <- + using together
- `14b-memory-management-and-lifetimes_014.zbr` — basic example
- `14b-memory-management-and-lifetimes_015.zbr` — basic example
- `14b-memory-management-and-lifetimes_016.zbr` — basic example
- `14b-memory-management-and-lifetimes_017.zbr` — basic example
- `14b-memory-management-and-lifetimes_018.zbr` — basic example
- `14b-memory-management-and-lifetimes_019.zbr` — basic example
- `14b-memory-management-and-lifetimes_020.zbr` — basic example
- `14b-memory-management-and-lifetimes_021.zbr` — basic example
- `14b-memory-management-and-lifetimes_022.zbr` — basic example
- `14b-memory-management-and-lifetimes_023.zbr` — basic example
- `14b-memory-management-and-lifetimes_024.zbr` — basic example
- `14b-memory-management-and-lifetimes_025.zbr` — basic example

### 14c-Concurrency-Channels-and-Threads (24 examples)
- `14c-concurrency-channels-and-threads_000.zbr` — basic example
- `14c-concurrency-channels-and-threads_001.zbr` — basic example
- `14c-concurrency-channels-and-threads_002.zbr` — basic example
- `14c-concurrency-channels-and-threads_003.zbr` — basic example
- `14c-concurrency-channels-and-threads_004.zbr` — basic example
- `14c_pipeline.zbr` — producer/consumer with Chan
- `14c-concurrency-channels-and-threads_006.zbr` — basic example
- `14c-concurrency-channels-and-threads_007.zbr` — basic example
- `14c-concurrency-channels-and-threads_008.zbr` — basic example
- `14c-concurrency-channels-and-threads_009.zbr` — basic example
- `14c-concurrency-channels-and-threads_010.zbr` — basic example
- `14c_parallel_files.zbr` — ThreadPool + Chan for parallel I/O
- `14c-concurrency-channels-and-threads_012.zbr` — basic example
- `14c-concurrency-channels-and-threads_013.zbr` — basic example
- `14c-concurrency-channels-and-threads_014.zbr` — basic example
- `14c-concurrency-channels-and-threads_015.zbr` — basic example
- `14c-concurrency-channels-and-threads_016.zbr` — basic example
- `14c-concurrency-channels-and-threads_017.zbr` — basic example
- `14c-concurrency-channels-and-threads_018.zbr` — basic example
- `14c-concurrency-channels-and-threads_019.zbr` — basic example
- `14c-concurrency-channels-and-threads_020.zbr` — basic example
- `14c-concurrency-channels-and-threads_021.zbr` — basic example
- `14c-concurrency-channels-and-threads_022.zbr` — basic example
- `14c-concurrency-channels-and-threads_023.zbr` — basic example

### 15-Pipelines-and-Function-Composition (16 examples)
- `15-pipelines-and-function-composition_000.zbr` — basic example
- `15-pipelines-and-function-composition_001.zbr` — basic example
- `15_pipeline_basics.zbr` — pipeline operator
- `15_pipeline_chain.zbr` — chaining operations
- `15_pipeline_collections.zbr` — piping through collections
- `15_pipeline_custom.zbr` — custom functions in pipelines
- `15_pipeline_real_world.zbr` — realistic pipeline
- `15_function_composition.zbr` — composing functions
- `15_pipeline_results.zbr` — pipelines with error handling
- `15-pipelines-and-function-composition_009.zbr` — basic example
- `15-pipelines-and-function-composition_010.zbr` — basic example
- `15-pipelines-and-function-composition_011.zbr` — basic example
- `15-pipelines-and-function-composition_012.zbr` — basic example
- `15-pipelines-and-function-composition_013.zbr` — basic example
- `15-pipelines-and-function-composition_014.zbr` — basic example
- `15-pipelines-and-function-composition_015.zbr` — basic example

### 16-Project-1-CLI-Tool (11 examples)
- `cli_args.zbr` — argument parsing
- `file_processor.zbr` — file I/O and text processing
- `pattern_search.zbr` — pattern matching and filtering
- `project1_main.zbr` — orchestrating modules
- `16-project-1-cli-tool_004.zbr` — basic example
- `16-project-1-cli-tool_005.zbr` — basic example
- `16-project-1-cli-tool_006.zbr` — basic example
- `16-project-1-cli-tool_007.zbr` — basic example
- `16-project-1-cli-tool_008.zbr` — basic example
- `16-project-1-cli-tool_009.zbr` — basic example
- `16-project-1-cli-tool_010.zbr` — basic example

### 17-18_Projects-2-3 (8 examples)
- `http_types.zbr` — protocol data structures
- `router.zbr` — request routing and dispatching
- `http_server.zbr` — network server programming
- `frequency_analysis.zbr` — frequency counting and sorting
- `ngram_analysis.zbr` — n-gram extraction and pattern detection
- `similarity_analysis.zbr` — similarity metrics and comparison
- `analysis_main.zbr` — combining analysis modules
- `17-18_projects-2-3_007.zbr` — basic example

### 19-22_Final-Chapters (12 examples)
- `19-22_final-chapters_000.zbr` — basic example
- `19-22_final-chapters_001.zbr` — basic example
- `19-22_final-chapters_002.zbr` — basic example
- `19-22_final-chapters_003.zbr` — basic example
- `19-22_final-chapters_004.zbr` — basic example
- `19-22_final-chapters_005.zbr` — basic example
- `19-22_final-chapters_006.zbr` — basic example
- `19-22_final-chapters_007.zbr` — basic example
- `19-22_final-chapters_008.zbr` — basic example
- `19-22_final-chapters_009.zbr` — basic example
- `19-22_final-chapters_010.zbr` — basic example
- `19-22_final-chapters_011.zbr` — basic example

### 19-Standard-Library-Tour (21 examples)
- `stdlib-string-inspect.zbr` — string properties and inspection methods
- `stdlib-string-case.zbr` — case conversion methods
- `stdlib-string-split-join.zbr` — splitting and joining strings
- `stdlib-string-trim.zbr` — removing whitespace from strings
- `stdlib-string-builder.zbr` — efficient string building
- `stdlib-list-ops.zbr` — list operations and patterns
- `stdlib-hashmap-ops.zbr` — hashmap operations and patterns
- `stdlib-math-constants.zbr` — Math module constants
- `stdlib-math-functions.zbr` — Math module functions
- `stdlib-type-conversions.zbr` — converting between types and strings
- `stdlib-sys-args.zbr` — accessing command-line arguments
- `stdlib-arg-parse.zbr` — structured argument parsing
- `stdlib-json.zbr` — JSON parsing and generation
- `stdlib-file-io.zbr` — file system operations
- `stdlib-console-io.zbr` — printing to console
- `19-standard-library-tour_015.zbr` — basic example
- `19-standard-library-tour_016.zbr` — basic example
- `19-standard-library-tour_017.zbr` — basic example
- `19-standard-library-tour_018.zbr` — basic example
- `19-standard-library-tour_019.zbr` — basic example
- `stdlib-data-processing.zbr` — combining stdlib functions for data processing

### 20-File-IO-and-System-Access (19 examples)
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
- `20-file-io-and-system-access_012.zbr` — basic example
- `20-file-io-and-system-access_013.zbr` — basic example
- `20-file-io-and-system-access_014.zbr` — basic example
- `20-file-io-and-system-access_015.zbr` — basic example
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

### 22-FFI-and-Interop (22 examples)
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
- `greeter.zbr` — @export class for DynLib plugins
- `22-ffi-and-interop_019.zbr` — basic example
- `greeter_host.zbr` — DynLib.open + lookup
- `22-ffi-and-interop_021.zbr` — basic example

### 22b-Build-System-and-Tooling (14 examples)
- `build.zbr` — basic example
- `build.zbr` — imperative-style build script
- `22b-build-system-and-tooling_002.zbr` — basic example
- `22b-build-system-and-tooling_003.zbr` — basic example
- `build.zbr` — declarative-style build script
- `22b-build-system-and-tooling_005.zbr` — basic example
- `22b-build-system-and-tooling_006.zbr` — basic example
- `22b-build-system-and-tooling_007.zbr` — basic example
- `22b-build-system-and-tooling_008.zbr` — basic example
- `22b-build-system-and-tooling_009.zbr` — basic example
- `22b-build-system-and-tooling_010.zbr` — basic example
- `22b-build-system-and-tooling_011.zbr` — basic example
- `22b-build-system-and-tooling_012.zbr` — basic example
- `22b-build-system-and-tooling_013.zbr` — basic example

### 22c-Testing-and-Validation (17 examples)
- `22c_first_test.zbr` — writing a single test
- `22c_assertions.zbr` — the four assertion forms
- `22c_tags.zbr` — @tag-based test filtering
- `22c-testing-and-validation_003.zbr` — basic example
- `arithmetic_test.zbr` — class-scoped tests
- `22c-testing-and-validation_005.zbr` — basic example
- `22c-testing-and-validation_006.zbr` — basic example
- `22c-testing-and-validation_007.zbr` — basic example
- `22c-testing-and-validation_008.zbr` — basic example
- `22c-testing-and-validation_009.zbr` — basic example
- `22c-testing-and-validation_010.zbr` — basic example
- `22c-testing-and-validation_011.zbr` — basic example
- `22c-testing-and-validation_012.zbr` — basic example
- `22c-testing-and-validation_013.zbr` — basic example
- `22c-testing-and-validation_014.zbr` — basic example
- `22c-testing-and-validation_015.zbr` — basic example
- `22c-testing-and-validation_016.zbr` — basic example

### Appendix-A-Grammar (53 examples)
- `appendix-a-grammar_000.zbr` — basic example
- `appendix-a-grammar_001.zbr` — basic example
- `appendix-a-grammar_002.zbr` — basic example
- `appendix-a-grammar_003.zbr` — basic example
- `appendix-a-grammar_004.zbr` — basic example
- `appendix-a-grammar_005.zbr` — basic example
- `appendix-a-grammar_006.zbr` — basic example
- `appendix-a-grammar_007.zbr` — basic example
- `appendix-a-grammar_008.zbr` — basic example
- `appendix-a-grammar_009.zbr` — basic example
- `appendix-a-grammar_010.zbr` — basic example
- `appendix-a-grammar_011.zbr` — basic example
- `appendix-a-grammar_012.zbr` — basic example
- `appendix-a-grammar_013.zbr` — basic example
- `appendix-a-grammar_014.zbr` — basic example
- `appendix-a-grammar_015.zbr` — basic example
- `appendix-a-grammar_016.zbr` — basic example
- `appendix-a-grammar_017.zbr` — basic example
- `appendix-a-grammar_018.zbr` — basic example
- `appendix-a-grammar_019.zbr` — basic example
- `appendix-a-grammar_020.zbr` — basic example
- `appendix-a-grammar_021.zbr` — basic example
- `appendix-a-grammar_022.zbr` — basic example
- `appendix-a-grammar_023.zbr` — basic example
- `appendix-a-grammar_024.zbr` — basic example
- `appendix-a-grammar_025.zbr` — basic example
- `appendix-a-grammar_026.zbr` — basic example
- `appendix-a-grammar_027.zbr` — basic example
- `appendix-a-grammar_028.zbr` — basic example
- `appendix-a-grammar_029.zbr` — basic example
- `appendix-a-grammar_030.zbr` — basic example
- `appendix-a-grammar_031.zbr` — basic example
- `appendix-a-grammar_032.zbr` — basic example
- `appendix-a-grammar_033.zbr` — basic example
- `appendix-a-grammar_034.zbr` — basic example
- `appendix-a-grammar_035.zbr` — basic example
- `appendix-a-grammar_036.zbr` — basic example
- `appendix-a-grammar_037.zbr` — basic example
- `appendix-a-grammar_038.zbr` — basic example
- `appendix-a-grammar_039.zbr` — basic example
- `appendix-a-grammar_040.zbr` — basic example
- `appendix-a-grammar_041.zbr` — basic example
- `appendix-a-grammar_042.zbr` — basic example
- `appendix-a-grammar_043.zbr` — basic example
- `appendix-a-grammar_044.zbr` — basic example
- `appendix-a-grammar_045.zbr` — basic example
- `appendix-a-grammar_046.zbr` — basic example
- `appendix-a-grammar_047.zbr` — basic example
- `appendix-a-grammar_048.zbr` — basic example
- `appendix-a-grammar_049.zbr` — basic example
- `appendix-a-grammar_050.zbr` — basic example
- `appendix-a-grammar_051.zbr` — basic example
- `appendix-a-grammar_052.zbr` — basic example

### Appendix-B-Stdlib (50 examples)
- `appendix-b-stdlib_000.zbr` — basic example
- `appendix-b-stdlib_001.zbr` — basic example
- `appendix-b-stdlib_002.zbr` — basic example
- `appendix-b-stdlib_003.zbr` — basic example
- `appendix-b-stdlib_004.zbr` — basic example
- `appendix-b-stdlib_005.zbr` — basic example
- `appendix-b-stdlib_006.zbr` — basic example
- `appendix-b-stdlib_007.zbr` — basic example
- `appendix-b-stdlib_008.zbr` — basic example
- `appendix-b-stdlib_009.zbr` — basic example
- `appendix-b-stdlib_010.zbr` — basic example
- `appendix-b-stdlib_011.zbr` — basic example
- `appendix-b-stdlib_012.zbr` — basic example
- `appendix-b-stdlib_013.zbr` — basic example
- `appendix-b-stdlib_014.zbr` — basic example
- `appendix-b-stdlib_015.zbr` — basic example
- `appendix-b-stdlib_016.zbr` — basic example
- `appendix-b-stdlib_017.zbr` — basic example
- `appendix-b-stdlib_018.zbr` — basic example
- `appendix-b-stdlib_019.zbr` — basic example
- `appendix-b-stdlib_020.zbr` — basic example
- `appendix-b-stdlib_021.zbr` — basic example
- `appendix-b-stdlib_022.zbr` — basic example
- `appendix-b-stdlib_023.zbr` — basic example
- `appendix-b-stdlib_024.zbr` — basic example
- `appendix-b-stdlib_025.zbr` — basic example
- `appendix-b-stdlib_026.zbr` — basic example
- `appendix-b-stdlib_027.zbr` — basic example
- `appendix-b-stdlib_028.zbr` — basic example
- `appendix-b-stdlib_029.zbr` — basic example
- `appendix-b-stdlib_030.zbr` — basic example
- `appendix-b-stdlib_031.zbr` — basic example
- `appendix-b-stdlib_032.zbr` — basic example
- `appendix-b-stdlib_033.zbr` — basic example
- `appendix-b-stdlib_034.zbr` — basic example
- `appendix-b-stdlib_035.zbr` — basic example
- `appendix-b-stdlib_036.zbr` — basic example
- `appendix-b-stdlib_037.zbr` — basic example
- `appendix-b-stdlib_038.zbr` — basic example
- `appendix-b-stdlib_039.zbr` — basic example
- `appendix-b-stdlib_040.zbr` — basic example
- `appendix-b-stdlib_041.zbr` — basic example
- `appendix-b-stdlib_042.zbr` — basic example
- `appendix-b-stdlib_043.zbr` — basic example
- `appendix-b-stdlib_044.zbr` — basic example
- `appendix-b-stdlib_045.zbr` — basic example
- `appendix-b-stdlib_046.zbr` — basic example
- `appendix-b-stdlib_047.zbr` — basic example
- `appendix-b-stdlib_048.zbr` — basic example
- `appendix-b-stdlib_049.zbr` — basic example

### Appendix-C-Troubleshooting (62 examples)
- `appendix-c-troubleshooting_000.zbr` — basic example
- `appendix-c-troubleshooting_001.zbr` — basic example
- `appendix-c-troubleshooting_002.zbr` — basic example
- `appendix-c-troubleshooting_003.zbr` — basic example
- `appendix-c-troubleshooting_004.zbr` — basic example
- `appendix-c-troubleshooting_005.zbr` — basic example
- `appendix-c-troubleshooting_006.zbr` — basic example
- `appendix-c-troubleshooting_007.zbr` — basic example
- `appendix-c-troubleshooting_008.zbr` — basic example
- `appendix-c-troubleshooting_009.zbr` — basic example
- `appendix-c-troubleshooting_010.zbr` — basic example
- `appendix-c-troubleshooting_011.zbr` — basic example
- `appendix-c-troubleshooting_012.zbr` — basic example
- `appendix-c-troubleshooting_013.zbr` — basic example
- `appendix-c-troubleshooting_014.zbr` — basic example
- `appendix-c-troubleshooting_015.zbr` — basic example
- `appendix-c-troubleshooting_016.zbr` — basic example
- `appendix-c-troubleshooting_017.zbr` — basic example
- `appendix-c-troubleshooting_018.zbr` — basic example
- `appendix-c-troubleshooting_019.zbr` — basic example
- `appendix-c-troubleshooting_020.zbr` — basic example
- `appendix-c-troubleshooting_021.zbr` — basic example
- `appendix-c-troubleshooting_022.zbr` — basic example
- `appendix-c-troubleshooting_023.zbr` — basic example
- `appendix-c-troubleshooting_024.zbr` — basic example
- `appendix-c-troubleshooting_025.zbr` — basic example
- `appendix-c-troubleshooting_026.zbr` — basic example
- `appendix-c-troubleshooting_027.zbr` — basic example
- `appendix-c-troubleshooting_028.zbr` — basic example
- `appendix-c-troubleshooting_029.zbr` — basic example
- `appendix-c-troubleshooting_030.zbr` — basic example
- `appendix-c-troubleshooting_031.zbr` — basic example
- `appendix-c-troubleshooting_032.zbr` — basic example
- `appendix-c-troubleshooting_033.zbr` — basic example
- `appendix-c-troubleshooting_034.zbr` — basic example
- `appendix-c-troubleshooting_035.zbr` — basic example
- `appendix-c-troubleshooting_036.zbr` — basic example
- `appendix-c-troubleshooting_037.zbr` — basic example
- `appendix-c-troubleshooting_038.zbr` — basic example
- `appendix-c-troubleshooting_039.zbr` — basic example
- `appendix-c-troubleshooting_040.zbr` — basic example
- `appendix-c-troubleshooting_041.zbr` — basic example
- `appendix-c-troubleshooting_042.zbr` — basic example
- `appendix-c-troubleshooting_043.zbr` — basic example
- `appendix-c-troubleshooting_044.zbr` — basic example
- `appendix-c-troubleshooting_045.zbr` — basic example
- `appendix-c-troubleshooting_046.zbr` — basic example
- `appendix-c-troubleshooting_047.zbr` — basic example
- `appendix-c-troubleshooting_048.zbr` — basic example
- `appendix-c-troubleshooting_049.zbr` — basic example
- `appendix-c-troubleshooting_050.zbr` — basic example
- `appendix-c-troubleshooting_051.zbr` — basic example
- `appendix-c-troubleshooting_052.zbr` — basic example
- `appendix-c-troubleshooting_053.zbr` — basic example
- `appendix-c-troubleshooting_054.zbr` — basic example
- `appendix-c-troubleshooting_055.zbr` — basic example
- `appendix-c-troubleshooting_056.zbr` — basic example
- `appendix-c-troubleshooting_057.zbr` — basic example
- `appendix-c-troubleshooting_058.zbr` — basic example
- `appendix-c-troubleshooting_059.zbr` — basic example
- `appendix-c-troubleshooting_060.zbr` — basic example
- `appendix-c-troubleshooting_061.zbr` — basic example

### Appendix-D-Attributes (8 examples)
- `appendix-d-attributes_000.zbr` — basic example
- `appendix-d-attributes_001.zbr` — basic example
- `appendix-d-attributes_002.zbr` — basic example
- `appendix-d-attributes_003.zbr` — basic example
- `appendix-d-attributes_004.zbr` — basic example
- `appendix-d-attributes_005.zbr` — basic example
- `appendix-d-attributes_006.zbr` — basic example
- `appendix-d-attributes_007.zbr` — basic example

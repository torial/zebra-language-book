# Zebra Programming Book - Code Examples

This directory contains 795 runnable code examples extracted from the Zebra Programming Book.

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

Each `.zbr` file is one code block from the book. Many are complete programs; some are
fragments illustrating one construct, one half of a two-module example, or a deliberate
"common mistake". Run a complete one with:

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

It checks each example with the compiler's front end (`zebra -c`: parse and type-check,
no Zig build, no run) and fails when an example that used to pass stops passing. It does
NOT prove an example builds or prints what its comments say -- `--full` adds a real
build (`--check-full`) for the examples that have a `main`.

## By the Numbers

- **Total Examples:** 795
- **Chapters Covered:** 36
- **Topics:** 220

## Quick Reference

### Examples by Chapter


### 01-Getting-Started (13 examples)
- `hello.zbr` — hello world, the print function
- `01-getting-started_498a42ab.zbr` — basic example
- `01-getting-started_f54e0a8a.zbr` — basic example
- `01-getting-started_e480b520.zbr` — basic example
- `greet.zbr` — variables, string interpolation
- `01-getting-started_b069eac4.zbr` — basic example
- `01-getting-started_18a99d1c.zbr` — basic example
- `01-getting-started_57cf93e3.zbr` — basic example
- `math_utils.zbr` — basic example
- `main.zbr` — basic example
- `01-getting-started_b931f5aa.zbr` — basic example
- `01-getting-started_dc5bda7c.zbr` — basic example
- `01-getting-started_1abdcdcc.zbr` — basic example

### 02-Values-and-Types (24 examples)
- `02_integers.zbr` — integer types, arithmetic
- `02-values-and-types_8821ebd1.zbr` — basic example
- `02_floats.zbr` — float types, precision
- `02_bools.zbr` — boolean values, logic
- `02_strings.zbr` — string type, string operations
- `02_tuples.zbr` — tuple types, literals, destructuring, and indexing
- `02-values-and-types_350676a8.zbr` — basic example
- `02-values-and-types_7861a141.zbr` — basic example
- `02-values-and-types_5fb1a5d4.zbr` — basic example
- `02_comparisons.zbr` — comparison operators
- `02-values-and-types_9cd62d3c.zbr` — basic example
- `02_conversions.zbr` — type conversion
- `02_nullables.zbr` — nullable types introduction
- `02-values-and-types_ec972f5c.zbr` — basic example
- `02_user_data.zbr` — realistic variable use
- `02-values-and-types_e0c51a57.zbr` — basic example
- `02-values-and-types_f15b5132.zbr` — basic example
- `02-values-and-types_3be0afa8.zbr` — basic example
- `02-values-and-types_91e9bda8.zbr` — basic example
- `02-values-and-types_6d68373c.zbr` — basic example
- `02-values-and-types_c6bd144c.zbr` — basic example
- `02-values-and-types_58d14b38.zbr` — basic example
- `02-values-and-types_44d051d9.zbr` — basic example
- `02-values-and-types_64a41368.zbr` — basic example

### 03-Collections (17 examples)
- `03_lists.zbr` — list creation and access
- `03_list_ops.zbr` — list manipulation
- `03_iteration.zbr` — different iteration styles
- `03_hashmaps.zbr` — hashmap creation and access
- `03_hashmap_ops.zbr` — hashmap manipulation
- `03_dedup.zbr` — using HashMap for uniqueness
- `03_real_world.zbr` — collections in realistic scenarios
- `03_patterns.zbr` — collection patterns
- `03-collections_815f5ccf.zbr` — basic example
- `03-collections_006870da.zbr` — basic example
- `03-collections_24998c4e.zbr` — basic example
- `03-collections_72452026.zbr` — basic example
- `03-collections_f5bad3b8.zbr` — basic example
- `03-collections_1e74492f.zbr` — basic example
- `03-collections_49b6ab22.zbr` — basic example
- `03-collections_a14c856b.zbr` — basic example
- `03-collections_d0aa4532.zbr` — basic example

### 04-Functions-and-Scope (26 examples)
- `04_functions.zbr` — function definition and calling
- `04_multi_params.zbr` — multiple parameters
- `04_void.zbr` — functions that don't return values
- `04_scope.zbr` — variable scope
- `04-functions-and-scope_ad9fd5bf.zbr` — basic example
- `04_closures.zbr` — closures and variable capture
- `04_capture.zbr` — capture blocks
- `04_utilities.zbr` — practical function use
- `04_patterns.zbr` — early return pattern
- `04-functions-and-scope_fe19b111.zbr` — basic example
- `04-functions-and-scope_20f27014.zbr` — basic example
- `04_higher_order.zbr` — functions as arguments
- `04_sig.zbr` — named function types with sig
- `04-functions-and-scope_7920fbe7.zbr` — basic example
- `04-functions-and-scope_38b439c7.zbr` — basic example
- `04_lambda_arg.zbr` — lambda as call argument (statement-body form)
- `04_nested_lambda.zbr` — nested lambda as argument
- `04-functions-and-scope_a08f772f.zbr` — basic example
- `04-functions-and-scope_c277040d.zbr` — basic example
- `04-functions-and-scope_1d066557.zbr` — basic example
- `04-functions-and-scope_c307c846.zbr` — basic example
- `04-functions-and-scope_9620d369.zbr` — basic example
- `04-functions-and-scope_95a99283.zbr` — basic example
- `04-functions-and-scope_8f662d40.zbr` — basic example
- `04-functions-and-scope_1b6405a4.zbr` — basic example
- `04-functions-and-scope_7a99a107.zbr` — basic example

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
- `05-control-flow_842f4539.zbr` — basic example
- `05-control-flow_d101b2ab.zbr` — basic example
- `05-control-flow_64c681e6.zbr` — basic example
- `05-control-flow_ed7fddf0.zbr` — basic example
- `05-control-flow_e4036fa8.zbr` — basic example
- `05-control-flow_1a006f1a.zbr` — basic example
- `05-control-flow_39d3b13e.zbr` — basic example
- `05-control-flow_deb62335.zbr` — basic example
- `05-control-flow_165edb51.zbr` — basic example
- `05-control-flow_9f4f061d.zbr` — basic example
- `05-control-flow_8bbd15f6.zbr` — basic example
- `05-control-flow_241852de.zbr` — basic example

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
- `06-strings-and-unicode_20ce1a50.zbr` — basic example
- `06-strings-and-unicode_e7a97887.zbr` — basic example
- `06-strings-and-unicode_2bf0ec41.zbr` — basic example
- `06-strings-and-unicode_ccbfc266.zbr` — basic example
- `06-strings-and-unicode_f4191d80.zbr` — basic example
- `06-strings-and-unicode_0235037c.zbr` — basic example
- `06-strings-and-unicode_692f9664.zbr` — basic example
- `06-strings-and-unicode_edc42ee7.zbr` — basic example
- `06-strings-and-unicode_3a204be8.zbr` — basic example
- `06-strings-and-unicode_1cce7ad8.zbr` — basic example
- `06-strings-and-unicode_0ee1576d.zbr` — basic example
- `06-strings-and-unicode_2e9caf9b.zbr` — basic example

### 07-Classes-and-Instances (18 examples)
- `07_class_basic.zbr` — class definition, cue init
- `07_init.zbr` — field defaults vs. explicit init
- `07_methods.zbr` — instance methods
- `07_static.zbr` — static (class-level) methods
- `07-classes-and-instances_14ca828c.zbr` — basic example
- `07-classes-and-instances_6e8129f9.zbr` — basic example
- `07-classes-and-instances_5bbcf3df.zbr` — basic example
- `07-classes-and-instances_2bda6c7b.zbr` — basic example
- `07_user_system.zbr` — realistic class design
- `07-classes-and-instances_b7847e8f.zbr` — basic example
- `07-classes-and-instances_8f4af621.zbr` — basic example
- `07-classes-and-instances_206fd7cf.zbr` — basic example
- `07-classes-and-instances_acd52f2c.zbr` — basic example
- `07-classes-and-instances_80f4a214.zbr` — basic example
- `07-classes-and-instances_0fd5c6ea.zbr` — basic example
- `07-classes-and-instances_f4d84292.zbr` — basic example
- `07-classes-and-instances_5df57d66.zbr` — basic example
- `07-classes-and-instances_999d2640.zbr` — basic example

### 07b-Structs-Unions-and-Value-Types (11 examples)
- `07b_struct_basic.zbr` — struct definition and value semantics
- `07b_except.zbr` — except struct update syntax
- `07b-structs-unions-and-value-types_6dc357df.zbr` — basic example
- `07b_enum.zbr` — enum types
- `07b_union_basic.zbr` — union definition and construction
- `07b_branch.zbr` — branch pattern matching
- `07b-structs-unions-and-value-types_57becac2.zbr` — basic example
- `07b_heap_indirect.zbr` — ^T heap indirection
- `07b-structs-unions-and-value-types_c4ad853b.zbr` — basic example
- `07b_mini_ast.zbr` — combining structs, unions, and ^T
- `07b-structs-unions-and-value-types_520cba8b.zbr` — basic example

### 08-Interfaces-and-Protocols (17 examples)
- `08_interface_basic.zbr` — interface definition
- `08_interface_methods.zbr` — interface with multiple methods
- `08_polymorphism.zbr` — polymorphic behavior
- `08_collection_interface.zbr` — storing different implementations
- `08_logger_system.zbr` — realistic interface use
- `08-interfaces-and-protocols_68521313.zbr` — basic example
- `08-interfaces-and-protocols_7dbcc68c.zbr` — basic example
- `08-interfaces-and-protocols_6949889b.zbr` — basic example
- `08-interfaces-and-protocols_1e528267.zbr` — basic example
- `08-interfaces-and-protocols_c522f5dc.zbr` — basic example
- `08-interfaces-and-protocols_ef196069.zbr` — basic example
- `08-interfaces-and-protocols_a0d9b811.zbr` — basic example
- `08-interfaces-and-protocols_5721bf55.zbr` — basic example
- `08-interfaces-and-protocols_759c96d9.zbr` — basic example
- `08-interfaces-and-protocols_f62f36a2.zbr` — basic example
- `08-interfaces-and-protocols_c0c84554.zbr` — basic example
- `08-interfaces-and-protocols_afa3ef4b.zbr` — basic example

### 09-Composition-and-Mixins (15 examples)
- `09_mixin_basic.zbr` — declaring and using mixins
- `09-composition-and-mixins_5791e66f.zbr` — basic example
- `09_composition.zbr` — composition with helper classes
- `09_multiple_mixins.zbr` — combining multiple mixins
- `09_polymorphism.zbr` — interface-based polymorphism (instead of inheritance)
- `09_document_capabilities.zbr` — combining interface + mixin + composition
- `09-composition-and-mixins_60402067.zbr` — basic example
- `09-composition-and-mixins_81577d7a.zbr` — basic example
- `09-composition-and-mixins_a62e5f38.zbr` — basic example
- `09-composition-and-mixins_c3430bba.zbr` — basic example
- `09-composition-and-mixins_37f752cf.zbr` — basic example
- `09-composition-and-mixins_5e2ee9d9.zbr` — basic example
- `09-composition-and-mixins_f2ee0e78.zbr` — basic example
- `09-composition-and-mixins_d011b693.zbr` — basic example
- `09-composition-and-mixins_b1cb8fa5.zbr` — basic example

### 10-Properties-and-Computed-Values (19 examples)
- `10_getter.zbr` — computed properties
- `10_derived.zbr` — deriving values from fields
- `10_setter_validation.zbr` — setters with validation
- `10_setter_effects.zbr` — setters with side effects
- `10_computed.zbr` — expensive computed properties
- `10_lazy_init.zbr` — lazy initialization
- `10_temperature.zbr` — properties in realistic scenarios
- `10_config.zbr` — configuration management
- `10-properties-and-computed-values_6387430c.zbr` — basic example
- `10-properties-and-computed-values_a8b69e63.zbr` — basic example
- `10-properties-and-computed-values_4a750d17.zbr` — basic example
- `10-properties-and-computed-values_f7082870.zbr` — basic example
- `10-properties-and-computed-values_061cd3ff.zbr` — basic example
- `10-properties-and-computed-values_c508b6ad.zbr` — basic example
- `10-properties-and-computed-values_c4ebd993.zbr` — basic example
- `10-properties-and-computed-values_ec28210c.zbr` — basic example
- `10-properties-and-computed-values_7e7e7813.zbr` — basic example
- `10-properties-and-computed-values_16e0e3cf.zbr` — basic example
- `10-properties-and-computed-values_d969d240.zbr` — basic example

### 10b-Modules-Namespaces-and-Visibility (36 examples)
- `math_utils.zbr` — basic example
- `main.zbr` — basic example
- `main__2.zbr` — basic example
- `10b-modules-namespaces-and-visibility_dcfa7b54.zbr` — basic example
- `10b-modules-namespaces-and-visibility_c0cfefd6.zbr` — basic example
- `10b-modules-namespaces-and-visibility_ecdd924b.zbr` — basic example
- `wallet.zbr` — basic example
- `main__3.zbr` — basic example
- `colors.zbr` — basic example
- `10b-modules-namespaces-and-visibility_9db5d7b1.zbr` — basic example
- `10b-modules-namespaces-and-visibility_e10b63b7.zbr` — basic example
- `10b-modules-namespaces-and-visibility_afbd02f8.zbr` — basic example
- `10b-modules-namespaces-and-visibility_88d5cd55.zbr` — basic example
- `10b-modules-namespaces-and-visibility_8ecdbb90.zbr` — basic example
- `10b-modules-namespaces-and-visibility_954bbcd9.zbr` — basic example
- `helpers.zbr` — basic example
- `main__4.zbr` — basic example
- `Wallet__2.zbr` — basic example
- `Wallet.transactions.zbr` — basic example
- `10b-modules-namespaces-and-visibility_957755c7.zbr` — basic example
- `10b-modules-namespaces-and-visibility_ceaa36c9.zbr` — basic example
- `10b-modules-namespaces-and-visibility_38e75178.zbr` — basic example
- `10b-modules-namespaces-and-visibility_37d7f8a5.zbr` — basic example
- `10b-modules-namespaces-and-visibility_204aadbb.zbr` — basic example
- `10b-modules-namespaces-and-visibility_cd323f0c.zbr` — basic example
- `10b-modules-namespaces-and-visibility_a21845dc.zbr` — basic example
- `10b-modules-namespaces-and-visibility_2feef21c.zbr` — basic example
- `10b-modules-namespaces-and-visibility_e574ce18.zbr` — basic example
- `10b-modules-namespaces-and-visibility_e30ee4d2.zbr` — basic example
- `10b-modules-namespaces-and-visibility_bf1dca5c.zbr` — basic example
- `10b-modules-namespaces-and-visibility_36b894bc.zbr` — basic example
- `10b-modules-namespaces-and-visibility_12af035b.zbr` — basic example
- `10b-modules-namespaces-and-visibility_617af081.zbr` — basic example
- `10b-modules-namespaces-and-visibility_9ac03b78.zbr` — basic example
- `10b-modules-namespaces-and-visibility_e996c51f.zbr` — basic example
- `10b-modules-namespaces-and-visibility_bf9e70d6.zbr` — basic example

### 11-Nil-Tracking-and-Safety (20 examples)
- `11_nullable.zbr` — nullable types
- `11_nil_check.zbr` — nil checking
- `11_narrowing.zbr` — type narrowing
- `11-nil-tracking-and-safety_fe35ee05.zbr` — basic example
- `11_if_as.zbr` — optional unwrap binding form
- `11-nil-tracking-and-safety_50b4484d.zbr` — basic example
- `11_unwrap.zbr` — force-unwrap operator
- `11_unwrap_or.zbr` — safe unwrapping
- `11_database.zbr` — nil in realistic scenarios
- `11-nil-tracking-and-safety_9480165c.zbr` — basic example
- `11-nil-tracking-and-safety_3f2cc56c.zbr` — basic example
- `11-nil-tracking-and-safety_976512ff.zbr` — basic example
- `11-nil-tracking-and-safety_4fa25bd5.zbr` — basic example
- `11-nil-tracking-and-safety_376ed26c.zbr` — basic example
- `11-nil-tracking-and-safety_20db6b3e.zbr` — basic example
- `11-nil-tracking-and-safety_4e2f6de0.zbr` — basic example
- `11-nil-tracking-and-safety_ea7180a9.zbr` — basic example
- `11-nil-tracking-and-safety_af3a8379.zbr` — basic example
- `11-nil-tracking-and-safety_f1b0080c.zbr` — basic example
- `11-nil-tracking-and-safety_16528b75.zbr` — basic example

### 12-Error-Handling-with-Results (9 examples)
- `12_throws_basic.zbr` — throws annotation
- `12_raise.zbr` — raise statement
- `12_method_catch.zbr` — method-level catch clause
- `12_catch_binding.zbr` — catch with error binding
- `12_catch_expr.zbr` — catch expression for defaults
- `12_propagation.zbr` — error propagation
- `12_api_client.zbr` — realistic error handling
- `12-error-handling-with-results_d274c687.zbr` — basic example
- `12-error-handling-with-results_5e79caeb.zbr` — basic example

### 13-Generics-and-Type-Constraints (19 examples)
- `13-generics-and-type-constraints_fcf4cbb1.zbr` — basic example
- `13_generic_container.zbr` — generic class definition
- `13_generic_pair.zbr` — multiple type parameters
- `13_generic_methods.zbr` — generic methods
- `13_generic_function.zbr` — top-level generic function declaration
- `13_generic_collections.zbr` — using generic stdlib types
- `13_type_constraints.zbr` — interface constraints
- `13_generic_constraints_advanced.zbr` — constraints in generic methods
- `13_type_aliases.zbr` — type aliases with constraints
- `13_refinement_types.zbr` — parametric refinement types
- `13-generics-and-type-constraints_a9621b9b.zbr` — basic example
- `13_generic_cache.zbr` — realistic generic class
- `13-generics-and-type-constraints_77ff531d.zbr` — basic example
- `13-generics-and-type-constraints_2c044550.zbr` — basic example
- `13-generics-and-type-constraints_8b342377.zbr` — basic example
- `13-generics-and-type-constraints_3c7724b9.zbr` — basic example
- `13-generics-and-type-constraints_c3dd165d.zbr` — basic example
- `13-generics-and-type-constraints_2b47179c.zbr` — basic example
- `13-generics-and-type-constraints_b13a66ab.zbr` — basic example

### 14-Contracts-and-Assertions (16 examples)
- `14-contracts-and-assertions_2785b00d.zbr` — basic example
- `14_require.zbr` — precondition checking with require
- `14_ensure.zbr` — postcondition checking with ensure
- `14_ensure_result.zbr` — result in ensure clauses
- `14_ensure_old.zbr` — old snapshots in ensure clauses
- `14_invariant.zbr` — class invariants
- `14_assert.zbr` — assert statement
- `14_sorted_list.zbr` — combining require, ensure, and invariant
- `14-contracts-and-assertions_c9345dac.zbr` — basic example
- `14-contracts-and-assertions_3a406f6b.zbr` — basic example
- `14-contracts-and-assertions_65e55ff5.zbr` — basic example
- `14-contracts-and-assertions_5adeef34.zbr` — basic example
- `14-contracts-and-assertions_ddfa9af6.zbr` — basic example
- `14-contracts-and-assertions_993950d3.zbr` — basic example
- `14-contracts-and-assertions_d853fd97.zbr` — basic example
- `14-contracts-and-assertions_024f63e6.zbr` — basic example

### 14b-Memory-Management-and-Lifetimes (25 examples)
- `14b-memory-management-and-lifetimes_177786cc.zbr` — basic example
- `14b-memory-management-and-lifetimes_70896cbb.zbr` — basic example
- `14b-memory-management-and-lifetimes_0e543589.zbr` — basic example
- `14b-memory-management-and-lifetimes_8f128a32.zbr` — basic example
- `14b-memory-management-and-lifetimes_57c9399b.zbr` — basic example
- `14b-memory-management-and-lifetimes_2911730e.zbr` — basic example
- `14b-memory-management-and-lifetimes_e8865ebd.zbr` — basic example
- `14b-memory-management-and-lifetimes_edc3f51a.zbr` — basic example
- `14b-memory-management-and-lifetimes_8d8bb072.zbr` — basic example
- `14b-memory-management-and-lifetimes_25265c25.zbr` — basic example
- `14b-memory-management-and-lifetimes_651c75c0.zbr` — basic example
- `14b-memory-management-and-lifetimes_62f04674.zbr` — basic example
- `14b_streaming_processor.zbr` — allocate + <<- + using together
- `14b-memory-management-and-lifetimes_ce9fd152.zbr` — basic example
- `14b-memory-management-and-lifetimes_e11c9eba.zbr` — basic example
- `14b-memory-management-and-lifetimes_235da576.zbr` — basic example
- `14b-memory-management-and-lifetimes_295f4141.zbr` — basic example
- `14b-memory-management-and-lifetimes_096abb79.zbr` — basic example
- `14b-memory-management-and-lifetimes_59263fa8.zbr` — basic example
- `14b-memory-management-and-lifetimes_5cb23dd9.zbr` — basic example
- `14b-memory-management-and-lifetimes_10610e58.zbr` — basic example
- `14b-memory-management-and-lifetimes_40d1cec3.zbr` — basic example
- `14b-memory-management-and-lifetimes_b2f9deb6.zbr` — basic example
- `14b-memory-management-and-lifetimes_7378df50.zbr` — basic example
- `14b-memory-management-and-lifetimes_be3cf20d.zbr` — basic example

### 14c-Concurrency-Channels-and-Threads (24 examples)
- `14c-concurrency-channels-and-threads_dea2f875.zbr` — basic example
- `14c-concurrency-channels-and-threads_c557f7ab.zbr` — basic example
- `14c-concurrency-channels-and-threads_ef8cbd87.zbr` — basic example
- `14c-concurrency-channels-and-threads_5af9a940.zbr` — basic example
- `14c-concurrency-channels-and-threads_fad2e03c.zbr` — basic example
- `14c_pipeline.zbr` — producer/consumer with Chan
- `14c-concurrency-channels-and-threads_23133e47.zbr` — basic example
- `14c-concurrency-channels-and-threads_8a69f176.zbr` — basic example
- `14c-concurrency-channels-and-threads_0440916c.zbr` — basic example
- `14c-concurrency-channels-and-threads_5e59ccbf.zbr` — basic example
- `14c-concurrency-channels-and-threads_6cb4cf2a.zbr` — basic example
- `14c_parallel_files.zbr` — ThreadPool + Chan for parallel I/O
- `14c-concurrency-channels-and-threads_7fd29274.zbr` — basic example
- `14c-concurrency-channels-and-threads_872d3c5e.zbr` — basic example
- `14c-concurrency-channels-and-threads_5967e626.zbr` — basic example
- `14c-concurrency-channels-and-threads_75531924.zbr` — basic example
- `14c-concurrency-channels-and-threads_dcba6f55.zbr` — basic example
- `14c-concurrency-channels-and-threads_54867e72.zbr` — basic example
- `14c-concurrency-channels-and-threads_8684b53a.zbr` — basic example
- `14c-concurrency-channels-and-threads_bed5ba0b.zbr` — basic example
- `14c-concurrency-channels-and-threads_785634a5.zbr` — basic example
- `14c-concurrency-channels-and-threads_bbfa879b.zbr` — basic example
- `14c-concurrency-channels-and-threads_2cd63d75.zbr` — basic example
- `14c-concurrency-channels-and-threads_8e61a283.zbr` — basic example

### 15-Pipelines-and-Function-Composition (16 examples)
- `15-pipelines-and-function-composition_2b11bfa8.zbr` — basic example
- `15-pipelines-and-function-composition_7fd22695.zbr` — basic example
- `15_pipeline_basics.zbr` — pipeline operator
- `15_pipeline_chain.zbr` — chaining operations
- `15_pipeline_collections.zbr` — piping through collections
- `15_pipeline_custom.zbr` — custom functions in pipelines
- `15_pipeline_real_world.zbr` — realistic pipeline
- `15_function_composition.zbr` — composing functions
- `15_pipeline_results.zbr` — pipelines with error handling
- `15-pipelines-and-function-composition_61e63207.zbr` — basic example
- `15-pipelines-and-function-composition_2ef32288.zbr` — basic example
- `15-pipelines-and-function-composition_5edb027e.zbr` — basic example
- `15-pipelines-and-function-composition_a1d66172.zbr` — basic example
- `15-pipelines-and-function-composition_0ca524ae.zbr` — basic example
- `15-pipelines-and-function-composition_8da91d38.zbr` — basic example
- `15-pipelines-and-function-composition_cfcc4560.zbr` — basic example

### 16-Project-1-CLI-Tool (11 examples)
- `cli_args.zbr` — argument parsing
- `file_processor.zbr` — file I/O and text processing
- `pattern_search.zbr` — pattern matching and filtering
- `project1_main.zbr` — orchestrating modules
- `16-project-1-cli-tool_7d59bc64.zbr` — basic example
- `16-project-1-cli-tool_d6c2d473.zbr` — basic example
- `16-project-1-cli-tool_40411c20.zbr` — basic example
- `16-project-1-cli-tool_4391557c.zbr` — basic example
- `16-project-1-cli-tool_1e39043c.zbr` — basic example
- `16-project-1-cli-tool_acd8f0d1.zbr` — basic example
- `16-project-1-cli-tool_56204edf.zbr` — basic example

### 17-18_Projects-2-3 (8 examples)
- `user_store.zbr` — module-level state, a small data model, JSON output
- `router.zbr` — routing on method and path, path parameters, status codes
- `http_server.zbr` — starting a real server with Http.serve
- `frequency_analysis.zbr` — frequency counting and sorting
- `ngram_analysis.zbr` — n-gram extraction and pattern detection
- `similarity_analysis.zbr` — similarity metrics and comparison
- `analysis_main.zbr` — combining analysis modules
- `17-18_projects-2-3_5e9b37d2.zbr` — basic example

### 18b-GUI-Applications (22 examples)
- `counter.zbr` — MVU, Gui.run, g.send, hbox layout
- `greeter.zbr` — payload messages, g.field, mixed unions
- `widgets.zbr` — toggle, field, slider; the on function
- `layout.zbr` — using g.vbox / g.hbox, nesting, stretch
- `18b-gui-applications_9904c184.zbr` — basic example
- `settings_form.zbr` — g.beginForm / g.endForm, a widget's label as its row label, m except
- `file_tree.zbr` — g.beginTree / treeNode / treeLeaf / treePop / endTree, the model owns what is open
- `board.zbr` — g.area, a draw closure with capture, the mouse-press message
- `canvas.zbr` — g.canvas, mouse move/release and keys as messages, a drag in update
- `18b-gui-applications_571561da.zbr` — basic example
- `clipboard.zbr` — g.tooltip, Gui.clipboardText / setClipboardText, treeNodeIcon / treeLeafIcon
- `toolbar.zbr` — g.beginToolbar / tool / toolIcon / toolSeparator / toolEnabled, a toolbar that follows the model
- `editor.zbr` — CodeEditor, class Model, widget handles
- `18b-gui-applications_f06072f8.zbr` — basic example
- `18b-gui-applications_0cbfa83f.zbr` — basic example
- `18b-gui-applications_3d7a47c8.zbr` — basic example
- `18b-gui-applications_66d3f2a3.zbr` — basic example
- `18b-gui-applications_6ae0e22b.zbr` — basic example
- `18b-gui-applications_90ee5102.zbr` — basic example
- `18b-gui-applications_4a1ded9b.zbr` — basic example
- `18b-gui-applications_8f61992f.zbr` — basic example
- `18b-gui-applications_34d6a6b9.zbr` — basic example

### 19-22_Final-Chapters (12 examples)
- `19-22_final-chapters_a0432448.zbr` — basic example
- `19-22_final-chapters_e3975313.zbr` — basic example
- `19-22_final-chapters_424b329b.zbr` — basic example
- `19-22_final-chapters_99ceb0b3.zbr` — basic example
- `19-22_final-chapters_7d3e3913.zbr` — basic example
- `19-22_final-chapters_ebc1f62a.zbr` — basic example
- `19-22_final-chapters_6d4557da.zbr` — basic example
- `19-22_final-chapters_6b14ee37.zbr` — basic example
- `19-22_final-chapters_a40b8bbd.zbr` — basic example
- `19-22_final-chapters_eeba5bbf.zbr` — basic example
- `19-22_final-chapters_9f6e3064.zbr` — basic example
- `19-22_final-chapters_b28cfe07.zbr` — basic example

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
- `19-standard-library-tour_64552e94.zbr` — basic example
- `19-standard-library-tour_b340ac6e.zbr` — basic example
- `19-standard-library-tour_c66f6eb5.zbr` — basic example
- `19-standard-library-tour_2f7f8822.zbr` — basic example
- `19-standard-library-tour_a8709205.zbr` — basic example
- `stdlib-data-processing.zbr` — combining stdlib functions for data processing

### 20-File-IO-and-System-Access (19 examples)
- `file-read-simple.zbr` — simple file reading
- `file-read-unwrap.zbr` — wrapping File.read in a throws function for catch/? handling
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
- `20-file-io-and-system-access_eb2bdbc3.zbr` — basic example
- `20-file-io-and-system-access_e14125ea.zbr` — basic example
- `20-file-io-and-system-access_a6fab3da.zbr` — basic example
- `20-file-io-and-system-access_f46780c7.zbr` — basic example
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
- `22-ffi-and-interop_a05611e2.zbr` — basic example
- `greeter_host.zbr` — DynLib.open + lookup
- `22-ffi-and-interop_bf2cc6a9.zbr` — basic example

### 22b-Build-System-and-Tooling (14 examples)
- `build.zbr` — basic example
- `build__2.zbr` — imperative-style build script
- `22b-build-system-and-tooling_e6c57be2.zbr` — basic example
- `22b-build-system-and-tooling_eb7a15a6.zbr` — basic example
- `build__3.zbr` — declarative-style build script
- `22b-build-system-and-tooling_8394c7ab.zbr` — basic example
- `22b-build-system-and-tooling_4a770990.zbr` — basic example
- `22b-build-system-and-tooling_fd52fc95.zbr` — basic example
- `22b-build-system-and-tooling_d244c54b.zbr` — basic example
- `22b-build-system-and-tooling_5f9642f4.zbr` — basic example
- `22b-build-system-and-tooling_f9fd4f57.zbr` — basic example
- `22b-build-system-and-tooling_e1b3e185.zbr` — basic example
- `22b-build-system-and-tooling_489777a7.zbr` — basic example
- `22b-build-system-and-tooling_246b02c3.zbr` — basic example

### 22c-Testing-and-Validation (17 examples)
- `22c_first_test.zbr` — writing a single test
- `22c_assertions.zbr` — assert on comparisons, and what its failure says
- `22c_tags.zbr` — @tag-based test filtering
- `22c-testing-and-validation_b4c60a70.zbr` — basic example
- `arithmetic_test.zbr` — class-scoped tests
- `22c-testing-and-validation_c5e4f4b9.zbr` — basic example
- `22c-testing-and-validation_b1a37953.zbr` — basic example
- `22c-testing-and-validation_01c09300.zbr` — basic example
- `22c-testing-and-validation_8815c08d.zbr` — basic example
- `22c-testing-and-validation_cc71a48e.zbr` — basic example
- `22c-testing-and-validation_bebbbadc.zbr` — basic example
- `22c-testing-and-validation_fcad3968.zbr` — basic example
- `22c-testing-and-validation_dcd13d26.zbr` — basic example
- `22c-testing-and-validation_090134fe.zbr` — basic example
- `22c-testing-and-validation_32af4041.zbr` — basic example
- `22c-testing-and-validation_67b791d4.zbr` — basic example
- `22c-testing-and-validation_42b0f81c.zbr` — basic example

### Appendix-A-Grammar (53 examples)
- `appendix-a-grammar_672b569f.zbr` — basic example
- `appendix-a-grammar_4450cb39.zbr` — basic example
- `appendix-a-grammar_e485c91a.zbr` — basic example
- `appendix-a-grammar_42dbecde.zbr` — basic example
- `appendix-a-grammar_eecadf7e.zbr` — basic example
- `appendix-a-grammar_1b423ed9.zbr` — basic example
- `appendix-a-grammar_0b923c20.zbr` — basic example
- `appendix-a-grammar_8de85031.zbr` — basic example
- `appendix-a-grammar_464c82aa.zbr` — basic example
- `appendix-a-grammar_f34939d5.zbr` — basic example
- `appendix-a-grammar_b17568a0.zbr` — basic example
- `appendix-a-grammar_2466cfde.zbr` — basic example
- `appendix-a-grammar_950af8e5.zbr` — basic example
- `appendix-a-grammar_88e0099c.zbr` — basic example
- `appendix-a-grammar_eb8664f9.zbr` — basic example
- `appendix-a-grammar_336d5d84.zbr` — basic example
- `appendix-a-grammar_7dcc49cc.zbr` — basic example
- `appendix-a-grammar_881f3871.zbr` — basic example
- `appendix-a-grammar_6af77ad1.zbr` — basic example
- `appendix-a-grammar_ae0f9753.zbr` — basic example
- `appendix-a-grammar_2708d80c.zbr` — basic example
- `appendix-a-grammar_60d04641.zbr` — basic example
- `appendix-a-grammar_8322970c.zbr` — basic example
- `appendix-a-grammar_522f36d1.zbr` — basic example
- `appendix-a-grammar_e0643ed8.zbr` — basic example
- `appendix-a-grammar_aeb8e866.zbr` — basic example
- `appendix-a-grammar_e2592b3e.zbr` — basic example
- `appendix-a-grammar_2f78904b.zbr` — basic example
- `appendix-a-grammar_587b7398.zbr` — basic example
- `appendix-a-grammar_87d219df.zbr` — basic example
- `appendix-a-grammar_5d5e67e5.zbr` — basic example
- `appendix-a-grammar_e6198bb8.zbr` — basic example
- `appendix-a-grammar_bac37d13.zbr` — basic example
- `appendix-a-grammar_02ee5b82.zbr` — basic example
- `appendix-a-grammar_29e0b1f8.zbr` — basic example
- `appendix-a-grammar_7e0c726f.zbr` — basic example
- `appendix-a-grammar_5d72f6ec.zbr` — basic example
- `appendix-a-grammar_16a8e466.zbr` — basic example
- `appendix-a-grammar_31e10b65.zbr` — basic example
- `appendix-a-grammar_5fb8d51e.zbr` — basic example
- `appendix-a-grammar_054becd6.zbr` — basic example
- `appendix-a-grammar_67e8a866.zbr` — basic example
- `appendix-a-grammar_c5243692.zbr` — basic example
- `appendix-a-grammar_7e4e92c9.zbr` — basic example
- `appendix-a-grammar_1dac5543.zbr` — basic example
- `appendix-a-grammar_2af8653d.zbr` — basic example
- `appendix-a-grammar_72c22ea2.zbr` — basic example
- `appendix-a-grammar_88a1f60c.zbr` — basic example
- `appendix-a-grammar_288b174a.zbr` — basic example
- `appendix-a-grammar_52d62e5d.zbr` — basic example
- `appendix-a-grammar_d0bb8dab.zbr` — basic example
- `appendix-a-grammar_5fe519b9.zbr` — basic example
- `appendix-a-grammar_10c2d92a.zbr` — basic example

### Appendix-B-Stdlib (50 examples)
- `appendix-b-stdlib_a8845bbc.zbr` — basic example
- `appendix-b-stdlib_7ba353c5.zbr` — basic example
- `appendix-b-stdlib_77582fa9.zbr` — basic example
- `appendix-b-stdlib_24935b55.zbr` — basic example
- `appendix-b-stdlib_81103174.zbr` — basic example
- `appendix-b-stdlib_09913062.zbr` — basic example
- `appendix-b-stdlib_1b5021af.zbr` — basic example
- `appendix-b-stdlib_353d9e16.zbr` — basic example
- `appendix-b-stdlib_f0b71348.zbr` — basic example
- `appendix-b-stdlib_22031907.zbr` — basic example
- `appendix-b-stdlib_c7d05958.zbr` — basic example
- `appendix-b-stdlib_1dab84c8.zbr` — basic example
- `appendix-b-stdlib_b8c47de1.zbr` — basic example
- `appendix-b-stdlib_9bdbcfcc.zbr` — basic example
- `appendix-b-stdlib_6055af66.zbr` — basic example
- `appendix-b-stdlib_df386a5d.zbr` — basic example
- `appendix-b-stdlib_872c287a.zbr` — basic example
- `appendix-b-stdlib_78404d47.zbr` — basic example
- `appendix-b-stdlib_70dc66d7.zbr` — basic example
- `appendix-b-stdlib_e1142187.zbr` — basic example
- `appendix-b-stdlib_10c9e73b.zbr` — basic example
- `appendix-b-stdlib_63a6b799.zbr` — basic example
- `appendix-b-stdlib_772fb9a5.zbr` — basic example
- `appendix-b-stdlib_16fefd06.zbr` — basic example
- `appendix-b-stdlib_c310bc80.zbr` — basic example
- `appendix-b-stdlib_6956a9fc.zbr` — basic example
- `appendix-b-stdlib_10b9d6ab.zbr` — basic example
- `appendix-b-stdlib_0c11e627.zbr` — basic example
- `appendix-b-stdlib_a841398e.zbr` — basic example
- `appendix-b-stdlib_03603019.zbr` — basic example
- `appendix-b-stdlib_f3398174.zbr` — basic example
- `appendix-b-stdlib_839d40d1.zbr` — basic example
- `appendix-b-stdlib_7c27aa46.zbr` — basic example
- `appendix-b-stdlib_6a325e69.zbr` — basic example
- `appendix-b-stdlib_dd28b593.zbr` — basic example
- `appendix-b-stdlib_e6198bb8.zbr` — basic example
- `appendix-b-stdlib_d8e69aa3.zbr` — basic example
- `appendix-b-stdlib_2ad30dcd.zbr` — basic example
- `appendix-b-stdlib_266a0a77.zbr` — basic example
- `appendix-b-stdlib_7866898d.zbr` — basic example
- `appendix-b-stdlib_93e2a037.zbr` — basic example
- `appendix-b-stdlib_1db03188.zbr` — basic example
- `appendix-b-stdlib_0a00b9d8.zbr` — basic example
- `appendix-b-stdlib_2739d3f3.zbr` — basic example
- `appendix-b-stdlib_b3fa2054.zbr` — basic example
- `appendix-b-stdlib_bbbb70ce.zbr` — basic example
- `appendix-b-stdlib_c9ce7322.zbr` — basic example
- `appendix-b-stdlib_29abc7cc.zbr` — basic example
- `appendix-b-stdlib_12df5116.zbr` — basic example
- `appendix-b-stdlib_178f2e9e.zbr` — basic example

### Appendix-C-Troubleshooting (60 examples)
- `appendix-c-troubleshooting_8bbf5ba3.zbr` — basic example
- `appendix-c-troubleshooting_0b7bb411.zbr` — basic example
- `appendix-c-troubleshooting_01f7bac9.zbr` — basic example
- `appendix-c-troubleshooting_b074544d.zbr` — basic example
- `appendix-c-troubleshooting_74e9d12a.zbr` — basic example
- `appendix-c-troubleshooting_7b5b8464.zbr` — basic example
- `appendix-c-troubleshooting_54646699.zbr` — basic example
- `appendix-c-troubleshooting_d19cd133.zbr` — basic example
- `appendix-c-troubleshooting_da67e718.zbr` — basic example
- `appendix-c-troubleshooting_5d638035.zbr` — basic example
- `appendix-c-troubleshooting_294f51c0.zbr` — basic example
- `appendix-c-troubleshooting_6081bf9a.zbr` — basic example
- `appendix-c-troubleshooting_e1f89631.zbr` — basic example
- `appendix-c-troubleshooting_69057b3a.zbr` — basic example
- `appendix-c-troubleshooting_8fe8810a.zbr` — basic example
- `appendix-c-troubleshooting_0a9cf8b5.zbr` — basic example
- `appendix-c-troubleshooting_022873e6.zbr` — basic example
- `appendix-c-troubleshooting_8ba6c2c4.zbr` — basic example
- `appendix-c-troubleshooting_2a1a28a5.zbr` — basic example
- `appendix-c-troubleshooting_b5b1941f.zbr` — basic example
- `appendix-c-troubleshooting_cefd8fc4.zbr` — basic example
- `appendix-c-troubleshooting_c0d12aef.zbr` — basic example
- `appendix-c-troubleshooting_097011e4.zbr` — basic example
- `appendix-c-troubleshooting_0f5b1537.zbr` — basic example
- `appendix-c-troubleshooting_9c7a193e.zbr` — basic example
- `appendix-c-troubleshooting_82a9e1bc.zbr` — basic example
- `appendix-c-troubleshooting_320af2a3.zbr` — basic example
- `appendix-c-troubleshooting_9478ea7a.zbr` — basic example
- `appendix-c-troubleshooting_4c6c059d.zbr` — basic example
- `appendix-c-troubleshooting_f1d52765.zbr` — basic example
- `appendix-c-troubleshooting_23731487.zbr` — basic example
- `appendix-c-troubleshooting_3fe87a98.zbr` — basic example
- `appendix-c-troubleshooting_40911c92.zbr` — basic example
- `appendix-c-troubleshooting_43f3ef30.zbr` — basic example
- `appendix-c-troubleshooting_2548ab25.zbr` — basic example
- `appendix-c-troubleshooting_6a01f8b1.zbr` — basic example
- `appendix-c-troubleshooting_37435856.zbr` — basic example
- `appendix-c-troubleshooting_eee87649.zbr` — basic example
- `appendix-c-troubleshooting_62a324ff.zbr` — basic example
- `appendix-c-troubleshooting_47aba230.zbr` — basic example
- `appendix-c-troubleshooting_936c1476.zbr` — basic example
- `appendix-c-troubleshooting_86fda4c8.zbr` — basic example
- `appendix-c-troubleshooting_0312a1dd.zbr` — basic example
- `appendix-c-troubleshooting_b3ba51b6.zbr` — basic example
- `appendix-c-troubleshooting_9f6ac354.zbr` — basic example
- `appendix-c-troubleshooting_37bec9af.zbr` — basic example
- `appendix-c-troubleshooting_763918fd.zbr` — basic example
- `appendix-c-troubleshooting_e20b82c3.zbr` — basic example
- `appendix-c-troubleshooting_c2996b84.zbr` — basic example
- `appendix-c-troubleshooting_026ab9c7.zbr` — basic example
- `appendix-c-troubleshooting_6acb55f4.zbr` — basic example
- `appendix-c-troubleshooting_8fbea400.zbr` — basic example
- `appendix-c-troubleshooting_2739d3f3.zbr` — basic example
- `appendix-c-troubleshooting_9d9607fd.zbr` — basic example
- `appendix-c-troubleshooting_bf957a6d.zbr` — basic example
- `appendix-c-troubleshooting_826a10a3.zbr` — basic example
- `appendix-c-troubleshooting_80caa434.zbr` — basic example
- `appendix-c-troubleshooting_45e92fd4.zbr` — basic example
- `appendix-c-troubleshooting_2a9629c0.zbr` — basic example
- `appendix-c-troubleshooting_3d14b543.zbr` — basic example

### Appendix-D-Attributes (9 examples)
- `appendix-d-attributes_bf382540.zbr` — basic example
- `appendix-d-attributes_c69af0d2.zbr` — basic example
- `appendix-d-attributes_17e9dbf9.zbr` — basic example
- `appendix-d-attributes_b161ae24.zbr` — basic example
- `appendix-d-attributes_13178587.zbr` — basic example
- `appendix-d-attributes_4476b8be.zbr` — basic example
- `appendix-d-attributes_816270dd.zbr` — basic example
- `deprecated_demo.zbr` — basic example
- `appendix-d-attributes_a05611e2.zbr` — basic example

### ref-cheatsheet-syntax (23 examples)
- `ref-cheatsheet-syntax_519f6869.zbr` — basic example
- `ref-cheatsheet-syntax_59798476.zbr` — basic example
- `ref-cheatsheet-syntax_c8e3541e.zbr` — basic example
- `ref-cheatsheet-syntax_a5d4ff3b.zbr` — basic example
- `ref-cheatsheet-syntax_f6cfe617.zbr` — basic example
- `ref-cheatsheet-syntax_4ef11683.zbr` — basic example
- `ref-cheatsheet-syntax_d0331aea.zbr` — basic example
- `ref-cheatsheet-syntax_f9c0ad06.zbr` — basic example
- `ref-cheatsheet-syntax_44efbac7.zbr` — basic example
- `ref-cheatsheet-syntax_052709cc.zbr` — basic example
- `ref-cheatsheet-syntax_ea3f3994.zbr` — basic example
- `ref-cheatsheet-syntax_94e0ad54.zbr` — basic example
- `ref-cheatsheet-syntax_17c47e5a.zbr` — basic example
- `ref-cheatsheet-syntax_fad686e2.zbr` — basic example
- `ref-cheatsheet-syntax_41d4eb10.zbr` — basic example
- `ref-cheatsheet-syntax_37642502.zbr` — basic example
- `ref-cheatsheet-syntax_2a9eb0b7.zbr` — basic example
- `ref-cheatsheet-syntax_c7da2544.zbr` — basic example
- `ref-cheatsheet-syntax_ca15e190.zbr` — basic example
- `ref-cheatsheet-syntax_71db613c.zbr` — basic example
- `ref-cheatsheet-syntax_e83232d8.zbr` — basic example
- `ref-cheatsheet-syntax_983ad7b7.zbr` — basic example
- `ref-cheatsheet-syntax_0e61ca98.zbr` — basic example

### ref-patterns-common-tasks (56 examples)
- `ref-patterns-common-tasks_1354f748.zbr` — basic example
- `ref-patterns-common-tasks_5267fec2.zbr` — basic example
- `ref-patterns-common-tasks_640b4c6a.zbr` — basic example
- `ref-patterns-common-tasks_ef4d58a2.zbr` — basic example
- `ref-patterns-common-tasks_5803ff74.zbr` — basic example
- `ref-patterns-common-tasks_5e8ff171.zbr` — basic example
- `ref-patterns-common-tasks_09515c39.zbr` — basic example
- `ref-patterns-common-tasks_59220c01.zbr` — basic example
- `ref-patterns-common-tasks_4038413a.zbr` — basic example
- `ref-patterns-common-tasks_bc649800.zbr` — basic example
- `ref-patterns-common-tasks_786694bb.zbr` — basic example
- `ref-patterns-common-tasks_70e79120.zbr` — basic example
- `ref-patterns-common-tasks_f57a1fad.zbr` — basic example
- `ref-patterns-common-tasks_53a0820a.zbr` — basic example
- `ref-patterns-common-tasks_8e9d44b3.zbr` — basic example
- `ref-patterns-common-tasks_c17dbfec.zbr` — basic example
- `ref-patterns-common-tasks_031d9f03.zbr` — basic example
- `ref-patterns-common-tasks_713d12e0.zbr` — basic example
- `ref-patterns-common-tasks_d8d73c0b.zbr` — basic example
- `ref-patterns-common-tasks_3fddbb95.zbr` — basic example
- `ref-patterns-common-tasks_a8b8cf2a.zbr` — basic example
- `ref-patterns-common-tasks_fd933897.zbr` — basic example
- `ref-patterns-common-tasks_fd4ab8b6.zbr` — basic example
- `ref-patterns-common-tasks_41a45fdf.zbr` — basic example
- `ref-patterns-common-tasks_ba33ca4c.zbr` — basic example
- `ref-patterns-common-tasks_52c699b3.zbr` — basic example
- `ref-patterns-common-tasks_465b4d83.zbr` — basic example
- `ref-patterns-common-tasks_bd8472bd.zbr` — basic example
- `ref-patterns-common-tasks_b5d6585f.zbr` — basic example
- `ref-patterns-common-tasks_d0fd31b1.zbr` — basic example
- `ref-patterns-common-tasks_32f18e1c.zbr` — basic example
- `ref-patterns-common-tasks_9b784d59.zbr` — basic example
- `ref-patterns-common-tasks_66dde561.zbr` — basic example
- `ref-patterns-common-tasks_106b9ef4.zbr` — basic example
- `ref-patterns-common-tasks_226cd724.zbr` — basic example
- `ref-patterns-common-tasks_b41423e4.zbr` — basic example
- `ref-patterns-common-tasks_3e3d5b28.zbr` — basic example
- `ref-patterns-common-tasks_3d67c5a4.zbr` — basic example
- `ref-patterns-common-tasks_3febe494.zbr` — basic example
- `ref-patterns-common-tasks_e18e4d3f.zbr` — basic example
- `ref-patterns-common-tasks_ecc75b64.zbr` — basic example
- `ref-patterns-common-tasks_8b98cc4a.zbr` — basic example
- `ref-patterns-common-tasks_2b05dcd8.zbr` — basic example
- `ref-patterns-common-tasks_42564ca8.zbr` — basic example
- `ref-patterns-common-tasks_d77a0c1b.zbr` — basic example
- `ref-patterns-common-tasks_eb8664f9.zbr` — basic example
- `ref-patterns-common-tasks_713a5623.zbr` — basic example
- `ref-patterns-common-tasks_71ac7894.zbr` — basic example
- `ref-patterns-common-tasks_7a76a260.zbr` — basic example
- `ref-patterns-common-tasks_7e020294.zbr` — basic example
- `ref-patterns-common-tasks_493a3399.zbr` — basic example
- `ref-patterns-common-tasks_57c2b54b.zbr` — basic example
- `ref-patterns-common-tasks_29b4bc32.zbr` — basic example
- `ref-patterns-common-tasks_b3b468e9.zbr` — basic example
- `ref-patterns-common-tasks_23861494.zbr` — basic example
- `ref-patterns-common-tasks_b4a32c19.zbr` — basic example

### ref-quickstart-30-minutes (9 examples)
- `ref-quickstart-30-minutes_a71d43b6.zbr` — basic example
- `ref-quickstart-30-minutes_4cad8406.zbr` — basic example
- `ref-quickstart-30-minutes_9b83e792.zbr` — basic example
- `ref-quickstart-30-minutes_20e6a025.zbr` — basic example
- `ref-quickstart-30-minutes_c483d479.zbr` — basic example
- `ref-quickstart-30-minutes_8ca55ad1.zbr` — basic example
- `ref-quickstart-30-minutes_fc760d0f.zbr` — basic example
- `ref-quickstart-30-minutes_22522988.zbr` — basic example
- `ref-quickstart-30-minutes_7c07b7c4.zbr` — basic example

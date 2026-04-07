# Contributing to the Zebra Book

Thank you for your interest in improving this book! Here's how to help.

## Before You Start

- This is a **living document** that iterates alongside the Zebra language
- All examples **must compile** with the current Zebra compiler
- The book targets **experienced programmers**, not complete beginners (but we include beginner sidebars)

## Types of Contributions

### 1. Report an Error
- **Code doesn't compile?** File an issue with: the chapter, the code block, the error message
- **Typo or unclear explanation?** File an issue with a quote of the problematic text
- **Example is outdated?** Zig 0.16 broke it? File an issue with the version affected

### 2. Suggest an Example
- Clearer way to explain a concept? Suggest it in an issue with:
  - Current explanation (quote)
  - Why it's confusing
  - Your suggested approach
  - (Optionally) the code for the example

### 3. Improve a Chapter
- Want to rewrite a section for clarity? Open an issue first describing what and why
- Want to add an exercise? Include the problem, solution, and learning objective
- Want to improve a diagram? Describe what's confusing about the current one

### 4. Add New Content
- New chapter? Open an issue describing the topic and why it matters
- New project? Pitch it with a paragraph on what you'd build and what you'd learn
- New appendix section? Describe what information is missing

## How to Contribute Code

### Step 1: Set Up
```bash
git clone https://github.com/your-fork/cobra-language.git
cd zebra-book
```

### Step 2: Make Changes
- Edit `.md` files in the appropriate chapter directory
- Create example files in `examples/`
- Follow the chapter template (see below)

### Step 3: Validate
```bash
make build    # Extract and validate all examples
make lint     # Check for common mistakes
```

### Step 4: Submit
- Open a pull request with a clear description of what changed and why
- Reference any related issues
- Ensure all checks pass (build, examples compile, lint)

## Chapter Template

Every chapter should have this structure:

```markdown
# NN: Chapter Title

**Audience:** All (or "Experienced only" or "All with sidebar for beginners")  
**Time:** X minutes  
**Prerequisites:** Chapters N, M  
**You'll learn:** Bullet list of skills/concepts  

## The Big Picture

[1-2 paragraphs explaining why this topic matters and what you'll use it for]

## Intuition First (Head First style)

[Visual/intuitive explanation. Could include:
- Simple analogy
- Diagram description
- Comparison to something familiar
- "Aha!" moment setup]

### If you're new to programming
> This sidebox explains a concept that might be unfamiliar. [explanation]

### If you know Python
> Comparison: Python does X this way, Zebra does it like this.

## The Problem (Problem-First style)

[Describe a real situation where you'd use this feature]

### Example: [Real scenario]
```zebra
// Example code
```

**What happened here:** [Explanation]

## Deeper: How It Works

[Detailed explanation with multiple examples, showing:
- Basic usage
- Edge cases
- Common patterns
- Performance notes (if relevant)]

### Pattern 1: [Name]
```zebra
// First pattern
```

### Pattern 2: [Name]
```zebra
// Second pattern
```

## Real World

[Show this feature in actual Zebra code. Could be:
- Code from the stdlib
- A pattern from a real project
- How experienced Zebra developers use this]

## Common Mistakes

> ❌ **Mistake:** [Bad example]
>
> 💡 **Why it's wrong:** [Explanation]
>
> ✅ **Better:** [Good example]

> ❌ **Mistake 2:** [Bad example]
>
> 💡 **Why:** [Explanation]
>
> ✅ **Better:** [Good example]

## Exercises

Try these to solidify your understanding:

### Exercise 1: [Name]
[Problem description]

<details>
<summary>Solution</summary>

```zebra
// Solution code
```

**Why this works:** [Explanation]

</details>

### Exercise 2: [Name]
[Problem description]

<details>
<summary>Solution</summary>

```zebra
// Solution code
```

</details>

## Next Steps

- → [Related chapter 1] — deeper dive into related concept
- → [Related chapter 2] — see this in practice
- 🏋️ [Project X] uses this heavily

## Key Takeaways

- **Point 1:** One sentence summary
- **Point 2:** One sentence summary
- **Point 3:** One sentence summary
```

## Code Example Standards

Every code example should:

1. **Have metadata as a comment:**
   ```zebra
   // file: 02_hello.zbr
   // teaches: hello world, print statements
   // chapter: 01-Getting-Started
   ```

2. **Be complete and runnable:**
   ```bash
   zebra examples/02_hello.zbr
   ```
   Should produce output without errors.

3. **Be simple enough to understand:**
   - Single concept per example
   - ~10-30 lines typically
   - Real variable names (not a, b, x unless explaining a math concept)

4. **Include comments explaining non-obvious parts:**
   ```zebra
   // Don't do this:
   var x = 5 + 3
   
   // Do this:
   var greeting_count = 5 + 3  // How many people to greet
   ```

## Style Guide

### Tone
- Friendly but professional
- Assume reader knows how to program (don't explain what a loop is)
- Use "we" when explaining (not "this tutorial will...")
- Avoid "simply," "just," "easy" (implies it should be obvious)

### Formatting
- **Bold:** Key concepts on first mention
- `Code`: Inline code (variable names, operators, functions)
- ```zebra: Code blocks for examples
- > Blockquotes for sidebars and warnings
- Backticks for `true`, `false`, `nil`, builtin types

### Structure
- Use ## for chapter sections (one # per file)
- Use ### for subsections
- Break up text with examples and sidebars
- Aim for 2000-3000 words per chapter

### Technical Accuracy
- Test all examples before submitting
- Verify against the current Zebra compiler version
- Note any compiler versions or known issues
- Link to related documentation

## Testing Changes

### Before submitting:
```bash
# 1. Validate examples compile
make validate

# 2. Check for common issues
make lint

# 3. (Optional) Build artifacts to see how it looks
make html
```

### If an example fails:
1. Check the error message: `make validate` will show it
2. Update the example or the explanation
3. Re-run `make validate`
4. Don't commit until all examples pass

## Questions?

- File an issue with the "question" label
- Tag @<author> in comments on related PRs
- Check existing issues/discussions first

---

**Thank you for contributing to making Zebra easier to learn! 🦓**

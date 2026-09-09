# Chapter 21: Regular Expressions

**Time:** 90 min | **Audience:** Intermediate-Advanced | **Prerequisites:** Chapter 06

---

## Learning Outcomes

After this chapter, you will:
- Understand regex syntax and pattern construction
- Use character classes, quantifiers, and anchors
- Apply regexes to validation, extraction, and transformation
- Avoid common regex pitfalls
- Know when regex is the right (and wrong) tool

---

## Overview: Pattern Matching with Regular Expressions

Regular expressions (regexes) are patterns for matching strings. They're incredibly powerful but also a frequent source of confusion and bugs. This chapter covers practical regex usage for real-world tasks.

Zebra's regex engine uses **Thompson NFA** with **Laurikari** for proper unicode support—fast, correct, and predictable.

Key principle: **Regexes are for pattern matching, not parsing.** Use a real parser for structured data (XML, JSON, code).

A note on the API before the examples: a compiled pattern is a `Regex`, built with
`Regex.compile(pattern)`. Its `.match(s)` checks whether the **whole** string `s`
matches the pattern (both ends anchored) and returns `bool` — there is no `.matches()`
method, on `Regex` or on `str`. To check whether the pattern occurs *anywhere* in a
larger string, use `.find(s) != ""` instead (`.find` returns the first matching
substring, or `""` if there's no match).

---

## Regex Basics

### Literal Characters

The simplest regex is just literal characters:

```zebra
# file: regex-literals.zbr
# teaches: basic regex literal matching
# chapter: 21

def main()
    var text = "The cat sat on the mat"
    var pattern = Regex.compile("cat")
    
    if pattern.find(text) != ""
        print("Pattern found!")
    
    # Case-sensitive
    var upper_pattern = Regex.compile("CAT")
    if upper_pattern.find(text) == ""
        print("'CAT' doesn't match 'cat'")
    
    # Substring matching
    if text.contains("sat")
        print("'sat' is in the text")
    
    # Note: for simple substring matching, use .contains()
    # Don't overcomplicate with regex
    
    # Finding position
    var pos = text.indexOf("mat")  # 19
    if pos >= 0
        print("Found at position ${pos}")
```

### The Dot (.) Wildcard

The dot matches any single character except newline:

```zebra
# file: regex-dot.zbr
# teaches: dot wildcard in regex patterns
# chapter: 21

def main()
    var re = Regex.compile("c.t")
    
    # Matches: cat, cot, cut, c9t, c t
    if re.match("cat")
        print("Matches 'cat'")
    
    if re.match("cot")
        print("Matches 'cot'")
    
    if re.match("cut")
        print("Matches 'cut'")
    
    if not re.match("coat")  # 'oa' is two chars, not one
        print("Doesn't match 'coat'")
    
    # Practical: match email-ish pattern (simplified)
    var email_pattern = ".+@.+"
    var email_re = Regex.compile(email_pattern)
    
    if email_re.match("user@example.com")
        print("Valid email pattern")
```

---

## Character Classes

Character classes match one character from a set:

```zebra
# file: regex-character-classes.zbr
# teaches: character classes and ranges
# chapter: 21

def main()
    # Single character from a set
    var re1 = Regex.compile("[aeiou]")  # Match any vowel
    
    if re1.match("a")
        print("'a' is a vowel")
    
    if re1.match("e")
        print("'e' is a vowel")
    
    if not re1.match("x")
        print("'x' is not a vowel")
    
    # Character ranges
    var digit_re = Regex.compile("[0-9]")  # Any digit
    
    if digit_re.match("5")
        print("'5' is a digit")
    
    if not digit_re.match("a")
        print("'a' is not a digit")
    
    var letter_re = Regex.compile("[a-zA-Z]")  # Any letter
    
    if letter_re.match("X")
        print("'X' is a letter")
    
    # Negation: NOT in set
    var non_vowel_re = Regex.compile("[^aeiou]")
    
    if non_vowel_re.match("b")
        print("'b' is not a vowel")
    
    if not non_vowel_re.match("a")
        print("'a' is a vowel (excluded by ^)")
```

### Common Character Classes (Shortcuts)

Zebra provides shortcuts for common patterns:

```zebra
# file: regex-shortcuts.zbr
# teaches: common regex shortcuts
# chapter: 21

def main()
    # \d = [0-9] = digit
    var digit_re = Regex.compile("\\d")
    
    if digit_re.match("7")
        print("Found digit")
    
    # \w = [a-zA-Z0-9_] = word character
    var word_re = Regex.compile("\\w")
    
    if word_re.match("a")
        print("'a' is a word character")
    
    if word_re.match("_")
        print("'_' is a word character")
    
    if not word_re.match("-")
        print("'-' is not a word character")
    
    # \s = whitespace (space, tab, newline)
    var space_re = Regex.compile("\\s")
    
    if space_re.match(" ")
        print("Space matches whitespace")
    
    if space_re.match("\t")
        print("Tab matches whitespace")
    
    # Inverse (uppercase)
    # \D = not digit
    # \W = not word character
    # \S = not whitespace
    
    var not_digit = Regex.compile("\\D")
    
    if not_digit.match("x")
        print("'x' is not a digit")
    
    if not not_digit.match("5")
        print("'5' is a digit (excluded by \\D)")
```

---

## Quantifiers

Quantifiers specify how many times a pattern repeats:

```zebra
# file: regex-quantifiers.zbr
# teaches: repetition quantifiers
# chapter: 21

def main()
    # * = zero or more
    var re_star = Regex.compile("ab*c")  # ac, abc, abbc, abbbc, etc.
    
    if re_star.match("ac")
        print("Matches 'ac' (zero b's)")
    
    if re_star.match("abc")
        print("Matches 'abc' (one b)")
    
    if re_star.match("abbbc")
        print("Matches 'abbbc' (three b's)")
    
    if not re_star.match("aXc")
        print("Doesn't match 'aXc' (X is not b)")
    
    # + = one or more
    var re_plus = Regex.compile("ab+c")  # abc, abbc, abbbc, etc. (NOT ac)
    
    if not re_plus.match("ac")
        print("Doesn't match 'ac' (need at least one b)")
    
    if re_plus.match("abc")
        print("Matches 'abc'")
    
    if re_plus.match("abbc")
        print("Matches 'abbc'")
    
    # ? = zero or one
    var re_optional = Regex.compile("colou?r")  # color or colour
    
    if re_optional.match("color")
        print("Matches 'color' (American spelling)")
    
    if re_optional.match("colour")
        print("Matches 'colour' (British spelling)")
    
    if not re_optional.match("coloor")
        print("Doesn't match 'coloor' (too many o's)")
    
    # Exact count: {n}
    var re_exact = Regex.compile("a{3}")  # exactly three a's
    
    if re_exact.match("aaa")
        print("Matches 'aaa'")
    
    if not re_exact.match("aa")
        print("Doesn't match 'aa'")
    
    # Range: {n,m}
    var re_range = Regex.compile("a{2,4}")  # 2 to 4 a's
    
    if re_range.match("aa")
        print("Matches 'aa'")
    
    if re_range.match("aaa")
        print("Matches 'aaa'")
    
    if re_range.match("aaaa")
        print("Matches 'aaaa'")
    
    if not re_range.match("aaaaa")
        print("Doesn't match 'aaaaa' (too many)")
```

---

## Anchors

Anchors assert position, not content:

```zebra
# file: regex-anchors.zbr
# teaches: position anchors in regex
# chapter: 21

def main()
    # ^ = start of string
    var starts_with_hello = Regex.compile("^hello")
    
    if starts_with_hello.match("hello world")
        print("Matches: string starts with 'hello'")
    
    if not starts_with_hello.match("say hello")
        print("Doesn't match: 'hello' is not at start")
    
    # $ = end of string
    var ends_with_txt = Regex.compile("\\.txt$")
    
    if ends_with_txt.match("document.txt")
        print("Matches: filename ends with .txt")
    
    if not ends_with_txt.match("document.txt.bak")
        print("Doesn't match: .txt is not at end")
    
    # Combining ^ and $
    var exact_pattern = Regex.compile("^[a-z]+$")  # Only lowercase letters
    
    if exact_pattern.match("hello")
        print("Matches: all lowercase")
    
    if not exact_pattern.match("Hello")
        print("Doesn't match: has uppercase")
    
    if not exact_pattern.match("hello123")
        print("Doesn't match: has numbers")
    
    # Word boundary: \b
    var word_boundary = Regex.compile("\\bhello\\b")
    
    if word_boundary.match("hello world")
        print("Matches: 'hello' is a word")
    
    if not word_boundary.match("helloworld")
        print("Doesn't match: 'hello' is part of 'helloworld'")
```

---

## Groups and Alternation

Groups collect parts together, and alternation provides choices:

```zebra
# file: regex-groups.zbr
# teaches: grouping and alternation patterns
# chapter: 21

def main()
    # Alternation: |
    var greeting_re = Regex.compile("hello|hi|hey")
    
    if greeting_re.match("hello")
        print("Matches 'hello'")
    
    if greeting_re.match("hi")
        print("Matches 'hi'")
    
    if greeting_re.match("hey")
        print("Matches 'hey'")
    
    if not greeting_re.match("goodbye")
        print("Doesn't match 'goodbye'")
    
    # Groups with quantifiers
    var repeating_group = Regex.compile("(ab)+")  # ab, abab, ababab, etc.
    
    if repeating_group.match("ab")
        print("Matches 'ab'")
    
    if repeating_group.match("abab")
        print("Matches 'abab'")
    
    if repeating_group.match("ababab")
        print("Matches 'ababab'")
    
    if not repeating_group.match("aba")
        print("Doesn't match 'aba'")
    
    # Optional group
    var optional_group = Regex.compile("colou?r|color")
    # Actually redundant—simpler: colou?r
    
    if optional_group.match("color")
        print("Matches 'color'")
    
    if optional_group.match("colour")
        print("Matches 'colour'")
```

---

## Practical Validation Patterns

### Email Validation

Warning: email validation is complex! This is a *simplified* pattern.

```zebra
# file: regex-email.zbr
# teaches: email validation pattern (simplified)
# chapter: 21

def is_valid_email(email: str): bool
    # Must have @ and .
    if not email.contains("@")
        return false
    
    var parts = email.split("@")
    if parts.count() != 2
        return false  # Multiple @ signs
    
    var local = parts.at(0)
    var domain = parts.at(1)
    
    if local.len == 0 or domain.len == 0
        return false  # Empty parts
    
    if not domain.contains(".")
        return false  # No TLD
    
    return true

def main()
    # Very basic email pattern
    # In production, use an email verification service
    var email_pattern = Regex.compile("[a-z0-9]+@[a-z]+\\.[a-z]+")
    
    if email_pattern.match("user@example.com")
        print("Valid format")
    
    if not email_pattern.match("invalid.email@")
        print("Invalid: missing domain")
    
    if not email_pattern.match("no-at-sign.com")
        print("Invalid: no @ sign")
    
    # Better validation: check length, etc. (top-level def — a `def` can't be
    # nested inside another function's body in Zebra)
    if is_valid_email("alice@example.com")
        print("Email looks valid")
```

### Phone Number Validation

```zebra
# file: regex-phone.zbr
# teaches: phone number pattern matching
# chapter: 21

def is_valid_phone_flexible(phone: str): bool
    # Must have at least 10 digits
    var digits_only = phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    
    var digit_count = 0
    for ch in digits_only.chars()
        if Regex.compile("\\d").match("${ch:c}")
            digit_count = digit_count + 1
    
    return digit_count >= 10 and digit_count <= 15

def main()
    # US format: 123-456-7890
    var us_phone = Regex.compile("\\d{3}-\\d{3}-\\d{4}")
    
    if us_phone.match("555-123-4567")
        print("Valid US phone")
    
    if not us_phone.match("5551234567")  # Missing dashes
        print("Invalid: wrong format")
    
    # International: +1-234-567-8900
    var intl_phone = Regex.compile("\\+\\d{1,3}-\\d{3}-\\d{3}-\\d{4}")
    
    if intl_phone.match("+1-555-123-4567")
        print("Valid international")
    
    # Flexible: accept various formats (top-level def, see regex-email.zbr note)
    if is_valid_phone_flexible("(555) 123-4567")
        print("Flexible format accepted")
```

### URL Validation

```zebra
# file: regex-url.zbr
# teaches: URL pattern matching
# chapter: 21

def is_valid_url(url: str): bool
    if not url.startsWith("http://") and not url.startsWith("https://")
        return false
    
    var after_protocol = url.substring(7, url.len)
    if after_protocol.len == 0
        return false
    
    # Must have at least one dot
    if not after_protocol.contains(".")
        return false
    
    # No spaces
    if after_protocol.contains(" ")
        return false
    
    return true

def main()
    # Basic HTTP(S) URL
    var url_pattern = Regex.compile("https?://[a-z0-9]+\\.[a-z0-9]+")
    
    if url_pattern.match("https://example.com")
        print("Valid HTTPS URL")
    
    if url_pattern.match("http://example.co.uk")
        print("Valid HTTP URL")
    
    if not url_pattern.match("ftp://example.com")
        print("Doesn't match: FTP not in pattern")
    
    # More complete (top-level def, see regex-email.zbr note)
    if is_valid_url("https://example.com/path")
        print("Complete validation passed")
```

---

## Finding and Extracting Patterns

### Finding Matches

```zebra
# file: regex-finding.zbr
# teaches: finding matches within text
# chapter: 21

def main()
    var text = "The prices are: $10, $25, and $100"
    
    # Find prices (simple pattern)
    var price_pattern = Regex.compile("\\$\\d+")
    
    # Find first match
    if price_pattern.match(text)
        print("Contains price pattern")
    
    # Extract all prices
    var prices: List(str) = []
    
    # Manual extraction (since full regex API varies). indexOf takes one
    # argument — to search from an offset, use indexOfFrom, which returns int?
    var search_start = 0
    while search_start < text.len
        var dollar_pos = text.indexOfFrom("$", search_start)
        if dollar_pos == nil
            break
        var dp = dollar_pos!
        
        var num_start = dp + 1
        var num_end = num_start
        
        while num_end < text.len
            # charAt returns a byte, not a str — format it with :c to get a
            # 1-character str Regex.match can take.
            var digit_char = "${text.charAt(num_end):c}"
            if Regex.compile("\\d").match(digit_char)
                num_end = num_end + 1
            else
                break
        
        var price = text.substring(dp, num_end)
        prices.add(price)
        search_start = num_end
    
    print("Found prices:")
    for price in prices
        print("  ${price}")
```

### Extracting from Structured Text

```zebra
# file: regex-extract-structured.zbr
# teaches: extracting data from formatted text
# chapter: 21

def extract_person_data(line: str): HashMap(str, str)?
    # Expected format: Name | Age | Email
    var pattern = Regex.compile("^(.+)\\|(.+)\\|(.+)$")
    
    # Simplified: just split by |
    var parts = line.split("|")
    if parts.count() != 3
        return nil
    
    var data = HashMap(str, str)()
    data.set("name", parts.at(0).trim())
    data.set("age", parts.at(1).trim())
    data.set("email", parts.at(2).trim())
    
    return data

def main()
    var record = "John Smith | 30 | john@example.com"
    
    if extract_person_data(record) as extracted
        # .get() returns V? (str?) — a HashMap(str,str) lookup can miss, so
        # interpolating it needs an unwrap. orelse gives a fallback for a
        # genuinely-missing key; here we know the keys are present.
        print("Name: ${extracted.get("name") orelse ""}")
        print("Age: ${extracted.get("age") orelse ""}")
        print("Email: ${extracted.get("email") orelse ""}")
```

---

## Text Replacement with Patterns

### Simple Replacement

```zebra
# file: regex-replace.zbr
# teaches: pattern-based text replacement
# chapter: 21

def main()
    var text = "The cat sat on the mat"
    
    # re.replace(s, repl) replaces EVERY match — there's no separate
    # single-replacement or `.replaceAll` on Regex (that name exists on `str`,
    # not on `Regex`).
    var pattern = Regex.compile("at")
    var replaced = pattern.replace(text, "AT")
    print(replaced)  # "The cAT sAT on the mAT"
    
    # Case-insensitive replacement (if supported)
    var case_insensitive = text.lower().replace("cat", "dog")
    # Note: this loses original case
```

### Data Transformation

```zebra
# file: regex-transform.zbr
# teaches: using regex for data transformation
# chapter: 21

def escape_html(text: str): str
    var escaped = text.replace("&", "&amp;")
    escaped = escaped.replace("<", "&lt;")
    escaped = escaped.replace(">", "&gt;")
    escaped = escaped.replace("\"", "&quot;")
    escaped = escaped.replace("'", "&#39;")
    return escaped

def main()
    # Convert dates from MM/DD/YYYY to YYYY-MM-DD
    var date = "03/15/2025"
    
    var parts = date.split("/")
    if parts.count() == 3
        var month = parts.at(0)
        var day = parts.at(1)
        var year = parts.at(2)
        
        var iso_date = "${year}-${month}-${day}"
        print(iso_date)  # 2025-03-15
    
    # Escape special characters (top-level def, see regex-email.zbr note)
    var html_unsafe = "<script>alert('XSS')</script>"
    print(escape_html(html_unsafe))
```

---

## Common Pitfalls

### Greedy vs. Non-Greedy

```zebra
# file: regex-greedy.zbr
# teaches: understanding greedy matching
# chapter: 21

def main()
    # Greedy: matches as much as possible
    var text = "<name>John</name> and <name>Jane</name>"
    
    # This is too greedy!
    var greedy = Regex.compile("<name>.*</name>")
    # Matches: <name>John</name> and <name>Jane</name> (TOO MUCH!)
    
    # Better: be more specific
    var specific = Regex.compile("<name>[^<]+</name>")
    # Matches: <name>John</name> or <name>Jane</name> (correctly)
    
    # For non-greedy, many regex engines use .*? (with ?)
    # Check Zebra's specific syntax for your version
```

### Special Characters Need Escaping

```zebra
# file: regex-escaping.zbr
# teaches: escaping special characters
# chapter: 21

def main()
    # These characters have special meaning:
    # . ^ $ * + ? { } [ ] \ | ( )
    
    # To match a literal dot
    var file_extension = Regex.compile("\\.txt$")
    
    if file_extension.match("document.txt")
        print("Matches text file")
    
    # To match a literal dollar sign
    var price_pattern = Regex.compile("\\$[0-9]+")
    
    if price_pattern.match("$50")
        print("Matches price")
    
    # To match a literal backslash
    var path_pattern = Regex.compile("C:\\\\Users")  # Note: double backslash
    
    if path_pattern.match("C:\\Users")
        print("Matches Windows path")
```

### Know Your Regex Dialect

Different tools support different features. Zebra uses Thompson NFA, which:
- ✅ Supports basic patterns well
- ✅ Has predictable performance (no catastrophic backtracking)
- ⚠ May not support all advanced features like lookahead

Check documentation for your version.

---

## Practical Application: Log Analysis

```zebra
# file: regex-log-analysis.zbr
# teaches: using regex for real log analysis
# chapter: 21

def analyze_logs(filename: str)
    if not File.exists(filename)
        print("Error: ${filename} not found")
        return
    
    var content = File.read(filename)
    var lines = content.split("\n")
    
    var error_count = 0
    var warning_count = 0
    var error_lines: List(str) = []
    
    for line in lines
        if line.contains("[ERROR]")
            error_count = error_count + 1
            error_lines.add(line)
        else if line.contains("[WARN]")
            warning_count = warning_count + 1
    
    print("Log Analysis:")
    print("  Errors: ${error_count}")
    print("  Warnings: ${warning_count}")
    
    if error_count > 0
        print("\nErrors:")
        for error_line in error_lines
            print("  ${error_line}")

def main()
    analyze_logs("app.log")
```

---

## Key Takeaways

1. **Regex for Patterns** — Use for validation, searching, and pattern-based extraction.

2. **Not for Parsing** — Use a real parser for JSON, XML, structured formats.

3. **Be Specific** — Avoid greedy patterns. Use character classes to narrow matches.

4. **Test Thoroughly** — Regex bugs are subtle. Test edge cases.

5. **Document Your Patterns** — Future you will thank you.

6. **Simple First** — Is `.contains()` sufficient? Use it instead of regex overhead.

---

## Exercises

1. **URL Extractor** — Find all URLs in text matching http(s)://
2. **Log Severity Counter** — Count [ERROR], [WARN], [INFO] lines in a log file
3. **Email List Validator** — Read CSV, validate email column, report invalid entries
4. **Phone Formatter** — Read list of numbers in various formats, output consistent format
5. **JSON Key Extractor** — Extract all JSON key names from a file

---

## What's Next

Chapter 22 covers FFI (Foreign Function Interface)—calling code written in other languages. Regexes are often used to parse data from external systems, making them a natural precursor.

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

---

## Regex Basics

### Literal Characters

The simplest regex is just literal characters:

```zebra
// file: regex-literals.zbr
// teaches: basic regex literal matching
// chapter: 21

def main()
    var text = "The cat sat on the mat"
    var pattern = "cat"
    
    if text.matches(pattern)
        println("Pattern found!")
    
    // Case-sensitive
    if not text.matches("CAT")
        println("'CAT' doesn't match 'cat'")
    
    // Substring matching
    if text.contains("sat")
        println("'sat' is in the text")
    
    // Note: for simple substring matching, use .contains()
    // Don't overcomplicate with regex
    
    // Finding position
    var pos = text.indexOf("mat")  # 19
    if pos >= 0
        println("Found at position ${pos}")
```

### The Dot (.) Wildcard

The dot matches any single character except newline:

```zebra
// file: regex-dot.zbr
// teaches: dot wildcard in regex patterns
// chapter: 21

def main()
    var re = Regex.compile("c.t")
    
    // Matches: cat, cot, cut, c9t, c t
    if re.matches("cat")
        println("Matches 'cat'")
    
    if re.matches("cot")
        println("Matches 'cot'")
    
    if re.matches("cut")
        println("Matches 'cut'")
    
    if not re.matches("coat")  # 'oa' is two chars, not one
        println("Doesn't match 'coat'")
    
    // Practical: match email-ish pattern (simplified)
    var email_pattern = ".+@.+"
    var email_re = Regex.compile(email_pattern)
    
    if email_re.matches("user@example.com")
        println("Valid email pattern")
```

---

## Character Classes

Character classes match one character from a set:

```zebra
// file: regex-character-classes.zbr
// teaches: character classes and ranges
// chapter: 21

def main()
    // Single character from a set
    var re1 = Regex.compile("[aeiou]")  # Match any vowel
    
    if re1.matches("a")
        println("'a' is a vowel")
    
    if re1.matches("e")
        println("'e' is a vowel")
    
    if not re1.matches("x")
        println("'x' is not a vowel")
    
    // Character ranges
    var digit_re = Regex.compile("[0-9]")  # Any digit
    
    if digit_re.matches("5")
        println("'5' is a digit")
    
    if not digit_re.matches("a")
        println("'a' is not a digit")
    
    var letter_re = Regex.compile("[a-zA-Z]")  # Any letter
    
    if letter_re.matches("X")
        println("'X' is a letter")
    
    // Negation: NOT in set
    var non_vowel_re = Regex.compile("[^aeiou]")
    
    if non_vowel_re.matches("b")
        println("'b' is not a vowel")
    
    if not non_vowel_re.matches("a")
        println("'a' is a vowel (excluded by ^)")
```

### Common Character Classes (Shortcuts)

Zebra provides shortcuts for common patterns:

```zebra
// file: regex-shortcuts.zbr
// teaches: common regex shortcuts
// chapter: 21

def main()
    // \d = [0-9] = digit
    var digit_re = Regex.compile("\\d")
    
    if digit_re.matches("7")
        println("Found digit")
    
    // \w = [a-zA-Z0-9_] = word character
    var word_re = Regex.compile("\\w")
    
    if word_re.matches("a")
        println("'a' is a word character")
    
    if word_re.matches("_")
        println("'_' is a word character")
    
    if not word_re.matches("-")
        println("'-' is not a word character")
    
    // \s = whitespace (space, tab, newline)
    var space_re = Regex.compile("\\s")
    
    if space_re.matches(" ")
        println("Space matches whitespace")
    
    if space_re.matches("\t")
        println("Tab matches whitespace")
    
    // Inverse (uppercase)
    // \D = not digit
    // \W = not word character
    // \S = not whitespace
    
    var not_digit = Regex.compile("\\D")
    
    if not_digit.matches("x")
        println("'x' is not a digit")
    
    if not not_digit.matches("5")
        println("'5' is a digit (excluded by \\D)")
```

---

## Quantifiers

Quantifiers specify how many times a pattern repeats:

```zebra
// file: regex-quantifiers.zbr
// teaches: repetition quantifiers
// chapter: 21

def main()
    // * = zero or more
    var re_star = Regex.compile("ab*c")  // ac, abc, abbc, abbbc, etc.
    
    if re_star.matches("ac")
        println("Matches 'ac' (zero b's)")
    
    if re_star.matches("abc")
        println("Matches 'abc' (one b)")
    
    if re_star.matches("abbbc")
        println("Matches 'abbbc' (three b's)")
    
    if not re_star.matches("aXc")
        println("Doesn't match 'aXc' (X is not b)")
    
    // + = one or more
    var re_plus = Regex.compile("ab+c")  // abc, abbc, abbbc, etc. (NOT ac)
    
    if not re_plus.matches("ac")
        println("Doesn't match 'ac' (need at least one b)")
    
    if re_plus.matches("abc")
        println("Matches 'abc'")
    
    if re_plus.matches("abbc")
        println("Matches 'abbc'")
    
    // ? = zero or one
    var re_optional = Regex.compile("colou?r")  // color or colour
    
    if re_optional.matches("color")
        println("Matches 'color' (American spelling)")
    
    if re_optional.matches("colour")
        println("Matches 'colour' (British spelling)")
    
    if not re_optional.matches("coloor")
        println("Doesn't match 'coloor' (too many o's)")
    
    // Exact count: {n}
    var re_exact = Regex.compile("a{3}")  // exactly three a's
    
    if re_exact.matches("aaa")
        println("Matches 'aaa'")
    
    if not re_exact.matches("aa")
        println("Doesn't match 'aa'")
    
    // Range: {n,m}
    var re_range = Regex.compile("a{2,4}")  // 2 to 4 a's
    
    if re_range.matches("aa")
        println("Matches 'aa'")
    
    if re_range.matches("aaa")
        println("Matches 'aaa'")
    
    if re_range.matches("aaaa")
        println("Matches 'aaaa'")
    
    if not re_range.matches("aaaaa")
        println("Doesn't match 'aaaaa' (too many)")
```

---

## Anchors

Anchors assert position, not content:

```zebra
// file: regex-anchors.zbr
// teaches: position anchors in regex
// chapter: 21

def main()
    // ^ = start of string
    var starts_with_hello = Regex.compile("^hello")
    
    if starts_with_hello.matches("hello world")
        println("Matches: string starts with 'hello'")
    
    if not starts_with_hello.matches("say hello")
        println("Doesn't match: 'hello' is not at start")
    
    // $ = end of string
    var ends_with_txt = Regex.compile("\\.txt$")
    
    if ends_with_txt.matches("document.txt")
        println("Matches: filename ends with .txt")
    
    if not ends_with_txt.matches("document.txt.bak")
        println("Doesn't match: .txt is not at end")
    
    // Combining ^ and $
    var exact_pattern = Regex.compile("^[a-z]+$")  // Only lowercase letters
    
    if exact_pattern.matches("hello")
        println("Matches: all lowercase")
    
    if not exact_pattern.matches("Hello")
        println("Doesn't match: has uppercase")
    
    if not exact_pattern.matches("hello123")
        println("Doesn't match: has numbers")
    
    // Word boundary: \b
    var word_boundary = Regex.compile("\\bhello\\b")
    
    if word_boundary.matches("hello world")
        println("Matches: 'hello' is a word")
    
    if not word_boundary.matches("helloworld")
        println("Doesn't match: 'hello' is part of 'helloworld'")
```

---

## Groups and Alternation

Groups collect parts together, and alternation provides choices:

```zebra
// file: regex-groups.zbr
// teaches: grouping and alternation patterns
// chapter: 21

def main()
    // Alternation: |
    var greeting_re = Regex.compile("hello|hi|hey")
    
    if greeting_re.matches("hello")
        println("Matches 'hello'")
    
    if greeting_re.matches("hi")
        println("Matches 'hi'")
    
    if greeting_re.matches("hey")
        println("Matches 'hey'")
    
    if not greeting_re.matches("goodbye")
        println("Doesn't match 'goodbye'")
    
    // Groups with quantifiers
    var repeating_group = Regex.compile("(ab)+")  // ab, abab, ababab, etc.
    
    if repeating_group.matches("ab")
        println("Matches 'ab'")
    
    if repeating_group.matches("abab")
        println("Matches 'abab'")
    
    if repeating_group.matches("ababab")
        println("Matches 'ababab'")
    
    if not repeating_group.matches("aba")
        println("Doesn't match 'aba'")
    
    // Optional group
    var optional_group = Regex.compile("colou?r|color")
    // Actually redundant—simpler: colou?r
    
    if optional_group.matches("color")
        println("Matches 'color'")
    
    if optional_group.matches("colour")
        println("Matches 'colour'")
```

---

## Practical Validation Patterns

### Email Validation

Warning: email validation is complex! This is a *simplified* pattern.

```zebra
// file: regex-email.zbr
// teaches: email validation pattern (simplified)
// chapter: 21

def main()
    // Very basic email pattern
    // In production, use an email verification service
    var email_pattern = Regex.compile("[a-z0-9]+@[a-z]+\\.[a-z]+")
    
    if email_pattern.matches("user@example.com")
        println("Valid format")
    
    if not email_pattern.matches("invalid.email@")
        println("Invalid: missing domain")
    
    if not email_pattern.matches("no-at-sign.com")
        println("Invalid: no @ sign")
    
    // Better validation: check length, etc.
    def is_valid_email(email as str) as bool
        // Must have @ and .
        if not email.contains("@")
            return false
        
        var parts = email.split("@")
        if parts.count() != 2
            return false  // Multiple @ signs
        
        var local = parts.at(0)
        var domain = parts.at(1)
        
        if local.len == 0 or domain.len == 0
            return false  // Empty parts
        
        if not domain.contains(".")
            return false  // No TLD
        
        return true
    
    if is_valid_email("alice@example.com")
        println("Email looks valid")
```

### Phone Number Validation

```zebra
// file: regex-phone.zbr
// teaches: phone number pattern matching
// chapter: 21

def main()
    // US format: 123-456-7890
    var us_phone = Regex.compile("\\d{3}-\\d{3}-\\d{4}")
    
    if us_phone.matches("555-123-4567")
        println("Valid US phone")
    
    if not us_phone.matches("5551234567")  // Missing dashes
        println("Invalid: wrong format")
    
    // International: +1-234-567-8900
    var intl_phone = Regex.compile("\\+\\d{1,3}-\\d{3}-\\d{3}-\\d{4}")
    
    if intl_phone.matches("+1-555-123-4567")
        println("Valid international")
    
    // Flexible: accept various formats
    def is_valid_phone_flexible(phone as str) as bool
        // Must have at least 10 digits
        var digits_only = phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        
        var digit_count = 0
        for char in digits_only.split("")
            if Regex.compile("\\d").matches(char)
                digit_count = digit_count + 1
        
        return digit_count >= 10 and digit_count <= 15
```

### URL Validation

```zebra
// file: regex-url.zbr
// teaches: URL pattern matching
// chapter: 21

def main()
    // Basic HTTP(S) URL
    var url_pattern = Regex.compile("https?://[a-z0-9]+\\.[a-z0-9]+")
    
    if url_pattern.matches("https://example.com")
        println("Valid HTTPS URL")
    
    if url_pattern.matches("http://example.co.uk")
        println("Valid HTTP URL")
    
    if not url_pattern.matches("ftp://example.com")
        println("Doesn't match: FTP not in pattern")
    
    // More complete
    def is_valid_url(url as str) as bool
        if not url.startsWith("http://") and not url.startsWith("https://")
            return false
        
        var after_protocol = url.substring(7, url.len)
        if after_protocol.len == 0
            return false
        
        // Must have at least one dot
        if not after_protocol.contains(".")
            return false
        
        // No spaces
        if after_protocol.contains(" ")
            return false
        
        return true
```

---

## Finding and Extracting Patterns

### Finding Matches

```zebra
// file: regex-finding.zbr
// teaches: finding matches within text
// chapter: 21

def main()
    var text = "The prices are: $10, $25, and $100"
    
    // Find prices (simple pattern)
    var price_pattern = Regex.compile("\\$\\d+")
    
    // Find first match
    if price_pattern.matches(text)
        println("Contains price pattern")
    
    // Extract all prices
    var prices = List(str)()
    
    // Manual extraction (since full regex API varies)
    var search_start = 0
    while search_start < text.len
        var dollar_pos = text.indexOf("$", search_start)
        if dollar_pos < 0
            break
        
        var num_start = dollar_pos + 1
        var num_end = num_start
        
        while num_end < text.len
            var char = text.charAt(num_end)
            if Regex.compile("\\d").matches(char)
                num_end = num_end + 1
            else
                break
        
        var price = text.substring(dollar_pos, num_end)
        prices.add(price)
        search_start = num_end
    
    println("Found prices:")
    for price in prices
        println("  ${price}")
```

### Extracting from Structured Text

```zebra
// file: regex-extract-structured.zbr
// teaches: extracting data from formatted text
// chapter: 21

def extract_person_data(line as str) as HashMap(str, str)?
    // Expected format: Name | Age | Email
    var pattern = Regex.compile("^(.+)\\|(.+)\\|(.+)$")
    
    // Simplified: just split by |
    var parts = line.split("|")
    if parts.count() != 3
        return nil
    
    var data = HashMap(str, str)()
    data.put("name", parts.at(0).trim())
    data.put("age", parts.at(1).trim())
    data.put("email", parts.at(2).trim())
    
    return data

def main()
    var record = "John Smith | 30 | john@example.com"
    
    var extracted = extract_person_data(record)
    
    if extracted != nil
        println("Name: ${extracted.fetch("name")}")
        println("Age: ${extracted.fetch("age")}")
        println("Email: ${extracted.fetch("email")}")
```

---

## Text Replacement with Patterns

### Simple Replacement

```zebra
// file: regex-replace.zbr
// teaches: pattern-based text replacement
// chapter: 21

def main()
    var text = "The cat sat on the mat"
    
    // Replace first occurrence of pattern
    var pattern = Regex.compile("at")
    var replaced = pattern.replace(text, "AT")
    println(replaced)  // "The cAT sat on the mat"
    
    // Replace all occurrences
    var all_replaced = pattern.replaceAll(text, "AT")
    println(all_replaced)  // "The cAT sAT on the mAT"
    
    // Case-insensitive replacement (if supported)
    var case_insensitive = text.lower().replace("cat", "dog")
    // Note: this loses original case
```

### Data Transformation

```zebra
// file: regex-transform.zbr
// teaches: using regex for data transformation
// chapter: 21

def main()
    // Convert dates from MM/DD/YYYY to YYYY-MM-DD
    var date = "03/15/2025"
    
    var parts = date.split("/")
    if parts.count() == 3
        var month = parts.at(0)
        var day = parts.at(1)
        var year = parts.at(2)
        
        var iso_date = "${year}-${month}-${day}"
        println(iso_date)  // 2025-03-15
    
    // Escape special characters
    def escape_html(text as str) as str
        var escaped = text.replace("&", "&amp;")
        escaped = escaped.replace("<", "&lt;")
        escaped = escaped.replace(">", "&gt;")
        escaped = escaped.replace("\"", "&quot;")
        escaped = escaped.replace("'", "&#39;")
        return escaped
    
    var html_unsafe = "<script>alert('XSS')</script>"
    println(escape_html(html_unsafe))
```

---

## Common Pitfalls

### Greedy vs. Non-Greedy

```zebra
// file: regex-greedy.zbr
// teaches: understanding greedy matching
// chapter: 21

def main()
    // Greedy: matches as much as possible
    var text = "<name>John</name> and <name>Jane</name>"
    
    // This is too greedy!
    var greedy = Regex.compile("<name>.*</name>")
    // Matches: <name>John</name> and <name>Jane</name> (TOO MUCH!)
    
    // Better: be more specific
    var specific = Regex.compile("<name>[^<]+</name>")
    // Matches: <name>John</name> or <name>Jane</name> (correctly)
    
    // For non-greedy, many regex engines use .*? (with ?)
    // Check Zebra's specific syntax for your version
```

### Special Characters Need Escaping

```zebra
// file: regex-escaping.zbr
// teaches: escaping special characters
// chapter: 21

def main()
    // These characters have special meaning:
    // . ^ $ * + ? { } [ ] \ | ( )
    
    // To match a literal dot
    var file_extension = Regex.compile("\\.txt$")
    
    if file_extension.matches("document.txt")
        println("Matches text file")
    
    // To match a literal dollar sign
    var price_pattern = Regex.compile("\\$[0-9]+")
    
    if price_pattern.matches("$50")
        println("Matches price")
    
    // To match a literal backslash
    var path_pattern = Regex.compile("C:\\\\Users")  // Note: double backslash
    
    if path_pattern.matches("C:\\Users")
        println("Matches Windows path")
```

### Know Your Regex Dialect

Different tools support different features. Zebra uses Thompson NFA, which:
- ✅ Supports basic patterns well
- ✅ Has predictable performance (no catastrophic backtracking)
- ⚠️ May not support all advanced features like lookahead

Check documentation for your version.

---

## Practical Application: Log Analysis

```zebra
// file: regex-log-analysis.zbr
// teaches: using regex for real log analysis
// chapter: 21

def analyze_logs(filename as str)
    var result = File.read(filename)
    if result.isErr()
        println("Error: ${result.error()}")
        return
    
    var content = result.value()
    var lines = content.split("\n")
    
    var error_count = 0
    var warning_count = 0
    var error_lines = List(str)()
    
    for line in lines
        if line.contains("[ERROR]")
            error_count = error_count + 1
            error_lines.add(line)
        elif line.contains("[WARN]")
            warning_count = warning_count + 1
    
    println("Log Analysis:")
    println("  Errors: ${error_count}")
    println("  Warnings: ${warning_count}")
    
    if error_count > 0
        println("\nErrors:")
        for error_line in error_lines
            println("  ${error_line}")

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

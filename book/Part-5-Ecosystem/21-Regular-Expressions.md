# Chapter 21: Regular Expressions

**Time:** 90 min | **Audience:** Intermediate-Advanced | **Prerequisites:** Chapter 06

---

## Learning Outcomes

After this chapter, you will:
- Understand regex syntax and pattern construction
- Use character classes, quantifiers, and anchors
- Pull pieces out of text with capture groups
- Apply regexes to validation, extraction, and transformation
- Avoid common regex pitfalls
- Know when regex is the right (and wrong) tool

---

## Overview: Pattern Matching with Regular Expressions

Regular expressions (regexes) are patterns for matching strings. They're incredibly powerful but also a frequent source of confusion and bugs. This chapter covers practical regex usage for real-world tasks.

Zebra's regex engine is a **Thompson NFA**: it tracks every possible match position at once instead of backtracking, so matching time grows with the length of the input, never exponentially. It works on **bytes**: `\w`, `\d`, `[a-z]` and the case-insensitive flag are ASCII rules, and a multi-byte UTF-8 character counts as several characters to `.`.

Key principle: **Regexes are for pattern matching, not parsing.** Use a real parser for structured data (XML, JSON, code).

### The API at a glance

A compiled pattern is a `Regex`, built with `Regex.compile(pattern)` (or
`Regex.compile(pattern, flags)` — see [Flags](#flags)). Every method takes the text to
search:

| Call | Returns | What it does |
|---|---|---|
| `re.match(s)` | `bool` | `true` only if the pattern matches **all** of `s` (both ends anchored) |
| `re.find(s)` | `str` | the first matching substring, or `""` if there is none |
| `re.findAll(s)` | `List(str)` | every non-overlapping match, left to right |
| `re.groups(s)` | `List(str)` | the capture groups of the first match (see [Capture Groups](#capture-groups-pulling-pieces-out)) |
| `re.replace(s, repl)` | `str` | `s` with **every** match replaced by `repl` |
| `re.split(s)` | `List(str)` | the pieces of `s` between matches |

There is no `.matches()` method, on `Regex` or on `str`. To ask whether the pattern
occurs *anywhere* in a larger string, use `re.find(s) != ""`. That distinction —
`match` for "is the whole thing this shape?", `find` for "is this shape in there?" — is
the one most often gotten wrong, and several examples below lean on it.

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

Anchors assert position, not content. Because `.match()` already has to cover the whole
string, anchors earn their keep with `.find()`, `.findAll()` and `.replace()`:

```zebra
# file: regex-anchors.zbr
# teaches: position anchors in regex
# chapter: 21

def main()
    # ^ = start of string. Anchors matter with .find(), which searches;
    # .match() is already pinned to both ends of the string.
    var starts_with_hello = Regex.compile("^hello")

    if starts_with_hello.find("hello world") != ""
        print("'hello world' starts with hello")

    if starts_with_hello.find("say hello") == ""
        print("'say hello' does not")

    # $ = end of string
    var ends_with_txt = Regex.compile("\\.txt$")

    if ends_with_txt.find("document.txt") != ""
        print("document.txt ends with .txt")

    if ends_with_txt.find("document.txt.bak") == ""
        print("document.txt.bak does not")

    # With .match(), ^ and $ are implied: the whole string must fit
    var lowercase = Regex.compile("[a-z]+")
    print(lowercase.match("hello"))      # true
    print(lowercase.match("hello123"))   # false
    print(lowercase.find("hello123"))    # hello

    # Word boundary: \b
    var whole_word = Regex.compile("\\bcat\\b")
    print(whole_word.find("the cat sat"))         # cat
    print(whole_word.find("concatenate") == "")   # true
```

Output:

```text
'hello world' starts with hello
'say hello' does not
document.txt ends with .txt
document.txt.bak does not
true
false
hello
cat
true
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

    # A group bounds an alternation: gr(a|e)y, not gra|ey
    var grey = Regex.compile("gr(a|e)y")

    if grey.match("gray") and grey.match("grey")
        print("Matches 'gray' and 'grey'")
```

### Capture Groups: Pulling Pieces Out

Parentheses do a second job: each `(...)` **captures** the text it matched. `re.groups(s)`
finds the first match in `s` and returns what each group captured, as a `List(str)` in
the order the opening parentheses appear:

```zebra
# file: regex-capture.zbr
# teaches: capture groups with groups()
# chapter: 21

def main()
    var date_re = Regex.compile("(\\d{4})-(\\d{2})-(\\d{2})")
    var text = "Released 2026-10-05, patched 2026-11-02"

    # groups() finds the FIRST match and returns its capture groups, in order
    var parts = date_re.groups(text)
    print(parts.count())   # 3
    print(parts.at(0))     # 2026
    print(parts.at(1))     # 10
    print(parts.at(2))     # 05

    # Element 0 is the first group, not the whole match — use find() for that
    print(date_re.find(text))   # 2026-10-05

    # No match: an empty list
    var none = date_re.groups("no date here")
    print(none.count())    # 0

    # (?:...) groups without capturing
    var setting = Regex.compile("(?:name|title)=(\\w+)")
    print(setting.groups("title=Zebra"))   # ["Zebra"]
```

Output:

```text
3
2026
10
05
2026-10-05
0
["Zebra"]
```

Three things to know about the list `groups()` returns:

- **Element 0 is the first group**, not the whole match. If you want the whole match,
  call `find()`.
- **No match gives an empty list**, so `g.count()` is the check: compare it with the
  number of groups you wrote before reading any element.
- **It describes the first match only.** For the groups of every match, combine it with
  `findAll()` — each substring `findAll` returns is itself a match, so `groups()` on it
  succeeds:

```zebra
# file: regex-capture-all.zbr
# teaches: capture groups from every match (findAll + groups)
# chapter: 21

def main()
    var pair_re = Regex.compile("(\\w+)=(\\d+)")
    var config = "width=80, height=24, depth=3"

    # findAll returns each matching substring; groups() on each one splits it up
    for pair in pair_re.findAll(config)
        var g = pair_re.groups(pair)
        print("${g.at(0)} -> ${g.at(1)}")
```

Output:

```text
width -> 80
height -> 24
depth -> 3
```

> **Current limitation:** a group that does not take part in the match — an optional
> `(...)?` that was skipped, or the losing side of `(a)|(b)` — ends the list early, so
> the groups after it are missing too (`(a)?(b)` on `"b"` gives `[]`). Write patterns
> whose groups always participate: put the alternation *inside* one group, as in
> `(ERROR|WARN|INFO)`, rather than across several.

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
    # Ignore the formatting; count the digits
    var digit = Regex.compile("\\d")
    var digit_count = digit.findAll(phone).count()
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

    # Flexible: accept various formats
    if is_valid_phone_flexible("(555) 123-4567")
        print("Flexible format accepted")

    # Pull the three parts out with groups
    var parts_re = Regex.compile("\\(?(\\d{3})\\)?[ -]?(\\d{3})-(\\d{4})")
    var parts = parts_re.groups("(555) 123-4567")
    print("${parts.at(0)}-${parts.at(1)}-${parts.at(2)}")   # 555-123-4567
```

Output:

```text
Valid US phone
Invalid: wrong format
Valid international
Flexible format accepted
555-123-4567
```

### URL Validation

```zebra
# file: regex-url.zbr
# teaches: URL pattern matching and splitting a URL with groups
# chapter: 21

def main()
    # Basic HTTP(S) URL: scheme, then dot-separated host labels
    var url_pattern = Regex.compile("https?://[a-z0-9-]+(\\.[a-z0-9-]+)+")

    if url_pattern.match("https://example.com")
        print("Valid HTTPS URL")

    if url_pattern.match("http://example.co.uk")
        print("Valid HTTP URL")

    if not url_pattern.match("ftp://example.com")
        print("Doesn't match: FTP not in pattern")

    # Take a URL apart: scheme, host, path
    var parts_re = Regex.compile("^(https?)://([^/]+)(/.*)$")
    var parts = parts_re.groups("https://example.com/docs/regex")
    print("scheme: ${parts.at(0)}")   # https
    print("host:   ${parts.at(1)}")   # example.com
    print("path:   ${parts.at(2)}")   # /docs/regex
```

Output:

```text
Valid HTTPS URL
Valid HTTP URL
Doesn't match: FTP not in pattern
scheme: https
host:   example.com
path:   /docs/regex
```

---

## Finding and Extracting Patterns

### Finding Matches

`find` gives the first match, `findAll` gives all of them, and `split` gives what lies
between them:

```zebra
# file: regex-finding.zbr
# teaches: finding matches within text
# chapter: 21

def main()
    var text = "The prices are: $10, $25, and $100"
    var price_pattern = Regex.compile("\\$\\d+")

    # Does it occur anywhere? (.match would demand the WHOLE string be a price)
    if price_pattern.find(text) != ""
        print("Contains a price")

    # The first match
    print(price_pattern.find(text))   # $10

    # Every match, left to right
    var prices = price_pattern.findAll(text)
    print("Found ${prices.count()} prices:")
    for price in prices
        print("  ${price}")

    # The text BETWEEN matches
    var comma = Regex.compile(",\\s*")
    var fields = comma.split("red, green,blue,  yellow")
    print(fields)   # ["red", "green", "blue", "yellow"]
```

Output:

```text
Contains a price
$10
Found 3 prices:
  $10
  $25
  $100
["red", "green", "blue", "yellow"]
```

### Extracting from Structured Text

Capture groups turn "does this line have the right shape?" and "give me its fields" into
a single call:

```zebra
# file: regex-extract-structured.zbr
# teaches: extracting data from formatted text with capture groups
# chapter: 21

def extract_person_data(line: str): HashMap(str, str)?
    # Expected format: Name | Age | Email
    var pattern = Regex.compile("^([^|]+)\\|\\s*(\\d+)\\s*\\|\\s*(\\S+)\\s*$")
    var g = pattern.groups(line)
    if g.count() != 3
        return nil   # the line did not have the expected shape

    var data = HashMap(str, str)()
    data.set("name", g.at(0).trim())
    data.set("age", g.at(1))
    data.set("email", g.at(2))
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

    if extract_person_data("John Smith | thirty | john@example.com") == nil
        print("Rejected: age is not a number")
```

Output:

```text
Name: John Smith
Age: 30
Email: john@example.com
Rejected: age is not a number
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
    print(pattern.replace(text, "AT"))   # The cAT sAT on the mAT

    # Collapse runs of whitespace
    var spaces = Regex.compile("\\s+")
    print(spaces.replace("too    many   spaces", " "))   # too many spaces

    # Case-insensitive: pass "i" as the second argument to compile
    var cat_any_case = Regex.compile("cat", "i")
    print(cat_any_case.replace("Cat, CAT and cat", "dog"))   # dog, dog and dog

    # The replacement is inserted literally — there are no $1-style references
    var digits = Regex.compile("(\\d+)")
    print(digits.replace("order 42", "#$1"))   # order #$1
```

Output:

```text
The cAT sAT on the mAT
too many spaces
dog, dog and dog
order #$1
```

Because the replacement text is literal, a rewrite that needs pieces of the match —
reordering a date, say — is done with `groups()`, as in the next example.

### Data Transformation

```zebra
# file: regex-transform.zbr
# teaches: using regex for data transformation
# chapter: 21

def us_to_iso(date: str): str?
    # MM/DD/YYYY -> YYYY-MM-DD
    var us_date = Regex.compile("^(\\d{2})/(\\d{2})/(\\d{4})$")
    var g = us_date.groups(date)
    if g.count() != 3
        return nil
    return "${g.at(2)}-${g.at(0)}-${g.at(1)}"

def escape_html(text: str): str
    var escaped = text.replace("&", "&amp;")
    escaped = escaped.replace("<", "&lt;")
    escaped = escaped.replace(">", "&gt;")
    escaped = escaped.replace("\"", "&quot;")
    escaped = escaped.replace("'", "&#39;")
    return escaped

def main()
    print(us_to_iso("03/15/2025") orelse "not a date")   # 2025-03-15
    print(us_to_iso("15.03.2025") orelse "not a date")   # not a date

    # Rewrite every date in a sentence: findAll, then groups on each match
    var date_re = Regex.compile("(\\d{2})/(\\d{2})/(\\d{4})")
    var note = "Shipped 03/15/2025, delivered 03/18/2025."
    for d in date_re.findAll(note)
        note = note.replace(d, us_to_iso(d) orelse d)
    print(note)   # Shipped 2025-03-15, delivered 2025-03-18.

    # Escaping is plain str.replace — no regex needed
    var html_unsafe = "<script>alert('XSS')</script>"
    print(escape_html(html_unsafe))
```

Output:

```text
2025-03-15
not a date
Shipped 2025-03-15, delivered 2025-03-18.
&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;
```

> **Note:** bind the compiled pattern to a variable before calling a method on it, as
> these examples do. Calling a method straight off the compile in a declaration —
> `var g = Regex.compile(p).groups(s)` — passes `zebra -c` today but fails to build.

---

## Common Pitfalls

### Greedy vs. Non-Greedy

```zebra
# file: regex-greedy.zbr
# teaches: greedy, specific, and lazy matching
# chapter: 21

def main()
    var text = "<name>John</name> and <name>Jane</name>"

    # Greedy: .* runs as far as it can, swallowing both tags
    var greedy = Regex.compile("<name>.*</name>")
    print(greedy.find(text))      # <name>John</name> and <name>Jane</name>

    # Specific: [^<]+ cannot cross into the next tag
    var specific = Regex.compile("<name>[^<]+</name>")
    print(specific.findAll(text)) # ["<name>John</name>", "<name>Jane</name>"]

    # Lazy: .*? takes as little as it can
    var lazy = Regex.compile("<name>.*?</name>")
    print(lazy.findAll(text))     # ["<name>John</name>", "<name>Jane</name>"]

    # Pull out just the names
    var name_re = Regex.compile("<name>([^<]+)</name>")
    for tag in name_re.findAll(text)
        print(name_re.groups(tag).at(0))
```

Output:

```text
<name>John</name> and <name>Jane</name>
["<name>John</name>", "<name>Jane</name>"]
["<name>John</name>", "<name>Jane</name>"]
John
Jane
```

The lazy forms are `*?`, `+?` and `??`. One caveat specific to this engine: laziness
applies to the **whole pattern**, not to the one quantifier you wrote it on — a single `?`
suffix makes every match the shortest possible. If you need a greedy part and a lazy
part in one pattern, prefer a specific character class like `[^<]+`, which says what
you mean and behaves the same either way.

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

    if file_extension.find("document.txt") != ""
        print("Matches text file")

    # To match a literal dollar sign
    var price_pattern = Regex.compile("\\$[0-9]+")

    if price_pattern.match("$50")
        print("Matches price")

    # To match a literal backslash
    var path_pattern = Regex.compile("C:\\\\Users")  # Note: double backslash

    if path_pattern.match("C:\\Users")
        print("Matches Windows path")

    # A raw string keeps backslashes literal, so the pattern reads as written
    var raw_path = Regex.compile(r"C:\\Users")
    if raw_path.match("C:\\Users")
        print("Raw-string pattern matches too")
```

### Flags

The optional second argument to `Regex.compile` is a string of flag letters:

```zebra
# file: regex-flags.zbr
# teaches: compile flags (i, m, s)
# chapter: 21

def main()
    # i: ignore case
    var hello = Regex.compile("hello", "i")
    print(hello.match("HeLLo"))   # true

    # m: ^ and $ match at every line, not just the ends of the string
    var lines = "alpha\nbeta\ngamma"
    print(Regex.compile("^\\w+$").findAll(lines))        # []
    print(Regex.compile("^\\w+$", "m").findAll(lines))   # ["alpha", "beta", "gamma"]

    # s: . also matches a newline
    print(Regex.compile("a.b").match("a\nb"))        # false
    print(Regex.compile("a.b", "s").match("a\nb"))   # true

    # Flags combine
    print(Regex.compile("^B\\w+", "im").find(lines))   # beta
```

Output:

```text
true
[]
["alpha", "beta", "gamma"]
false
true
beta
```

| Flag | Effect |
|---|---|
| `i` | ignore ASCII case |
| `m` | `^` and `$` match at the start and end of every line |
| `s` | `.` matches a newline too |
| `U` | lift the cap on counted repetition (`{n,m}` is otherwise limited to 100) |

### Know Your Regex Dialect

Different tools support different features. Zebra's engine supports:

- ✅ Literals, `.`, classes `[...]` / `[^...]`, and the shortcuts `\d \w \s` with their
  negations `\D \W \S`
- ✅ Quantifiers `* + ? {n} {n,} {n,m}`, and lazy `*? +? ??`
- ✅ Anchors `^ $` and word boundaries `\b \B`
- ✅ Capturing `(...)` (up to 10 per pattern) and non-capturing `(?:...)` groups
- ✅ Alternation `|`
- ✅ Predictable performance — no catastrophic backtracking

It does **not** support:

- ❌ Lookahead or lookbehind (`(?=...)`, `(?!...)`, `(?<=...)`)
- ❌ Backreferences (`\1`) in a pattern, or `$1` in a replacement
- ❌ Unicode classes — matching is byte-by-byte ASCII
- ❌ Named groups (`(?<name>...)`)

---

## Practical Application: Log Analysis

Each log line has a time, a level and a message. One pattern with three groups both
checks a line's shape and takes it apart:

```zebra
# file: regex-log-analysis.zbr
# teaches: using regex for real log analysis
# chapter: 21

def analyze_logs(content: str)
    # time, level, message — all three groups take part in every match
    var entry_re = Regex.compile("^(\\d{2}:\\d{2}:\\d{2}) \\[(ERROR|WARN|INFO)\\] (.*)$")

    var counts = HashMap(str, int)()
    var errors: List(str) = []
    var unparsed = 0

    for line in content.lines()
        var g = entry_re.groups(line)
        if g.count() != 3
            unparsed = unparsed + 1
            continue
        var level = g.at(1)
        counts.set(level, (counts.get(level) orelse 0) + 1)
        if level == "ERROR"
            errors.add("${g.at(0)}  ${g.at(2)}")

    print("Log Analysis:")
    for level in ["ERROR", "WARN", "INFO"]
        print("  ${level}: ${counts.get(level) orelse 0}")
    print("  unparsed: ${unparsed}")

    if errors.count() > 0
        print("Errors:")
        for e in errors
            print("  ${e}")

def main()
    # In a real program: analyze_logs(File.read("app.log"))
    var log = "09:00:01 [INFO] server started\n09:00:05 [WARN] cache miss rate 40%\n09:01:12 [ERROR] database timeout after 30s\n--- rotated ---\n09:02:40 [INFO] request served\n09:03:02 [ERROR] disk 91% full\n"
    analyze_logs(log)
```

Output:

```text
Log Analysis:
  ERROR: 2
  WARN: 1
  INFO: 2
  unparsed: 1
Errors:
  09:01:12  database timeout after 30s
  09:03:02  disk 91% full
```

---

## Key Takeaways

1. **Regex for Patterns** — Use for validation, searching, and pattern-based extraction.

2. **`match` vs. `find`** — `match` asks whether the whole string fits; `find` asks whether the pattern occurs anywhere.

3. **Groups Do the Extraction** — `groups()` returns what each `(...)` captured; check `count()` before reading.

4. **Not for Parsing** — Use a real parser for JSON, XML, structured formats.

5. **Be Specific** — Avoid greedy patterns. Use character classes to narrow matches.

6. **Test Thoroughly** — Regex bugs are subtle. Test edge cases.

7. **Simple First** — Is `.contains()` sufficient? Use it instead of regex overhead.

---

## Exercises

1. **URL Extractor** — Find all URLs in text matching http(s)://
2. **Log Severity Counter** — Count [ERROR], [WARN], [INFO] lines in a log file
3. **Email List Validator** — Read CSV, validate email column, report invalid entries
4. **Phone Formatter** — Read list of numbers in various formats, output consistent format with `groups()`
5. **JSON Key Extractor** — Extract all JSON key names from a file

---

## What's Next

Chapter 22 covers FFI (Foreign Function Interface)—calling code written in other languages. Regexes are often used to parse data from external systems, making them a natural precursor.

# Unit 8 - Regular Expressions and Threads

**Course:** BT151CO - Object-Oriented Programming  
<!-- **Prepared by:** [Bishnu Khadka]    -->

| | |
|---|---|
| **Duration** | 4 Hours |
| **CLO** | CLO 4 - Apply advanced Python modules to solve real-world text processing and concurrency problems |
| **Pre-requisite** | Unit 7 - Network Programming; Unit 2 - OOP |

---

## Table of Contents

**Part A : Regular Expressions**

1. [What Is a Regular Expression?](#1-what-is-a-regular-expression)
2. [The `re` Module and `split()`](#2-the-re-module-and-split)
3. [Special Characters and Character Classes](#3-special-characters-and-character-classes)
4. [Working with Dates and Emails](#4-working-with-dates-and-emails)
5. [Quantifiers](#5-quantifiers)
6. [The `match()` Method](#6-the-match-method)
7. [The `findall()` Method](#7-the-findall-method)
8. [Character Sequences](#8-character-sequences)
9. [Substitution with `sub()`](#9-substitution-with-sub)
10. [The `search()` Method](#10-the-search-method)

---

# Part A - Regular Expressions

# 1. What Is a Regular Expression?

## 1.1 The Problem Regular Expressions Solve

Imagine you are working at a university library. Every day, students submit paper forms to register their library cards. The forms contain information like:

- Student ID: `BT2024-0042`
- Email: `alice.student@university.edu`
- Date of birth: `12/05/2004`
- Phone: `+44 7700 900123`

Now imagine you have **10,000 of these forms** scanned into a big text file. Your job is to:

1. Extract all email addresses
2. Find all students born before 2000
3. Check whether any phone numbers are in the wrong format
4. Replace all UK date formats (`DD/MM/YYYY`) with ISO format (`YYYY-MM-DD`)

How would you do this with regular Python string methods? You could write hundreds of `if` statements, loops, and `.split()` calls - and it would be fragile, messy, and slow to change.

**A regular expression (regex) solves all four tasks in four lines.**

---

## 1.2 The Concept - A Pattern Language

A **regular expression** is a **pattern** written in a special mini-language that describes what text you are looking for. Think of it like a **search template**.

Real-world analogy - the **form template**:

> When you fill in a registration form, the form already has boxes with instructions:
> - `[First Name] _______` - the box tells you what goes here
> - `[Date] __/__/____` - the format is built into the box shape

A regular expression is the same idea - you describe the **shape** of the text you expect, and Python finds all the text that fits that shape.

| Plain English | Regular Expression | What It Matches |
|---|---|---|
| Any digit | `\d` | `0`, `1`, `5`, `9` |
| Any letter | `[a-zA-Z]` | `a`, `Z`, `m` |
| An email address | `\S+@\S+\.\S+` | `alice@example.com` |
| A UK date | `\d{2}/\d{2}/\d{4}` | `12/05/2004` |

---

## 1.3 Importing the `re` Module

Python's regular expression tools live in the built-in `re` module - no installation needed.

```python
import re  # The regular expression module

# All regex work is done through functions in this module:
# re.match(), re.search(), re.findall(), re.sub(), re.split()
```

---

# 2. The `re` Module and `split()`

## 2.1 Plain String `split()` vs `re.split()`

You already know Python's built-in `.split()` method:

```python
# Built-in split - splits on ONE fixed separator
sentence = "Alice scored 95 in maths"
words = sentence.split(" ")   # only splits on a space
print(words)
```

```
['Alice', 'scored', '95', 'in', 'maths']
```

This works fine when your separator is always the same character. But real-world text is messy. Student names in a spreadsheet might be separated by commas, semicolons, or extra spaces:

```python
# Problem: inconsistent separators
student_list = "Alice, Bob;  Charlie,   Diana; Eve"

# Built-in split can only handle ONE separator at a time
print(student_list.split(","))
# ['Alice', ' Bob;  Charlie', '   Diana; Eve'] - not what we want!
```

**`re.split()`** accepts a **pattern** as the separator, so it can handle all of them at once.

---

## 2.2 `re.split()` - Syntax and Usage

```python
re.split(pattern, string, maxsplit=0, flags=0)
```

| Parameter | Meaning |
|---|---|
| `pattern` | A regex pattern describing the separator |
| `string` | The text to split |
| `maxsplit` | Maximum number of splits (0 = unlimited) |
| `flags` | Optional modifiers (e.g., `re.IGNORECASE`) |

---

## 2.3 Example - Splitting a Messy Student List

```python
import re

# Student names separated by commas, semicolons, or extra spaces
student_list = "Alice, Bob;  Charlie,   Diana; Eve"

# Pattern: one or more of: comma, semicolon, or whitespace
parts = re.split(r"[,;\s]+", student_list)
print(parts)
```

```
['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
```

**Breaking down the pattern `[,;\s]+`:**

| Part | Meaning |
|---|---|
| `[...]` | Character class - "any ONE of these characters" |
| `,` | A literal comma |
| `;` | A literal semicolon |
| `\s` | Any whitespace character (space, tab, newline) |
| `+` | One or more of the preceding element |

**Together:** Split wherever you see one or more commas, semicolons, or spaces.

---

## 2.4 Example - Splitting a Shopping Receipt

```python
import re

# Items on a till receipt - separated by commas or " and " or " & "
receipt = "Milk, Bread and Eggs & Butter, Coffee"

items = re.split(r",\s*|\s+and\s+|\s*&\s*", receipt)
print(items)
```

```
['Milk', 'Bread', 'Eggs', 'Butter', 'Coffee']
```

**Pattern breakdown `r",\s*|\s+and\s+|\s*&\s*"`:**

| Part | Meaning |
|---|---|
| `,\s*` | A comma followed by zero or more spaces |
| `\|` | OR (try the next alternative) |
| `\s+and\s+` | " and " with spaces around it |
| `\|` | OR |
| `\s*&\s*` | "&" with optional spaces |

> **Note:** The `r"..."` prefix is a **raw string**. Always use raw strings for regex patterns. Without `r`, Python would interpret `\s` as an escape sequence before regex even sees it.

---

## 2.5 `maxsplit` - Limiting How Many Splits Occur

```python
import re

# A game scoreboard entry: "PlayerName:Score:Level:Badge"
entry = "Alice:1500:12:Gold"

# Split on colon, but only the first split - get name separately
name, rest = re.split(r":", entry, maxsplit=1)
print(f"Name : {name}")
print(f"Rest : {rest}")
```

```
Name : Alice
Rest : 1500:12:Gold
```

---

> **Common Mistake 1:** Forgetting the `r` prefix on the pattern string.
>
> ```python
> # BAD - Python interprets \s before regex sees it
> re.split("\s+", text)   # may work, but unreliable
>
> # GOOD - raw string passes \s directly to the regex engine
> re.split(r"\s+", text)  # always use r"..." for patterns
> ```

---

# 3. Special Characters and Character Classes

---

## 3.1 Why "Special" Characters?

In a regular expression, most characters match themselves literally. The letter `a` in a pattern matches the letter `a` in the text. But some characters have **special meaning** - they are instructions to the regex engine, not literal characters to match.

These special characters are called **metacharacters**:

```
. ^ $ * + ? { } [ ] \ | ( )
```

---

## 3.2 The Metacharacters - Quick Reference

| Symbol | Name | What It Does | Example |
|---|---|---|---|
| `.` | Dot | Matches **any single character** except newline | `c.t` matches `cat`, `cut`, `c9t` |
| `^` | Caret | Matches the **start** of the string | `^Dear` matches if string starts with "Dear" |
| `$` | Dollar | Matches the **end** of the string | `\.pdf$` matches strings ending in ".pdf" |
| `*` | Star | Zero or more of the preceding element | `go*gle` matches `ggle`, `gogle`, `google` |
| `+` | Plus | One or more of the preceding element | `go+gle` matches `gogle`, `google`, NOT `ggle` |
| `?` | Question mark | Zero or one (makes something optional) | `colou?r` matches `color` and `colour` |
| `\` | Backslash | Escapes a metacharacter; or introduces a sequence | `\.` matches a literal dot |
| `\|` | Pipe | OR - try left side, then right side | `cat\|dog` matches `cat` or `dog` |

---

## 3.3 Character Classes `[...]`

A character class lets you define a **set** of characters - the pattern matches if any ONE of them appears at that position.

```python
import re

# Find all vowels in a student's name
name = "Bartholomew"
vowels = re.findall(r"[aeiouAEIOU]", name)
print(f"Vowels in '{name}': {vowels}")
print(f"Count: {len(vowels)}")
```

```
Vowels in 'Bartholomew': ['a', 'o', 'o', 'e', 'o']
Count: 5
```

**Ranges inside character classes:**

| Pattern | Matches |
|---|---|
| `[a-z]` | Any lowercase letter |
| `[A-Z]` | Any uppercase letter |
| `[0-9]` | Any digit (same as `\d`) |
| `[a-zA-Z]` | Any letter, upper or lower |
| `[a-zA-Z0-9]` | Any letter or digit (alphanumeric) |
| `[^aeiou]` | Any character that is NOT a vowel (`^` inside `[...]` means NOT) |

---

## 3.4 Predefined Character Sequences

Python's `re` module provides shorthand sequences for common character classes:

| Sequence | Meaning | Equivalent class |
|---|---|---|
| `\d` | Any digit | `[0-9]` |
| `\D` | Any non-digit | `[^0-9]` |
| `\w` | Any word character (letter, digit, underscore) | `[a-zA-Z0-9_]` |
| `\W` | Any non-word character | `[^a-zA-Z0-9_]` |
| `\s` | Any whitespace (space, tab, newline) | `[ \t\n\r\f\v]` |
| `\S` | Any non-whitespace | `[^ \t\n\r\f\v]` |
| `\b` | Word boundary (between word and non-word character) | (zero-width) |

```python
import re

game_log = "Player1 scored 250 points. Player2 scored 1800 points."

# \d+ means "one or more digits"
scores = re.findall(r"\d+", game_log)
print(f"Scores found: {scores}")
```

```
Scores found: ['1', '250', '2', '1800']
```

> Notice it also found `1` and `2` from `Player1` and `Player2`. We will handle this precisely with `search()` and `findall()` in later sections.

---

## 3.5 Escaping Metacharacters

When you want to match a **literal** metacharacter (e.g., an actual dot or dollar sign), you must **escape** it with a backslash:

```python
import re

# Prices on a shopping list - match the literal "£" and digits
prices = "Tea: £2.50, Coffee: £3.75, Cake: £1.20"

# \d+ matches digits; \. matches a literal dot (not any character)
found = re.findall(r"£\d+\.\d{2}", prices)
print(found)
```

```
['£2.50', '£3.75', '£1.20']
```

Without escaping the dot (`\.`), `\d+.\d{2}` would match `£250` followed by any character and two digits - giving wrong results.

---

# 4. Working with Dates and Emails

---

## 4.1 Matching Date Formats

Dates appear in many formats in real data. A university database might store:
- `12/05/2024` (UK: DD/MM/YYYY)
- `2024-05-12` (ISO: YYYY-MM-DD)
- `12 May 2024` (Written)

Let's match UK dates first:

```python
import re

# Library borrowing log - find all return dates
borrow_log = """
Alice borrowed "Python Cookbook" on 01/03/2024, due back 15/03/2024.
Bob borrowed "Clean Code" on 22/02/2024, due back 07/03/2024.
Diana borrowed "Fluent Python" on 14/03/2024, due back 28/03/2024.
"""

# \d{2} = exactly 2 digits, \d{4} = exactly 4 digits
dates = re.findall(r"\d{2}/\d{2}/\d{4}", borrow_log)
print("Dates found:")
for d in dates:
    print(f"  {d}")
```

```
Dates found:
  01/03/2024
  15/03/2024
  22/02/2024
  07/03/2024
  14/03/2024
  28/03/2024
```

---

## 4.2 Capturing Groups - Extracting Date Parts

What if you want each part of the date (day, month, year) separately? Use **capturing groups** with parentheses `( )`:

```python
import re

dates_text = "Student enrolled on 12/05/2024 and will graduate on 30/06/2028."

# Parentheses () create capturing groups
# Each group captures one part of the date
pattern = r"(\d{2})/(\d{2})/(\d{4})"
matches = re.findall(pattern, dates_text)

print("Captured date parts:")
for day, month, year in matches:
    print(f"  Day: {day}, Month: {month}, Year: {year}")
    # Convert to ISO format
    print(f"  ISO: {year}-{month}-{day}")
```

```
Captured date parts:
  Day: 12, Month: 05, Year: 2024
  ISO: 2024-05-12
  Day: 30, Month: 06, Year: 2028
  ISO: 2028-06-30
```

---

## 4.3 Matching Email Addresses

Email addresses have a predictable structure: `local-part @ domain . extension`

```python
import re

# Student registration emails from a university system
registration_data = """
Name: Alice Smith       Email: alice.smith@university.edu
Name: Bob Jones         Email: b.jones99@college.ac.uk
Name: Charlie Brown     Email: charlie_b@student.org
Name: INVALID ENTRY     Email: not-an-email
Name: Diana Prince      Email: diana@example.com
"""

# Pattern breakdown:
# \S+   = one or more non-whitespace characters (local part)
# @     = literal @ symbol
# \S+   = one or more non-whitespace (domain name)
# \.    = literal dot
# \S+   = one or more non-whitespace (extension, e.g. com, edu, ac.uk)
pattern = r"\S+@\S+\.\S+"

emails = re.findall(pattern, registration_data)
print("Email addresses found:")
for email in emails:
    print(f"  {email}")
```

```
Email addresses found:
  alice.smith@university.edu
  b.jones99@college.ac.uk
  charlie_b@student.org
  diana@example.com
```

> Note: `not-an-email` was correctly excluded because it has no `@` symbol.

---

## 4.4 A More Precise Email Pattern

The simple `\S+@\S+\.\S+` is a good start but would match `"email@example.com,"` (with the trailing comma). A more robust pattern:

```python
import re

emails_raw = "Contact: alice@uni.edu, bob@college.ac.uk, or support@help.org for issues."

# More precise: word chars and dots in local part, then @, then domain
pattern = r"[\w.\-]+@[\w.\-]+\.[a-zA-Z]{2,}"

# Breakdown:
# [\w.\-]+    = letters, digits, underscore, dot, or hyphen (local part)
# @           = literal @
# [\w.\-]+    = domain name
# \.          = literal dot
# [a-zA-Z]{2,} = extension of 2 or more letters (com, uk, edu, etc.)

emails = re.findall(pattern, emails_raw)
print(emails)
```

```
['alice@uni.edu', 'bob@college.ac.uk', 'support@help.org']
```

---

# 5. Quantifiers

---

## 5.1 What Is a Quantifier?

A **quantifier** tells the regex engine **how many times** the preceding element should appear. Without quantifiers, every element matches exactly once.

---

## 5.2 The Six Quantifiers

| Quantifier | Meaning | Example | Matches |
|---|---|---|---|
| `*` | 0 or more | `go*gle` | `ggle`, `gogle`, `google`, `goooogle` |
| `+` | 1 or more | `go+gle` | `gogle`, `google` (NOT `ggle`) |
| `?` | 0 or 1 (optional) | `colou?r` | `color`, `colour` |
| `{n}` | Exactly n | `\d{4}` | `2024`, `0042` |
| `{n,m}` | Between n and m | `\d{2,4}` | `12`, `123`, `1234` |
| `{n,}` | n or more | `\d{3,}` | `100`, `9999`, `123456` |

---

## 5.3 Examples - Student IDs and Game Scores

```python
import re

# Student IDs: exactly 2 letters then exactly 4 digits
student_ids = "Valid IDs: BT2024, CS1999, AB0001. Bad IDs: B2024, BTS12345."
valid_ids = re.findall(r"[A-Z]{2}\d{4}", student_ids)
print(f"Valid student IDs: {valid_ids}")
```

```
Valid student IDs: ['BT2024', 'CS1999', 'AB0001']
```

```python
import re

# Game high scores - 3 to 6 digit scores only
scoreboard = "Alice: 950, Bob: 12, Charlie: 15000, Diana: 4250, Eve: 1"
# \b = word boundary (prevents matching part of a larger number)
scores = re.findall(r"\b\d{3,6}\b", scoreboard)
print(f"Valid scores (3-6 digits): {scores}")
```

```
Valid scores (3-6 digits): ['950', '15000', '4250']
```

> `Bob: 12` and `Eve: 1` were excluded (too few digits). `Charlie: 15000` was included because 15000 is 5 digits.

---

## 5.4 Greedy vs Non-Greedy Matching

By default, quantifiers are **greedy** - they match **as much text as possible**. Adding `?` after a quantifier makes it **non-greedy** (matches as little as possible).

```python
import re

# Shopping cart HTML snippet (simplified)
html = "<item>Milk</item><item>Bread</item>"

# GREEDY - matches from first < to last >
greedy_match = re.findall(r"<.*>", html)
print(f"Greedy : {greedy_match}")

# NON-GREEDY - matches the shortest possible string
non_greedy = re.findall(r"<.*?>", html)
print(f"Non-greedy: {non_greedy}")
```

```
Greedy : ['<item>Milk</item><item>Bread</item>']
Non-greedy: ['<item>', '</item>', '<item>', '</item>']
```

> **Rule of thumb:** Use `*?` or `+?` when you want to match the smallest possible piece of text between two delimiters.

---

## 5.5 The `?` Quantifier - Optional Elements

```python
import re

# Bank account numbers - may or may not have a dash
accounts = ["ACC-0042", "ACC0043", "ACC-9999", "ACC8888"]

pattern = r"ACC-?\d{4}"  # The hyphen is optional

for acc in accounts:
    match = re.match(pattern, acc)
    if match:
        print(f"  Valid: {acc}")
    else:
        print(f"  Invalid: {acc}")
```

```
  Valid: ACC-0042
  Valid: ACC0043
  Valid: ACC-9999
  Valid: ACC8888
```

---

# 6. The `match()` Method

---

## 6.1 What `match()` Does

`re.match(pattern, string)` tries to match the pattern **at the very beginning** of the string. It returns a **Match object** if the pattern is found at the start, or `None` if it is not.

> **Critical:** `match()` only checks the start. It does not search the entire string.

```python
re.match(pattern, string, flags=0)
```

---

## 6.2 The Match Object

When `match()` succeeds it returns a **Match object**. The most useful methods:

| Method | Returns |
|---|---|
| `.group()` or `.group(0)` | The entire matched text |
| `.group(1)`, `.group(2)` | Captured groups (from parentheses) |
| `.start()` | Start position of the match |
| `.end()` | End position of the match |
| `.span()` | Tuple `(start, end)` |

---

## 6.3 Example - Validating a Student ID Format

```python
import re

def validate_student_id(student_id):
    """Check that a student ID matches the pattern: 2 letters + 4 digits."""
    # ^ anchors to the start; $ anchors to the end
    pattern = r"^[A-Z]{2}\d{4}$"
    match = re.match(pattern, student_id)
    if match:
        print(f"  '{student_id}' is VALID - matched: '{match.group()}'")
    else:
        print(f"  '{student_id}' is INVALID")

# Test a range of IDs
test_ids = ["BT2024", "cs1999", "BTS12345", "AB00", "CS2000", "123456"]
for sid in test_ids:
    validate_student_id(sid)
```

```
  'BT2024' is VALID - matched: 'BT2024'
  'cs1999' is INVALID
  'BTS12345' is INVALID
  'AB00' is INVALID
  'CS2000' is VALID - matched: 'CS2000'
  '123456' is INVALID
```

> `'cs1999'` failed because the pattern requires uppercase `[A-Z]`. To accept both cases, use `re.IGNORECASE` as a flag, or change the pattern to `[A-Za-z]{2}`.

---

## 6.4 Example - Validating Bank Account Numbers

```python
import re

# Account number format: "ACC" then optional dash then 4-8 digits
pattern = r"^ACC-?\d{4,8}$"

accounts = [
    "ACC-00421234",  # 8 digits - valid
    "ACC5678",       # no dash, 4 digits - valid
    "ACC-123",       # only 3 digits - invalid
    "ACCOUNT-9999",  # wrong prefix - invalid
    "ACC-000000000", # 9 digits - invalid (too many)
]

print("Bank account validation:")
for acc in accounts:
    result = re.match(pattern, acc)
    status = "VALID" if result else "INVALID"
    print(f"  {acc:<20} -> {status}")
```

```
Bank account validation:
  ACC-00421234         -> VALID
  ACC5678              -> VALID
  ACC-123              -> INVALID
  ACCOUNT-9999         -> INVALID
  ACC-000000000        -> INVALID
```

---

## 6.5 Using Named Groups

You can give a capturing group a name using `(?P<name>...)`. This makes the code much more readable:

```python
import re

# Parse a library catalogue entry: "AUTHOR_TITLE_YEAR"
entry = "Lutz_LearningPython_2013"

pattern = r"^(?P<author>\w+)_(?P<title>\w+)_(?P<year>\d{4})$"
match = re.match(pattern, entry)

if match:
    print(f"Author : {match.group('author')}")
    print(f"Title  : {match.group('title')}")
    print(f"Year   : {match.group('year')}")
```

```
Author : Lutz
Title  : LearningPython
Year   : 2013
```

---

# 7. The `findall()` Method

---

## 7.1 What `findall()` Does

`re.findall(pattern, string)` searches the **entire string** and returns a **list** of every non-overlapping match. Unlike `match()`, it does not stop at the first match and does not require the match to be at the start.

```python
re.findall(pattern, string, flags=0)
```

**Return value:**
- If the pattern has **no groups**: returns a list of strings (the matched text)
- If the pattern has **one group**: returns a list of strings (just the group content)
- If the pattern has **multiple groups**: returns a list of tuples

---

## 7.2 Example - Finding All Scores in a Game Report

```python
import re

game_report = """
Round 1: Alice scored 1200, Bob scored 850.
Round 2: Alice scored 980, Bob scored 1650.
Round 3: Alice scored 2100, Bob scored 1100.
"""

# Find every score (sequence of digits)
all_scores = re.findall(r"\d+", game_report)
print(f"All numbers found: {all_scores}")

# Find scores 4 digits or more (1000+)
high_scores = re.findall(r"\b\d{4,}\b", game_report)
print(f"High scores (4+ digits): {high_scores}")
```

```
All numbers found: ['1', '1200', '850', '2', '980', '1650', '3', '2100', '1100']
High scores (4+ digits): ['1200', '1650', '2100', '1100']
```

---

## 7.3 Example - Extracting Book Details from a Library Catalogue

```python
import re

catalogue = """
[001] Learning Python - Mark Lutz - 2013
[002] Fluent Python - Luciano Ramalho - 2022
[003] Clean Code - Robert C. Martin - 2008
[004] Python Cookbook - David Beazley - 2013
"""

# Extract: ID, title, author from each line
# Pattern with three capturing groups
pattern = r"\[(\d{3})\] (.+?) - (.+?) - \d{4}"
books = re.findall(pattern, catalogue)

print(f"{'ID':<6} {'Title':<25} Author")
print("-" * 55)
for book_id, title, author in books:
    print(f"[{book_id}]  {title:<25} {author}")
```

```
ID     Title                     Author
-------------------------------------------------------
[001]  Learning Python           Mark Lutz
[002]  Fluent Python             Luciano Ramalho
[003]  Clean Code                Robert C. Martin
[004]  Python Cookbook           David Beazley
```

---

## 7.4 Example - Extracting Prices from a Shopping List

```python
import re

shopping_data = """
Item: Milk       Price: £1.09
Item: Bread      Price: £1.35
Item: Coffee     Price: £4.99
Item: Tea bags   Price: £2.50
Total: £9.93
"""

# Extract all prices (£ followed by digits.2digits)
prices = re.findall(r"£(\d+\.\d{2})", shopping_data)
print(f"Prices found: {prices}")

# The group () captures only the number part (without £)
total = sum(float(p) for p in prices)
print(f"Sum of all prices: £{total:.2f}")
```

```
Prices found: ['1.09', '1.35', '4.99', '2.50', '9.93']
Sum of all prices: £19.86
```

> Notice the group `()` around `\d+\.\d{2}` captures only the number, not the `£` symbol. This makes converting to `float()` straightforward.

---

## 7.5 `findall()` vs `finditer()`

`findall()` returns a list - all matches at once.  
`finditer()` returns an **iterator** of Match objects - useful when you need position info or when the text is very large.

```python
import re

text = "Students: Alice (ID: 101), Bob (ID: 202), Charlie (ID: 303)"

# finditer() gives Match objects with position info
for match in re.finditer(r"\d{3}", text):
    print(f"  Found '{match.group()}' at position {match.start()}-{match.end()}")
```

```
  Found '101' at position 21-24
  Found '202' at position 32-35
  Found '303' at position 46-49
```

---

# 8. Character Sequences

---

## 8.1 Predefined Sequences - Deep Dive

You met the predefined sequences in Section 3.4. Here is a deeper look with practical examples.

---

## 8.2 `\w` and `\W` - Word Characters

```python
import re

# \w matches letters, digits, and underscore
# Useful for extracting identifiers, usernames, variable names

code_snippet = "student_name = 'Alice'; score_2024 = 95"

# Find all Python identifiers (words including underscores)
identifiers = re.findall(r"\b\w+\b", code_snippet)
print(f"Identifiers: {identifiers}")

# Find all NON-word characters (punctuation, spaces, operators)
non_word = re.findall(r"\W", code_snippet)
print(f"Non-word chars: {non_word}")
```

```
Identifiers: ['student_name', 'Alice', 'score_2024', '95']
Non-word chars: [' ', '=', ' ', "'", "'", ';', ' ', ' ', '=', ' ']
```

---

## 8.3 `\b` - Word Boundaries

`\b` is a **zero-width assertion** - it matches a position between a word character and a non-word character. It does not consume any characters.

```python
import re

# Without \b - "cat" matches inside "scatter" and "concatenate"
text = "The cat scattered across the concatenation of books."
matches_no_boundary = re.findall(r"cat", text)
print(f"Without \\b: {matches_no_boundary}")

# With \b - only the standalone word "cat"
matches_with_boundary = re.findall(r"\bcat\b", text)
print(f"With \\b:    {matches_with_boundary}")
```

```
Without \b: ['cat', 'cat', 'cat']
With \b:    ['cat']
```

---

## 8.4 `\d` and `\D` - Digits and Non-Digits

```python
import re

# Library book ISBN - digits only, no spaces or hyphens
isbn_raw = "ISBN: 978-0-13-468599-1"

# Extract all digits
digits_only = re.findall(r"\d", isbn_raw)
clean_isbn = "".join(digits_only)
print(f"Raw ISBN    : {isbn_raw}")
print(f"Digits only : {clean_isbn}")
print(f"Valid ISBN-13: {len(clean_isbn) == 13}")
```

```
Raw ISBN    : ISBN: 978-0-13-468599-1
Digits only : 9780134685991
Valid ISBN-13: True
```

---

## 8.5 `\s` and `\S` - Whitespace and Non-Whitespace

```python
import re

# Normalise student essay - collapse multiple spaces into one
messy_text = "The   student  wrote   an    essay    about    Python."

clean_text = re.sub(r"\s+", " ", messy_text)
print(f"Original : {messy_text!r}")
print(f"Cleaned  : {clean_text!r}")
```

```
Original : 'The   student  wrote   an    essay    about    Python.'
Cleaned  : 'The student wrote an essay about Python.'
```

---

# 9. Substitution with `sub()`

---

## 9.1 What `sub()` Does

`re.sub(pattern, replacement, string, count=0, flags=0)` finds all matches of `pattern` in `string` and **replaces** them with `replacement`. It returns a **new string** - the original is unchanged.

```python
re.sub(pattern, replacement, string, count=0, flags=0)
```

| Parameter | Meaning |
|---|---|
| `pattern` | What to find |
| `replacement` | What to replace it with |
| `string` | The text to search |
| `count` | Max number of replacements (0 = replace all) |

---

## 9.2 Example - Censoring Student Exam Answers

```python
import re

# Redact all student names in an exam script for anonymous marking
exam_script = """
Student: Alice Johnson
Q1: The capital of France is Paris.
Q2: Signed: Alice Johnson, 12/05/2024
"""

# Replace full names (Two Titlecase Words)
anonymous = re.sub(r"[A-Z][a-z]+ [A-Z][a-z]+", "[REDACTED]", exam_script)
print(anonymous)
```

```

Student: [REDACTED]
Q1: The capital of France is Paris.
Q2: Signed: [REDACTED], 12/05/2024
```

---

## 9.3 Example - Converting Date Formats

```python
import re

# Library records stored in DD/MM/YYYY - convert to ISO YYYY-MM-DD
borrow_records = """
Alice borrowed: 15/03/2024
Bob borrowed:   22/02/2024
Diana borrowed: 01/04/2024
"""

# Capturing groups let us rearrange the parts in the replacement
# \1 = day, \2 = month, \3 = year
iso_records = re.sub(
    r"(\d{2})/(\d{2})/(\d{4})",  # pattern with 3 groups
    r"\3-\2-\1",                  # replacement: year-month-day
    borrow_records
)
print(iso_records)
```

```
Alice borrowed: 2024-03-15
Bob borrowed:   2024-02-22
Diana borrowed: 2024-04-01
```

**How `\1`, `\2`, `\3` work:**
- In the replacement string, `\1` inserts what group 1 captured (DD)
- `\2` inserts what group 2 captured (MM)
- `\3` inserts what group 3 captured (YYYY)

---

## 9.4 Example - Cleaning Up a Shopping Price List

```python
import re

# Raw price list with inconsistent currency formats
prices_raw = "Milk:$1.50, Bread:$1.35, Coffee:$4.99"

# Replace dollar signs with pound signs
prices_gbp = re.sub(r"\$", "£", prices_raw)
print(prices_gbp)
```

```
Milk:£1.50, Bread:£1.35, Coffee:£4.99
```

---

## 9.5 Using a Function as the Replacement

The `replacement` argument can be a **function** that takes a Match object and returns a string. This allows context-sensitive replacements.

```python
import re

# Increase every game score in a report by 10%
game_results = "Alice: 1000 points, Bob: 850 points, Charlie: 1200 points"

def boost_score(match):
    """Multiply the matched score by 1.1 and return as integer string."""
    original = int(match.group())
    boosted  = int(original * 1.1)
    return str(boosted)

# Replace every number with its boosted version
boosted_results = re.sub(r"\d+", boost_score, game_results)
print(f"Original : {game_results}")
print(f"Boosted  : {boosted_results}")
```

```
Original : Alice: 1000 points, Bob: 850 points, Charlie: 1200 points
Boosted  : Alice: 1100 points, Bob: 935 points, Charlie: 1320 points
```

---

## 9.6 `subn()` - Substitution with a Count

`re.subn()` works exactly like `sub()` but returns a **tuple** `(new_string, number_of_replacements)`. Useful for auditing how many changes were made.

```python
import re

text = "The bank balance is £500. After withdrawal: £500 - £200 = £300."

new_text, count = re.subn(r"£\d+", "[AMOUNT REDACTED]", text)
print(f"Result : {new_text}")
print(f"Changed: {count} amount(s) redacted")
```

```
Result : The bank balance is [AMOUNT REDACTED]. After withdrawal: [AMOUNT REDACTED] - [AMOUNT REDACTED] = [AMOUNT REDACTED].
Changed: 4 amount(s) redacted
```

---

> **Common Mistake 2:** Forgetting that `sub()` returns a new string - it does NOT modify the original.
>
> ```python
> text = "Hello World"
> re.sub(r"World", "Python", text)   # BAD - result is discarded
> print(text)                        # still "Hello World"
>
> text = re.sub(r"World", "Python", text)  # GOOD - assign the result
> print(text)                              # "Hello Python"
> ```

---

# 10. The `search()` Method

---

## 10.1 `search()` vs `match()`

| Feature | `match()` | `search()` |
|---|---|---|
| Where it looks | Only at the **start** of the string | **Anywhere** in the string |
| Returns | Match object or `None` | Match object or `None` |
| Stops at | First match | First match |
| Use when | Validating format of a whole string | Finding something inside a string |

---

## 10.2 Syntax

```python
re.search(pattern, string, flags=0)
```

---

## 10.3 Example - Finding a Student Number Inside a Sentence

```python
import re

# match() fails because the ID is not at the start
text = "Welcome back! Your student ID is BT2024."

# match() - looks only at the start
result_match = re.match(r"[A-Z]{2}\d{4}", text)
print(f"match()  : {result_match}")   # None - ID is not at position 0

# search() - scans the whole string
result_search = re.search(r"[A-Z]{2}\d{4}", text)
if result_search:
    print(f"search() : found '{result_search.group()}' at position {result_search.start()}")
```

```
match()  : None
search() : found 'BT2024' at position 33
```

---

## 10.4 Example - Detecting Suspicious Transactions

```python
import re

def check_transaction(description):
    """Flag a bank transaction if it contains suspicious keywords."""
    # search() finds the keyword anywhere in the description
    suspicious_pattern = r"\b(withdraw|transfer|overseas|foreign)\b"
    match = re.search(suspicious_pattern, description, re.IGNORECASE)
    if match:
        print(f"  FLAGGED: '{description}' - keyword: '{match.group()}'")
    else:
        print(f"  OK     : '{description}'")

transactions = [
    "Purchase at Book Store - £24.99",
    "OVERSEAS transfer to account 9876",
    "Monthly salary credit",
    "Cash withdraw at ATM",
    "Coffee shop payment",
]

print("Transaction review:")
for t in transactions:
    check_transaction(t)
```

```
Transaction review:
  OK     : 'Purchase at Book Store - £24.99'
  FLAGGED: 'OVERSEAS transfer to account 9876' - keyword: 'OVERSEAS'
  OK     : 'Monthly salary credit'
  FLAGGED: 'Cash withdraw at ATM' - keyword: 'withdraw'
  OK     : 'Coffee shop payment'
```

---

## 10.5 Example - Parsing Game Chat for Commands

```python
import re

def parse_command(chat_message):
    """Extract a game command (e.g., /buy sword) from a chat message."""
    # Commands start with "/" followed by a word and optional arguments
    match = re.search(r"/(\w+)(?:\s+(.+))?", chat_message)
    if match:
        command = match.group(1)
        argument = match.group(2) if match.group(2) else "(none)"
        print(f"  Command: {command:<12} Argument: {argument}")
    else:
        print(f"  No command in: {chat_message!r}")

messages = [
    "Player says: hello everyone! /buy sword",
    "/attack dragon",
    "/heal",
    "Just chatting, no command here",
    "Let me check: /inventory items",
]

print("Chat command parser:")
for msg in messages:
    parse_command(msg)
```

```
Chat command parser:
  Command: buy          Argument: sword
  Command: attack       Argument: dragon
  Command: heal         Argument: (none)
  No command in: 'Just chatting, no command here'
  Command: inventory    Argument: items
```

---

## 10.6 `re.IGNORECASE` and Other Flags

Flags modify how the regex engine works:

| Flag | Short form | Effect |
|---|---|---|
| `re.IGNORECASE` | `re.I` | Case-insensitive matching |
| `re.MULTILINE` | `re.M` | `^` and `$` match start/end of each line |
| `re.DOTALL` | `re.S` | `.` matches newlines too |
| `re.VERBOSE` | `re.X` | Allow whitespace and comments in the pattern |

```python
import re

# Case-insensitive search for library genre tags
catalogue_entry = "Genre: SCIENCE FICTION - suitable for advanced students"
match = re.search(r"science fiction", catalogue_entry, re.IGNORECASE)
if match:
    print(f"Genre found: '{match.group()}'")
```

```
Genre found: 'SCIENCE FICTION'
```

---

## 10.7 Compiling Patterns - `re.compile()`

If you use the same pattern many times (e.g., inside a loop), compile it first for better performance:

```python
import re

# Compile once, use many times
student_id_pattern = re.compile(r"^[A-Z]{2}\d{4}$")

student_ids = ["BT2024", "cs9999", "AB1234", "XYZ123", "CS2025"]

print("Batch validation:")
for sid in student_ids:
    if student_id_pattern.match(sid):
        print(f"  PASS: {sid}")
    else:
        print(f"  FAIL: {sid}")
```

```
Batch validation:
  PASS: BT2024
  FAIL: cs9999
  PASS: AB1234
  FAIL: XYZ123
  PASS: CS2025
```

---



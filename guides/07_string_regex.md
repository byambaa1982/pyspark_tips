# String & Regex Operations

Master string manipulations, pattern matching, and text processing in PySpark.

---

## 🎯 Quick Reference

| Operation | PySpark Function | Example |
|-----------|-----------------|---------|
| **Uppercase** | `upper()` | `upper(col("name"))` |
| **Lowercase** | `lower()` | `lower(col("name"))` |
| **Trim** | `trim()` | `trim(col("text"))` |
| **Concatenate** | `concat()` | `concat(col("first"), lit(" "), col("last"))` |
| **Contains** | `contains()` | `col("text").contains("keyword")` |
| **Regex extract** | `regexp_extract()` | `regexp_extract(col("text"), r"(\d+)", 1)` |
| **Regex replace** | `regexp_replace()` | `regexp_replace(col("text"), r"\d+", "X")` |

---

## 📚 Basic String Operations

### Case Conversion

```python
from pyspark.sql.functions import upper, lower, initcap

df = df.withColumn("upper_name", upper(col("name"))) \
    .withColumn("lower_name", lower(col("name"))) \
    .withColumn("title_case", initcap(col("name")))

# Examples:
# "john doe" → "JOHN DOE" (upper)
# "JOHN DOE" → "john doe" (lower)
# "john doe" → "John Doe" (initcap)
```

### Trimming & Padding

```python
from pyspark.sql.functions import trim, ltrim, rtrim, lpad, rpad

df = df.withColumn("trimmed", trim(col("text"))) \
    .withColumn("left_trimmed", ltrim(col("text"))) \
    .withColumn("right_trimmed", rtrim(col("text"))) \
    .withColumn("padded", lpad(col("id"), 10, "0")) \
    .withColumn("right_padded", rpad(col("name"), 20, " "))

# Examples:
# "  hello  " → "hello" (trim)
# "00123" → "0000000123" (lpad to 10 chars)
```

### String Concatenation

```python
from pyspark.sql.functions import concat, concat_ws, lit

# Simple concatenation
df = df.withColumn("full_name", 
    concat(col("first_name"), lit(" "), col("last_name"))
)

# Concatenation with separator
df = df.withColumn("address",
    concat_ws(", ", col("street"), col("city"), col("state"), col("zip"))
)

# Handle nulls
df = df.withColumn("safe_concat",
    concat_ws(" ", col("first_name"), col("middle_name"), col("last_name"))
)  # Skips nulls automatically
```

### String Length

```python
from pyspark.sql.functions import length, char_length

df = df.withColumn("name_length", length(col("name"))) \
    .withColumn("char_count", char_length(col("text")))

# Filter by length
df = df.filter(length(col("password")) >= 8)
```

---

## ✂️ Substring Operations

### Extract Substrings

```python
from pyspark.sql.functions import substring, substr

# Extract substring (position is 1-based)
df = df.withColumn("first_3_chars", substring(col("text"), 1, 3))
df = df.withColumn("from_position_5", substring(col("text"), 5, 10))

# Extract from right
df = df.withColumn("last_3_chars", substring(col("text"), -3, 3))

# Examples:
# "Hello World" → "Hel" (first 3)
# "Hello World" → "o World" (from position 5)
```

### Split Strings

```python
from pyspark.sql.functions import split, explode

# Split into array
df = df.withColumn("words", split(col("sentence"), " "))
df = df.withColumn("parts", split(col("email"), "@"))

# Explode array into rows
df = df.withColumn("word", explode(split(col("sentence"), " ")))

# Access array elements
df = df.withColumn("first_word", split(col("sentence"), " ")[0])
df = df.withColumn("domain", split(col("email"), "@")[1])
```

---

## 🔍 Pattern Matching

### Simple Pattern Matching

```python
from pyspark.sql.functions import contains, startswith, endswith, like

# Contains
df = df.filter(col("text").contains("keyword"))

# Starts with
df = df.filter(col("name").startswith("John"))

# Ends with
df = df.filter(col("email").endswith("@gmail.com"))

# SQL LIKE pattern
df = df.filter(col("name").like("J%"))  # Starts with J
df = df.filter(col("email").like("%@gmail.com"))  # Ends with @gmail.com
df = df.filter(col("phone").like("___-___-____"))  # Pattern matching
```

### Regular Expressions

```python
from pyspark.sql.functions import regexp_extract, regexp_replace, rlike

# Extract with regex
df = df.withColumn("area_code", 
    regexp_extract(col("phone"), r"(\d{3})-\d{3}-\d{4}", 1)
)

df = df.withColumn("email_username",
    regexp_extract(col("email"), r"([^@]+)@", 1)
)

df = df.withColumn("email_domain",
    regexp_extract(col("email"), r"@(.+)", 1)
)

# Replace with regex
df = df.withColumn("masked_phone",
    regexp_replace(col("phone"), r"\d", "X")
)

df = df.withColumn("clean_text",
    regexp_replace(col("text"), r"[^a-zA-Z0-9\s]", "")
)

# Match with regex (returns boolean)
df = df.filter(col("email").rlike(r"^[\w\.-]+@[\w\.-]+\.\w+$"))
```

---

## 🎯 Common Regex Patterns

### Email Validation

```python
email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

df = df.withColumn("is_valid_email", 
    col("email").rlike(email_pattern)
)

# Extract email components
df = df.withColumn("username", 
    regexp_extract(col("email"), r"([^@]+)@", 1)
)
df = df.withColumn("domain",
    regexp_extract(col("email"), r"@(.+)", 1)
)
```

### Phone Number Formatting

```python
# Extract phone components
df = df.withColumn("area_code",
    regexp_extract(col("phone"), r"(\d{3})", 1)
)

# Format phone number
df = df.withColumn("formatted_phone",
    concat(
        lit("("), regexp_extract(col("phone"), r"(\d{3})", 1), lit(") "),
        regexp_extract(col("phone"), r"\d{3}(\d{3})", 1), lit("-"),
        regexp_extract(col("phone"), r"\d{6}(\d{4})", 1)
    )
)

# Clean phone number (remove non-digits)
df = df.withColumn("clean_phone",
    regexp_replace(col("phone"), r"[^\d]", "")
)
```

### URL Parsing

```python
# Extract domain
df = df.withColumn("domain",
    regexp_extract(col("url"), r"https?://([^/]+)", 1)
)

# Extract protocol
df = df.withColumn("protocol",
    regexp_extract(col("url"), r"(https?)", 1)
)

# Extract path
df = df.withColumn("path",
    regexp_extract(col("url"), r"https?://[^/]+(.+)", 1)
)
```

### Extract Numbers

```python
# Extract first number
df = df.withColumn("first_number",
    regexp_extract(col("text"), r"(\d+)", 1)
)

# Extract all numbers
df = df.withColumn("all_numbers",
    regexp_extract(col("text"), r"(\d+)", 0)
)

# Extract decimal numbers
df = df.withColumn("price",
    regexp_extract(col("text"), r"(\d+\.\d+)", 1)
)
```

---

## 🧹 Text Cleaning

### Remove Special Characters

```python
# Remove all special characters
df = df.withColumn("clean_text",
    regexp_replace(col("text"), r"[^a-zA-Z0-9\s]", "")
)

# Remove extra whitespace
df = df.withColumn("normalized_text",
    regexp_replace(trim(col("text")), r"\s+", " ")
)

# Remove HTML tags
df = df.withColumn("plain_text",
    regexp_replace(col("html"), r"<[^>]+>", "")
)
```

### Standardize Text

```python
# Convert to lowercase and remove special chars
df = df.withColumn("standardized",
    lower(trim(regexp_replace(col("text"), r"[^a-zA-Z0-9\s]", "")))
)

# Remove multiple spaces
df = df.withColumn("clean",
    regexp_replace(col("text"), r"\s+", " ")
)
```

---

## 📊 Advanced String Operations

### Conditional String Operations

```python
from pyspark.sql.functions import when

# Conditional replacement
df = df.withColumn("category",
    when(col("text").contains("urgent"), "High Priority")
    .when(col("text").contains("important"), "Medium Priority")
    .otherwise("Low Priority")
)

# Multiple conditions
df = df.withColumn("email_provider",
    when(col("email").endswith("@gmail.com"), "Gmail")
    .when(col("email").endswith("@yahoo.com"), "Yahoo")
    .when(col("email").endswith("@outlook.com"), "Outlook")
    .otherwise("Other")
)
```

### String Aggregation

```python
from pyspark.sql.functions import collect_list, concat_ws

# Concatenate strings in group
df.groupBy("category") \
    .agg(concat_ws(", ", collect_list("name")).alias("all_names")) \
    .show()
```

### Levenshtein Distance

```python
from pyspark.sql.functions import levenshtein

# Calculate edit distance
df = df.withColumn("similarity",
    levenshtein(col("name1"), col("name2"))
)

# Find similar strings
similar = df.filter(levenshtein(col("name1"), col("name2")) <= 3)
```

---

## 🎓 Best Practices

### ✅ DO

```python
# Use built-in functions
df.withColumn("upper", upper(col("name")))

# Use concat_ws for nullable columns
df.withColumn("full_name", concat_ws(" ", col("first"), col("middle"), col("last")))

# Compile regex patterns once
pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
df = df.withColumn("valid_email", col("email").rlike(pattern))

# Chain string operations
df = df.withColumn("clean",
    trim(lower(regexp_replace(col("text"), r"[^a-zA-Z0-9\s]", "")))
)
```

### ❌ DON'T

```python
# Don't use Python string methods
# ❌ Bad
@udf(StringType())
def to_upper(s):
    return s.upper()

# ✅ Good
df.withColumn("upper", upper(col("name")))

# Don't forget to handle nulls
# ❌ Bad - crashes on null
df.withColumn("length", length(col("text")))

# ✅ Good
df.withColumn("length", 
    when(col("text").isNotNull(), length(col("text"))).otherwise(0)
)
```

---

## 📊 Common Patterns

### Pattern 1: Email Validation & Cleaning

```python
# Validate and extract email parts
df = df.withColumn("email_clean", lower(trim(col("email")))) \
    .withColumn("is_valid",
        col("email_clean").rlike(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    ) \
    .withColumn("username",
        regexp_extract(col("email_clean"), r"([^@]+)@", 1)
    ) \
    .withColumn("domain",
        regexp_extract(col("email_clean"), r"@(.+)", 1)
    )
```

### Pattern 2: Name Standardization

```python
# Standardize names
df = df.withColumn("name_clean",
    initcap(trim(regexp_replace(col("name"), r"\s+", " ")))
)

# Split full name
df = df.withColumn("first_name", split(col("full_name"), " ")[0]) \
    .withColumn("last_name", split(col("full_name"), " ")[-1])
```

### Pattern 3: Text Tokenization

```python
# Tokenize and count words
df = df.withColumn("words", split(lower(col("text")), r"\s+")) \
    .withColumn("word_count", size(col("words"))) \
    .withColumn("unique_words", size(array_distinct(col("words"))))
```

### Pattern 4: Data Masking

```python
# Mask sensitive data
df = df.withColumn("masked_ssn",
    concat(
        lit("XXX-XX-"),
        substring(col("ssn"), -4, 4)
    )
)

df = df.withColumn("masked_credit_card",
    concat(
        lit("****-****-****-"),
        substring(col("cc_number"), -4, 4)
    )
)
```

---

## 🚀 Performance Tips

1. **Use built-in functions** - Much faster than UDFs
2. **Filter early** - Apply string filters before other operations
3. **Avoid complex regex** - Simple patterns are faster
4. **Cache after expensive operations** - Especially after regex operations
5. **Use concat_ws for nulls** - Handles nulls automatically

---

## 🔗 Related Guides

- [01. DataFrame Basics](01_dataframe_basics.md)
- [05. UDFs & Built-in Functions](05_udfs_functions.md)
- [08. Performance Optimization](08_performance_tuning.md)

---

## 📚 Additional Resources

- [PySpark String Functions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html#string-functions)
- [Regular Expressions in Java](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)

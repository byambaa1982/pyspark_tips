# UDFs & Built-in Functions

Master user-defined functions (UDFs), pandas UDFs, and leverage PySpark's rich library of built-in functions.

---

## 🎯 Quick Reference

| Function Type | Performance | Use Case |
|--------------|-------------|----------|
| **Built-in Functions** | ⚡⚡⚡ Fast | Always prefer when available |
| **Pandas UDF** | ⚡⚡ Good | Vectorized operations, complex logic |
| **Python UDF** | ⚡ Slow | Simple transformations, last resort |

---

## 📚 Built-in Functions

### String Functions

```python
from pyspark.sql.functions import (
    upper, lower, initcap, trim, ltrim, rtrim,
    concat, concat_ws, substring, length, split,
    regexp_extract, regexp_replace
)

df = df.withColumn("upper_name", upper(col("name"))) \
    .withColumn("lower_name", lower(col("name"))) \
    .withColumn("title_case", initcap(col("name"))) \
    .withColumn("trimmed", trim(col("name"))) \
    .withColumn("full_name", concat(col("first_name"), lit(" "), col("last_name"))) \
    .withColumn("name_length", length(col("name"))) \
    .withColumn("first_3_chars", substring(col("name"), 1, 3))
```

### Numeric Functions

```python
from pyspark.sql.functions import (
    abs, round, floor, ceil, sqrt, pow,
    rand, randn, log, exp
)

df = df.withColumn("absolute", abs(col("value"))) \
    .withColumn("rounded", round(col("price"), 2)) \
    .withColumn("floor_value", floor(col("price"))) \
    .withColumn("ceiling", ceil(col("price"))) \
    .withColumn("square_root", sqrt(col("number"))) \
    .withColumn("squared", pow(col("number"), 2)) \
    .withColumn("random", rand()) \
    .withColumn("log_value", log(col("number")))
```

### Date & Time Functions

```python
from pyspark.sql.functions import (
    current_date, current_timestamp, date_add, date_sub,
    datediff, months_between, year, month, dayofmonth,
    dayofweek, date_format, to_date, to_timestamp
)

df = df.withColumn("current_date", current_date()) \
    .withColumn("current_timestamp", current_timestamp()) \
    .withColumn("date_plus_7", date_add(col("date"), 7)) \
    .withColumn("days_diff", datediff(current_date(), col("date"))) \
    .withColumn("year", year(col("date"))) \
    .withColumn("month", month(col("date"))) \
    .withColumn("formatted_date", date_format(col("date"), "yyyy-MM-dd"))
```

### Conditional Functions

```python
from pyspark.sql.functions import when, coalesce, lit, isnull

# When/Otherwise
df = df.withColumn("category",
    when(col("age") < 18, "Minor")
    .when(col("age") < 65, "Adult")
    .otherwise("Senior")
)

# Coalesce (first non-null value)
df = df.withColumn("contact", coalesce(col("phone"), col("email"), lit("No contact")))

# Check for null
df = df.withColumn("has_email", ~isnull(col("email")))
```

### Array & Map Functions

```python
from pyspark.sql.functions import (
    array, array_contains, explode, size,
    create_map, map_keys, map_values
)

# Array operations
df = df.withColumn("tags", array(lit("tag1"), lit("tag2"))) \
    .withColumn("has_tag", array_contains(col("tags"), "tag1")) \
    .withColumn("array_size", size(col("tags")))

# Explode array
df = df.withColumn("tag", explode(col("tags")))

# Map operations
df = df.withColumn("map_col", create_map(lit("key1"), lit("value1"))) \
    .withColumn("keys", map_keys(col("map_col"))) \
    .withColumn("values", map_values(col("map_col")))
```

---

## 🐍 Python UDFs

### Basic Python UDF

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, IntegerType

# Define Python function
def categorize_age(age):
    if age < 18:
        return "Minor"
    elif age < 65:
        return "Adult"
    else:
        return "Senior"

# Register UDF
categorize_udf = udf(categorize_age, StringType())

# Use UDF
df = df.withColumn("age_category", categorize_udf(col("age")))
```

### UDF with Multiple Parameters

```python
from pyspark.sql.types import DoubleType

def calculate_bmi(weight, height):
    if height > 0:
        return weight / (height ** 2)
    else:
        return None

bmi_udf = udf(calculate_bmi, DoubleType())

df = df.withColumn("bmi", bmi_udf(col("weight_kg"), col("height_m")))
```

### UDF with Complex Return Types

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Define return schema
return_schema = StructType([
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("name_length", IntegerType(), True)
])

def parse_name(full_name):
    parts = full_name.split()
    return {
        "first_name": parts[0] if len(parts) > 0 else None,
        "last_name": parts[-1] if len(parts) > 1 else None,
        "name_length": len(full_name)
    }

parse_name_udf = udf(parse_name, return_schema)

df = df.withColumn("name_parts", parse_name_udf(col("full_name")))
df = df.select("*", "name_parts.*")
```

---

## 🐼 Pandas UDFs

### Scalar Pandas UDF

```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def calculate_tax(amounts: pd.Series) -> pd.Series:
    return amounts * 0.08

df = df.withColumn("tax", calculate_tax(col("amount")))
```

### Pandas UDF with Multiple Columns

```python
from pyspark.sql.types import DoubleType

@pandas_udf(DoubleType())
def calculate_total(price: pd.Series, quantity: pd.Series) -> pd.Series:
    return price * quantity * 1.08  # Include tax

df = df.withColumn("total", calculate_total(col("price"), col("quantity")))
```

### Grouped Map Pandas UDF

```python
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

output_schema = StructType([
    StructField("department", StringType(), True),
    StructField("avg_salary", DoubleType(), True),
    StructField("std_salary", DoubleType(), True)
])

@pandas_udf(output_schema, PandasUDFType.GROUPED_MAP)
def calculate_stats(pdf: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "department": [pdf['department'].iloc[0]],
        "avg_salary": [pdf['salary'].mean()],
        "std_salary": [pdf['salary'].std()]
    })

result = df.groupBy("department").apply(calculate_stats)
```

### Pandas UDF for Machine Learning

```python
from sklearn.preprocessing import StandardScaler

@pandas_udf("double")
def standardize_column(values: pd.Series) -> pd.Series:
    scaler = StandardScaler()
    scaled = scaler.fit_transform(values.values.reshape(-1, 1))
    return pd.Series(scaled.flatten())

df = df.withColumn("standardized_value", standardize_column(col("value")))
```

---

## 🎯 Advanced Patterns

### Chaining UDFs

```python
@udf(StringType())
def clean_text(text):
    return text.strip().lower()

@udf(IntegerType())
def count_words(text):
    return len(text.split())

df = df.withColumn("cleaned", clean_text(col("text"))) \
    .withColumn("word_count", count_words(col("cleaned")))
```

### Conditional UDF Application

```python
@udf(DoubleType())
def apply_discount(price, customer_type):
    if customer_type == "VIP":
        return price * 0.8
    elif customer_type == "Regular":
        return price * 0.9
    else:
        return price

df = df.withColumn("final_price", apply_discount(col("price"), col("customer_type")))
```

### UDF with Exception Handling

```python
from pyspark.sql.types import StringType

@udf(StringType())
def safe_parse(value):
    try:
        # Some complex parsing logic
        result = complex_operation(value)
        return result
    except Exception as e:
        return f"ERROR: {str(e)}"

df = df.withColumn("parsed", safe_parse(col("raw_data")))
```

---

## 🎓 Best Practices

### ✅ DO

```python
# Use built-in functions whenever possible
df.withColumn("upper_name", upper(col("name")))  # Fast

# Use Pandas UDFs for vectorized operations
@pandas_udf("double")
def vectorized_operation(values: pd.Series) -> pd.Series:
    return values * 2

# Cache DataFrame before applying UDFs multiple times
df.cache()
df = df.withColumn("col1", udf1(col("input")))
df = df.withColumn("col2", udf2(col("input")))

# Specify return types explicitly
@udf(StringType())
def my_function(value):
    return str(value)
```

### ❌ DON'T

```python
# Don't use Python UDF when built-in exists
# ❌ Bad
@udf(StringType())
def to_upper(text):
    return text.upper()

# ✅ Good
df.withColumn("upper", upper(col("name")))

# Don't apply UDFs to entire DataFrame at once
# ❌ Bad - processes millions of rows
df.withColumn("result", expensive_udf(col("value")))

# ✅ Better - filter first
df.filter(col("status") == "active") \
  .withColumn("result", expensive_udf(col("value")))

# Don't forget to handle nulls in UDFs
# ❌ Bad
@udf(IntegerType())
def unsafe_operation(value):
    return len(value)  # Crashes on null!

# ✅ Good
@udf(IntegerType())
def safe_operation(value):
    return len(value) if value else 0
```

---

## 📊 Performance Comparison

```python
import time

# Built-in function (fastest)
start = time.time()
df.withColumn("upper", upper(col("name"))).count()
print(f"Built-in: {time.time() - start:.2f}s")

# Pandas UDF (good)
@pandas_udf("string")
def pandas_upper(s: pd.Series) -> pd.Series:
    return s.str.upper()

start = time.time()
df.withColumn("upper", pandas_upper(col("name"))).count()
print(f"Pandas UDF: {time.time() - start:.2f}s")

# Python UDF (slowest)
@udf(StringType())
def python_upper(text):
    return text.upper()

start = time.time()
df.withColumn("upper", python_upper(col("name"))).count()
print(f"Python UDF: {time.time() - start:.2f}s")
```

---

## 🚀 Performance Tips

1. **Always prefer built-in functions** - 10-100x faster than UDFs
2. **Use Pandas UDFs over Python UDFs** - Vectorized operations are faster
3. **Filter data before applying UDFs** - Process less data
4. **Handle nulls explicitly** - Avoid crashes and unexpected behavior
5. **Cache when applying multiple UDFs** - Avoid recomputation
6. **Specify return types** - Improves performance and reliability

---

## 🔗 Related Guides

- [01. DataFrame Basics](01_dataframe_basics.md)
- [07. String & Regex Operations](07_string_regex.md)
- [08. Performance Optimization](08_performance_tuning.md)

---

## 📚 Additional Resources

- [PySpark SQL Functions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)
- [Pandas UDFs](https://spark.apache.org/docs/latest/sql-pyspark-pandas-with-arrow.html#pandas-udfs-aka-vectorized-udfs)

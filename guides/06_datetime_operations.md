# Date & Time Operations

Master date and time manipulations, time series analysis, and timezone handling in PySpark.

---

## 🎯 Quick Reference

| Operation | PySpark Function | Example |
|-----------|-----------------|---------|
| **Current date** | `current_date()` | `df.withColumn("today", current_date())` |
| **Current timestamp** | `current_timestamp()` | `df.withColumn("now", current_timestamp())` |
| **Parse string to date** | `to_date()` | `to_date(col("date_str"), "yyyy-MM-dd")` |
| **Date difference** | `datediff()` | `datediff(col("end"), col("start"))` |
| **Add days** | `date_add()` | `date_add(col("date"), 7)` |
| **Extract year** | `year()` | `year(col("date"))` |

---

## 📅 Date Creation & Parsing

### Creating Date/Timestamp Columns

```python
from pyspark.sql.functions import (
    current_date, current_timestamp, 
    to_date, to_timestamp, lit
)

df = df.withColumn("today", current_date()) \
    .withColumn("now", current_timestamp()) \
    .withColumn("fixed_date", lit("2024-01-01").cast("date"))
```

### Parsing Strings to Dates

```python
from pyspark.sql.functions import to_date, to_timestamp

# Parse with default format (yyyy-MM-dd)
df = df.withColumn("date", to_date(col("date_string")))

# Parse with custom format
df = df.withColumn("date", to_date(col("date_string"), "MM/dd/yyyy"))
df = df.withColumn("date", to_date(col("date_string"), "dd-MMM-yyyy"))

# Parse to timestamp
df = df.withColumn("timestamp", to_timestamp(col("timestamp_string"), "yyyy-MM-dd HH:mm:ss"))

# Handle invalid dates
df = df.withColumn("parsed_date", 
    when(to_date(col("date_string"), "yyyy-MM-dd").isNotNull(),
         to_date(col("date_string"), "yyyy-MM-dd"))
    .otherwise(None)
)
```

### Common Date Formats

```python
formats = {
    "2024-01-15": "yyyy-MM-dd",
    "01/15/2024": "MM/dd/yyyy",
    "15-Jan-2024": "dd-MMM-yyyy",
    "2024/01/15 14:30:00": "yyyy/MM/dd HH:mm:ss",
    "15.01.2024": "dd.MM.yyyy",
}

for date_str, format_str in formats.items():
    df = df.withColumn("parsed", to_date(lit(date_str), format_str))
```

---

## 🔢 Date Arithmetic

### Adding & Subtracting Dates

```python
from pyspark.sql.functions import date_add, date_sub, add_months

# Add days
df = df.withColumn("next_week", date_add(col("date"), 7))
df = df.withColumn("tomorrow", date_add(col("date"), 1))

# Subtract days
df = df.withColumn("last_week", date_sub(col("date"), 7))
df = df.withColumn("yesterday", date_sub(col("date"), 1))

# Add months
df = df.withColumn("next_month", add_months(col("date"), 1))
df = df.withColumn("next_year", add_months(col("date"), 12))

# Dynamic date arithmetic
df = df.withColumn("future_date", date_add(col("date"), col("days_to_add")))
```

### Date Differences

```python
from pyspark.sql.functions import datediff, months_between

# Difference in days
df = df.withColumn("days_diff", datediff(col("end_date"), col("start_date")))
df = df.withColumn("days_since", datediff(current_date(), col("event_date")))

# Difference in months
df = df.withColumn("months_diff", months_between(col("end_date"), col("start_date")))

# Age calculation
df = df.withColumn("age_years", 
    floor(datediff(current_date(), col("birth_date")) / 365)
)
```

---

## 📊 Extracting Date Components

### Basic Components

```python
from pyspark.sql.functions import (
    year, month, dayofmonth, dayofweek, 
    dayofyear, weekofyear, quarter
)

df = df.withColumn("year", year(col("date"))) \
    .withColumn("month", month(col("date"))) \
    .withColumn("day", dayofmonth(col("date"))) \
    .withColumn("day_of_week", dayofweek(col("date")))  # 1=Sunday, 7=Saturday \
    .withColumn("day_of_year", dayofyear(col("date"))) \
    .withColumn("week_of_year", weekofyear(col("date"))) \
    .withColumn("quarter", quarter(col("date")))
```

### Time Components

```python
from pyspark.sql.functions import hour, minute, second

df = df.withColumn("hour", hour(col("timestamp"))) \
    .withColumn("minute", minute(col("timestamp"))) \
    .withColumn("second", second(col("timestamp")))

# Create hour ranges
df = df.withColumn("hour_range",
    when(hour(col("timestamp")) < 6, "Night")
    .when(hour(col("timestamp")) < 12, "Morning")
    .when(hour(col("timestamp")) < 18, "Afternoon")
    .otherwise("Evening")
)
```

### Custom Date Components

```python
from pyspark.sql.functions import date_format

# Format as string
df = df.withColumn("formatted_date", date_format(col("date"), "yyyy-MM-dd"))
df = df.withColumn("month_name", date_format(col("date"), "MMMM"))
df = df.withColumn("day_name", date_format(col("date"), "EEEE"))
df = df.withColumn("year_month", date_format(col("date"), "yyyy-MM"))

# Custom formats
df = df.withColumn("custom", date_format(col("date"), "dd/MM/yyyy HH:mm:ss"))
```

---

## 🌍 Timezone Handling

### Converting Timezones

```python
from pyspark.sql.functions import from_utc_timestamp, to_utc_timestamp

# Convert from UTC to local timezone
df = df.withColumn("local_time", 
    from_utc_timestamp(col("utc_timestamp"), "America/New_York")
)

# Convert from local timezone to UTC
df = df.withColumn("utc_time",
    to_utc_timestamp(col("local_timestamp"), "America/Los_Angeles")
)

# Common timezones
timezones = [
    "UTC",
    "America/New_York",  # EST/EDT
    "America/Los_Angeles",  # PST/PDT
    "Europe/London",  # GMT/BST
    "Asia/Tokyo",  # JST
    "Australia/Sydney",  # AEST/AEDT
]
```

### Working with Unix Timestamps

```python
from pyspark.sql.functions import unix_timestamp, from_unixtime

# Convert date to Unix timestamp
df = df.withColumn("unix_ts", unix_timestamp(col("date")))

# Convert Unix timestamp to date
df = df.withColumn("date_from_unix", from_unixtime(col("unix_timestamp")))

# Custom format
df = df.withColumn("formatted", 
    from_unixtime(col("unix_timestamp"), "yyyy-MM-dd HH:mm:ss")
)
```

---

## 📈 Time Series Operations

### Date Ranges

```python
from pyspark.sql.functions import sequence, explode, expr

# Generate date range
df = spark.sql("""
    SELECT sequence(
        to_date('2024-01-01'),
        to_date('2024-12-31'),
        interval 1 day
    ) as date_array
""")

# Explode into rows
date_range = df.select(explode(col("date_array")).alias("date"))

# Generate month range
month_range = spark.sql("""
    SELECT sequence(
        to_date('2024-01-01'),
        to_date('2024-12-01'),
        interval 1 month
    ) as date_array
""").select(explode(col("date_array")).alias("date"))
```

### Rolling Windows

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import avg, sum, lag, lead

# 7-day rolling average
window_7d = Window.partitionBy("product_id") \
    .orderBy("date") \
    .rowsBetween(-6, 0)

df = df.withColumn("rolling_avg_7d", avg("sales").over(window_7d))

# 30-day rolling sum
window_30d = Window.partitionBy("category") \
    .orderBy("date") \
    .rowsBetween(-29, 0)

df = df.withColumn("rolling_sum_30d", sum("revenue").over(window_30d))
```

### Time-based Lag/Lead

```python
from pyspark.sql.functions import lag, lead

window_spec = Window.partitionBy("product_id").orderBy("date")

# Previous day's value
df = df.withColumn("previous_sales", lag("sales", 1).over(window_spec))

# Next day's value
df = df.withColumn("next_sales", lead("sales", 1).over(window_spec))

# Day-over-day change
df = df.withColumn("sales_change", 
    col("sales") - lag("sales", 1).over(window_spec)
)

# Percentage change
df = df.withColumn("sales_pct_change",
    ((col("sales") - lag("sales", 1).over(window_spec)) / lag("sales", 1).over(window_spec)) * 100
)
```

---

## 📊 Common Date Patterns

### Pattern 1: Business Days Calculation

```python
from pyspark.sql.functions import dayofweek

# Filter to business days only (Monday-Friday)
business_days = df.filter(
    (dayofweek(col("date")) >= 2) & (dayofweek(col("date")) <= 6)
)

# Mark weekend vs weekday
df = df.withColumn("is_weekend",
    when((dayofweek(col("date")) == 1) | (dayofweek(col("date")) == 7), True)
    .otherwise(False)
)
```

### Pattern 2: Age Calculation

```python
from pyspark.sql.functions import datediff, floor

# Calculate age in years
df = df.withColumn("age",
    floor(datediff(current_date(), col("birth_date")) / 365.25)
)

# Age groups
df = df.withColumn("age_group",
    when(col("age") < 18, "0-17")
    .when(col("age") < 30, "18-29")
    .when(col("age") < 45, "30-44")
    .when(col("age") < 60, "45-59")
    .otherwise("60+")
)
```

### Pattern 3: Fiscal Year/Quarter

```python
from pyspark.sql.functions import when, month

# Fiscal year starting in April
df = df.withColumn("fiscal_year",
    when(month(col("date")) < 4, year(col("date")))
    .otherwise(year(col("date")) + 1)
)

# Fiscal quarter
df = df.withColumn("fiscal_quarter",
    when(month(col("date")).isin([4, 5, 6]), "Q1")
    .when(month(col("date")).isin([7, 8, 9]), "Q2")
    .when(month(col("date")).isin([10, 11, 12]), "Q3")
    .otherwise("Q4")
)
```

### Pattern 4: Date Binning

```python
# Group dates into bins
df = df.withColumn("date_bin",
    when(col("date") < "2024-01-01", "Before 2024")
    .when(col("date") < "2024-07-01", "H1 2024")
    .otherwise("H2 2024")
)

# Month start/end
df = df.withColumn("month_start", trunc(col("date"), "month"))
df = df.withColumn("month_end", last_day(col("date")))
```

---

## 🎓 Best Practices

### ✅ DO

```python
# Use built-in date functions
df.withColumn("year", year(col("date")))

# Handle null dates explicitly
df.withColumn("valid_date", 
    when(col("date").isNotNull(), col("date"))
    .otherwise(current_date())
)

# Use appropriate date types
df = df.withColumn("date", col("date_string").cast("date"))
df = df.withColumn("timestamp", col("ts_string").cast("timestamp"))

# Cache when doing multiple date operations
df.cache()
df = df.withColumn("year", year(col("date")))
df = df.withColumn("month", month(col("date")))
```

### ❌ DON'T

```python
# Don't use string operations on dates
# ❌ Bad
df.withColumn("year", substring(col("date_string"), 1, 4))

# ✅ Good
df.withColumn("year", year(to_date(col("date_string"))))

# Don't forget to specify date format
# ❌ Bad - may fail
df.withColumn("date", to_date(col("custom_format")))

# ✅ Good
df.withColumn("date", to_date(col("custom_format"), "dd/MM/yyyy"))
```

---

## 🚀 Performance Tips

1. **Use date types** - Don't keep dates as strings
2. **Partition by date** - Improves query performance
3. **Filter by date early** - Reduce data volume
4. **Cache time series DataFrames** - Avoid recomputation
5. **Use built-in functions** - Much faster than UDFs

---

## 🔗 Related Guides

- [01. DataFrame Basics](01_dataframe_basics.md)
- [03. Aggregations & GroupBy](03_aggregations_groupby.md)
- [05. UDFs & Built-in Functions](05_udfs_functions.md)

---

## 📚 Additional Resources

- [PySpark Date Functions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html#datetime-functions)
- [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

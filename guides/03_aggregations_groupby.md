# Aggregations & GroupBy

Master split-apply-combine operations, window functions, and advanced aggregation techniques in PySpark.

---

## 🎯 Quick Reference

| Operation | PySpark | Pandas Equivalent |
|-----------|---------|-------------------|
| **GroupBy** | `df.groupBy('col').agg(...)` | `df.groupby('col').agg(...)` |
| **Count** | `df.groupBy('col').count()` | `df.groupby('col').size()` |
| **Multiple aggs** | `df.groupBy('col').agg(sum('x'), avg('y'))` | `df.groupby('col').agg({'x': 'sum', 'y': 'mean'})` |
| **Window function** | `df.withColumn('rank', rank().over(window))` | `df['rank'] = df.groupby('col')['val'].rank()` |

---

## 📚 Basic Aggregations

### Simple Aggregations

```python
from pyspark.sql.functions import count, sum, avg, max, min, mean, stddev

# Single aggregation
df.agg(count("*")).show()
df.agg(sum("salary")).show()
df.agg(avg("age")).show()

# Multiple aggregations
df.agg(
    count("*").alias("total_count"),
    sum("salary").alias("total_salary"),
    avg("age").alias("average_age"),
    max("salary").alias("max_salary"),
    min("salary").alias("min_salary")
).show()
```

### Column-Specific Aggregations

```python
# Using select with agg functions
df.select(
    count("employee_id").alias("employee_count"),
    sum("sales").alias("total_sales"),
    avg("rating").alias("avg_rating")
).show()
```

---

## 🔄 GroupBy Operations

### Basic GroupBy

```python
# Single column groupBy
df.groupBy("department").count().show()

# Multiple column groupBy
df.groupBy("department", "city").count().show()

# GroupBy with alias
df.groupBy("department").agg(
    count("*").alias("employee_count")
).show()
```

### GroupBy with Multiple Aggregations

```python
from pyspark.sql.functions import sum, avg, max, min, count, countDistinct

result = df.groupBy("department").agg(
    count("*").alias("total_employees"),
    countDistinct("employee_id").alias("unique_employees"),
    sum("salary").alias("total_salary"),
    avg("salary").alias("avg_salary"),
    max("salary").alias("max_salary"),
    min("salary").alias("min_salary")
)

result.show()
```

### GroupBy with Filtering

```python
# Filter before groupBy
df.filter(col("status") == "active") \
    .groupBy("department") \
    .agg(avg("salary").alias("avg_salary")) \
    .show()

# Filter after groupBy (using having)
df.groupBy("department") \
    .agg(avg("salary").alias("avg_salary")) \
    .filter(col("avg_salary") > 50000) \
    .show()
```

---

## 🪟 Window Functions

### Basic Window Operations

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank, lag, lead

# Define window specification
window_spec = Window.partitionBy("department").orderBy(col("salary").desc())

# Add window functions
result = df.withColumn("row_num", row_number().over(window_spec)) \
    .withColumn("rank", rank().over(window_spec)) \
    .withColumn("dense_rank", dense_rank().over(window_spec))

result.show()
```

### Window Aggregations

```python
from pyspark.sql.functions import sum, avg, count

# Running total
window_spec = Window.partitionBy("department").orderBy("date") \
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)

df.withColumn("running_total", sum("sales").over(window_spec)).show()

# Moving average (last 3 rows)
window_spec = Window.partitionBy("product").orderBy("date") \
    .rowsBetween(-2, 0)

df.withColumn("moving_avg", avg("sales").over(window_spec)).show()

# Cumulative average
window_spec = Window.partitionBy("category").orderBy("date") \
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)

df.withColumn("cumulative_avg", avg("price").over(window_spec)).show()
```

### Lag and Lead

```python
from pyspark.sql.functions import lag, lead

window_spec = Window.partitionBy("product_id").orderBy("date")

result = df.withColumn("previous_price", lag("price", 1).over(window_spec)) \
    .withColumn("next_price", lead("price", 1).over(window_spec)) \
    .withColumn("price_change", col("price") - lag("price", 1).over(window_spec))

result.show()
```

### Ranking Functions

```python
from pyspark.sql.functions import row_number, rank, dense_rank, percent_rank, ntile

window_spec = Window.partitionBy("department").orderBy(col("salary").desc())

result = df.withColumn("row_number", row_number().over(window_spec)) \
    .withColumn("rank", rank().over(window_spec)) \
    .withColumn("dense_rank", dense_rank().over(window_spec)) \
    .withColumn("percent_rank", percent_rank().over(window_spec)) \
    .withColumn("quartile", ntile(4).over(window_spec))

result.show()
```

---

## 📊 Pivot Tables

### Basic Pivot

```python
# Create pivot table
pivot_df = df.groupBy("year").pivot("quarter").sum("sales")
pivot_df.show()

# Pivot with multiple aggregations
pivot_df = df.groupBy("year").pivot("quarter") \
    .agg(
        sum("sales").alias("total_sales"),
        avg("sales").alias("avg_sales")
    )
pivot_df.show()
```

### Pivot with Specified Values

```python
# More efficient - specify pivot values
pivot_df = df.groupBy("year") \
    .pivot("quarter", ["Q1", "Q2", "Q3", "Q4"]) \
    .sum("sales")

pivot_df.show()
```

### Unpivot (Melt)

```python
from pyspark.sql.functions import expr

# Unpivot using stack
unpivot_df = df.selectExpr(
    "id",
    "stack(4, 'Q1', Q1, 'Q2', Q2, 'Q3', Q3, 'Q4', Q4) as (quarter, sales)"
)

unpivot_df.show()
```

---

## 🎯 Advanced Aggregation Patterns

### Custom Aggregations

```python
from pyspark.sql.functions import expr, collect_list, collect_set

# Collect values into array
df.groupBy("department") \
    .agg(collect_list("employee_name").alias("employees")) \
    .show(truncate=False)

# Collect unique values
df.groupBy("department") \
    .agg(collect_set("skill").alias("unique_skills")) \
    .show(truncate=False)

# String aggregation
df.groupBy("department") \
    .agg(expr("concat_ws(', ', collect_list(employee_name))").alias("employee_list")) \
    .show(truncate=False)
```

### Conditional Aggregations

```python
from pyspark.sql.functions import when, sum, count

# Count with condition
result = df.groupBy("department").agg(
    count(when(col("salary") > 50000, 1)).alias("high_earners"),
    count(when(col("salary") <= 50000, 1)).alias("low_earners"),
    sum(when(col("bonus") > 0, col("bonus"))).alias("total_bonus")
)

result.show()
```

### Percentiles and Quantiles

```python
from pyspark.sql.functions import expr, percentile_approx

# Approximate percentiles
result = df.groupBy("department").agg(
    percentile_approx("salary", 0.5).alias("median_salary"),
    percentile_approx("salary", 0.25).alias("q1_salary"),
    percentile_approx("salary", 0.75).alias("q3_salary")
)

result.show()

# Multiple percentiles at once
result = df.groupBy("department").agg(
    percentile_approx("salary", [0.25, 0.5, 0.75]).alias("salary_quantiles")
)

result.show(truncate=False)
```

---

## 🎓 Best Practices

### ✅ DO

```python
# Specify pivot values for better performance
df.groupBy("year").pivot("quarter", ["Q1", "Q2", "Q3", "Q4"]).sum("sales")

# Use window functions instead of self-joins
window_spec = Window.partitionBy("dept").orderBy("salary")
df.withColumn("rank", rank().over(window_spec))

# Cache before multiple aggregations
df.cache()
result1 = df.groupBy("dept").count()
result2 = df.groupBy("city").sum("sales")

# Use built-in aggregation functions
from pyspark.sql.functions import sum, avg, count
df.agg(sum("amount"), avg("price"), count("*"))
```

### ❌ DON'T

```python
# Don't use collect() before aggregating
# ❌ Bad
rows = df.collect()
total = sum(row['amount'] for row in rows)

# ✅ Good
total = df.agg(sum("amount")).collect()[0][0]

# Don't create unnecessary windows
# ❌ Bad - multiple windows
window1 = Window.partitionBy("dept")
window2 = Window.partitionBy("dept")

# ✅ Good - reuse window
window = Window.partitionBy("dept")

# Don't forget to filter before aggregating
# ❌ Bad - aggregate everything then filter
df.groupBy("dept").sum("sales").filter(col("sum(sales)") > 1000)

# ✅ Better - filter first
df.filter(col("status") == "completed").groupBy("dept").sum("sales")
```

---

## 📊 Common Patterns

### Pattern 1: Top N per Group

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

# Get top 3 earners per department
window_spec = Window.partitionBy("department").orderBy(col("salary").desc())

result = df.withColumn("rank", row_number().over(window_spec)) \
    .filter(col("rank") <= 3) \
    .drop("rank")

result.show()
```

### Pattern 2: Running Totals and Differences

```python
from pyspark.sql.functions import sum, lag

window_spec = Window.partitionBy("product_id").orderBy("date")

result = df.withColumn("running_total", sum("sales").over(
    window_spec.rowsBetween(Window.unboundedPreceding, Window.currentRow)
))

result = result.withColumn("previous_sales", lag("sales", 1).over(window_spec)) \
    .withColumn("sales_diff", col("sales") - lag("sales", 1).over(window_spec))

result.show()
```

### Pattern 3: Cohort Analysis

```python
from pyspark.sql.functions import min, datediff

# Find first purchase date per customer
first_purchase = df.groupBy("customer_id").agg(
    min("purchase_date").alias("first_purchase_date")
)

# Calculate days since first purchase
cohort_df = df.join(first_purchase, "customer_id") \
    .withColumn("days_since_first", datediff(col("purchase_date"), col("first_purchase_date"))) \
    .withColumn("cohort_month", date_format(col("first_purchase_date"), "yyyy-MM"))

# Analyze retention
retention = cohort_df.groupBy("cohort_month", "days_since_first") \
    .agg(countDistinct("customer_id").alias("customers"))

retention.show()
```

### Pattern 4: Year-over-Year Comparison

```python
from pyspark.sql.functions import year, lag

window_spec = Window.partitionBy("product_id").orderBy("year")

result = df.withColumn("previous_year_sales", lag("sales", 1).over(window_spec)) \
    .withColumn("yoy_growth", 
        (col("sales") - col("previous_year_sales")) / col("previous_year_sales") * 100
    )

result.show()
```

---

## 🚀 Performance Tips

1. **Specify pivot values** - Dramatically improves pivot performance
2. **Filter before groupBy** - Reduce data volume early
3. **Use appropriate window bounds** - Unbounded windows are expensive
4. **Cache intermediate results** - When doing multiple aggregations
5. **Avoid collect() before aggregation** - Let Spark do distributed aggregation

---

## 🔗 Related Guides

- [01. DataFrame Basics](01_dataframe_basics.md)
- [02. Transformations & Actions](02_transformations_actions.md)
- [04. Joins & Unions](04_joins_unions.md)
- [08. Performance Optimization](08_performance_tuning.md)

---

## 📚 Additional Resources

- [PySpark SQL Functions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)
- [Window Functions Guide](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-window.html)

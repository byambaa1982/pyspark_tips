# Joins & Unions

Master different join types, optimize join performance, handle data skew, and combine DataFrames effectively.

---

## 🎯 Quick Reference

| Join Type | PySpark | Description |
|-----------|---------|-------------|
| **Inner** | `df1.join(df2, "key", "inner")` | Only matching rows |
| **Left** | `df1.join(df2, "key", "left")` | All from left, matching from right |
| **Right** | `df1.join(df2, "key", "right")` | All from right, matching from left |
| **Outer** | `df1.join(df2, "key", "outer")` | All rows from both |
| **Cross** | `df1.crossJoin(df2)` | Cartesian product |
| **Semi** | `df1.join(df2, "key", "left_semi")` | Left rows with match (no right columns) |
| **Anti** | `df1.join(df2, "key", "left_anti")` | Left rows without match |

---

## 📚 Basic Joins

### Inner Join

```python
# Join on single column (same name in both DataFrames)
result = df1.join(df2, "id", "inner")

# Join on multiple columns
result = df1.join(df2, ["id", "country"], "inner")

# Join on different column names
result = df1.join(df2, df1.customer_id == df2.user_id, "inner")

# Join with explicit condition
result = df1.join(df2, (df1.id == df2.id) & (df1.date == df2.date), "inner")
```

### Left Join (Left Outer)

```python
# Keep all records from left DataFrame
result = df1.join(df2, "id", "left")

# With different column names
result = df1.join(df2, df1.id == df2.customer_id, "left")

# Check for nulls from right table
result = df1.join(df2, "id", "left") \
    .withColumn("has_match", when(col("df2_column").isNull(), False).otherwise(True))
```

### Right Join (Right Outer)

```python
# Keep all records from right DataFrame
result = df1.join(df2, "id", "right")
```

### Full Outer Join

```python
# Keep all records from both DataFrames
result = df1.join(df2, "id", "outer")

# Identify source of each row
result = df1.join(df2, "id", "outer") \
    .withColumn("source", 
        when(col("df1_column").isNull(), "right_only")
        .when(col("df2_column").isNull(), "left_only")
        .otherwise("both")
    )
```

---

## 🎯 Special Joins

### Semi Join

Returns rows from left DataFrame where there's a match in right (no columns from right).

```python
# Get customers who made purchases (no purchase details)
customers_with_purchases = customers.join(
    purchases, 
    "customer_id", 
    "left_semi"
)

# Equivalent to:
customers_with_purchases = customers.filter(
    col("customer_id").isin(purchases.select("customer_id"))
)
```

### Anti Join

Returns rows from left DataFrame where there's NO match in right.

```python
# Get customers who never made purchases
customers_without_purchases = customers.join(
    purchases,
    "customer_id",
    "left_anti"
)

# Equivalent to:
customers_without_purchases = customers.filter(
    ~col("customer_id").isin(purchases.select("customer_id"))
)
```

### Cross Join

Cartesian product - every row from left with every row from right.

```python
# ⚠️ Warning: Can produce very large results!
result = df1.crossJoin(df2)

# More practical: Cross join with filter
result = df1.crossJoin(df2).filter(col("df1.category") == col("df2.type"))
```

---

## ⚡ Broadcast Joins

### When to Use Broadcast

Use when one DataFrame is small enough to fit in memory on each executor (typically < 10MB).

```python
from pyspark.sql.functions import broadcast

# Small table (< 10MB) - broadcast it!
result = large_df.join(broadcast(small_df), "id", "inner")

# Configure broadcast threshold
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 10485760)  # 10MB
```

### Benefits

✅ **No shuffle** - Small table sent to all executors
✅ **Faster execution** - Eliminates shuffle overhead
✅ **Better for small-to-large joins**

### Manual Broadcast

```python
from pyspark.sql.functions import broadcast

# Explicitly broadcast small DataFrame
large_df.join(broadcast(small_lookup), "lookup_key", "left")
```

---

## 🔧 Handling Join Challenges

### Duplicate Column Names

```python
# Problem: Both DataFrames have 'id' column
# Solution 1: Alias DataFrames
df1_aliased = df1.alias("a")
df2_aliased = df2.alias("b")

result = df1_aliased.join(df2_aliased, col("a.id") == col("b.id"), "inner") \
    .select("a.id", "a.name", "b.value")

# Solution 2: Rename columns before join
df2_renamed = df2.withColumnRenamed("id", "df2_id")
result = df1.join(df2_renamed, df1.id == df2_renamed.df2_id, "inner")

# Solution 3: Drop duplicate column after join
result = df1.join(df2, "id", "inner").drop(df2.id)
```

### Multiple Join Conditions

```python
# Join on multiple conditions
result = df1.join(
    df2,
    (df1.customer_id == df2.customer_id) & 
    (df1.date == df2.date) &
    (df1.country == df2.country),
    "inner"
)
```

### Null-Safe Join

```python
from pyspark.sql.functions import col

# Regular join - nulls don't match
result = df1.join(df2, df1.id == df2.id, "inner")

# Null-safe join - nulls match each other
result = df1.join(df2, df1.id.eqNullSafe(df2.id), "inner")
```

---

## 🐌 Data Skew Solutions

### Problem: Data Skew

When one or few keys have significantly more records than others, causing performance bottlenecks.

### Solution 1: Salting

```python
from pyspark.sql.functions import rand, floor

# Add salt to skewed key
num_salts = 10

df1_salted = df1.withColumn("salt", floor(rand() * num_salts))
df1_salted = df1_salted.withColumn("salted_key", 
    concat(col("key"), lit("_"), col("salt"))
)

# Replicate small table
df2_replicated = df2.withColumn("salt", explode(array([lit(i) for i in range(num_salts)])))
df2_replicated = df2_replicated.withColumn("salted_key",
    concat(col("key"), lit("_"), col("salt"))
)

# Join on salted key
result = df1_salted.join(df2_replicated, "salted_key", "inner") \
    .drop("salt", "salted_key")
```

### Solution 2: Broadcast Join

```python
# If small table causing skew, broadcast it
from pyspark.sql.functions import broadcast

result = large_skewed_df.join(broadcast(small_df), "key", "inner")
```

### Solution 3: Repartition

```python
# Repartition by join key before joining
df1_repartitioned = df1.repartition(200, "join_key")
df2_repartitioned = df2.repartition(200, "join_key")

result = df1_repartitioned.join(df2_repartitioned, "join_key", "inner")
```

---

## 🔗 Unions

### Basic Union

```python
# Union (includes duplicates)
result = df1.union(df2)

# Union distinct (removes duplicates)
result = df1.union(df2).distinct()

# UnionAll (alias for union - includes duplicates)
result = df1.unionAll(df2)
```

### Union by Name

```python
# Union by column name (order doesn't matter)
result = df1.unionByName(df2)

# Union by name with missing columns filled as null
result = df1.unionByName(df2, allowMissingColumns=True)
```

### Multiple DataFrame Union

```python
from functools import reduce

dfs = [df1, df2, df3, df4, df5]

# Union all DataFrames
result = reduce(lambda x, y: x.union(y), dfs)
```

---

## 🎓 Best Practices

### ✅ DO

```python
# Broadcast small DataFrames
result = large_df.join(broadcast(small_df), "key", "inner")

# Filter before joining
filtered_df1 = df1.filter(col("status") == "active")
result = filtered_df1.join(df2, "id", "inner")

# Cache frequently joined DataFrames
df1.cache()
result1 = df1.join(df2, "id", "inner")
result2 = df1.join(df3, "id", "inner")

# Use appropriate join type
# Use left_semi instead of inner join + select
customers.join(purchases, "customer_id", "left_semi")
```

### ❌ DON'T

```python
# Don't use cross join without filter
result = df1.crossJoin(df2)  # ⚠️ Huge result!

# Don't join without considering skew
# Check key distribution first!

# Don't forget to handle duplicate columns
result = df1.join(df2, "id", "inner")  # May have duplicate 'id'

# Don't join large DataFrames without partitioning
# Repartition first if needed!
```

---

## 📊 Common Patterns

### Pattern 1: Lookup Enrichment

```python
# Enrich data with lookup table
from pyspark.sql.functions import broadcast

transactions = transactions.join(
    broadcast(product_lookup),
    "product_id",
    "left"
)
```

### Pattern 2: Deduplication

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

# Keep latest record per key
window_spec = Window.partitionBy("customer_id").orderBy(col("timestamp").desc())

deduplicated = df.withColumn("row_num", row_number().over(window_spec)) \
    .filter(col("row_num") == 1) \
    .drop("row_num")
```

### Pattern 3: Finding New Records

```python
# Find records in current not in previous
new_records = current_df.join(
    previous_df,
    "id",
    "left_anti"
)
```

### Pattern 4: Full Outer Join Analysis

```python
# Identify matches and mismatches
result = df1.join(df2, "id", "outer") \
    .withColumn("match_type",
        when(col("df1.id").isNull(), "right_only")
        .when(col("df2.id").isNull(), "left_only")
        .otherwise("matched")
    )

# Count by match type
result.groupBy("match_type").count().show()
```

---

## 🚀 Performance Tips

1. **Broadcast small tables** - Use `broadcast()` for tables < 10MB
2. **Filter before joining** - Reduce data volume early
3. **Handle skew** - Use salting for skewed keys
4. **Appropriate join types** - Use semi/anti joins when possible
5. **Partition data** - Repartition by join key if needed
6. **Cache reused DataFrames** - Avoid recomputation

---

## 🔗 Related Guides

- [02. Transformations & Actions](02_transformations_actions.md)
- [03. Aggregations & GroupBy](03_aggregations_groupby.md)
- [08. Performance Optimization](08_performance_tuning.md)

---

## 📚 Additional Resources

- [Spark SQL Join Strategies](https://spark.apache.org/docs/latest/sql-performance-tuning.html#join-strategy-hints)
- [Handling Skew in Spark](https://medium.com/@achilleus/https-medium-com-joins-in-apache-spark-part-3-handling-data-skew-6d2b7e1e8c5b)

# Transformations & Actions

Understand PySpark's lazy evaluation model and master the difference between transformations and actions.

---

## 🎯 Quick Reference

| Type | Examples | Triggers Execution |
|------|----------|-------------------|
| **Transformations** | `select()`, `filter()`, `groupBy()`, `join()` | ❌ No (Lazy) |
| **Actions** | `show()`, `count()`, `collect()`, `write()` | ✅ Yes (Eager) |

---

## 📚 Understanding Lazy Evaluation

### What is Lazy Evaluation?

PySpark doesn't execute transformations immediately. Instead, it builds a **logical execution plan** and only executes when an action is called.

```python
# These are just transformations - nothing executes yet!
df1 = df.filter(col("age") > 25)  # Not executed
df2 = df1.select("name", "salary")  # Not executed
df3 = df2.orderBy("salary")  # Not executed

# This action triggers execution of ALL previous transformations
df3.show()  # NOW everything executes!
```

### Why Lazy Evaluation?

✅ **Optimization**: Spark can optimize the entire execution plan before running
✅ **Efficiency**: Combines multiple operations into fewer stages
✅ **Resource Management**: Doesn't waste resources on intermediate results

---

## 🔄 Transformations (Lazy)

### Narrow Transformations

Operations where each input partition contributes to at most one output partition. **No shuffle required!**

```python
# Narrow transformations
df.select("name", "age")           # Select
df.filter(col("age") > 25)         # Filter
df.withColumn("age_plus_1", col("age") + 1)  # Add column
df.drop("temp_column")             # Drop column
df.distinct()                      # Distinct (on same partition)
df.union(df2)                      # Union
df.map(lambda x: x)                # Map
df.flatMap(lambda x: x.split())    # FlatMap
```

**Performance**: ⚡ Fast - No network shuffling

### Wide Transformations

Operations where input partitions contribute to multiple output partitions. **Shuffle required!**

```python
# Wide transformations
df.groupBy("department").count()           # GroupBy
df.orderBy("salary")                       # OrderBy (sort)
df.repartition(10)                         # Repartition
df.join(df2, "id")                         # Join
df.distinct()                              # Distinct (across partitions)
df.intersect(df2)                          # Intersect
df.subtract(df2)                           # Subtract
```

**Performance**: 🐌 Slower - Requires shuffling data across network

---

## ⚡ Actions (Eager)

Actions trigger the execution of all pending transformations and return results to the driver or write to storage.

### Display Actions

```python
# Show data
df.show()                    # Show 20 rows
df.show(5)                   # Show 5 rows
df.show(5, truncate=False)   # Show without truncating
df.head(5)                   # Return first 5 rows as Row objects
df.first()                   # Return first row
df.take(10)                  # Return first 10 rows
```

### Collection Actions

```python
# Collect all data to driver
rows = df.collect()          # ⚠️ Dangerous for large datasets!
row = df.first()            # Get first row
rows = df.take(10)          # Get first 10 rows
rows = df.head(10)          # Same as take(10)

# Convert to pandas
pandas_df = df.toPandas()   # ⚠️ Dangerous for large datasets!
```

### Aggregation Actions

```python
# Count operations
total = df.count()          # Count all rows
num_cols = len(df.columns)  # Count columns

# Statistical operations
df.describe().show()        # Summary statistics
df.summary().show()         # Extended statistics
```

### Write Actions

```python
# Write to storage
df.write.csv("output.csv")
df.write.parquet("output.parquet")
df.write.json("output.json")

# Write modes
df.write.mode("overwrite").parquet("output.parquet")
df.write.mode("append").csv("output.csv")
df.write.mode("ignore").json("output.json")
df.write.mode("error").parquet("output.parquet")  # Default
```

### Execution Actions

```python
# Force execution without returning data
df.foreach(lambda row: print(row))
df.foreachPartition(lambda partition: process(partition))
```

---

## 💾 Caching and Persistence

### Why Cache?

When you reuse a DataFrame multiple times, cache it to avoid recomputing.

```python
# Without caching - computes twice!
df_filtered = df.filter(col("age") > 25)
result1 = df_filtered.groupBy("department").count()
result2 = df_filtered.groupBy("city").count()

# With caching - computes once!
df_filtered = df.filter(col("age") > 25).cache()
result1 = df_filtered.groupBy("department").count()
result2 = df_filtered.groupBy("city").count()
```

### Cache vs Persist

```python
from pyspark import StorageLevel

# Cache in memory (default)
df.cache()

# Persist with storage level
df.persist(StorageLevel.MEMORY_ONLY)
df.persist(StorageLevel.MEMORY_AND_DISK)
df.persist(StorageLevel.DISK_ONLY)
df.persist(StorageLevel.MEMORY_AND_DISK_SER)  # Serialized

# Unpersist when done
df.unpersist()
```

### Storage Levels

| Storage Level | Memory | Disk | Serialized | Replication |
|--------------|--------|------|------------|-------------|
| `MEMORY_ONLY` | ✅ | ❌ | ❌ | 1 |
| `MEMORY_AND_DISK` | ✅ | ✅ | ❌ | 1 |
| `DISK_ONLY` | ❌ | ✅ | ❌ | 1 |
| `MEMORY_ONLY_SER` | ✅ | ❌ | ✅ | 1 |
| `MEMORY_AND_DISK_SER` | ✅ | ✅ | ✅ | 1 |

---

## 🎓 Best Practices

### ✅ DO

```python
# Cache DataFrames that are reused multiple times
df_cached = df.filter(col("status") == "active").cache()
result1 = df_cached.count()
result2 = df_cached.groupBy("city").count()

# Use actions only when needed
# Don't call count() unnecessarily
if df.filter(col("age") > 100).isEmpty():  # Better
    print("No outliers")

# Chain transformations before action
result = df.select("name", "age") \
    .filter(col("age") > 25) \
    .orderBy("age") \
    .show()  # Single action at the end

# Unpersist when done
df_cached.unpersist()
```

### ❌ DON'T

```python
# Don't collect() large datasets
all_data = df.collect()  # ⚠️ Can crash driver!

# Don't call actions in loops
for i in range(10):
    df.filter(col("id") == i).count()  # ❌ Inefficient!

# Don't cache everything
df1 = df.filter(col("age") > 25).cache()  # Only used once - unnecessary!
result = df1.count()

# Don't forget to unpersist
df.cache()
# ... use df ...
# df.unpersist()  # Don't forget this!
```

---

## 📊 Common Patterns

### Pattern 1: Multi-Branch Processing

```python
# Base DataFrame
base_df = df.filter(col("status") == "active").cache()

# Multiple downstream operations
high_value = base_df.filter(col("amount") > 1000)
low_value = base_df.filter(col("amount") <= 1000)

# Process each branch
high_value.groupBy("category").sum("amount").show()
low_value.groupBy("category").count().show()

# Cleanup
base_df.unpersist()
```

### Pattern 2: Iterative Refinement

```python
# Start with raw data
df1 = spark.read.csv("data.csv", header=True, inferSchema=True)

# Apply transformations iteratively
df2 = df1.filter(col("status") == "active")
df3 = df2.withColumn("processed_date", current_date())
df4 = df3.drop("temp_column")

# Cache before multiple actions
df4.cache()
df4.write.parquet("output/processed")
df4.groupBy("category").count().show()
```

### Pattern 3: Checkpoint for Long Lineages

```python
# Set checkpoint directory
spark.sparkContext.setCheckpointDir("/tmp/checkpoints")

# Long chain of transformations
df1 = df.filter(col("a") > 0)
df2 = df1.join(df_lookup, "id")
df3 = df2.groupBy("category").agg(sum("amount"))
df4 = df3.filter(col("sum(amount)") > 1000)

# Checkpoint to break lineage
df4 = df4.checkpoint()

# Continue with more transformations
result = df4.orderBy("category")
```

---

## 🚀 Performance Comparison

### Transformation Types

```python
import time

# Narrow transformation (fast)
start = time.time()
df_narrow = df.select("name", "age").filter(col("age") > 25)
df_narrow.count()
print(f"Narrow: {time.time() - start:.2f}s")

# Wide transformation (slower)
start = time.time()
df_wide = df.groupBy("department").agg(avg("salary"))
df_wide.count()
print(f"Wide: {time.time() - start:.2f}s")
```

### Caching Impact

```python
# Without cache
start = time.time()
df_filtered = df.filter(col("age") > 25)
df_filtered.count()
df_filtered.groupBy("dept").count().show()
print(f"Without cache: {time.time() - start:.2f}s")

# With cache
start = time.time()
df_filtered = df.filter(col("age") > 25).cache()
df_filtered.count()
df_filtered.groupBy("dept").count().show()
print(f"With cache: {time.time() - start:.2f}s")
```

---

## 🔧 Debugging Tips

### View Execution Plan

```python
# Logical plan
df.explain()

# Physical plan
df.explain(True)

# Extended explanation
df.explain("extended")

# Cost analysis
df.explain("cost")
```

### Check Caching Status

```python
# Check if DataFrame is cached
df.is_cached

# View storage level
df.storageLevel
```

---

## 🔗 Related Guides

- [01. DataFrame Basics](01_dataframe_basics.md)
- [08. Performance Optimization](08_performance_tuning.md)
- [10. Debugging & Best Practices](10_debugging_best_practices.md)

---

## 📚 Additional Resources

- [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)
- [Spark SQL Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html)

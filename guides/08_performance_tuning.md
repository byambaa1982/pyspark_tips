# Performance Optimization

Master PySpark performance tuning techniques, from partitioning strategies to caching and shuffle optimization.

---

## 🎯 Quick Reference

| Technique | When to Use | Impact |
|-----------|-------------|--------|
| **Caching** | Reusing DataFrames multiple times | 🟢 High |
| **Broadcast Join** | Joining with small tables (<10MB) | 🟢 High |
| **Partitioning** | Large datasets, uneven distribution | 🟢 High |
| **Coalesce** | Reducing partition count | 🟡 Medium |
| **Filter Early** | Before expensive operations | 🟢 High |
| **Built-in Functions** | Instead of UDFs | 🟢 High |

---

## 📊 Understanding Partitions

### What are Partitions?

Partitions are the basic unit of parallelism in Spark. Data is divided into partitions, and each partition is processed independently.

```python
# Check number of partitions
print(f"Partitions: {df.rdd.getNumPartitions()}")

# Check data distribution across partitions
df.rdd.glom().map(len).collect()  # Shows rows per partition
```

### Optimal Partition Size

✅ **Target**: 100-200MB per partition
❌ **Too small**: High overhead, slow
❌ **Too large**: Memory issues, slow tasks

```python
# Calculate optimal partitions
file_size_mb = 10000  # 10GB
optimal_partitions = file_size_mb // 128  # ~78 partitions

df = spark.read.parquet("data.parquet") \
    .repartition(optimal_partitions)
```

---

## 🔄 Partitioning Strategies

### Repartition vs Coalesce

```python
# Repartition (full shuffle - expensive)
df_repart = df.repartition(100)  # Can increase or decrease

# Coalesce (no shuffle - efficient)
df_coalesce = df.coalesce(50)  # Can only decrease

# When to use:
# - Repartition: Need to increase partitions or redistribute data
# - Coalesce: Only need to reduce partitions
```

### Partition by Column

```python
# Repartition by column (for joins/groupBy)
df = df.repartition(200, "department")

# Multiple columns
df = df.repartition(200, "year", "month")

# Benefits:
# - Co-locate related data
# - Optimize joins and groupBy
# - Reduce shuffle in downstream operations
```

### Adaptive Query Execution (AQE)

```python
# Enable AQE (Spark 3.0+)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# AQE automatically:
# - Adjusts partition counts
# - Handles data skew
# - Optimizes join strategies
```

---

## 💾 Caching & Persistence

### When to Cache

Cache DataFrames that are:
- Used multiple times
- Expensive to compute
- Small enough to fit in memory

```python
# Cache in memory
df.cache()

# Or use persist with storage level
from pyspark import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK)

# Use the cached DataFrame
result1 = df.groupBy("category").count()
result2 = df.groupBy("region").sum("sales")

# Unpersist when done
df.unpersist()
```

### Storage Levels

```python
from pyspark import StorageLevel

# Memory only (fastest, but may fail if not enough memory)
df.persist(StorageLevel.MEMORY_ONLY)

# Memory and disk (recommended)
df.persist(StorageLevel.MEMORY_AND_DISK)

# Disk only (slowest)
df.persist(StorageLevel.DISK_ONLY)

# Serialized in memory (saves space)
df.persist(StorageLevel.MEMORY_ONLY_SER)
```

### Caching Best Practices

```python
# ✅ Good - cache when reusing
df_filtered = df.filter(col("status") == "active").cache()
result1 = df_filtered.count()
result2 = df_filtered.groupBy("category").sum("amount")
df_filtered.unpersist()

# ❌ Bad - unnecessary cache
df_temp = df.filter(col("status") == "active").cache()  # Used only once
result = df_temp.count()

# ❌ Bad - caching everything
df1.cache()
df2.cache()
df3.cache()  # May run out of memory!
```

---

## ⚡ Join Optimization

### Broadcast Joins

Best for joining large DataFrame with small DataFrame (<10MB).

```python
from pyspark.sql.functions import broadcast

# Automatic broadcast (if < threshold)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 10485760)  # 10MB

# Manual broadcast (recommended)
large_df.join(broadcast(small_df), "id", "inner")

# Benefits:
# - No shuffle
# - Much faster
# - Lower memory usage on executors
```

### Sort-Merge Join

For large-large joins.

```python
# Hint for sort-merge join
df1.hint("merge").join(df2, "key")

# Pre-partition by join key
df1_part = df1.repartition(200, "key")
df2_part = df2.repartition(200, "key")
result = df1_part.join(df2_part, "key")
```

### Handling Skewed Joins

```python
# Enable skew join optimization (Spark 3.0+)
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")

# Manual salting for severe skew
from pyspark.sql.functions import rand, floor

num_salts = 10
df1_salted = df1.withColumn("salt", floor(rand() * num_salts))
# ... (see Joins guide for full example)
```

---

## 🚀 Transformation Optimization

### Filter Early

```python
# ✅ Good - filter first
df.filter(col("date") >= "2024-01-01") \
  .filter(col("status") == "active") \
  .groupBy("category").count()

# ❌ Bad - filter after heavy operation
df.groupBy("category").count() \
  .filter(col("count") > 100)
```

### Use Built-in Functions

```python
# ❌ Bad - Python UDF
@udf(StringType())
def to_upper(s):
    return s.upper()

df.withColumn("upper", to_upper(col("name")))  # Slow!

# ✅ Good - built-in function
df.withColumn("upper", upper(col("name")))  # Fast!

# Performance difference: 10-100x faster!
```

### Avoid Collect

```python
# ❌ Bad - brings all data to driver
all_data = df.collect()  # May crash!
for row in all_data:
    process(row)

# ✅ Good - process distributedly
df.foreach(lambda row: process(row))

# ✅ Good - aggregate first
total = df.agg(sum("amount")).collect()[0][0]
```

### Column Pruning

```python
# ❌ Bad - reading all columns
df.select("*").filter(col("status") == "active")

# ✅ Good - select only needed columns
df.select("id", "name", "status").filter(col("status") == "active")
```

---

## 📁 File Format Optimization

### Parquet (Recommended)

```python
# Write Parquet
df.write.mode("overwrite") \
    .option("compression", "snappy") \
    .parquet("output.parquet")

# Benefits:
# - Columnar format
# - Excellent compression
# - Schema evolution
# - Predicate pushdown
```

### Partitioned Writes

```python
# Partition by date
df.write.mode("overwrite") \
    .partitionBy("year", "month") \
    .parquet("output")

# Benefits:
# - Faster queries with date filters
# - Better data organization
# - Easier data management
```

### File Size Management

```python
# Control file size with coalesce
df.coalesce(10).write.parquet("output")  # ~10 files

# Target file size
df.repartition(100).write.parquet("output")  # More control
```

---

## 🔧 Configuration Tuning

### Memory Configuration

```python
# Executor memory
spark = SparkSession.builder \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "4") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()
```

### Shuffle Configuration

```python
# Shuffle partitions (default: 200)
spark.conf.set("spark.sql.shuffle.partitions", "400")

# Rule of thumb:
# - Small data (<1GB): 50-100 partitions
# - Medium data (1-10GB): 200-500 partitions
# - Large data (>10GB): 500-2000 partitions
```

### Serialization

```python
# Use Kryo serialization (faster than Java)
spark = SparkSession.builder \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()
```

---

## 📊 Monitoring & Debugging

### Explain Plan

```python
# View logical plan
df.explain()

# View physical plan
df.explain(True)

# View detailed plan
df.explain("extended")

# Cost-based plan
df.explain("cost")
```

### Spark UI

Monitor:
- Jobs and stages
- Task execution time
- Data shuffled
- Memory usage
- Executor status

Access at: `http://localhost:4040`

### Debugging Slow Jobs

```python
# Check partition sizes
df.rdd.glom().map(len).collect()

# Count partitions
df.rdd.getNumPartitions()

# Sample data
df.sample(0.01).show()

# Check schema
df.printSchema()
```

---

## 🎓 Best Practices Summary

### ✅ DO

```python
# 1. Cache reused DataFrames
df.cache()

# 2. Broadcast small tables
large_df.join(broadcast(small_df), "key")

# 3. Filter early
df.filter(col("date") >= "2024-01-01").groupBy("category").count()

# 4. Use appropriate partitioning
df.repartition(200, "key")

# 5. Use built-in functions
df.withColumn("upper", upper(col("name")))

# 6. Use Parquet format
df.write.parquet("output")

# 7. Enable AQE
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

### ❌ DON'T

```python
# 1. Don't collect large datasets
all_data = df.collect()  # Dangerous!

# 2. Don't use Python UDFs unnecessarily
@udf(StringType())
def to_upper(s): return s.upper()

# 3. Don't have too many small files
df.write.parquet("output")  # Could create 1000s of small files

# 4. Don't cache everything
df1.cache(); df2.cache(); df3.cache()  # Memory issues!

# 5. Don't forget to unpersist
df.cache()
# ... use df ...
# df.unpersist()  # Don't forget!
```

---

## 📈 Performance Checklist

- [ ] Enable Adaptive Query Execution (AQE)
- [ ] Use appropriate partition count (100-200MB per partition)
- [ ] Broadcast small tables in joins
- [ ] Cache DataFrames used multiple times
- [ ] Filter data as early as possible
- [ ] Use built-in functions instead of UDFs
- [ ] Use Parquet format with compression
- [ ] Partition data by common filter columns
- [ ] Monitor Spark UI for bottlenecks
- [ ] Unpersist cached DataFrames when done

---

## 🔗 Related Guides

- [02. Transformations & Actions](02_transformations_actions.md)
- [04. Joins & Unions](04_joins_unions.md)
- [05. UDFs & Built-in Functions](05_udfs_functions.md)
- [09. Data I/O & Formats](09_data_io_formats.md)

---

## 📚 Additional Resources

- [Spark Performance Tuning Guide](https://spark.apache.org/docs/latest/sql-performance-tuning.html)
- [Spark Configuration](https://spark.apache.org/docs/latest/configuration.html)
- [Adaptive Query Execution](https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution)

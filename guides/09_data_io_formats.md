# Data I/O & Formats

Master reading and writing data in various formats with optimal performance and schema management.

---

## 🎯 Quick Reference

| Format | Read Speed | Write Speed | Compression | Schema | Best For |
|--------|-----------|-------------|-------------|---------|----------|
| **Parquet** | ⚡⚡⚡ | ⚡⚡⚡ | ✅ Excellent | ✅ Yes | Analytics, large datasets |
| **CSV** | ⚡ | ⚡ | ❌ Poor | ❌ Manual | Small files, human-readable |
| **JSON** | ⚡⚡ | ⚡⚡ | ❌ Poor | ✅ Partial | Semi-structured data |
| **ORC** | ⚡⚡⚡ | ⚡⚡⚡ | ✅ Excellent | ✅ Yes | Hive integration |
| **Delta Lake** | ⚡⚡⚡ | ⚡⚡⚡ | ✅ Excellent | ✅ Yes | ACID transactions, time travel |
| **Avro** | ⚡⚡ | ⚡⚡ | ✅ Good | ✅ Yes | Schema evolution |

---

## 📁 CSV Operations

### Reading CSV

```python
# Basic read
df = spark.read.csv("data.csv", header=True, inferSchema=True)

# With options
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("delimiter", ",") \
    .option("quote", '"') \
    .option("escape", "\\") \
    .option("nullValue", "NA") \
    .csv("data.csv")

# Multiple files
df = spark.read.csv("data/*.csv", header=True, inferSchema=True)

# With explicit schema (recommended for production)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", DoubleType(), True)
])

df = spark.read.csv("data.csv", header=True, schema=schema)
```

### Writing CSV

```python
# Basic write
df.write.mode("overwrite").csv("output.csv", header=True)

# With options
df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .option("delimiter", ",") \
    .option("quote", '"') \
    .option("compression", "gzip") \
    .csv("output.csv")

# Single file output
df.coalesce(1).write.csv("output.csv", header=True)
```

---

## 📦 Parquet Operations (Recommended)

### Reading Parquet

```python
# Basic read
df = spark.read.parquet("data.parquet")

# Multiple files/directories
df = spark.read.parquet("data/*.parquet")
df = spark.read.parquet("data/year=2024/month=*")

# With predicate pushdown (automatic)
df = spark.read.parquet("data.parquet") \
    .filter(col("date") >= "2024-01-01")  # Only reads relevant partitions

# Schema evolution
df = spark.read \
    .option("mergeSchema", "true") \
    .parquet("data.parquet")
```

### Writing Parquet

```python
# Basic write
df.write.mode("overwrite").parquet("output.parquet")

# With compression
df.write \
    .mode("overwrite") \
    .option("compression", "snappy") \
    .parquet("output.parquet")

# Compression options: snappy (default), gzip, lzo, uncompressed

# Partitioned write (highly recommended)
df.write \
    .mode("overwrite") \
    .partitionBy("year", "month") \
    .parquet("output.parquet")

# Control file size
df.repartition(50) \
    .write.mode("overwrite") \
    .parquet("output.parquet")
```

---

## 🔷 JSON Operations

### Reading JSON

```python
# Basic read
df = spark.read.json("data.json")

# Multiline JSON
df = spark.read \
    .option("multiline", "true") \
    .json("data.json")

# With schema
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("metadata", StringType(), True)
])

df = spark.read.schema(schema).json("data.json")

# Corrupted records
df = spark.read \
    .option("mode", "PERMISSIVE") \
    .option("columnNameOfCorruptRecord", "_corrupt_record") \
    .json("data.json")
```

### Writing JSON

```python
# Basic write
df.write.mode("overwrite").json("output.json")

# Pretty print
df.write \
    .mode("overwrite") \
    .option("compression", "gzip") \
    .json("output.json")

# Single line per record (default)
df.write.json("output.json")
```

---

## 🗄️ Database Operations

### JDBC Connections

```python
# Read from database
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "users") \
    .option("user", "username") \
    .option("password", "password") \
    .option("driver", "org.postgresql.Driver") \
    .load()

# Read with query
query = "(SELECT * FROM users WHERE age > 25) AS subquery"
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", query) \
    .option("user", "username") \
    .option("password", "password") \
    .load()

# Partitioned read (for large tables)
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "users") \
    .option("user", "username") \
    .option("password", "password") \
    .option("partitionColumn", "id") \
    .option("lowerBound", "1") \
    .option("upperBound", "1000000") \
    .option("numPartitions", "100") \
    .load()
```

### Writing to Database

```python
# Write to database
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "output_table") \
    .option("user", "username") \
    .option("password", "password") \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()

# Append mode
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "output_table") \
    .option("user", "username") \
    .option("password", "password") \
    .mode("append") \
    .save()
```

---

## 🌊 Delta Lake

### Reading Delta Tables

```python
# Read Delta table
df = spark.read.format("delta").load("path/to/delta/table")

# Or using table name
df = spark.read.table("my_delta_table")

# Time travel - read historical version
df = spark.read \
    .format("delta") \
    .option("versionAsOf", 0) \
    .load("path/to/delta/table")

# Time travel by timestamp
df = spark.read \
    .format("delta") \
    .option("timestampAsOf", "2024-01-01") \
    .load("path/to/delta/table")
```

### Writing Delta Tables

```python
# Write Delta table
df.write.format("delta").mode("overwrite").save("path/to/delta/table")

# Append
df.write.format("delta").mode("append").save("path/to/delta/table")

# Merge (Upsert)
from delta.tables import DeltaTable

deltaTable = DeltaTable.forPath(spark, "path/to/delta/table")

deltaTable.alias("target").merge(
    source_df.alias("source"),
    "target.id = source.id"
).whenMatchedUpdate(set = {
    "name": "source.name",
    "age": "source.age"
}).whenNotMatchedInsert(values = {
    "id": "source.id",
    "name": "source.name",
    "age": "source.age"
}).execute()
```

### Delta Lake Operations

```python
from delta.tables import DeltaTable

# Optimize table
deltaTable = DeltaTable.forPath(spark, "path/to/delta/table")
deltaTable.optimize().executeCompaction()

# Vacuum (remove old files)
deltaTable.vacuum()  # Default: 7 days retention
deltaTable.vacuum(168)  # 168 hours = 7 days

# View history
deltaTable.history().show()
```

---

## 🎯 Best Practices

### Schema Management

```python
# ✅ Define schema explicitly (production)
schema = StructType([
    StructField("id", IntegerType(), False),  # Not nullable
    StructField("name", StringType(), True),
    StructField("email", StringType(), True)
])

df = spark.read.schema(schema).csv("data.csv")

# ✅ Save schema
df.schema.json()  # Serialize schema

# ✅ Load schema
from pyspark.sql.types import StructType
schema = StructType.fromJson(json.loads(schema_json))
```

### Partitioning Strategy

```python
# ✅ Good - partition by commonly filtered columns
df.write \
    .partitionBy("year", "month", "day") \
    .parquet("output")

# ❌ Bad - too many partitions (small files problem)
df.write \
    .partitionBy("year", "month", "day", "hour", "minute") \
    .parquet("output")

# ❌ Bad - high cardinality column
df.write \
    .partitionBy("user_id") \
    .parquet("output")  # Millions of partitions!
```

### File Size Management

```python
# Target: 100-200MB per file

# Control number of output files
num_output_files = total_data_size_mb / 128
df.repartition(num_output_files) \
    .write.parquet("output")

# For small datasets
df.coalesce(1).write.parquet("output")
```

---

## 📊 Format Comparison

### When to Use Each Format

**Parquet**: 
- ✅ Large analytical workloads
- ✅ Column-oriented queries
- ✅ Need compression
- ✅ Schema evolution

**CSV**: 
- ✅ Small files
- ✅ Human readability
- ✅ Simple data exchange
- ❌ Large datasets (use Parquet!)

**JSON**: 
- ✅ Semi-structured data
- ✅ Nested structures
- ✅ API responses
- ❌ Large datasets

**Delta Lake**: 
- ✅ ACID transactions
- ✅ Time travel
- ✅ Upserts/Deletes
- ✅ Schema evolution
- ✅ Production data lakes

---

## 🚀 Performance Tips

### Reading Optimization

```python
# 1. Use predicate pushdown
df = spark.read.parquet("data") \
    .filter(col("date") >= "2024-01-01")  # Pushed to storage

# 2. Select only needed columns
df = spark.read.parquet("data") \
    .select("id", "name", "amount")

# 3. Use partitioned reads
df = spark.read.parquet("data/year=2024/month=*")

# 4. Enable vectorized readers (Parquet, ORC)
spark.conf.set("spark.sql.parquet.enableVectorizedReader", "true")
```

### Writing Optimization

```python
# 1. Use optimal partitioning
df.write \
    .partitionBy("year", "month") \
    .parquet("output")

# 2. Control file size
df.repartition(50).write.parquet("output")

# 3. Use compression
df.write \
    .option("compression", "snappy") \
    .parquet("output")

# 4. Use Delta Lake for updates
df.write.format("delta").save("output")
```

---

## 🔗 Related Guides

- [01. DataFrame Basics](01_dataframe_basics.md)
- [08. Performance Optimization](08_performance_tuning.md)
- [10. Debugging & Best Practices](10_debugging_best_practices.md)

---

## 📚 Additional Resources

- [Parquet Documentation](https://parquet.apache.org/docs/)
- [Delta Lake Documentation](https://docs.delta.io/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-data-sources.html)

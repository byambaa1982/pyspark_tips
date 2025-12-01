# Debugging & Best Practices

Master debugging techniques, error handling, testing strategies, and production-ready code organization for PySpark.

---

## 🎯 Quick Reference

| Technique | Use Case | Tool/Method |
|-----------|----------|-------------|
| **View execution plan** | Understand query optimization | `df.explain()` |
| **Inspect schema** | Verify data types | `df.printSchema()` |
| **Sample data** | Quick data inspection | `df.show()`, `df.head()` |
| **Count records** | Validate transformations | `df.count()` |
| **Check nulls** | Data quality | `df.na.drop()` |
| **Monitor jobs** | Performance tracking | Spark UI |

---

## 🐛 Debugging Techniques

### Understanding Execution Plans

```python
# Logical plan only
df.explain()

# Full execution plan
df.explain(True)

# Extended plan with statistics
df.explain("extended")

# Formatted plan
df.explain("formatted")

# Example output analysis:
result = df.filter(col("age") > 25) \
    .groupBy("department") \
    .agg(avg("salary"))

result.explain()
"""
== Physical Plan ==
AdaptiveSparkPlan
+- HashAggregate
   +- Exchange (shuffle)
      +- HashAggregate
         +- Filter (age > 25)
            +- FileScan parquet
"""
```

### Inspecting Data

```python
# View schema
df.printSchema()

# Show sample data
df.show(5, truncate=False)

# View specific rows
df.head(3)
df.take(5)
df.first()

# Count records
df.count()

# Sample data
df.sample(0.01).show()  # 1% sample

# Describe statistics
df.describe().show()

# Get column summary
df.select("column").summary().show()
```

### Partition Analysis

```python
# Check partition count
print(f"Partitions: {df.rdd.getNumPartitions()}")

# Check data distribution
partition_sizes = df.rdd.glom().map(len).collect()
print(f"Rows per partition: {partition_sizes}")

# Check empty partitions
empty_partitions = sum(1 for size in partition_sizes if size == 0)
print(f"Empty partitions: {empty_partitions}")

# Identify skew
max_partition = max(partition_sizes)
min_partition = min(partition_sizes)
print(f"Skew ratio: {max_partition / min_partition if min_partition > 0 else 'inf'}")
```

---

## 🚨 Error Handling

### Common Errors and Solutions

#### 1. Out of Memory Error

```python
# Problem
# java.lang.OutOfMemoryError: GC overhead limit exceeded

# Solutions:
# 1. Increase executor memory
spark = SparkSession.builder \
    .config("spark.executor.memory", "8g") \
    .getOrCreate()

# 2. Increase partitions
df = df.repartition(400)

# 3. Filter early
df = df.filter(col("date") >= "2024-01-01")

# 4. Use cache strategically
df.cache()
```

#### 2. Task Not Serializable

```python
# Problem
# org.apache.spark.SparkException: Task not serializable

# ❌ Bad - class not serializable
class MyClass:
    def process(self, df):
        return df.filter(col("value") > self.threshold)

# ✅ Good - use local variables
def process_df(df, threshold):
    return df.filter(col("value") > threshold)

# ✅ Good - use broadcast for small data
from pyspark.sql.functions import broadcast
lookup_dict = {"A": 1, "B": 2}
broadcast_dict = spark.sparkContext.broadcast(lookup_dict)
```

#### 3. Analysis Exception (Column Not Found)

```python
# Problem
# pyspark.sql.utils.AnalysisException: Column 'age' does not exist

# Solution: Check schema
df.printSchema()

# Solution: Use proper column references
df.select(col("age"))  # Not df.select("ageee")

# Solution: Handle case sensitivity
spark.conf.set("spark.sql.caseSensitive", "true")
```

#### 4. Shuffle Read/Write Too Large

```python
# Problem
# Shuffle is taking too long

# Solutions:
# 1. Broadcast small tables
large_df.join(broadcast(small_df), "key")

# 2. Increase shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", "400")

# 3. Partition by join key
df1.repartition(200, "key").join(df2.repartition(200, "key"), "key")

# 4. Enable AQE
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

---

## ✅ Data Quality Checks

### Null Handling

```python
# Count nulls per column
from pyspark.sql.functions import count, when, col

null_counts = df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
])
null_counts.show()

# Filter rows with any null
df_no_nulls = df.na.drop()

# Filter rows with null in specific columns
df_clean = df.na.drop(subset=["age", "salary"])

# Fill nulls with default values
df_filled = df.na.fill({
    "age": 0,
    "name": "Unknown",
    "salary": 50000
})
```

### Duplicate Detection

```python
# Count duplicates
duplicates = df.groupBy(df.columns).count() \
    .filter(col("count") > 1)

duplicates.show()

# Remove duplicates
df_unique = df.dropDuplicates()

# Remove duplicates based on subset
df_unique = df.dropDuplicates(["id", "email"])
```

### Data Validation

```python
# Check value ranges
df.select(
    min("age").alias("min_age"),
    max("age").alias("max_age"),
    avg("age").alias("avg_age")
).show()

# Identify outliers
from pyspark.sql.functions import percentile_approx

outliers = df.filter(
    (col("age") < 0) | (col("age") > 120)
)

# Check distinct values
df.select("category").distinct().show()

# Check for expected values
valid_statuses = ["active", "inactive", "pending"]
invalid = df.filter(~col("status").isin(valid_statuses))
```

---

## 🧪 Testing Strategies

### Unit Testing DataFrames

```python
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

@pytest.fixture
def spark():
    return SparkSession.builder \
        .appName("test") \
        .master("local[2]") \
        .getOrCreate()

def test_transformation(spark):
    # Create test data
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True)
    ])
    
    data = [(1, "Alice", 25), (2, "Bob", 30)]
    df = spark.createDataFrame(data, schema)
    
    # Apply transformation
    result = df.filter(col("age") > 25)
    
    # Assert
    assert result.count() == 1
    assert result.first()["name"] == "Bob"

def test_schema(spark):
    df = spark.read.csv("data.csv", header=True, inferSchema=True)
    
    # Check schema
    assert "id" in df.columns
    assert df.schema["age"].dataType == IntegerType()
```

### Integration Testing

```python
def test_end_to_end_pipeline(spark):
    # Read
    df = spark.read.csv("input.csv", header=True, inferSchema=True)
    
    # Transform
    result = df.filter(col("status") == "active") \
        .groupBy("category") \
        .agg(sum("amount").alias("total"))
    
    # Validate
    assert result.count() > 0
    assert "total" in result.columns
    
    # Write
    result.write.mode("overwrite").parquet("output.parquet")
    
    # Verify write
    written = spark.read.parquet("output.parquet")
    assert written.count() == result.count()
```

---

## 📋 Best Practices

### Code Organization

```python
# ✅ Good - modular functions
def read_data(spark, path):
    """Read data from CSV file."""
    return spark.read.csv(path, header=True, inferSchema=True)

def clean_data(df):
    """Clean and validate data."""
    return df.filter(col("age") >= 0) \
        .filter(col("age") <= 120) \
        .na.drop(subset=["id", "name"])

def transform_data(df):
    """Apply business logic transformations."""
    return df.withColumn("age_group",
        when(col("age") < 18, "Minor")
        .when(col("age") < 65, "Adult")
        .otherwise("Senior")
    )

def write_data(df, path):
    """Write data to Parquet."""
    df.write.mode("overwrite") \
        .partitionBy("age_group") \
        .parquet(path)

# Main pipeline
def main():
    spark = SparkSession.builder.appName("MyApp").getOrCreate()
    
    df = read_data(spark, "input.csv")
    df = clean_data(df)
    df = transform_data(df)
    write_data(df, "output.parquet")
    
    spark.stop()

if __name__ == "__main__":
    main()
```

### Configuration Management

```python
# config.py
class Config:
    # Spark configs
    SPARK_APP_NAME = "MyApp"
    EXECUTOR_MEMORY = "4g"
    EXECUTOR_CORES = "4"
    
    # Data paths
    INPUT_PATH = "s3://bucket/input/"
    OUTPUT_PATH = "s3://bucket/output/"
    
    # Business logic
    MIN_AGE = 18
    MAX_AGE = 120

# main.py
from config import Config

spark = SparkSession.builder \
    .appName(Config.SPARK_APP_NAME) \
    .config("spark.executor.memory", Config.EXECUTOR_MEMORY) \
    .getOrCreate()

df = spark.read.parquet(Config.INPUT_PATH)
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_data(spark, input_path):
    logger.info(f"Reading data from {input_path}")
    df = spark.read.parquet(input_path)
    
    logger.info(f"Initial row count: {df.count()}")
    
    logger.info("Applying transformations")
    df = df.filter(col("status") == "active")
    
    logger.info(f"Final row count: {df.count()}")
    
    return df
```

---

## 🎓 Production Checklist

### Before Deployment

- [ ] Schema explicitly defined
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Unit tests written
- [ ] Integration tests passed
- [ ] Configuration externalized
- [ ] Memory settings optimized
- [ ] Partitioning strategy defined
- [ ] Caching strategy implemented
- [ ] Monitoring configured

### Code Review Checklist

- [ ] No collect() on large datasets
- [ ] Built-in functions used over UDFs
- [ ] Filter applied early
- [ ] Appropriate join types used
- [ ] Broadcast hints for small tables
- [ ] Proper error handling
- [ ] Logging statements added
- [ ] Code is modular and testable
- [ ] Configuration is externalized
- [ ] Documentation is complete

---

## 🔍 Monitoring in Production

### Spark UI Metrics

Monitor these key metrics:
- **Job duration**: Overall execution time
- **Stages**: Number and duration
- **Tasks**: Success/failure rate
- **Shuffle read/write**: Data movement
- **Memory usage**: Executor memory
- **Skew**: Task duration variance

### Custom Metrics

```python
from pyspark.sql.functions import current_timestamp

# Add processing timestamp
df = df.withColumn("processed_at", current_timestamp())

# Track record counts
input_count = df.count()
logger.info(f"Input records: {input_count}")

filtered_df = df.filter(col("status") == "active")
filtered_count = filtered_df.count()
logger.info(f"Filtered records: {filtered_count}")
logger.info(f"Filter rate: {filtered_count/input_count*100:.2f}%")
```

---

## 🚀 Performance Debugging

### Identify Slow Stages

```python
# Check execution plan
df.explain("extended")

# Profile partitions
df.rdd.glom().map(len).collect()

# Check for skew
df.groupBy("key").count().orderBy(col("count").desc()).show()
```

### Memory Profiling

```python
# Check DataFrame size estimate
df.cache()
df.count()
# Check Spark UI Storage tab for size

# Check serialized size
import sys
sample = df.take(1000)
size_mb = sys.getsizeof(sample) / (1024 * 1024)
print(f"Sample size: {size_mb:.2f} MB")
```

---

## 🔗 Related Guides

- [02. Transformations & Actions](02_transformations_actions.md)
- [08. Performance Optimization](08_performance_tuning.md)
- [09. Data I/O & Formats](09_data_io_formats.md)

---

## 📚 Additional Resources

- [PySpark Testing Best Practices](https://spark.apache.org/docs/latest/api/python/getting_started/testing_pyspark.html)
- [Spark Monitoring Guide](https://spark.apache.org/docs/latest/monitoring.html)
- [Debugging Spark Applications](https://spark.apache.org/docs/latest/tuning.html)

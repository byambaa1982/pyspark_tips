# ⚡ PySpark Pro Tips & Big Data Utilities

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/pyspark-%3E%3D3.0-orange)](https://spark.apache.org/)

**Master PySpark with battle-tested tips, optimization techniques, and real-world big data examples.**

Transform your big data processing skills with comprehensive guides covering everything from basic operations to advanced performance optimization strategies.

> 🌐 **Looking for more resources?** Visit [DataLogicHub.com](https://www.datalogichub.com/) and [DataLogicHub.net](https://www.datalogichub.net/) for tutorials, articles, and data analytics insights!

---

## 📚 What's Inside

### 🎓 PySpark Tips & Tricks

10 comprehensive guides covering essential PySpark concepts and advanced techniques:

| Guide | Topics Covered | Skill Level |
|-------|----------------|-------------|
| [**01. DataFrame Basics & Selection**](guides/01_dataframe_basics.md) | Creating DataFrames, column selection, filtering, `select()`, `filter()`, `where()` | 🟢 |
| [**02. Transformations & Actions**](guides/02_transformations_actions.md) | Lazy evaluation, common transformations, actions, caching strategies | 🟢 |
| [**03. Aggregations & GroupBy**](guides/03_aggregations_groupby.md) | `groupBy()`, `agg()`, window functions, pivot tables | 🟡 |
| [**04. Joins & Unions**](guides/04_joins_unions.md) | Inner/outer joins, broadcast joins, handling skew, union operations | 🟡 |
| [**05. UDFs & Built-in Functions**](guides/05_udfs_functions.md) | User-defined functions, pandas UDFs, built-in functions, when/otherwise | 🟡 |
| [**06. Date & Time Operations**](guides/06_datetime_operations.md) | Date parsing, timestamps, windows, time zones, date arithmetic | 🟢 |
| [**07. String & Regex Operations**](guides/07_string_regex.md) | String functions, regex patterns, text processing, extraction | 🟢 |
| [**08. Performance Optimization**](guides/08_performance_tuning.md) | Partitioning, caching, broadcast variables, shuffle optimization | 🔴 |
| [**09. Data I/O & Formats**](guides/09_data_io_formats.md) | Reading/writing CSV, Parquet, JSON, Delta Lake, schema management | 🟡 |
| [**10. Debugging & Best Practices**](guides/10_debugging_best_practices.md) | Error handling, logging, testing, common pitfalls, code organization | 🟡 |

🟢 Beginner | 🟡 Intermediate | 🔴 Advanced

✨ **Each guide includes:**
- Quick reference tables
- Code examples with explanations
- Performance comparisons
- Common pitfalls and solutions
- Real-world use cases
- Memory and execution optimization tips

---

## 🚀 Quick Start

### Prerequisites

```powershell
# Install PySpark
pip install pyspark

# Optional: Install additional dependencies
pip install pandas pyarrow delta-spark
```

### Basic Usage

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, max

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("PySparkProTips") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# Read data
df = spark.read.csv("data.csv", header=True, inferSchema=True)

# Basic operations
result = df.filter(col("age") > 25) \
    .groupBy("department") \
    .agg(
        count("*").alias("count"),
        avg("salary").alias("avg_salary")
    ) \
    .orderBy(col("avg_salary").desc())

# Show results
result.show()
```

---

## 📖 Learning Path

### For Pandas Users

Transitioning from pandas to PySpark? Start here:

1. **[DataFrame Basics](guides/01_dataframe_basics.md)** - Learn PySpark equivalents to pandas operations
2. **[Transformations & Actions](guides/02_transformations_actions.md)** - Understand lazy evaluation
3. **[Aggregations & GroupBy](guides/03_aggregations_groupby.md)** - Master split-apply-combine in PySpark

### For Big Data Engineers

Optimizing large-scale data processing:

1. **[Performance Optimization](guides/08_performance_tuning.md)** - Partitioning, caching, and shuffle optimization
2. **[Joins & Unions](guides/04_joins_unions.md)** - Handle data skew and optimize join strategies
3. **[Data I/O & Formats](guides/09_data_io_formats.md)** - Choose the right file format

### For Data Scientists

Building ML pipelines and data analysis:

1. **[UDFs & Built-in Functions](guides/05_udfs_functions.md)** - Custom transformations
2. **[Date & Time Operations](guides/06_datetime_operations.md)** - Time series analysis
3. **[Debugging & Best Practices](guides/10_debugging_best_practices.md)** - Production-ready code

---

## 🎯 Key Features

### Pandas vs PySpark Quick Reference

| Operation | Pandas | PySpark |
|-----------|--------|---------|
| **Select columns** | `df[['col1', 'col2']]` | `df.select('col1', 'col2')` |
| **Filter rows** | `df[df['age'] > 25]` | `df.filter(col('age') > 25)` |
| **GroupBy** | `df.groupby('dept').agg(...)` | `df.groupBy('dept').agg(...)` |
| **Add column** | `df['new'] = df['a'] + df['b']` | `df.withColumn('new', col('a') + col('b'))` |
| **Sort** | `df.sort_values('col')` | `df.orderBy('col')` |
| **Drop nulls** | `df.dropna()` | `df.na.drop()` |

### Performance Tips at a Glance

- ✅ Use built-in functions instead of UDFs
- ✅ Partition data appropriately (200MB per partition)
- ✅ Cache DataFrames when reusing
- ✅ Use broadcast joins for small tables (<10MB)
- ✅ Avoid `collect()` on large datasets
- ✅ Use Parquet or Delta Lake for storage
- ❌ Don't use pandas UDFs for simple operations
- ❌ Avoid wide transformations when possible

---

## 🛠️ Utility Scripts

### Spark Session Configuration Helper

```python
from pyspark.sql import SparkSession

def create_optimized_spark_session(app_name: str, 
                                   memory: str = "4g",
                                   cores: str = "4"):
    """Create a Spark session with optimized configurations."""
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.executor.memory", memory) \
        .config("spark.executor.cores", cores) \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()
```

### DataFrame Profiler

```python
def profile_dataframe(df):
    """Generate a quick profile of a PySpark DataFrame."""
    print(f"Row count: {df.count():,}")
    print(f"Column count: {len(df.columns)}")
    print(f"\nSchema:")
    df.printSchema()
    print(f"\nSample data:")
    df.show(5, truncate=False)
    print(f"\nNull counts:")
    df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()
```

---

## 📊 Real-World Examples

### ETL Pipeline

```python
# Extract
raw_df = spark.read.parquet("s3://bucket/raw-data/")

# Transform
cleaned_df = raw_df \
    .filter(col("status") == "active") \
    .withColumn("processed_date", current_date()) \
    .withColumn("full_name", concat(col("first_name"), lit(" "), col("last_name"))) \
    .drop("temp_column")

# Load
cleaned_df.write \
    .mode("overwrite") \
    .partitionBy("year", "month") \
    .parquet("s3://bucket/processed-data/")
```

### Aggregation with Window Functions

```python
from pyspark.sql.window import Window

window_spec = Window.partitionBy("department").orderBy(col("salary").desc())

result = df.withColumn("rank", rank().over(window_spec)) \
    .withColumn("running_total", sum("salary").over(window_spec)) \
    .filter(col("rank") <= 3)
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [DataLogicHub.com](https://www.datalogichub.com/)
- [DataLogicHub.net](https://www.datalogichub.net/)

---

**Happy Sparking! ⚡**

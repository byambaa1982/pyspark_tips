# DataFrame Basics & Selection

Master the fundamentals of PySpark DataFrames with essential selection and filtering techniques.

---

## 🎯 Quick Reference

| Operation | PySpark | Pandas Equivalent |
|-----------|---------|-------------------|
| **Select columns** | `df.select('col1', 'col2')` | `df[['col1', 'col2']]` |
| **Select with expressions** | `df.select(col('age') + 1)` | `df['age'] + 1` |
| **Filter rows** | `df.filter(col('age') > 25)` | `df[df['age'] > 25]` |
| **Multiple conditions** | `df.filter((col('age') > 25) & (col('salary') > 50000))` | `df[(df['age'] > 25) & (df['salary'] > 50000)]` |
| **Select and filter** | `df.select('name').filter(col('age') > 25)` | `df.loc[df['age'] > 25, ['name']]` |

---

## 📚 Creating DataFrames

### From Python Lists

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = SparkSession.builder.appName("DataFrameBasics").getOrCreate()

# Simple creation
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, ["name", "age"])

# With explicit schema
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])
df = spark.createDataFrame(data, schema)
```

### From Pandas DataFrame

```python
import pandas as pd

pandas_df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})

spark_df = spark.createDataFrame(pandas_df)
```

### From Files

```python
# CSV
df = spark.read.csv("data.csv", header=True, inferSchema=True)

# Parquet
df = spark.read.parquet("data.parquet")

# JSON
df = spark.read.json("data.json")
```

---

## 💡 Selection Techniques

### Basic Column Selection

```python
from pyspark.sql.functions import col

# Select single column
df.select("name")
df.select(col("name"))

# Select multiple columns
df.select("name", "age", "salary")
df.select(["name", "age", "salary"])

# Select with column expressions
df.select(col("name"), col("age") + 1)
```

### Advanced Selection

```python
# Select all columns
df.select("*")

# Select all columns plus a new one
df.select("*", (col("age") + 1).alias("next_age"))

# Select columns by pattern
df.select([c for c in df.columns if c.startswith("sales_")])

# Select columns by type
from pyspark.sql.types import StringType
string_cols = [f.name for f in df.schema.fields if isinstance(f.dataType, StringType)]
df.select(string_cols)
```

### Column Operations

```python
from pyspark.sql.functions import lit, expr

# Add new column
df.withColumn("country", lit("USA"))
df.withColumn("age_plus_10", col("age") + 10)

# Rename columns
df.withColumnRenamed("old_name", "new_name")

# Drop columns
df.drop("column_to_remove")
df.drop("col1", "col2", "col3")

# Using SQL expressions
df.selectExpr("name", "age", "age + 10 as age_plus_10")
```

---

## 🔍 Filtering Techniques

### Basic Filtering

```python
# Using filter()
df.filter(col("age") > 25)
df.filter("age > 25")  # SQL-style string

# Using where() (alias for filter)
df.where(col("age") > 25)

# Multiple conditions with AND
df.filter((col("age") > 25) & (col("salary") > 50000))

# Multiple conditions with OR
df.filter((col("age") < 25) | (col("age") > 60))

# NOT condition
df.filter(~(col("status") == "inactive"))
```

### Advanced Filtering

```python
from pyspark.sql.functions import isin, isnan, isnull, when

# Check if value in list
df.filter(col("country").isin(["USA", "UK", "Canada"]))

# String operations
df.filter(col("name").startswith("A"))
df.filter(col("email").endswith("@gmail.com"))
df.filter(col("description").contains("important"))

# Null handling
df.filter(col("age").isNull())
df.filter(col("age").isNotNull())

# Between values
df.filter(col("age").between(25, 35))

# Regex matching
df.filter(col("email").rlike(r"^[\w\.-]+@[\w\.-]+\.\w+$"))
```

### Complex Filtering

```python
# Combining multiple filters
df.filter(col("age") > 25) \
  .filter(col("salary") > 50000) \
  .filter(col("department").isin(["Engineering", "Sales"]))

# Using SQL expression
df.filter("age > 25 AND salary > 50000 AND department IN ('Engineering', 'Sales')")

# Conditional filtering with when/otherwise
df.withColumn("age_category", 
    when(col("age") < 18, "Minor")
    .when(col("age") < 65, "Adult")
    .otherwise("Senior")
)
```

---

## 🎓 Best Practices

### ✅ DO

```python
# Use Column objects for complex operations
from pyspark.sql.functions import col
df.filter(col("age") > 25)

# Chain operations for readability
result = df.select("name", "age") \
    .filter(col("age") > 25) \
    .orderBy("age")

# Use explicit column references
df.select(df["name"], df["age"])

# Cache when reusing DataFrames
df.cache()
result1 = df.filter(col("age") > 25)
result2 = df.filter(col("salary") > 50000)
```

### ❌ DON'T

```python
# Don't use collect() unnecessarily
rows = df.collect()  # Brings all data to driver!

# Don't iterate row by row
for row in df.collect():  # Inefficient!
    process(row)

# Don't use nested for loops
# Instead, use DataFrame operations

# Don't forget to use parentheses with multiple conditions
df.filter(col("age") > 25 & col("salary") > 50000)  # Wrong!
df.filter((col("age") > 25) & (col("salary") > 50000))  # Correct!
```

---

## 📊 Common Patterns

### Pattern 1: Select and Filter

```python
# Get names of high earners in Engineering
result = df.select("name", "salary", "department") \
    .filter((col("department") == "Engineering") & (col("salary") > 100000))
```

### Pattern 2: Conditional Column Creation

```python
# Create salary category
df.withColumn("salary_category",
    when(col("salary") < 50000, "Low")
    .when(col("salary") < 100000, "Medium")
    .otherwise("High")
)
```

### Pattern 3: Dynamic Column Selection

```python
# Select columns based on condition
numeric_cols = [f.name for f in df.schema.fields 
                if f.dataType in [IntegerType(), LongType(), DoubleType()]]
df.select(numeric_cols)
```

### Pattern 4: Null Handling

```python
# Filter out rows with any null
df.na.drop()

# Filter out rows with null in specific columns
df.na.drop(subset=["age", "salary"])

# Fill nulls with default values
df.na.fill({"age": 0, "name": "Unknown"})
```

---

## 🚀 Performance Tips

1. **Use Column objects for complex operations** - More efficient than string references
2. **Filter early** - Reduce data size as soon as possible
3. **Select only needed columns** - Don't select * if you don't need all columns
4. **Use built-in functions** - Always prefer built-in over UDFs
5. **Cache strategically** - Cache DataFrames that are reused multiple times

---

## 🔗 Related Guides

- [02. Transformations & Actions](02_transformations_actions.md)
- [03. Aggregations & GroupBy](03_aggregations_groupby.md)
- [08. Performance Optimization](08_performance_tuning.md)

---

## 📚 Additional Resources

- [PySpark SQL Functions Documentation](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)
- [DataFrame API Reference](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html)

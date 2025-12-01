"""useful_pyspark.utilities

Production-ready utilities for common PySpark operations and optimizations.
Includes helper functions for session creation, DataFrame profiling, and
performance optimization.

✨ Features:
- Optimized Spark session creation with best practices
- DataFrame profiling and data quality checks
- Performance monitoring utilities
- Common transformation helpers
- Schema validation tools

📖 Example usage:

    from utilities import create_spark_session, profile_dataframe
    
    # Create optimized Spark session
    spark = create_spark_session("MyApp", memory="8g", cores="4")
    
    # Read and profile data
    df = spark.read.parquet("data.parquet")
    profile_dataframe(df)
    
    # Apply optimizations
    df_optimized = optimize_partitions(df, target_size_mb=128)

Author: Byamba Enkhbat
License: MIT
"""

from typing import Dict, List, Optional, Union
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, count, when, isnull, sum as _sum
from pyspark import StorageLevel
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_spark_session(
    app_name: str,
    memory: str = "4g",
    cores: str = "4",
    enable_aqe: bool = True,
    shuffle_partitions: int = 200
) -> SparkSession:
    """Create an optimized Spark session with best practice configurations.
    
    This function creates a Spark session with sensible defaults and
    performance optimizations enabled.
    
    Args:
        app_name: Name of the Spark application
        memory: Executor memory (e.g., "4g", "8g")
        cores: Number of executor cores
        enable_aqe: Enable Adaptive Query Execution (Spark 3.0+)
        shuffle_partitions: Number of partitions for shuffle operations
    
    Returns:
        Configured SparkSession instance
    
    Example:
        >>> spark = create_spark_session("MyApp", memory="8g", cores="4")
        >>> df = spark.read.parquet("data.parquet")
    """
    logger.info(f"Creating Spark session: {app_name}")
    
    builder = SparkSession.builder \
        .appName(app_name) \
        .config("spark.executor.memory", memory) \
        .config("spark.executor.cores", cores) \
        .config("spark.sql.shuffle.partitions", str(shuffle_partitions)) \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    
    if enable_aqe:
        builder = builder \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.sql.adaptive.skewJoin.enabled", "true")
    
    spark = builder.getOrCreate()
    
    logger.info(f"Spark session created successfully")
    logger.info(f"Spark version: {spark.version}")
    
    return spark


def profile_dataframe(df: DataFrame, show_sample: bool = True) -> Dict:
    """Generate a comprehensive profile of a PySpark DataFrame.
    
    Provides statistics about the DataFrame including row count, column count,
    null counts, data types, and sample data.
    
    Args:
        df: DataFrame to profile
        show_sample: Whether to display sample data
    
    Returns:
        Dictionary containing profile statistics
    
    Example:
        >>> stats = profile_dataframe(df)
        >>> print(f"Total rows: {stats['row_count']}")
    """
    logger.info("Profiling DataFrame...")
    
    row_count = df.count()
    column_count = len(df.columns)
    partition_count = df.rdd.getNumPartitions()
    
    print(f"\n{'='*60}")
    print(f"DataFrame Profile")
    print(f"{'='*60}")
    print(f"Row count:       {row_count:,}")
    print(f"Column count:    {column_count}")
    print(f"Partition count: {partition_count}")
    print(f"\n{'Schema:':-^60}")
    df.printSchema()
    
    # Null counts
    print(f"\n{'Null Counts:':-^60}")
    null_counts = df.select([
        count(when(col(c).isNull(), c)).alias(c)
        for c in df.columns
    ])
    null_counts.show()
    
    # Sample data
    if show_sample:
        print(f"\n{'Sample Data (5 rows):':-^60}")
        df.show(5, truncate=False)
    
    # Data distribution across partitions
    partition_sizes = df.rdd.glom().map(len).collect()
    print(f"\n{'Partition Distribution:':-^60}")
    print(f"Min partition size:  {min(partition_sizes):,}")
    print(f"Max partition size:  {max(partition_sizes):,}")
    print(f"Avg partition size:  {sum(partition_sizes)//len(partition_sizes):,}")
    print(f"{'='*60}\n")
    
    return {
        'row_count': row_count,
        'column_count': column_count,
        'partition_count': partition_count,
        'partition_sizes': partition_sizes
    }


def check_data_quality(df: DataFrame, required_columns: Optional[List[str]] = None) -> Dict:
    """Perform data quality checks on a DataFrame.
    
    Checks for null values, duplicates, and validates required columns.
    
    Args:
        df: DataFrame to check
        required_columns: List of columns that must exist
    
    Returns:
        Dictionary with quality metrics
    
    Example:
        >>> quality = check_data_quality(df, required_columns=['id', 'name'])
        >>> if quality['has_nulls']:
        >>>     print("Warning: DataFrame contains null values")
    """
    logger.info("Checking data quality...")
    
    results = {
        'total_rows': df.count(),
        'has_nulls': False,
        'null_columns': [],
        'duplicate_count': 0,
        'missing_columns': []
    }
    
    # Check required columns
    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            results['missing_columns'] = list(missing)
            logger.warning(f"Missing required columns: {missing}")
    
    # Check for nulls
    null_counts = df.select([
        count(when(col(c).isNull(), c)).alias(c)
        for c in df.columns
    ]).collect()[0].asDict()
    
    for col_name, null_count in null_counts.items():
        if null_count > 0:
            results['has_nulls'] = True
            results['null_columns'].append({
                'column': col_name,
                'null_count': null_count,
                'null_percentage': (null_count / results['total_rows']) * 100
            })
    
    # Check for duplicates
    duplicate_count = df.count() - df.dropDuplicates().count()
    results['duplicate_count'] = duplicate_count
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Data Quality Report")
    print(f"{'='*60}")
    print(f"Total rows: {results['total_rows']:,}")
    print(f"Duplicate rows: {duplicate_count:,}")
    print(f"Columns with nulls: {len(results['null_columns'])}")
    
    if results['null_columns']:
        print(f"\n{'Null Summary:':-^60}")
        for null_info in results['null_columns']:
            print(f"  {null_info['column']}: {null_info['null_count']:,} "
                  f"({null_info['null_percentage']:.2f}%)")
    
    print(f"{'='*60}\n")
    
    return results


def optimize_partitions(df: DataFrame, target_size_mb: int = 128) -> DataFrame:
    """Optimize DataFrame partitioning based on data size.
    
    Automatically determines optimal partition count based on DataFrame size
    and target partition size.
    
    Args:
        df: DataFrame to optimize
        target_size_mb: Target size per partition in MB
    
    Returns:
        Repartitioned DataFrame
    
    Example:
        >>> df_optimized = optimize_partitions(df, target_size_mb=128)
    """
    logger.info("Optimizing partitions...")
    
    # Estimate DataFrame size (rough estimate)
    sample_size = df.sample(0.01).cache()
    sample_count = sample_size.count()
    
    if sample_count == 0:
        logger.warning("Empty sample, using default partitioning")
        return df
    
    total_count = df.count()
    
    # Rough size estimation based on sample
    # This is a simplified estimation
    estimated_size_mb = (total_count / sample_count) * 10  # Rough estimate
    
    optimal_partitions = max(1, int(estimated_size_mb / target_size_mb))
    current_partitions = df.rdd.getNumPartitions()
    
    logger.info(f"Current partitions: {current_partitions}")
    logger.info(f"Optimal partitions: {optimal_partitions}")
    
    if optimal_partitions < current_partitions:
        logger.info(f"Coalescing to {optimal_partitions} partitions")
        return df.coalesce(optimal_partitions)
    elif optimal_partitions > current_partitions:
        logger.info(f"Repartitioning to {optimal_partitions} partitions")
        return df.repartition(optimal_partitions)
    
    logger.info("Partitioning already optimal")
    return df


def cache_if_reused(df: DataFrame, reuse_count: int = 2) -> DataFrame:
    """Cache DataFrame if it will be reused multiple times.
    
    Args:
        df: DataFrame to potentially cache
        reuse_count: Number of times DataFrame will be reused
    
    Returns:
        Cached DataFrame if reuse_count > 1, otherwise original DataFrame
    
    Example:
        >>> df_cached = cache_if_reused(df, reuse_count=3)
        >>> result1 = df_cached.filter(col("status") == "active").count()
        >>> result2 = df_cached.groupBy("category").count()
    """
    if reuse_count > 1:
        logger.info(f"Caching DataFrame (will be reused {reuse_count} times)")
        return df.persist(StorageLevel.MEMORY_AND_DISK)
    return df


def safely_collect(df: DataFrame, limit: int = 10000) -> List:
    """Safely collect DataFrame rows with a limit to prevent memory issues.
    
    Args:
        df: DataFrame to collect
        limit: Maximum number of rows to collect
    
    Returns:
        List of rows (up to limit)
    
    Example:
        >>> rows = safely_collect(df, limit=1000)
        >>> for row in rows:
        >>>     print(row)
    """
    row_count = df.count()
    
    if row_count > limit:
        logger.warning(f"DataFrame has {row_count:,} rows, collecting only {limit:,}")
        return df.limit(limit).collect()
    
    logger.info(f"Collecting {row_count:,} rows")
    return df.collect()


def write_with_validation(
    df: DataFrame,
    path: str,
    format: str = "parquet",
    mode: str = "overwrite",
    partition_by: Optional[List[str]] = None
) -> bool:
    """Write DataFrame with validation and error handling.
    
    Args:
        df: DataFrame to write
        path: Output path
        format: Output format (parquet, csv, json, etc.)
        mode: Write mode (overwrite, append, etc.)
        partition_by: Columns to partition by
    
    Returns:
        True if successful, False otherwise
    
    Example:
        >>> success = write_with_validation(
        >>>     df, "output.parquet", 
        >>>     format="parquet",
        >>>     partition_by=["year", "month"]
        >>> )
    """
    try:
        logger.info(f"Writing DataFrame to {path}")
        logger.info(f"Format: {format}, Mode: {mode}")
        
        writer = df.write.mode(mode)
        
        if partition_by:
            logger.info(f"Partitioning by: {partition_by}")
            writer = writer.partitionBy(*partition_by)
        
        if format == "parquet":
            writer.option("compression", "snappy")
        
        getattr(writer, format)(path)
        
        logger.info("Write successful")
        return True
        
    except Exception as e:
        logger.error(f"Write failed: {str(e)}")
        return False


# Example usage
if __name__ == "__main__":
    # Create Spark session
    spark = create_spark_session("UtilitiesExample", memory="4g")
    
    # Create sample DataFrame
    data = [
        (1, "Alice", 25, "Engineering"),
        (2, "Bob", 30, "Sales"),
        (3, "Charlie", 35, "Engineering"),
        (4, None, 28, "Marketing"),
        (5, "Eve", None, "Sales")
    ]
    
    df = spark.createDataFrame(data, ["id", "name", "age", "department"])
    
    # Profile DataFrame
    stats = profile_dataframe(df)
    
    # Check data quality
    quality = check_data_quality(df, required_columns=["id", "name", "age"])
    
    # Optimize and write
    df_optimized = optimize_partitions(df)
    write_with_validation(df_optimized, "output.parquet", partition_by=["department"])
    
    spark.stop()

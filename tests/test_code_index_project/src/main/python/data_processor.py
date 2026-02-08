#!/usr/bin/env python3
"""
数据处理脚本
用于处理和分析用户数据
"""

import json
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Union, Callable
import logging
import asyncio
import threading
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import functools
from collections import defaultdict, namedtuple
import re
import datetime
import random
import math


# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 自定义异常
class DataProcessingError(Exception):
    """数据处理异常"""
    pass


class ValidationError(DataProcessingError):
    """验证错误"""
    pass


class ProcessingTimeoutError(DataProcessingError):
    """处理超时错误"""
    pass


# 数据类
@dataclass
class UserData:
    """用户数据类"""
    id: str
    name: str
    email: str
    age: Optional[int] = None
    department: str = "general"
    skills: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    def validate(self) -> None:
        """验证用户数据"""
        if not self.id:
            raise ValidationError("ID cannot be empty")
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', self.email):
            raise ValidationError("Invalid email format")
        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValidationError("Invalid age")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'department': self.department,
            'skills': self.skills,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


@dataclass
class ProcessingResult:
    """处理结果类"""
    success: bool
    data: Optional[pd.DataFrame] = None
    errors: List[str] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)
    processing_time: float = 0.0


# 抽象基类
class DataTransformer(ABC):
    """数据转换器抽象基类"""

    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """转换数据"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """获取转换器名称"""
        pass


class EmailNormalizer(DataTransformer):
    """邮箱标准化转换器"""

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """标准化邮箱地址"""
        data = data.copy()
        data['email'] = data['email'].str.lower().str.strip()
        return data

    def get_name(self) -> str:
        return "Email Normalizer"


class AgeCategorizer(DataTransformer):
    """年龄分类转换器"""

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """添加年龄分类"""
        data = data.copy()
        conditions = [
            (data['age'] < 18),
            (data['age'] >= 18) & (data['age'] < 30),
            (data['age'] >= 30) & (data['age'] < 50),
            (data['age'] >= 50)
        ]
        choices = ['minor', 'young_adult', 'adult', 'senior']
        data['age_category'] = np.select(conditions, choices, default='unknown')
        return data

    def get_name(self) -> str:
        return "Age Categorizer"


class SkillAnalyzer(DataTransformer):
    """技能分析转换器"""

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """分析技能"""
        data = data.copy()
        data['skill_count'] = data['skills'].apply(len)
        data['has_python'] = data['skills'].apply(lambda x: 'python' in [s.lower() for s in x])
        data['has_java'] = data['skills'].apply(lambda x: 'java' in [s.lower() for s in x])
        return data

    def get_name(self) -> str:
        return "Skill Analyzer"


# 装饰器
def timing_decorator(func: Callable) -> Callable:
    """计时装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"{func.__name__} took {duration:.2f} seconds")
        return result
    return wrapper


def retry_decorator(max_retries: int = 3, delay: float = 1.0) -> Callable:
    """重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay * (2 ** attempt))  # 指数退避
            return None
        return wrapper
    return decorator


# 枚举
class ProcessingMode:
    SYNC = "sync"
    ASYNC = "async"
    PARALLEL = "parallel"


class DataFormat:
    JSON = "json"
    CSV = "csv"
    XML = "xml"


# 命名元组
Point = namedtuple('Point', ['x', 'y'])
Stats = namedtuple('Stats', ['mean', 'median', 'std', 'min', 'max'])


class DataProcessor:
    """数据处理器类"""

    def __init__(self, mode: str = ProcessingMode.SYNC):
        self.data: List[Dict[str, Any]] = []
        self.transformers: List[DataTransformer] = []
        self.mode = mode
        self.cache: Dict[str, Any] = {}
        self.lock = threading.Lock()

    def add_transformer(self, transformer: DataTransformer) -> None:
        """添加转换器"""
        self.transformers.append(transformer)

    @retry_decorator(max_retries=3)
    def load_data(self, file_path: str, format_type: str = DataFormat.JSON) -> None:
        """从文件加载数据"""
        try:
            if format_type == DataFormat.JSON:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            elif format_type == DataFormat.CSV:
                df = pd.read_csv(file_path)
                self.data = df.to_dict('records')
            else:
                raise ValueError(f"Unsupported format: {format_type}")
            logger.info(f"Loaded {len(self.data)} records from {file_path}")
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise DataProcessingError(f"Data loading failed: {e}")

    @timing_decorator
    def process_data(self) -> pd.DataFrame:
        """处理数据并返回DataFrame"""
        if not self.data:
            raise DataProcessingError("No data loaded")

        df = pd.DataFrame(self.data)

        # 应用所有转换器
        for transformer in self.transformers:
            logger.info(f"Applying transformer: {transformer.get_name()}")
            df = transformer.transform(df)

        # 额外的复杂处理
        df = self._add_complex_calculations(df)
        df = self._add_text_analysis(df)
        df = self._add_statistical_features(df)

        return df

    def _add_complex_calculations(self, df: pd.DataFrame) -> pd.DataFrame:
        """添加复杂计算"""
        df = df.copy()

        # 计算年龄的复杂函数
        df['age_squared'] = df['age'] ** 2
        df['age_log'] = np.log(df['age'] + 1)  # 加1避免log(0)
        df['age_sqrt'] = np.sqrt(df['age'])

        # 字符串处理
        df['name_length'] = df['name'].str.len()
        df['name_initials'] = df['name'].apply(lambda x: ''.join([word[0] for word in x.split() if word]))

        # 日期处理
        df['days_since_creation'] = (pd.Timestamp.now() - pd.to_datetime(df['created_at'])).dt.days

        return df

    def _add_text_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """添加文本分析"""
        df = df.copy()

        # 邮箱域名分析
        df['email_domain'] = df['email'].str.split('@').str[1]
        df['domain_popularity'] = df.groupby('email_domain')['email_domain'].transform('count')

        # 技能分析
        df['skill_diversity'] = df['skills'].apply(lambda x: len(set(x)) / len(x) if x else 0)
        df['has_technical_skills'] = df['skills'].apply(
            lambda x: any(skill.lower() in ['python', 'java', 'javascript', 'c++', 'sql'] for skill in x)
        )

        # 名称分析
        df['name_words'] = df['name'].str.split().str.len()
        df['has_middle_name'] = df['name_words'] > 2

        return df

    def _add_statistical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """添加统计特征"""
        df = df.copy()

        # 数值列的统计
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[f'{col}_zscore'] = (df[col] - df[col].mean()) / df[col].std()
            df[f'{col}_percentile'] = df[col].rank(pct=True)

        # 分组统计
        dept_stats = df.groupby('department')['age'].agg(['mean', 'std', 'count'])
        dept_stats.columns = ['dept_age_mean', 'dept_age_std', 'dept_count']
        df = df.merge(dept_stats, left_on='department', right_index=True, how='left')

        return df

    def calculate_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """计算基本统计信息"""
        stats = {
            'total_users': len(df),
            'unique_domains': df['email_domain'].nunique() if 'email_domain' in df.columns else 0,
            'avg_name_length': df['name'].str.len().mean(),
            'avg_age': df['age'].mean(),
            'age_std': df['age'].std(),
            'skill_distribution': df['skill_count'].value_counts().to_dict() if 'skill_count' in df.columns else {},
            'department_distribution': df['department'].value_counts().to_dict(),
            'technical_skill_ratio': df['has_technical_skills'].mean() if 'has_technical_skills' in df.columns else 0,
            'age_categories': df['age_category'].value_counts().to_dict() if 'age_category' in df.columns else {}
        }

        # 更复杂的统计
        if 'age' in df.columns:
            stats['age_quartiles'] = df['age'].quantile([0.25, 0.5, 0.75]).to_dict()
            stats['age_skewness'] = df['age'].skew()
            stats['age_kurtosis'] = df['age'].kurtosis()

        if 'name_length' in df.columns:
            stats['name_length_stats'] = Stats(
                mean=df['name_length'].mean(),
                median=df['name_length'].median(),
                std=df['name_length'].std(),
                min=df['name_length'].min(),
                max=df['name_length'].max()
            )

        return stats

    @timing_decorator
    def save_processed_data(self, df: pd.DataFrame, output_path: str, format_type: str = DataFormat.CSV) -> None:
        """保存处理后的数据"""
        try:
            if format_type == DataFormat.CSV:
                df.to_csv(output_path, index=False)
            elif format_type == DataFormat.JSON:
                df.to_json(output_path, orient='records', indent=2)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
            logger.info(f"Data saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
            raise DataProcessingError(f"Data saving failed: {e}")

    async def process_async(self) -> ProcessingResult:
        """异步处理数据"""
        start_time = datetime.datetime.now()

        try:
            # 模拟异步操作
            await asyncio.sleep(0.1)
            df = self.process_data()
            stats = self.calculate_stats(df)

            end_time = datetime.datetime.now()
            processing_time = (end_time - start_time).total_seconds()

            return ProcessingResult(
                success=True,
                data=df,
                stats=stats,
                processing_time=processing_time
            )
        except Exception as e:
            end_time = datetime.datetime.now()
            processing_time = (end_time - start_time).total_seconds()

            return ProcessingResult(
                success=False,
                errors=[str(e)],
                processing_time=processing_time
            )

    def process_parallel(self, num_workers: int = 4) -> ProcessingResult:
        """并行处理数据"""
        start_time = datetime.datetime.now()

        try:
            # 这里简化并行处理，实际可以分割数据
            results = []
            chunk_size = max(1, len(self.data) // num_workers)

            def worker(chunk):
                processor = DataProcessor()
                processor.data = chunk
                return processor.process_data()

            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = []
                for i in range(0, len(self.data), chunk_size):
                    chunk = self.data[i:i + chunk_size]
                    future = executor.submit(worker, chunk)
                    futures.append(future)

                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())

            # 合并结果
            combined_df = pd.concat(results, ignore_index=True)
            stats = self.calculate_stats(combined_df)

            end_time = datetime.datetime.now()
            processing_time = (end_time - start_time).total_seconds()

            return ProcessingResult(
                success=True,
                data=combined_df,
                stats=stats,
                processing_time=processing_time
            )
        except Exception as e:
            end_time = datetime.datetime.now()
            processing_time = (end_time - start_time).total_seconds()

            return ProcessingResult(
                success=False,
                errors=[str(e)],
                processing_time=processing_time
            )


# 工厂函数
def create_data_processor(mode: str = ProcessingMode.SYNC) -> DataProcessor:
    """创建数据处理器工厂函数"""
    processor = DataProcessor(mode)

    # 添加默认转换器
    processor.add_transformer(EmailNormalizer())
    processor.add_transformer(AgeCategorizer())
    processor.add_transformer(SkillAnalyzer())

    return processor


# 上下文管理器
class DataProcessingContext:
    """数据处理上下文管理器"""

    def __init__(self, processor: DataProcessor):
        self.processor = processor

    def __enter__(self):
        logger.info("Entering data processing context")
        return self.processor

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("Exiting data processing context")
        if exc_type:
            logger.error(f"Error in context: {exc_val}")
        return False


# 生成器函数
def data_stream_generator(file_path: str) -> Any:
    """数据流生成器"""
    with open(file_path, 'r') as f:
        for line in f:
            yield json.loads(line.strip())


def fibonacci_generator(n: int) -> Any:
    """斐波那契数列生成器"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


# 高级函数
def compose_transformers(*transformers: DataTransformer) -> Callable[[pd.DataFrame], pd.DataFrame]:
    """组合转换器的高阶函数"""
    def composed(df: pd.DataFrame) -> pd.DataFrame:
        for transformer in transformers:
            df = transformer.transform(df)
        return df
    return composed


def memoize(func: Callable) -> Callable:
    """记忆化装饰器"""
    cache = {}

    @functools.wraps(func)
    def memoized(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized


@memoize
def expensive_calculation(x: int) -> int:
    """模拟 expensive 计算"""
    time.sleep(0.1)  # 模拟延迟
    return x ** 2 + math.sqrt(x)


# 更多类
class DataValidator:
    """数据验证器"""

    def __init__(self, rules: Dict[str, Callable] = None):
        self.rules = rules or self._default_rules()

    def _default_rules(self) -> Dict[str, Callable]:
        return {
            'id': lambda x: isinstance(x, str) and len(x) > 0,
            'name': lambda x: isinstance(x, str) and len(x) >= 2,
            'email': lambda x: re.match(r'^[^@]+@[^@]+\.[^@]+$', x) is not None,
            'age': lambda x: isinstance(x, int) and 0 <= x <= 150
        }

    def validate_record(self, record: Dict[str, Any]) -> List[str]:
        """验证单条记录"""
        errors = []
        for field, validator in self.rules.items():
            if field in record:
                try:
                    if not validator(record[field]):
                        errors.append(f"Invalid {field}: {record[field]}")
                except Exception as e:
                    errors.append(f"Validation error for {field}: {e}")
        return errors

    def validate_dataset(self, data: List[Dict[str, Any]]) -> Dict[int, List[str]]:
        """验证整个数据集"""
        return {i: self.validate_record(record) for i, record in enumerate(data)}


class ReportGenerator:
    """报告生成器"""

    def __init__(self, template: str = None):
        self.template = template or self._default_template()

    def _default_template(self) -> str:
        return """
Data Processing Report
======================

Total Records: {total_users}
Processing Time: {processing_time:.2f} seconds
Success Rate: {success_rate:.2%}

Statistics:
- Average Age: {avg_age:.1f}
- Unique Email Domains: {unique_domains}
- Technical Skill Ratio: {technical_skill_ratio:.2%}

Age Distribution:
{age_distribution}

Department Distribution:
{department_distribution}

Top Skills:
{top_skills}
"""

    def generate_report(self, result: ProcessingResult) -> str:
        """生成报告"""
        if not result.success:
            return f"Processing failed: {'; '.join(result.errors)}"

        stats = result.stats
        age_dist = "\n".join([f"  {k}: {v}" for k, v in stats.get('age_categories', {}).items()])
        dept_dist = "\n".join([f"  {k}: {v}" for k, v in stats.get('department_distribution', {}).items()])

        # 模拟 top skills
        top_skills = "  - Python\n  - Java\n  - JavaScript\n  - SQL"

        return self.template.format(
            total_users=stats.get('total_users', 0),
            processing_time=result.processing_time,
            success_rate=1.0,  # 假设成功
            avg_age=stats.get('avg_age', 0),
            unique_domains=stats.get('unique_domains', 0),
            technical_skill_ratio=stats.get('technical_skill_ratio', 0),
            age_distribution=age_dist,
            department_distribution=dept_dist,
            top_skills=top_skills
        )


# 导入缺失的模块
import time
import concurrent.futures


def main():
    """主函数"""
    logger.info("Starting data processing application")

    processor = create_data_processor()

    # 示例数据
    sample_data = [
        {"id": "1", "name": "Alice Johnson", "email": "alice@example.com", "age": 28, "department": "engineering", "skills": ["python", "java", "sql"]},
        {"id": "2", "name": "Bob Smith", "email": "bob@example.com", "age": 35, "department": "marketing", "skills": ["marketing", "analytics"]},
        {"id": "3", "name": "Charlie Brown", "email": "charlie@test.com", "age": 42, "department": "engineering", "skills": ["c++", "python", "machine learning"]},
        {"id": "4", "name": "Diana Prince", "email": "diana@wonder.com", "age": 30, "department": "hr", "skills": ["communication", "leadership"]},
        {"id": "5", "name": "Eve Adams", "email": "eve@secure.org", "age": 26, "department": "security", "skills": ["cryptography", "python", "networking"]},
        {"id": "6", "name": "Frank Miller", "email": "frank@art.com", "age": 55, "department": "design", "skills": ["photoshop", "illustrator", "creativity"]},
        {"id": "7", "name": "Grace Hopper", "email": "grace@tech.com", "age": 85, "department": "engineering", "skills": ["cobol", "fortran", "compilers"]},
        {"id": "8", "name": "Henry Ford", "email": "henry@auto.com", "age": 78, "department": "manufacturing", "skills": ["engineering", "business", "innovation"]},
        {"id": "9", "name": "Ivy League", "email": "ivy@univ.edu", "age": 22, "department": "education", "skills": ["teaching", "research", "python"]},
        {"id": "10", "name": "Jack Sparrow", "email": "jack@pirate.com", "age": 45, "department": "adventure", "skills": ["sailing", "swordsmanship", "treasure hunting"]}
    ]

    # 保存示例数据到临时文件
    with open('temp_data.json', 'w') as f:
        json.dump(sample_data, f)

    # 加载和处理数据
    processor.load_data('temp_data.json')
    df = processor.process_data()

    print("Processed Data (first 5 rows):")
    print(df.head())

    stats = processor.calculate_stats(df)
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")

    # 生成报告
    result = ProcessingResult(success=True, data=df, stats=stats, processing_time=1.5)
    report_gen = ReportGenerator()
    report = report_gen.generate_report(result)
    print("\nReport:")
    print(report)

    # 保存结果
    processor.save_processed_data(df, 'processed_users.csv')
    print("\nProcessed data saved to processed_users.csv")

    # 测试异步处理
    async def test_async():
        result = await processor.process_async()
        print(f"Async processing took {result.processing_time:.2f} seconds")

    asyncio.run(test_async())

    logger.info("Data processing application completed")


if __name__ == "__main__":
    main()
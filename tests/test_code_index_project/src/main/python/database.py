#!/usr/bin/env python3
"""
数据库管理模块
提供数据库连接、查询、事务管理等功能
"""

import sqlite3
import psycopg2
import mysql.connector
from typing import List, Dict, Any, Optional, Union
from contextlib import contextmanager
from dataclasses import dataclass
import logging
import time
import json
from abc import ABC, abstractmethod
from enum import Enum

logger = logging.getLogger(__name__)


class DatabaseType(Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"


@dataclass
class DatabaseConfig:
    """数据库配置"""
    db_type: DatabaseType
    host: str = "localhost"
    port: Optional[int] = None
    database: str = ""
    username: str = ""
    password: str = ""
    connection_pool_size: int = 10
    connection_timeout: int = 30
    max_retries: int = 3


class DatabaseConnectionError(Exception):
    """数据库连接异常"""
    pass


class DatabaseQueryError(Exception):
    """数据库查询异常"""
    pass


class DatabaseManager(ABC):
    """数据库管理器抽象基类"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._connection_pool = []
        self._active_connections = 0

    @abstractmethod
    def connect(self):
        """建立连接"""
        pass

    @abstractmethod
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """执行查询"""
        pass

    @abstractmethod
    def execute_update(self, query: str, params: tuple = None) -> int:
        """执行更新"""
        pass

    @abstractmethod
    def create_tables(self):
        """创建表"""
        pass

    def get_connection(self):
        """获取连接"""
        if self._connection_pool:
            return self._connection_pool.pop()
        return self.connect()

    def return_connection(self, conn):
        """归还连接"""
        if len(self._connection_pool) < self.config.connection_pool_size:
            self._connection_pool.append(conn)
        else:
            conn.close()

    @contextmanager
    def transaction(self):
        """事务上下文管理器"""
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.return_connection(conn)


class SQLiteManager(DatabaseManager):
    """SQLite 数据库管理器"""

    def connect(self):
        try:
            conn = sqlite3.connect(
                self.config.database,
                timeout=self.config.connection_timeout
            )
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"SQLite connection failed: {e}")

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            raise DatabaseQueryError(f"SQLite query failed: {e}")
        finally:
            self.return_connection(conn)

    def execute_update(self, query: str, params: tuple = None) -> int:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            conn.rollback()
            raise DatabaseQueryError(f"SQLite update failed: {e}")
        finally:
            self.return_connection(conn)

    def create_tables(self):
        """创建 SQLite 表"""
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            department TEXT,
            skills TEXT,  -- JSON string
            metadata TEXT, -- JSON string
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        create_activities_table = """
        CREATE TABLE IF NOT EXISTS user_activities (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            description TEXT,
            details TEXT, -- JSON string
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """

        create_audit_log_table = """
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT NOT NULL,
            user_id TEXT,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        with self.transaction() as conn:
            conn.execute(create_users_table)
            conn.execute(create_activities_table)
            conn.execute(create_audit_log_table)


class PostgreSQLManager(DatabaseManager):
    """PostgreSQL 数据库管理器"""

    def connect(self):
        try:
            conn = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
                connect_timeout=self.config.connection_timeout
            )
            return conn
        except psycopg2.Error as e:
            raise DatabaseConnectionError(f"PostgreSQL connection failed: {e}")

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        except psycopg2.Error as e:
            raise DatabaseQueryError(f"PostgreSQL query failed: {e}")
        finally:
            self.return_connection(conn)

    def execute_update(self, query: str, params: tuple = None) -> int:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.rowcount
        except psycopg2.Error as e:
            conn.rollback()
            raise DatabaseQueryError(f"PostgreSQL update failed: {e}")
        finally:
            self.return_connection(conn)

    def create_tables(self):
        """创建 PostgreSQL 表"""
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            age INTEGER,
            department VARCHAR(255),
            skills JSONB,
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        create_activities_table = """
        CREATE TABLE IF NOT EXISTS user_activities (
            id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL REFERENCES users(id),
            activity_type VARCHAR(255) NOT NULL,
            description TEXT,
            details JSONB,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        create_audit_log_table = """
        CREATE TABLE IF NOT EXISTS audit_log (
            id SERIAL PRIMARY KEY,
            operation VARCHAR(255) NOT NULL,
            user_id VARCHAR(255),
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(create_users_table)
            cursor.execute(create_activities_table)
            cursor.execute(create_audit_log_table)
            conn.commit()


class MySQLManager(DatabaseManager):
    """MySQL 数据库管理器"""

    def connect(self):
        try:
            conn = mysql.connector.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
                connection_timeout=self.config.connection_timeout
            )
            return conn
        except mysql.connector.Error as e:
            raise DatabaseConnectionError(f"MySQL connection failed: {e}")

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            return rows
        except mysql.connector.Error as e:
            raise DatabaseQueryError(f"MySQL query failed: {e}")
        finally:
            self.return_connection(conn)

    def execute_update(self, query: str, params: tuple = None) -> int:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.rowcount
        except mysql.connector.Error as e:
            conn.rollback()
            raise DatabaseQueryError(f"MySQL update failed: {e}")
        finally:
            self.return_connection(conn)

    def create_tables(self):
        """创建 MySQL 表"""
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            age INT,
            department VARCHAR(255),
            skills JSON,
            metadata JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """

        create_activities_table = """
        CREATE TABLE IF NOT EXISTS user_activities (
            id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            activity_type VARCHAR(255) NOT NULL,
            description TEXT,
            details JSON,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """

        create_audit_log_table = """
        CREATE TABLE IF NOT EXISTS audit_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            operation VARCHAR(255) NOT NULL,
            user_id VARCHAR(255),
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(create_users_table)
            cursor.execute(create_activities_table)
            cursor.execute(create_audit_log_table)
            conn.commit()


class DatabaseFactory:
    """数据库工厂"""

    @staticmethod
    def create_manager(config: DatabaseConfig) -> DatabaseManager:
        if config.db_type == DatabaseType.SQLITE:
            return SQLiteManager(config)
        elif config.db_type == DatabaseType.POSTGRESQL:
            return PostgreSQLManager(config)
        elif config.db_type == DatabaseType.MYSQL:
            return MySQLManager(config)
        else:
            raise ValueError(f"Unsupported database type: {config.db_type}")


class UserRepository:
    """用户仓库"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def save_user(self, user_data: Dict[str, Any]) -> str:
        """保存用户"""
        user_id = user_data['id']
        skills_json = json.dumps(user_data.get('skills', []))
        metadata_json = json.dumps(user_data.get('metadata', {}))

        query = """
        INSERT INTO users (id, name, email, age, department, skills, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            email = excluded.email,
            age = excluded.age,
            department = excluded.department,
            skills = excluded.skills,
            metadata = excluded.metadata,
            updated_at = CURRENT_TIMESTAMP
        """

        self.db.execute_update(query, (
            user_id, user_data['name'], user_data['email'],
            user_data.get('age'), user_data.get('department'),
            skills_json, metadata_json
        ))

        return user_id

    def find_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """根据ID查找用户"""
        query = "SELECT * FROM users WHERE id = ?"
        results = self.db.execute_query(query, (user_id,))
        if results:
            user = results[0]
            user['skills'] = json.loads(user['skills'] or '[]')
            user['metadata'] = json.loads(user['metadata'] or '{}')
            return user
        return None

    def find_users_by_department(self, department: str) -> List[Dict[str, Any]]:
        """根据部门查找用户"""
        query = "SELECT * FROM users WHERE department = ?"
        results = self.db.execute_query(query, (department,))
        for user in results:
            user['skills'] = json.loads(user['skills'] or '[]')
            user['metadata'] = json.loads(user['metadata'] or '{}')
        return results

    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        query = "DELETE FROM users WHERE id = ?"
        return self.db.execute_update(query, (user_id,)) > 0

    def get_all_users(self) -> List[Dict[str, Any]]:
        """获取所有用户"""
        query = "SELECT * FROM users ORDER BY created_at DESC"
        results = self.db.execute_query(query)
        for user in results:
            user['skills'] = json.loads(user['skills'] or '[]')
            user['metadata'] = json.loads(user['metadata'] or '{}')
        return results

    def search_users(self, search_term: str) -> List[Dict[str, Any]]:
        """搜索用户"""
        query = """
        SELECT * FROM users
        WHERE name LIKE ? OR email LIKE ? OR department LIKE ?
        """
        search_pattern = f"%{search_term}%"
        results = self.db.execute_query(query, (search_pattern, search_pattern, search_pattern))
        for user in results:
            user['skills'] = json.loads(user['skills'] or '[]')
            user['metadata'] = json.loads(user['metadata'] or '{}')
        return results


class ActivityRepository:
    """活动仓库"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def save_activity(self, activity_data: Dict[str, Any]) -> str:
        """保存活动"""
        activity_id = activity_data['id']
        details_json = json.dumps(activity_data.get('details', {}))

        query = """
        INSERT INTO user_activities (id, user_id, activity_type, description, details)
        VALUES (?, ?, ?, ?, ?)
        """

        self.db.execute_update(query, (
            activity_id, activity_data['user_id'], activity_data['activity_type'],
            activity_data.get('description'), details_json
        ))

        return activity_id

    def get_user_activities(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """获取用户活动"""
        query = """
        SELECT * FROM user_activities
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """
        results = self.db.execute_query(query, (user_id, limit))
        for activity in results:
            activity['details'] = json.loads(activity['details'] or '{}')
        return results


class AuditRepository:
    """审计仓库"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def log_operation(self, operation: str, user_id: Optional[str], details: str):
        """记录操作"""
        query = "INSERT INTO audit_log (operation, user_id, details) VALUES (?, ?, ?)"
        self.db.execute_update(query, (operation, user_id, details))

    def get_recent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取最近的日志"""
        query = "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ?"
        return self.db.execute_query(query, (limit,))


# 全局数据库管理器实例
_db_manager = None
_user_repo = None
_activity_repo = None
_audit_repo = None


def initialize_database(config: DatabaseConfig):
    """初始化数据库"""
    global _db_manager, _user_repo, _activity_repo, _audit_repo

    _db_manager = DatabaseFactory.create_manager(config)
    _db_manager.create_tables()

    _user_repo = UserRepository(_db_manager)
    _activity_repo = ActivityRepository(_db_manager)
    _audit_repo = AuditRepository(_db_manager)

    logger.info("Database initialized successfully")


def get_user_repository() -> UserRepository:
    """获取用户仓库"""
    if _user_repo is None:
        raise RuntimeError("Database not initialized")
    return _user_repo


def get_activity_repository() -> ActivityRepository:
    """获取活动仓库"""
    if _activity_repo is None:
        raise RuntimeError("Database not initialized")
    return _activity_repo


def get_audit_repository() -> AuditRepository:
    """获取审计仓库"""
    if _audit_repo is None:
        raise RuntimeError("Database not initialized")
    return _audit_repo


def get_db_manager() -> DatabaseManager:
    """获取数据库管理器"""
    if _db_manager is None:
        raise RuntimeError("Database not initialized")
    return _db_manager
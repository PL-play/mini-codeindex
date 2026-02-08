#!/usr/bin/env python3
"""
配置模块
提供配置管理功能
"""

import os
import json
import yaml
import logging
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import base64
from functools import lru_cache
import threading
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """配置异常"""
    pass


class ConfigProvider(ABC):
    """配置提供者抽象基类"""

    @abstractmethod
    def load_config(self, key: str) -> Any:
        """加载配置"""
        pass

    @abstractmethod
    def save_config(self, key: str, value: Any):
        """保存配置"""
        pass

    @abstractmethod
    def has_config(self, key: str) -> bool:
        """检查配置是否存在"""
        pass


class EnvironmentConfigProvider(ConfigProvider):
    """环境变量配置提供者"""

    def __init__(self, prefix: str = ""):
        self.prefix = prefix.upper()

    def load_config(self, key: str) -> Any:
        env_key = f"{self.prefix}{key.upper()}" if self.prefix else key.upper()
        value = os.getenv(env_key)
        if value is None:
            raise ConfigError(f"Environment variable {env_key} not found")
        return self._parse_value(value)

    def save_config(self, key: str, value: Any):
        # 环境变量通常不保存，这里只是设置
        env_key = f"{self.prefix}{key.upper()}" if self.prefix else key.upper()
        os.environ[env_key] = str(value)

    def has_config(self, key: str) -> bool:
        env_key = f"{self.prefix}{key.upper()}" if self.prefix else key.upper()
        return env_key in os.environ

    def _parse_value(self, value: str) -> Any:
        """解析值"""
        # 尝试转换为合适类型
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        try:
            # 尝试整数
            if '.' not in value:
                return int(value)
            else:
                return float(value)
        except ValueError:
            pass

        # 尝试 JSON
        if (value.startswith('{') and value.endswith('}')) or \
           (value.startswith('[') and value.endswith(']')):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass

        return value


class FileConfigProvider(ConfigProvider):
    """文件配置提供者"""

    def __init__(self, config_dir: str = "config", format_type: str = "json"):
        self.config_dir = Path(config_dir)
        self.format_type = format_type
        self.config_dir.mkdir(exist_ok=True)
        self._cache = {}
        self._lock = threading.Lock()

    def _get_file_path(self, key: str) -> Path:
        return self.config_dir / f"{key}.{self.format_type}"

    def load_config(self, key: str) -> Any:
        file_path = self._get_file_path(key)
        if not file_path.exists():
            raise ConfigError(f"Config file {file_path} not found")

        with self._lock:
            # 检查缓存
            cache_key = str(file_path)
            if cache_key in self._cache:
                return self._cache[cache_key]

            with open(file_path, 'r', encoding='utf-8') as f:
                if self.format_type == 'json':
                    data = json.load(f)
                elif self.format_type == 'yaml' or self.format_type == 'yml':
                    data = yaml.safe_load(f)
                else:
                    raise ConfigError(f"Unsupported format: {self.format_type}")

            self._cache[cache_key] = data
            return data

    def save_config(self, key: str, value: Any):
        file_path = self._get_file_path(key)

        with self._lock:
            with open(file_path, 'w', encoding='utf-8') as f:
                if self.format_type == 'json':
                    json.dump(value, f, indent=2, ensure_ascii=False)
                elif self.format_type == 'yaml' or self.format_type == 'yml':
                    yaml.dump(value, f, default_flow_style=False)
                else:
                    raise ConfigError(f"Unsupported format: {self.format_type}")

            # 更新缓存
            self._cache[str(file_path)] = value

    def has_config(self, key: str) -> bool:
        return self._get_file_path(key).exists()

    def invalidate_cache(self, key: str = None):
        """使缓存失效"""
        with self._lock:
            if key:
                file_path = self._get_file_path(key)
                self._cache.pop(str(file_path), None)
            else:
                self._cache.clear()


class DatabaseConfigProvider(ConfigProvider):
    """数据库配置提供者"""

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def load_config(self, key: str) -> Any:
        # 这里需要实现数据库查询逻辑
        # 简化实现
        query = "SELECT value FROM config WHERE key = ?"
        result = self.db_manager.execute_query(query, (key,))
        if result:
            value_str = result[0]['value']
            try:
                return json.loads(value_str)
            except json.JSONDecodeError:
                return value_str
        raise ConfigError(f"Config key {key} not found in database")

    def save_config(self, key: str, value: Any):
        value_str = json.dumps(value) if not isinstance(value, str) else value
        query = """
        INSERT INTO config (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """
        self.db_manager.execute_update(query, (key, value_str))

    def has_config(self, key: str) -> bool:
        query = "SELECT COUNT(*) as count FROM config WHERE key = ?"
        result = self.db_manager.execute_query(query, (key,))
        return result and result[0]['count'] > 0


@dataclass
class DatabaseSettings:
    """数据库设置"""
    type: str = "sqlite"
    host: str = "localhost"
    port: Optional[int] = None
    database: str = "user_management.db"
    username: str = ""
    password: str = ""
    connection_pool_size: int = 10


@dataclass
class EmailSettings:
    """邮件设置"""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    username: str = ""
    password: str = ""
    use_tls: bool = True
    from_email: str = ""


@dataclass
class SecuritySettings:
    """安全设置"""
    jwt_secret: str = ""
    jwt_expiration_hours: int = 24
    bcrypt_rounds: int = 12
    password_min_length: int = 8
    enable_2fa: bool = False
    session_timeout_minutes: int = 60


@dataclass
class APISettings:
    """API 设置"""
    base_url: str = "http://localhost:8000"
    api_key: str = ""
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60
    enable_cors: bool = True
    allowed_origins: List[str] = field(default_factory=lambda: ["*"])


@dataclass
class NotificationSettings:
    """通知设置"""
    email_enabled: bool = True
    sms_enabled: bool = False
    push_enabled: bool = False
    slack_webhook_url: str = ""
    discord_webhook_url: str = ""


@dataclass
class LoggingSettings:
    """日志设置"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "logs/app.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    enable_console: bool = True


@dataclass
class ApplicationConfig:
    """应用配置"""
    app_name: str = "User Management System"
    version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    secret_key: str = ""

    database: DatabaseSettings = field(default_factory=DatabaseSettings)
    email: EmailSettings = field(default_factory=EmailSettings)
    security: SecuritySettings = field(default_factory=SecuritySettings)
    api: APISettings = field(default_factory=APISettings)
    notifications: NotificationSettings = field(default_factory=NotificationSettings)
    logging: LoggingSettings = field(default_factory=LoggingSettings)


class ConfigManager:
    """配置管理器"""

    def __init__(self):
        self.providers: List[ConfigProvider] = []
        self.config_cache: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def add_provider(self, provider: ConfigProvider, priority: int = 0):
        """添加配置提供者"""
        # 按优先级插入（高优先级在前）
        insert_pos = 0
        for i, (p, pri) in enumerate(self.providers):
            if priority > pri:
                insert_pos = i
                break
            insert_pos = i + 1

        self.providers.insert(insert_pos, (provider, priority))

    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置"""
        with self._lock:
            if key in self.config_cache:
                return self.config_cache[key]

            for provider, _ in self.providers:
                try:
                    if provider.has_config(key):
                        value = provider.load_config(key)
                        self.config_cache[key] = value
                        return value
                except ConfigError:
                    continue

            if default is not None:
                return default

            raise ConfigError(f"Configuration key '{key}' not found in any provider")

    def set_config(self, key: str, value: Any, provider_index: int = 0):
        """设置配置"""
        with self._lock:
            if provider_index < len(self.providers):
                provider, _ = self.providers[provider_index]
                provider.save_config(key, value)
                self.config_cache[key] = value
            else:
                raise ConfigError(f"Provider index {provider_index} out of range")

    def has_config(self, key: str) -> bool:
        """检查配置是否存在"""
        for provider, _ in self.providers:
            if provider.has_config(key):
                return True
        return False

    def invalidate_cache(self, key: str = None):
        """使缓存失效"""
        with self._lock:
            if key:
                self.config_cache.pop(key, None)
            else:
                self.config_cache.clear()

            # 同时使文件提供者的缓存失效
            for provider, _ in self.providers:
                if hasattr(provider, 'invalidate_cache'):
                    provider.invalidate_cache(key)

    def load_application_config(self) -> ApplicationConfig:
        """加载应用配置"""
        config = ApplicationConfig()

        # 尝试从提供者加载各个部分
        try:
            # 基本信息
            config.app_name = self.get_config("app.name", config.app_name)
            config.version = self.get_config("app.version", config.version)
            config.environment = self.get_config("app.environment", config.environment)
            config.debug = self.get_config("app.debug", config.debug)
            config.secret_key = self.get_config("app.secret_key", config.secret_key)

            # 数据库配置
            config.database.type = self.get_config("database.type", config.database.type)
            config.database.host = self.get_config("database.host", config.database.host)
            config.database.port = self.get_config("database.port", config.database.port)
            config.database.database = self.get_config("database.database", config.database.database)
            config.database.username = self.get_config("database.username", config.database.username)
            config.database.password = self.get_config("database.password", config.database.password)

            # 邮件配置
            config.email.smtp_server = self.get_config("email.smtp_server", config.email.smtp_server)
            config.email.smtp_port = self.get_config("email.smtp_port", config.email.smtp_port)
            config.email.username = self.get_config("email.username", config.email.username)
            config.email.password = self.get_config("email.password", config.email.password)

            # 安全配置
            config.security.jwt_secret = self.get_config("security.jwt_secret", config.security.jwt_secret)
            config.security.enable_2fa = self.get_config("security.enable_2fa", config.security.enable_2fa)

            # API 配置
            config.api.base_url = self.get_config("api.base_url", config.api.base_url)
            config.api.api_key = self.get_config("api.api_key", config.api.api_key)

            # 通知配置
            config.notifications.email_enabled = self.get_config("notifications.email_enabled", config.notifications.email_enabled)

            # 日志配置
            config.logging.level = self.get_config("logging.level", config.logging.level)
            config.logging.file_path = self.get_config("logging.file_path", config.logging.file_path)

        except ConfigError as e:
            logger.warning(f"Some configuration values not found, using defaults: {e}")

        return config

    def save_application_config(self, config: ApplicationConfig):
        """保存应用配置"""
        # 将配置对象转换为字典并保存
        config_dict = {
            "app": {
                "name": config.app_name,
                "version": config.version,
                "environment": config.environment,
                "debug": config.debug,
                "secret_key": config.secret_key
            },
            "database": {
                "type": config.database.type,
                "host": config.database.host,
                "port": config.database.port,
                "database": config.database.database,
                "username": config.database.username,
                "password": config.database.password
            },
            "email": {
                "smtp_server": config.email.smtp_server,
                "smtp_port": config.email.smtp_port,
                "username": config.email.username,
                "password": config.email.password
            },
            "security": {
                "jwt_secret": config.security.jwt_secret,
                "enable_2fa": config.security.enable_2fa
            },
            "api": {
                "base_url": config.api.base_url,
                "api_key": config.api.api_key
            },
            "notifications": {
                "email_enabled": config.notifications.email_enabled
            },
            "logging": {
                "level": config.logging.level,
                "file_path": config.logging.file_path
            }
        }

        self.set_config("application", config_dict)


# 全局配置管理器实例
_config_manager = ConfigManager()


def get_config_manager() -> ConfigManager:
    """获取配置管理器"""
    return _config_manager


def initialize_config(config_dir: str = "config", env_prefix: str = "UMS_"):
    """初始化配置系统"""
    global _config_manager

    # 添加环境变量提供者（最高优先级）
    env_provider = EnvironmentConfigProvider(env_prefix)
    _config_manager.add_provider(env_provider, priority=10)

    # 添加文件配置提供者
    file_provider = FileConfigProvider(config_dir)
    _config_manager.add_provider(file_provider, priority=5)

    logger.info("Configuration system initialized")


def get_app_config() -> ApplicationConfig:
    """获取应用配置"""
    return _config_manager.load_application_config()


def get_config(key: str, default: Any = None) -> Any:
    """获取配置值"""
    return _config_manager.get_config(key, default)


def set_config(key: str, value: Any):
    """设置配置值"""
    _config_manager.set_config(key, value)


# 加密配置值
def encrypt_config_value(value: str, key: str) -> str:
    """加密配置值"""
    combined = (value + key).encode()
    hash_obj = hashlib.sha256(combined)
    return base64.b64encode(hash_obj.digest()).decode()


def decrypt_config_value(encrypted: str, key: str) -> str:
    """解密配置值（简化实现，实际应该使用对称加密）"""
    # 这里是简化实现，实际应用中应该使用真正的加密算法
    return encrypted  # 实际实现需要解密逻辑


# 配置验证
def validate_config(config: ApplicationConfig) -> List[str]:
    """验证配置"""
    errors = []

    if not config.app_name:
        errors.append("Application name is required")

    if not config.secret_key:
        errors.append("Secret key is required")

    if config.database.type not in ["sqlite", "postgresql", "mysql"]:
        errors.append("Invalid database type")

    if config.database.type != "sqlite":
        if not config.database.host:
            errors.append("Database host is required for non-SQLite databases")
        if not config.database.database:
            errors.append("Database name is required")

    if config.email.username and not config.email.password:
        errors.append("Email password is required when username is provided")

    if config.security.jwt_secret and len(config.security.jwt_secret) < 32:
        errors.append("JWT secret should be at least 32 characters long")

    return errors


# 配置热重载
class ConfigWatcher:
    """配置监视器"""

    def __init__(self, config_dir: str, callback: callable):
        self.config_dir = Path(config_dir)
        self.callback = callback
        self.watched_files = set()
        self.running = False

    def start_watching(self):
        """开始监视"""
        self.running = True
        # 这里可以实现文件监视逻辑
        # 简化实现，使用定时检查
        import time
        def watch_loop():
            while self.running:
                self._check_changes()
                time.sleep(5)

        import threading
        thread = threading.Thread(target=watch_loop, daemon=True)
        thread.start()

    def stop_watching(self):
        """停止监视"""
        self.running = False

    def _check_changes(self):
        """检查文件变化"""
        # 简化实现
        pass
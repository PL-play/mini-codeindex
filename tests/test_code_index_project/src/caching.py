"""
Advanced caching module with multiple cache backends, TTL support,
serialization, and distributed cache management.
"""

import asyncio
import hashlib
import json
import logging
import pickle
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from functools import wraps
from typing import Any, Dict, List, Optional, Set, Tuple, Union, Callable
from concurrent.futures import ThreadPoolExecutor
import redis
import sqlite3
from contextlib import contextmanager
import weakref
import gc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CacheError(Exception):
    """Base exception for cache operations."""
    pass


class CacheMissError(CacheError):
    """Raised when cache key is not found."""
    pass


class CacheBackendError(CacheError):
    """Raised when cache backend operation fails."""
    pass


class SerializationError(CacheError):
    """Raised when serialization/deserialization fails."""
    pass


class CacheStrategy(Enum):
    """Cache eviction strategies."""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    FIFO = "fifo"  # First In First Out
    RANDOM = "random"  # Random eviction
    TTL = "ttl"  # Time To Live based


class CacheBackend(Enum):
    """Supported cache backends."""
    MEMORY = "memory"
    REDIS = "redis"
    SQLITE = "sqlite"
    FILE = "file"
    DISTRIBUTED = "distributed"


@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    accessed_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    access_count: int = 0
    size_bytes: int = 0
    tags: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        """Check if entry has expired."""
        return self.expires_at is not None and datetime.now() > self.expires_at

    def touch(self):
        """Update access time and count."""
        self.accessed_at = datetime.now()
        self.access_count += 1

    def calculate_size(self):
        """Calculate approximate size in bytes."""
        try:
            self.size_bytes = len(pickle.dumps(self.value))
        except:
            self.size_bytes = len(str(self.value).encode('utf-8'))


@dataclass
class CacheStats:
    """Cache statistics."""
    hits: int = 0
    misses: int = 0
    sets: int = 0
    deletes: int = 0
    evictions: int = 0
    total_entries: int = 0
    total_size_bytes: int = 0
    hit_rate: float = 0.0

    def update_hit_rate(self):
        """Update hit rate calculation."""
        total_requests = self.hits + self.misses
        self.hit_rate = self.hits / total_requests if total_requests > 0 else 0.0

    def reset(self):
        """Reset all statistics."""
        self.hits = self.misses = self.sets = self.deletes = self.evictions = 0
        self.total_entries = self.total_size_bytes = 0
        self.hit_rate = 0.0


class Serializer(ABC):
    """Abstract base class for cache value serialization."""

    @abstractmethod
    def serialize(self, value: Any) -> bytes:
        """Serialize value to bytes."""
        pass

    @abstractmethod
    def deserialize(self, data: bytes) -> Any:
        """Deserialize bytes to value."""
        pass


class PickleSerializer(Serializer):
    """Pickle-based serializer."""

    def serialize(self, value: Any) -> bytes:
        try:
            return pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            raise SerializationError(f"Pickle serialization failed: {e}")

    def deserialize(self, data: bytes) -> Any:
        try:
            return pickle.loads(data)
        except Exception as e:
            raise SerializationError(f"Pickle deserialization failed: {e}")


class JSONSerializer(Serializer):
    """JSON-based serializer for simple types."""

    def serialize(self, value: Any) -> bytes:
        try:
            return json.dumps(value, default=str).encode('utf-8')
        except Exception as e:
            raise SerializationError(f"JSON serialization failed: {e}")

    def deserialize(self, data: bytes) -> Any:
        try:
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            raise SerializationError(f"JSON deserialization failed: {e}")


class CacheBackendBase(ABC):
    """Abstract base class for cache backends."""

    def __init__(self, serializer: Serializer = None):
        self.serializer = serializer or PickleSerializer()

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass

    @abstractmethod
    async def clear(self) -> bool:
        """Clear all cache entries."""
        pass

    @abstractmethod
    async def size(self) -> int:
        """Get number of entries in cache."""
        pass

    @abstractmethod
    async def keys(self, pattern: str = "*") -> List[str]:
        """Get keys matching pattern."""
        pass


class MemoryCacheBackend(CacheBackendBase):
    """In-memory cache backend with TTL and size limits."""

    def __init__(self, max_size: int = 1000, serializer: Serializer = None,
                 strategy: CacheStrategy = CacheStrategy.LRU):
        super().__init__(serializer)
        self.max_size = max_size
        self.strategy = strategy
        self.cache: Dict[str, CacheEntry] = {}
        self.access_order: List[str] = []  # For LRU
        self.frequency: Dict[str, int] = {}  # For LFU
        self.insertion_order: List[str] = []  # For FIFO
        self._lock = threading.RLock()

    async def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self.cache.get(key)
            if entry is None or entry.is_expired():
                if entry:
                    del self.cache[key]
                    self._remove_from_tracking(key)
                return None

            entry.touch()
            self._update_access_tracking(key)
            return entry.value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        with self._lock:
            # Remove expired entries
            self._cleanup_expired()

            # Check size limit
            if key not in self.cache and len(self.cache) >= self.max_size:
                self._evict_entries()

            expires_at = datetime.now() + timedelta(seconds=ttl) if ttl else None
            entry = CacheEntry(key=key, value=value, expires_at=expires_at)
            entry.calculate_size()

            self.cache[key] = entry
            self._add_to_tracking(key)

            return True

    async def delete(self, key: str) -> bool:
        with self._lock:
            if key in self.cache:
                del self.cache[key]
                self._remove_from_tracking(key)
                return True
            return False

    async def exists(self, key: str) -> bool:
        with self._lock:
            entry = self.cache.get(key)
            return entry is not None and not entry.is_expired()

    async def clear(self) -> bool:
        with self._lock:
            self.cache.clear()
            self.access_order.clear()
            self.frequency.clear()
            self.insertion_order.clear()
            return True

    async def size(self) -> int:
        with self._lock:
            self._cleanup_expired()
            return len(self.cache)

    async def keys(self, pattern: str = "*") -> List[str]:
        with self._lock:
            self._cleanup_expired()
            if pattern == "*":
                return list(self.cache.keys())
            # Simple pattern matching (could be enhanced)
            return [k for k in self.cache.keys() if pattern in k]

    def _cleanup_expired(self):
        """Remove expired entries."""
        expired_keys = [k for k, v in self.cache.items() if v.is_expired()]
        for key in expired_keys:
            del self.cache[key]
            self._remove_from_tracking(key)

    def _evict_entries(self):
        """Evict entries based on strategy."""
        if not self.cache:
            return

        if self.strategy == CacheStrategy.LRU:
            # Evict least recently used
            key_to_evict = self.access_order.pop(0)
        elif self.strategy == CacheStrategy.LFU:
            # Evict least frequently used
            key_to_evict = min(self.frequency.keys(),
                             key=lambda k: self.frequency[k])
        elif self.strategy == CacheStrategy.FIFO:
            # Evict first inserted
            key_to_evict = self.insertion_order.pop(0)
        else:  # RANDOM
            import random
            key_to_evict = random.choice(list(self.cache.keys()))

        del self.cache[key_to_evict]
        self._remove_from_tracking(key_to_evict)

    def _add_to_tracking(self, key: str):
        """Add key to tracking structures."""
        if self.strategy == CacheStrategy.LRU:
            self.access_order.append(key)
        elif self.strategy == CacheStrategy.LFU:
            self.frequency[key] = 0
        elif self.strategy == CacheStrategy.FIFO:
            self.insertion_order.append(key)

    def _remove_from_tracking(self, key: str):
        """Remove key from tracking structures."""
        if self.strategy == CacheStrategy.LRU:
            self.access_order = [k for k in self.access_order if k != key]
        elif self.strategy == CacheStrategy.LFU:
            self.frequency.pop(key, None)
        elif self.strategy == CacheStrategy.FIFO:
            self.insertion_order = [k for k in self.insertion_order if k != key]

    def _update_access_tracking(self, key: str):
        """Update access tracking for key."""
        if self.strategy == CacheStrategy.LRU:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
        elif self.strategy == CacheStrategy.LFU:
            self.frequency[key] += 1


class RedisCacheBackend(CacheBackendBase):
    """Redis cache backend."""

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0,
                 password: str = None, serializer: Serializer = None):
        super().__init__(serializer)
        self.redis_client = redis.Redis(
            host=host, port=port, db=db, password=password,
            decode_responses=False  # We handle serialization
        )
        self._executor = ThreadPoolExecutor(max_workers=4)

    async def get(self, key: str) -> Optional[Any]:
        def _get():
            data = self.redis_client.get(key)
            if data is None:
                return None
            return self.serializer.deserialize(data)

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _get)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        def _set():
            data = self.serializer.serialize(value)
            return self.redis_client.set(key, data, ex=ttl)

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _set)

    async def delete(self, key: str) -> bool:
        def _delete():
            return self.redis_client.delete(key) > 0

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _delete)

    async def exists(self, key: str) -> bool:
        def _exists():
            return self.redis_client.exists(key) > 0

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _exists)

    async def clear(self) -> bool:
        def _clear():
            return self.redis_client.flushdb()

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _clear)

    async def size(self) -> int:
        def _size():
            return self.redis_client.dbsize()

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _size)

    async def keys(self, pattern: str = "*") -> List[str]:
        def _keys():
            return self.redis_client.keys(pattern)

        loop = asyncio.get_event_loop()
        keys_bytes = await loop.run_in_executor(self._executor, _keys)
        return [k.decode('utf-8') if isinstance(k, bytes) else k for k in keys_bytes]


class SQLiteCacheBackend(CacheBackendBase):
    """SQLite-based persistent cache backend."""

    def __init__(self, db_path: str = ":memory:", serializer: Serializer = None):
        super().__init__(serializer)
        self.db_path = db_path
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value BLOB,
                    expires_at REAL,
                    created_at REAL,
                    accessed_at REAL,
                    access_count INTEGER DEFAULT 0
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_expires ON cache(expires_at)')
            conn.commit()

    @contextmanager
    def _get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    async def get(self, key: str) -> Optional[Any]:
        def _get():
            with self._get_connection() as conn:
                cursor = conn.execute('''
                    SELECT value, expires_at FROM cache WHERE key = ?
                ''', (key,))
                row = cursor.fetchone()

                if row is None:
                    return None

                value_blob, expires_at = row
                if expires_at and time.time() > expires_at:
                    # Expired, delete it
                    conn.execute('DELETE FROM cache WHERE key = ?', (key,))
                    conn.commit()
                    return None

                # Update access info
                conn.execute('''
                    UPDATE cache SET accessed_at = ?, access_count = access_count + 1
                    WHERE key = ?
                ''', (time.time(), key))
                conn.commit()

                return self.serializer.deserialize(value_blob)

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _get)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        def _set():
            with self._get_connection() as conn:
                value_blob = self.serializer.serialize(value)
                expires_at = time.time() + ttl if ttl else None
                created_at = time.time()

                conn.execute('''
                    INSERT OR REPLACE INTO cache
                    (key, value, expires_at, created_at, accessed_at, access_count)
                    VALUES (?, ?, ?, ?, ?, 0)
                ''', (key, value_blob, expires_at, created_at, created_at))
                conn.commit()
                return True

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _set)

    async def delete(self, key: str) -> bool:
        def _delete():
            with self._get_connection() as conn:
                cursor = conn.execute('DELETE FROM cache WHERE key = ?', (key,))
                conn.commit()
                return cursor.rowcount > 0

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _delete)

    async def exists(self, key: str) -> bool:
        def _exists():
            with self._get_connection() as conn:
                cursor = conn.execute('SELECT 1 FROM cache WHERE key = ? AND (expires_at IS NULL OR expires_at > ?)',
                                    (key, time.time()))
                return cursor.fetchone() is not None

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _exists)

    async def clear(self) -> bool:
        def _clear():
            with self._get_connection() as conn:
                conn.execute('DELETE FROM cache')
                conn.commit()
                return True

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _clear)

    async def size(self) -> int:
        def _size():
            with self._get_connection() as conn:
                cursor = conn.execute('SELECT COUNT(*) FROM cache WHERE expires_at IS NULL OR expires_at > ?',
                                    (time.time(),))
                return cursor.fetchone()[0]

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _size)

    async def keys(self, pattern: str = "*") -> List[str]:
        def _keys():
            with self._get_connection() as conn:
                if pattern == "*":
                    cursor = conn.execute('SELECT key FROM cache WHERE expires_at IS NULL OR expires_at > ?',
                                        (time.time(),))
                else:
                    # Simple LIKE pattern
                    cursor = conn.execute('SELECT key FROM cache WHERE key LIKE ? AND (expires_at IS NULL OR expires_at > ?)',
                                        (pattern.replace('*', '%'), time.time()))
                return [row[0] for row in cursor.fetchall()]

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, _keys)


class DistributedCacheBackend(CacheBackendBase):
    """Distributed cache backend that combines multiple backends."""

    def __init__(self, backends: List[CacheBackendBase], serializer: Serializer = None):
        super().__init__(serializer)
        self.backends = backends
        self.local_cache = MemoryCacheBackend(max_size=100)  # L1 cache

    async def get(self, key: str) -> Optional[Any]:
        # Try local cache first
        value = await self.local_cache.get(key)
        if value is not None:
            return value

        # Try distributed backends
        for backend in self.backends:
            try:
                value = await backend.get(key)
                if value is not None:
                    # Cache locally
                    await self.local_cache.set(key, value, ttl=300)  # 5 min TTL
                    return value
            except Exception as e:
                logger.warning(f"Backend {backend.__class__.__name__} failed: {e}")
                continue

        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        # Update local cache
        await self.local_cache.set(key, value, ttl)

        # Update distributed backends
        success_count = 0
        for backend in self.backends:
            try:
                if await backend.set(key, value, ttl):
                    success_count += 1
            except Exception as e:
                logger.warning(f"Backend {backend.__class__.__name__} set failed: {e}")

        # Require majority success for distributed writes
        return success_count > len(self.backends) // 2

    async def delete(self, key: str) -> bool:
        await self.local_cache.delete(key)

        success_count = 0
        for backend in self.backends:
            try:
                if await backend.delete(key):
                    success_count += 1
            except Exception as e:
                logger.warning(f"Backend {backend.__class__.__name__} delete failed: {e}")

        return success_count > 0

    async def exists(self, key: str) -> bool:
        if await self.local_cache.exists(key):
            return True

        for backend in self.backends:
            try:
                if await backend.exists(key):
                    return True
            except Exception as e:
                logger.warning(f"Backend {backend.__class__.__name__} exists failed: {e}")

        return False

    async def clear(self) -> bool:
        await self.local_cache.clear()

        success_count = 0
        for backend in self.backends:
            try:
                if await backend.clear():
                    success_count += 1
            except Exception as e:
                logger.warning(f"Backend {backend.__class__.__name__} clear failed: {e}")

        return success_count > 0

    async def size(self) -> int:
        # Return size from first backend (approximate)
        for backend in self.backends:
            try:
                return await backend.size()
            except Exception as e:
                logger.warning(f"Backend {backend.__class__.__name__} size failed: {e}")
        return 0

    async def keys(self, pattern: str = "*") -> List[str]:
        # Collect keys from all backends
        all_keys = set()
        for backend in self.backends:
            try:
                keys = await backend.keys(pattern)
                all_keys.update(keys)
            except Exception as e:
                logger.warning(f"Backend {backend.__class__.__name__} keys failed: {e}")

        return list(all_keys)


class CacheManager:
    """Main cache manager with advanced features."""

    def __init__(self, backend: CacheBackendBase, enable_stats: bool = True):
        self.backend = backend
        self.stats = CacheStats() if enable_stats else None
        self.tags_index: Dict[str, Set[str]] = {}  # tag -> keys
        self.key_tags: Dict[str, Set[str]] = {}  # key -> tags
        self._lock = threading.RLock()

    async def get(self, key: str) -> Any:
        """Get value from cache."""
        try:
            value = await self.backend.get(key)
            if self.stats:
                if value is not None:
                    self.stats.hits += 1
                else:
                    self.stats.misses += 1
                self.stats.update_hit_rate()
            return value
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            if self.stats:
                self.stats.misses += 1
                self.stats.update_hit_rate()
            raise CacheBackendError(f"Failed to get cache key {key}: {e}")

    async def set(self, key: str, value: Any, ttl: Optional[int] = None,
                  tags: Set[str] = None) -> bool:
        """Set value in cache with optional TTL and tags."""
        try:
            success = await self.backend.set(key, value, ttl)
            if success and self.stats:
                self.stats.sets += 1

            # Update tag index
            if tags:
                with self._lock:
                    self.key_tags[key] = tags.copy()
                    for tag in tags:
                        self.tags_index.setdefault(tag, set()).add(key)

            return success
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            raise CacheBackendError(f"Failed to set cache key {key}: {e}")

    async def get_or_set(self, key: str, default_func: Callable[[], Any],
                        ttl: Optional[int] = None, tags: Set[str] = None) -> Any:
        """Get value or set default if not exists."""
        value = await self.get(key)
        if value is None:
            value = default_func()
            await self.set(key, value, ttl, tags)
        return value

    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            success = await self.backend.delete(key)
            if success and self.stats:
                self.stats.deletes += 1

            # Update tag index
            with self._lock:
                if key in self.key_tags:
                    tags = self.key_tags[key]
                    for tag in tags:
                        self.tags_index.get(tag, set()).discard(key)
                    del self.key_tags[key]

            return success
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            raise CacheBackendError(f"Failed to delete cache key {key}: {e}")

    async def delete_by_tags(self, tags: Set[str]) -> int:
        """Delete all keys with given tags."""
        with self._lock:
            keys_to_delete = set()
            for tag in tags:
                keys_to_delete.update(self.tags_index.get(tag, set()))

            deleted_count = 0
            for key in keys_to_delete:
                if await self.delete(key):
                    deleted_count += 1

            return deleted_count

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate keys matching pattern."""
        keys = await self.backend.keys(pattern)
        deleted_count = 0
        for key in keys:
            if await self.delete(key):
                deleted_count += 1
        return deleted_count

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return await self.backend.exists(key)

    async def clear(self) -> bool:
        """Clear all cache entries."""
        try:
            success = await self.backend.clear()
            if success and self.stats:
                self.stats.reset()

            # Clear tag index
            with self._lock:
                self.tags_index.clear()
                self.key_tags.clear()

            return success
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            raise CacheBackendError(f"Failed to clear cache: {e}")

    async def size(self) -> int:
        """Get cache size."""
        return await self.backend.size()

    async def keys(self, pattern: str = "*") -> List[str]:
        """Get keys matching pattern."""
        return await self.backend.keys(pattern)

    def get_stats(self) -> Optional[CacheStats]:
        """Get cache statistics."""
        return self.stats

    def reset_stats(self):
        """Reset cache statistics."""
        if self.stats:
            self.stats.reset()

    def cached(self, ttl: Optional[int] = None, key_prefix: str = "",
               tags: Set[str] = None):
        """Decorator for caching function results."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                key_parts = [key_prefix or func.__name__]
                key_parts.extend(str(arg) for arg in args)
                key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
                cache_key = hashlib.md5("|".join(key_parts).encode()).hexdigest()

                # Try cache first
                cached_value = await self.get(cache_key)
                if cached_value is not None:
                    return cached_value

                # Execute function
                result = await func(*args, **kwargs)

                # Cache result
                await self.set(cache_key, result, ttl, tags)

                return result
            return wrapper
        return decorator


# Utility functions and decorators
def create_cache_manager(backend_type: CacheBackend = CacheBackend.MEMORY,
                        **backend_kwargs) -> CacheManager:
    """Factory function to create cache manager with specified backend."""

    if backend_type == CacheBackend.MEMORY:
        backend = MemoryCacheBackend(**backend_kwargs)
    elif backend_type == CacheBackend.REDIS:
        backend = RedisCacheBackend(**backend_kwargs)
    elif backend_type == CacheBackend.SQLITE:
        backend = SQLiteCacheBackend(**backend_kwargs)
    elif backend_type == CacheBackend.DISTRIBUTED:
        backends = backend_kwargs.get('backends', [])
        backend = DistributedCacheBackend(backends)
    else:
        raise ValueError(f"Unsupported backend type: {backend_type}")

    return CacheManager(backend)


async def warmup_cache(cache_manager: CacheManager, warmup_data: Dict[str, Any],
                      ttl: Optional[int] = None):
    """Warm up cache with initial data."""
    for key, value in warmup_data.items():
        await cache_manager.set(key, value, ttl)


async def backup_cache(cache_manager: CacheManager, backup_path: str):
    """Backup cache contents to file."""
    keys = await cache_manager.keys()
    backup_data = {}

    for key in keys:
        try:
            value = await cache_manager.get(key)
            if value is not None:
                backup_data[key] = value
        except Exception as e:
            logger.warning(f"Failed to backup key {key}: {e}")

    with open(backup_path, 'wb') as f:
        pickle.dump(backup_data, f)


async def restore_cache(cache_manager: CacheManager, backup_path: str,
                       ttl: Optional[int] = None):
    """Restore cache from backup file."""
    with open(backup_path, 'rb') as f:
        backup_data = pickle.load(f)

    await warmup_cache(cache_manager, backup_data, ttl)


# Example usage
async def example_usage():
    """Example usage of the caching system."""

    # Create memory cache
    cache = create_cache_manager(CacheBackend.MEMORY, max_size=100)

    # Basic operations
    await cache.set("user:123", {"name": "John", "age": 30}, ttl=3600)
    user = await cache.get("user:123")
    print(f"Cached user: {user}")

    # Tagged caching
    await cache.set("product:456", {"name": "Widget", "price": 19.99},
                   tags={"products", "electronics"})

    # Cached function
    @cache.cached(ttl=300, tags={"api_calls"})
    async def fetch_user_data(user_id: str):
        # Simulate API call
        await asyncio.sleep(0.1)
        return {"id": user_id, "data": f"User {user_id} data"}

    # First call (cache miss)
    data1 = await fetch_user_data("user123")
    print(f"First call: {data1}")

    # Second call (cache hit)
    data2 = await fetch_user_data("user123")
    print(f"Second call: {data2}")

    # Get stats
    stats = cache.get_stats()
    if stats:
        print(f"Cache stats: hits={stats.hits}, misses={stats.misses}, hit_rate={stats.hit_rate:.2%}")

    # Clean up
    await cache.clear()


if __name__ == "__main__":
    asyncio.run(example_usage())
"""Compatibility shim.

VectorCode uses a `vectorise` verb. In mini_code_index we call the operation
"indexing". This module keeps naming flexible while the project evolves.
"""

from __future__ import annotations

from .indexing import IndexConfig, IndexStats, index_directory

__all__ = ["IndexConfig", "IndexStats", "index_directory"]

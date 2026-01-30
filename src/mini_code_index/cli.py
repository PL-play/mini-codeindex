from __future__ import annotations

import argparse
import asyncio
import os
import sys

from .chunking import Config as ChunkConfig
from .db import ChromaStore
from .embedding import OpenAICompatibleEmbedder
from .indexing import IndexConfig, index_directory


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mini-code-index")
    sub = p.add_subparsers(dest="cmd", required=True)

    idx = sub.add_parser("index", help="Index a directory (scan -> chunk -> embed -> store)")
    idx.add_argument("root", help="Root directory to index")
    idx.add_argument(
        "--chroma-url",
        default=os.environ.get("CHROMA_URL", "http://127.0.0.1:8010"),
        help="ChromaDB base URL (default: %(default)s)",
    )
    idx.add_argument(
        "--write",
        action="store_true",
        help="Actually write to the vector store (default is dry-run)",
    )
    idx.add_argument(
        "--chunk-size",
        type=int,
        default=ChunkConfig().chunk_size,
        help="Chunk size (default: %(default)s)",
    )
    idx.add_argument(
        "--overlap",
        type=float,
        default=ChunkConfig().overlap_ratio,
        help="Overlap ratio (default: %(default)s)",
    )
    idx.add_argument(
        "--mode",
        default=ChunkConfig().mode,
        help="Chunking mode: file/type/function/auto_ast (default: %(default)s)",
    )

    ping = sub.add_parser("ping", help="Ping the configured ChromaDB")
    ping.add_argument(
        "--chroma-url",
        default=os.environ.get("CHROMA_URL", "http://127.0.0.1:8010"),
        help="ChromaDB base URL (default: %(default)s)",
    )

    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.cmd == "ping":
        store = ChromaStore(base_url=args.chroma_url)
        ok = asyncio.run(store.ping())
        print("ok" if ok else "failed")
        return 0 if ok else 1

    if args.cmd == "index":
        chunk_cfg = ChunkConfig(chunk_size=args.chunk_size, overlap_ratio=args.overlap, mode=args.mode)
        cfg = IndexConfig(root_dir=args.root, dry_run=not args.write)

        store = ChromaStore(base_url=args.chroma_url, root_dir=args.root)
        if not asyncio.run(store.ping()):
            print(f"ChromaDB is not reachable at {args.chroma_url}", file=sys.stderr)
            return 2

        embedder = None
        if args.write:
            embedder = OpenAICompatibleEmbedder.from_env()

        stats = asyncio.run(
            index_directory(cfg=cfg, chunk_cfg=chunk_cfg, embedder=embedder, store=store)
        )
        print(
            f"files_seen={stats.files_seen} files_indexed={stats.files_indexed} chunks={stats.chunks_emitted} dry_run={cfg.dry_run}"
        )
        return 0

    return 1

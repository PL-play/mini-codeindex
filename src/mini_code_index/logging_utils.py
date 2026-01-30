from __future__ import annotations

import logging
import os
from typing import Optional


def setup_logging(*, log_level: Optional[str] = None, log_file: Optional[str] = None) -> None:
    root = logging.getLogger()
    if getattr(root, "_mci_configured", False):
        return

    level_name = (log_level or os.environ.get("MCI_LOG_LEVEL") or "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    file_path = log_file or os.environ.get("MCI_LOG_FILE") or "mini_code_index.log"
    file_dir = os.path.dirname(file_path)
    if file_dir:
        os.makedirs(file_dir, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(file_path, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    root.setLevel(level)
    root.addHandler(stream_handler)
    root.addHandler(file_handler)
    setattr(root, "_mci_configured", True)
    
    # Suppress verbose httpx and other third-party logs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
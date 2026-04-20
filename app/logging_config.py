from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import structlog
from structlog.contextvars import merge_contextvars

from .pii import scrub_text

LOG_PATH = Path(os.getenv("LOG_PATH", "data/logs.jsonl"))


class JsonlFileProcessor:
    def __call__(self, logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        # Tạo bản sao để không làm hỏng dữ liệu gốc của các processor phía sau
        rendered = structlog.processors.JSONRenderer()(logger, method_name, event_dict)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(rendered + "\n")
            f.flush() # Đảm bảo log được ghi ngay lập tức
        return event_dict



def scrub_event(_: Any, __: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """Processor đệ quy để xóa sạch PII khỏi mọi trường trong log."""
    
    def _scrub_recursive(obj: Any) -> Any:
        if isinstance(obj, str):
            return scrub_text(obj)
        if isinstance(obj, dict):
            return {k: _scrub_recursive(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_scrub_recursive(i) for i in obj]
        return obj

    # Quét toàn bộ event_dict để đảm bảo không bỏ sót PII trong bất kỳ field nào
    # (Trừ các field hệ thống như ts, level, correlation_id)
    system_fields = {"ts", "level", "correlation_id", "service", "env"}
    for key, value in event_dict.items():
        if key not in system_fields:
            event_dict[key] = _scrub_recursive(value)
            
    return event_dict



def configure_logging() -> None:
    # Đồng bộ logging level giữa structlog và thư viện logging tiêu chuẩn
    log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
    logging.basicConfig(format="%(message)s", level=log_level)
    
    structlog.configure(
        processors=[
            merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True, key="ts"),
            # Đưa PII scrubbing lên trước khi ghi ra file hoặc render JSON
            scrub_event,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            JsonlFileProcessor(), # Ghi ra file JSONL
            structlog.processors.JSONRenderer(), # Trả về chuỗi JSON cho console/logging stream
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=True,
    )



def get_logger() -> structlog.typing.FilteringBoundLogger:
    return structlog.get_logger()

from __future__ import annotations

import os
from typing import Any

try:
    from langfuse import get_client, observe as _observe

    def observe(*args: Any, **kwargs: Any):
        if args and callable(args[0]) and not kwargs:
            return _observe(as_type="generation")(args[0])
        kwargs.setdefault("as_type", "generation")
        return _observe(**kwargs)

    class _LangfuseContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            get_client().update_current_trace(**kwargs)

        def update_current_observation(self, **kwargs: Any) -> None:
            get_client().update_current_generation(**kwargs)

    langfuse_context = _LangfuseContext()

except Exception:  # pragma: no cover
    def observe(*args: Any, **kwargs: Any):
        if args and callable(args[0]) and not kwargs:
            return args[0]

        def decorator(func):
            return func

        return decorator

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_observation(self, **kwargs: Any) -> None:
            return None

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


def flush_tracing() -> None:
    try:
        from langfuse import get_client

        get_client().flush()
    except Exception:
        pass

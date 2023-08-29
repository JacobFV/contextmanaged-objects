from __future__ import annotations

from abc import ABC
from contextlib import contextmanager
from functools import wraps
from typing import Any

from stringcase import snakecase
from contextmanaged_assign import assign
from inspect_mate_pp import get_regular_methods


class HasContextManagedFocus(ABC):
    @staticmethod
    def global_context() -> str:
        return 0

    @staticmethod
    def enable_threaded_context():
        import threading

        HasContextManagedFocus.global_context = lambda: threading.get_ident()

    @staticmethod
    def disable_threaded_context():
        HasContextManagedFocus.global_context = lambda: 0

    _STACKS_BY_CLS_BY_GLOBAL_CTX: dict[
        type[HasContextManagedFocus], dict[str, HasContextManagedFocus]
    ] = {}

    @classmethod
    def _STACK(cls) -> list[HasContextManagedFocus]:
        stack_by_global_ctx = cls._STACKS_BY_CLS_BY_GLOBAL_CTX.setdefault(cls, {})
        return stack_by_global_ctx.setdefault(
            HasContextManagedFocus.global_context(), []
        )

    @classmethod
    def current(cls) -> HasContextManagedFocus or None:
        """Returns the instance on top of the context stack, or None if the
        context stack is empty."""
        stack = cls._STACK()
        if not stack:
            return None
        return stack[-1]

    @contextmanager
    def as_current(self):
        """Context manager that puts the instance on top of its context stack"""

        stack = self._STACK()
        if stack and stack[-1] is self:
            yield
        else:
            stack.append(self)
            try:
                yield
            finally:
                tail = stack.pop()
                if tail is not self:
                    raise RuntimeError(
                        f"Context stack corrupted: expected {self} but got {tail}"
                    )


def make_current():
    """Decorator for instance methods when you want them to automatically
    put the instance on top of its context stack during invokation and
    remove after invokation is over."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            with self.as_current():
                return fn(self, *args, **kwargs)

        return wrapper

    return decorator


__all__ = ["make_current", "HasContextManagedFocus"]

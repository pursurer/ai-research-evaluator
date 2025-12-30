"""
Custom exceptions for AI Research Evaluator.
自定义异常类
"""


class EvaluatorException(Exception):
    """Base exception class for all evaluator errors."""

    pass


class DataLoadError(EvaluatorException):
    """Raised when data loading fails."""

    def __init__(self, message: str, path: str | None = None):
        self.path = path
        super().__init__(f"Data load error: {message}" + (f" (path: {path})" if path else ""))


class LLMAPIError(EvaluatorException):
    """Raised when LLM API call fails."""

    def __init__(self, provider: str, message: str, retry_after: int | None = None):
        self.provider = provider
        self.retry_after = retry_after
        super().__init__(f"[{provider}] {message}")


class ConfigurationError(EvaluatorException):
    """Raised when configuration is invalid or missing."""

    pass


class FuseTriggerError(EvaluatorException):
    """Raised when fuse mechanism is triggered (F_min < 3)."""

    def __init__(self, direction: str, f_min: float):
        self.direction = direction
        self.f_min = f_min
        super().__init__(
            f"Direction '{direction}' fused: F_min={f_min:.2f} < 3 (infeasible)"
        )

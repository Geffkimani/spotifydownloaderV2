import time
import logging
from functools import wraps
from typing import Callable, Any

def retry(attempts: int = 3, delay: int = 2, raise_on_fail: bool = True):
    """
    Retry a function on exception with optional delay and logging.

    Args:
        attempts (int): Number of retry attempts.
        delay (int): Delay in seconds between retries.
        raise_on_fail (bool): Raise the last exception after all retries or return None.

    Returns:
        Function wrapper.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for i in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"[Retry {i}/{attempts}] {func.__name__} failed: {e}")
                    if i < attempts:
                        time.sleep(delay)
                    else:
                        if raise_on_fail:
                            raise
                        else:
                            logging.error(f"{func.__name__} failed after {attempts} attempts. Suppressing exception.")
                            return None
        return wrapper
    return decorator

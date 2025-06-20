import time
import logging
from functools import wraps

def retry(attempts=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"Attempt {i + 1} failed: {str(e)}")
                    time.sleep(delay)
            raise Exception(f"Function {func.__name__} failed after {attempts} attempts.")
        return wrapper
    return decorator

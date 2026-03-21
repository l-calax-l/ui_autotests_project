import time
from typing import Any, Callable

from config.pydantic_config import settings


def wait_to_change(
    func: Callable[[], Any],
    timeout: float = settings.default_time_out,
    poll_interval: float = settings.poll_frequency,
    error_message: str = "Результат не получен за время таймаута",
    old_text: str = None,
) -> Any:
    """
    Ждет, пока func() вернет значение (не None, не False, не пустой список).
    Возвращает это значение.
    """
    start_time = time.time()
    last_exception = None

    while time.time() - start_time < timeout:
        try:
            result = func()
            if result is not None and result != old_text:
                return result
        except Exception as e:
            last_exception = e

        time.sleep(poll_interval)

    raise TimeoutError(f"{error_message}. Последняя ошибка: {last_exception}")

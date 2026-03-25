import logging
import os
import pickle

import allure
from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)


class CookieHelper:
    """Класс для работы с cookies в Selenium WebDriver.

    Позволяет сохранять и загружать cookies из файла с логированием и Allure-отчетами.
    """

    def __init__(self, driver: WebDriver, filename: str = "cookies.pkl") -> None:
        self.driver: WebDriver = driver
        self.cookies_dir: str = os.path.join(os.getcwd(), "cookies")
        self.cookies_file: str = os.path.join(self.cookies_dir, filename)
        self._ensure_cookies_dir()

    def _ensure_cookies_dir(self) -> None:
        """Создает директорию для cookies, если она не существует."""
        if not os.path.exists(self.cookies_dir):
            os.makedirs(self.cookies_dir)
            logger.info(f"Создана директория для cookies: {self.cookies_dir}")
            allure.attach(
                f"Создана директория: {self.cookies_dir}",
                name="Cookies directory created",
                attachment_type=allure.attachment_type.TEXT,
            )

    def check_cookies(self) -> bool:
        """Проверяет, существует ли файл с cookies."""
        with allure.step("Проверяет,существует ли файл с cookies."):
            exists = os.path.exists(self.cookies_file)
            logger.info(
                f"Проверка наличия файла cookies: {self.cookies_file} -> {exists}"
            )
            allure.attach(
                str(exists),
                name=f"File {self.cookies_file} exists",
                attachment_type=allure.attachment_type.TEXT,
            )
            return exists

    def save_cookies(self) -> None:
        """Сохраняет текущие cookies в файл."""
        try:
            cookies = self.driver.get_cookies()
            with open(self.cookies_file, "wb") as f:
                pickle.dump(cookies, f)
            logger.info(f"Сохранено {len(cookies)} cookies в {self.cookies_file}")
            allure.attach(
                f"Сохранено {len(cookies)} cookies в {self.cookies_file}",
                name="Cookies saved",
                attachment_type=allure.attachment_type.TEXT,
            )
        except Exception as e:
            logger.error(f"Ошибка при сохранении cookies: {e}")
            raise

    def load_cookies(self) -> None:
        """Загружает cookies из файла и обновляет страницу."""
        try:
            self.driver.delete_all_cookies()
            with open(self.cookies_file, "rb") as f:
                cookies = pickle.load(f)

            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    logger.error(f"Ошибка при добавлении cookie {cookie}: {e}")

            self.driver.refresh()
            loaded_cookies = len(self.driver.get_cookies())
            logger.info(f"Загружено {loaded_cookies} cookies")
            allure.attach(
                f"Загружено {loaded_cookies} cookies",
                name="Cookies loaded",
                attachment_type=allure.attachment_type.TEXT,
            )
        except FileNotFoundError:
            logger.warning(f"Файл cookies не найден: {self.cookies_file}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке cookies: {e}")
            raise

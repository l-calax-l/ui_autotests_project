import allure
from selenium.webdriver.common.by import By

from base.base_page import BasePage, logger
from config.links import Links


class AuthPage(BasePage):
    """Page Object страницы для проверки базовой авторизации."""

    PAGE_PATH = Links.AUTH_PAGE

    DISPLAY_IMAGE_BUTTON = (By.ID, "displayImage")

    SUCCESS_IMAGE = (By.TAG_NAME, "img")

    def login_with_basic_auth(self, login: str, password: str) -> None:
        url = Links.AUTH_SYSTEM_WINDOW.replace("http://", "").replace("https://", "")
        auth_url = f"https://{login}:{password}@{url}"

        with allure.step(
            f"Авторизация через Basic Auth на странице {self.__class__.__name__}"
        ):
            logger.info(f"Выполняется вход для пользователя: {login}")
            self.driver.get(auth_url)

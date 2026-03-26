import allure
import pytest

from base.base_test import BaseTest
from config.pydantic_config import settings


@allure.feature("Авторизация и сессии")
@allure.story("Работа с cookies")
class TestWithCookies(BaseTest):
    """Тестовый класс для проверки функционала сохранения/загрузки cookies."""

    @pytest.mark.smoke
    @allure.title("Проверка наличия cookies и авторизация")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_cookies(self):
        self.sql_page.open()

        check_cookies = self.cook_help.check_cookies()

        if check_cookies:
            self.cook_help.load_cookies()
        else:
            self.sql_page.perform_login()
            self.cook_help.save_cookies()

        current_name = self.sql_page.get_text(
            self.sql_page.LNK_USER, "Имя пользователя"
        )

        assert (
            settings.account_name == current_name
        ), f"Ожидалось '{settings.account_name}', получено '{current_name}'"

    @pytest.mark.smoke
    @allure.title("Проверка авторизации через cookies и открытие упражнений по SQL")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_auth_with_cookies(self):
        self.sql_page.open()

        self.cook_help.load_cookies()

        self.sql_page.click(self.sql_page.TAB_EXERCISE, "Упражнения по SQL")

        self.sql_page.click(self.sql_page.LNK_SELECT, "SELECT (обучающий этап)")

        list_exe_is_visible = self.sql_page.element_is_visible(
            self.sql_page.LNK_LIST_EXERCISE, "Список упражнений"
        )

        assert list_exe_is_visible, "Ссылки на список упражнений не видно"

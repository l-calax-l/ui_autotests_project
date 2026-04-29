import allure
import pytest

from base.base_test import BaseTest


@pytest.mark.website
@pytest.mark.auth
@allure.epic("Пользовательские взаимодействия")
class TestAuthPage(BaseTest):
    """Тестовый класс для проверки базовой авторизации."""

    @pytest.mark.smoke
    @allure.feature("Авторизация")
    @allure.story("Basic Authentication")
    @allure.title("Проверка базовой авторизации")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_basic_auth(self):

        self.auth_page.open()

        self.auth_page.scroll_to_element(
            self.auth_page.DISPLAY_IMAGE_BUTTON, "кнопка Display Image"
        )

        with allure.step("Нажать на Display Image"):
            self.auth_page.click(self.auth_page.DISPLAY_IMAGE_BUTTON, "Display Image")

        with allure.step(
            "Пройти авторизацию и проверить, что авторизация прошла успешно"
        ):
            self.auth_page.login_with_basic_auth("httpwatch", "httpwatch")

            assert self.auth_page.element_is_visible(
                self.auth_page.SUCCESS_IMAGE, "Изображение с авторизацией"
            ), "Изображение не загрузилось после авторизации"

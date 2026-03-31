import allure
import pytest

from base.base_test import BaseTest


@allure.feature("JavaScriptExecutor")
@allure.story("Снятие фокуса и проверка скролла")
class TestJsExecutor(BaseTest):
    """Тестовый класс для проверки тестов с JavaScriptExecutor."""

    @pytest.mark.regression
    @allure.title("JSExecutor: снятие фокуса и проверка скролла на SQL-ex")
    @allure.severity(allure.severity_level.MINOR)
    def test_js_executor(self, auth_on_sql_ex):
        with allure.step("Проверка наличия вертикального скролла на странице"):
            assert (
                self.sql_page.has_vertical_scroll()
            ), "Ожидалось, что на странице имеется вертикальный скролл"

        self.sql_page.move_to_exercise()

        with allure.step("Снятие фокуса с поля ввода SQL кода через JSExecutor"):
            text_input = self.sql_page.find_element(
                self.sql_page.FLD_CODE_EXERCISE,
                "Поле ввода SQL кода",
            )
            text_input.click()

            self.sql_page.blur_element(text_input)

            active = self.sql_page.driver.switch_to.active_element
            assert (
                active != text_input
            ), "Ожидалось, что фокус уйдёт с поля ввода SQL кода"

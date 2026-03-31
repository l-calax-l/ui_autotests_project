import allure
import pytest

from base.base_test import BaseTest


@pytest.mark.website
@pytest.mark.tabs
@allure.epic("Взаимодействие с элементами")
class TestTabs(BaseTest):
    """Тестовый класс для работы с вкладками и окнами."""

    @pytest.mark.smoke
    @allure.feature("Tabs & Windows")
    @allure.story("Открытие нескольких вкладок")
    @allure.title("Проверка открытия третьей вкладки")
    def test_new_tab(self):
        self.tabs_page.open()

        with allure.step("Переключиться в iframe и открыть вторую вкладку"):
            self.tabs_page.switch_to_frame(self.tabs_page.IFRAME_DEFAULT)
            self.tabs_page.click_new_tab_link()

        with allure.step("Перенести фокус на новую вкладку"):
            self.tabs_page.switch_to_last_window()

        with allure.step("Нажать на ссылку во второй вкладке"):
            self.tabs_page.click_new_tab_link()

        with allure.step("Убедиться, что открыто три вкладки"):
            count = self.tabs_page.get_windows_count()
            assert count == 3, f"Ожидалось 3 вкладки, но открыто {count}"

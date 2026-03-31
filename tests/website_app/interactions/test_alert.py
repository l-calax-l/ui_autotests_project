import allure
import pytest

from base.base_test import BaseTest


@pytest.mark.website
@pytest.mark.alerts
@allure.epic("Пользовательские взаимодействия")
class TestAlertPage(BaseTest):
    """Тестовый класс для проверки работы с Alert."""

    @pytest.mark.smoke
    @allure.feature("Работа с модальными окнами (Alerts)")
    @allure.story("Input Alert")
    @allure.title("Проверка отображения кастомного текста после ввода в Input Alert")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_input_alert(self):
        self.alert_page.open()

        custom_name = "Python Automation"

        with allure.step("Перейти на вкладку 'Input Alert'"):
            self.alert_page.click(
                self.alert_page.INPUT_ALERT_TAB, "Вкладка Input Alert"
            )

        with allure.step("Переключиться во фрейм и вызвать Alert"):
            self.alert_page.switch_to_frame(self.alert_page.IFRAME_INPUT)
            self.alert_page.click(self.alert_page.BUTTON_ALERT, "Кнопка вызова Alert")

        with allure.step("Заполнить данные в поле Alert и подтвердить"):
            self.alert_page.alert_send_keys(custom_name)
            self.alert_page.alert_accept()

        with allure.step("Проверить, что введенный текст отобразился на странице"):

            actual_text = self.alert_page.get_text(self.alert_page.RESULT_TEXT)
            assert (
                custom_name in actual_text
            ), f"Текст '{custom_name}' не найден в '{actual_text}'"

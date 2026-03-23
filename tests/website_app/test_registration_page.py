import allure
import pytest

from base.base_test import BaseTest
from data.data import RegPageData


@pytest.mark.website
@pytest.mark.registration
@allure.epic("Система управления доступом")  # Глобальная группа
@allure.feature("Регистрация и Авторизация")
class TestRegPage(BaseTest):

    @pytest.mark.regression
    @allure.story("Визуальная валидация формы")
    @allure.title("4.1 Проверка видимости полей и состояния кнопки Login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_4_1_login_form_initial_state(self):
        self.reg_page.open()

        with allure.step("Проверить видимость полей ввода"):
            username_is_visible = self.reg_page.element_is_visible(
                self.reg_page.FLD_USERNAME, "поле username"
            )
            password_is_visible = self.reg_page.element_is_visible(
                self.reg_page.FLD_PASSWORD, "поле password"
            )
            assert username_is_visible, "Поле username не отображается"
            assert password_is_visible, "Поле password не отображается"

        with allure.step("Проверить состояние кнопки Login"):
            login_button = self.reg_page.find_element(
                self.reg_page.BTN_LOGIN, "кнопка login"
            )
            assert not login_button.is_enabled(), "Кнопка должна быть задизейблена!"

    @pytest.mark.smoke
    @allure.story("Позитивные сценарии")
    @allure.title("4.2 Успешная авторизация с валидными данными")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_4_2_login_success_with_valid_data(self):
        self.reg_page.open()

        with allure.step("Ввести валидные данные"):
            self.reg_page.enter_reg_data(RegPageData.VALID)

        with allure.step("Нажать Login и дождаться загрузки"):
            self.reg_page.click(self.reg_page.BTN_LOGIN, "кнопка Login")
            self.reg_page.wait_until_invisible(self.reg_page.IMG_LOADING, "троббер")

        with allure.step("Проверить текст сообщения об успехе"):
            current_title = self.reg_page.get_text(
                self.reg_page.LBL_SUCCESS_MSG, "сообщение об успешной авторизации"
            )
            expected_title = "You're logged in!!"
            assert (
                expected_title in current_title
            ), f"Ожидалось сообщение {expected_title},получен {current_title}"

    @pytest.mark.parametrize('data',RegPageData.INVALID_LIST, ids=lambda d: d["username"])
    @pytest.mark.regression
    @pytest.mark.excel_data
    @allure.story("Негативные сценарии")
    @allure.title("4.3 Попытка входа с невалидными данными")
    @allure.severity(allure.severity_level.NORMAL)
    def test_4_3_login_failure_with_invalid_data(self, data):
        self.reg_page.open()

        with allure.step("Ввести невалидные данные"):
            self.reg_page.enter_reg_data(data)

        with allure.step("Нажать Login и дождаться загрузки"):
            self.reg_page.click(self.reg_page.BTN_LOGIN, "кнопка Login")
            self.reg_page.wait_until_invisible(self.reg_page.IMG_LOADING, "троббер")

        with allure.step("Проверить текст сообщения об ошибке"):
            current_title = self.reg_page.get_text(
                self.reg_page.LBL_ERROR_MSG, "сообщение об ошибке"
            )
            expected_title = "Username or password is incorrect"
            assert (
                expected_title in current_title
            ), f"Ожидалось сообщение {expected_title},получен {current_title}"

    @pytest.mark.regression
    @allure.story("Завершение сессии")
    @allure.title("4.4 Успешный выход из системы (Logout)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_4_4_logout_functionality(self, logged_in_session):
        with allure.step("Нажать кнопку Logout"):
            self.reg_page.click(self.reg_page.LNK_LOGOUT, "кнопка Logout")

        with allure.step("Проверить возврат к форме авторизации"):
            username_visible = self.reg_page.element_is_visible(
                self.reg_page.FLD_USERNAME, "поле username"
            )
            password_visible = self.reg_page.element_is_visible(
                self.reg_page.FLD_PASSWORD, "поле password"
            )
            assert (
                username_visible
            ), "После Logout поле Username не появилось на странице"
            assert (
                password_visible
            ), "После Logout поле Password не появилось на странице"

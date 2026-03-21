import allure
import pytest

from base.base_test import BaseTest
from data.data import BankLoginData, ManagerPageData


@pytest.mark.banking
@pytest.mark.manager
@allure.epic("Банковское приложение (XYZ Bank)")
class TestBankingPage(BaseTest):

    @pytest.mark.regression
    @allure.feature("Регистрация клиентов")
    @allure.story("Форма Sample Form")
    @allure.title("5.1. Регистрация нового пользователя с проверкой хобби")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_5_1_customer_registration_with_hobby(self):
        self.form_page.open()

        with allure.step("Поиск самого длинного хобби из списка"):
            longest_hobby = self.form_page.get_longest_hobby()
            expected_hobby = "Traveling"
            assert (
                longest_hobby == expected_hobby
            ), f"Ошибка при поиске хобби! Ожидалось '{expected_hobby}', получено '{longest_hobby}'"

        with allure.step("Заполнение формы регистрации"):
            self.form_page.fill_registration_form(
                BankLoginData.VALID, hobby="Sports", gender="Male", about=longest_hobby
            )
            self.form_page.click_register()

        with allure.step("Проверка сообщения об успешной регистрации"):
            message = self.form_page.get_text(
                self.form_page.LBL_SUCCESS_MSG, "сообщение об успешной регистрации"
            )
            expected_message = "registered successfully"
            assert (
                expected_message in message.lower()
            ), f"Регистрация не удалась! Ожидалось подтверждение '{expected_message}', но получено '{message}'"

    @pytest.mark.smoke
    @allure.feature("Администрирование (Manager)")
    @allure.story("Управление клиентами")
    @allure.title("5.2. Создание клиента через интерфейс менеджера")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_5_2_manager_add_customer(self):
        self.man_page.open()

        with allure.step("Переход к форме добавления клиента"):
            self.man_page.click_add_customer()

        with allure.step("Ввод данных нового клиента"):
            self.man_page.enter_data_and_send(ManagerPageData.VALID)

        with allure.step("Валидация системного Alert"):
            alert_message = self.man_page.grab_alert()
            expected_message = "Customer added successfully"
            assert (
                expected_message in alert_message
            ), f"Alert не содержит подтверждения! Ожидалось: '{expected_message}', получено: '{alert_message}'"

    @pytest.mark.smoke
    @allure.feature("Администрирование (Manager)")
    @allure.story("Управление счетами")
    @allure.title("5.2.1. Открытие счета для существующего клиента")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_5_2_1_manager_open_account(self, customer_data):
        self.man_page.click_open_account()

        with allure.step(f"Выбор клиента {customer_data} и валюты 'Dollar'"):
            self.man_page.select_customer(customer_data)
            self.man_page.select_currency("Dollar")
            self.man_page.click(self.man_page.BTN_SUBMIT)

        with allure.step("Валидация системного Alert о создании счета"):
            alert_msg = self.man_page.grab_alert()
            expected_msg = "Account created successfully"
            assert (
                expected_msg in alert_msg
            ), f"Счет не был создан! Ожидалось сообщение: '{expected_msg}', получено: '{alert_msg}'"

    @pytest.mark.smoke
    @allure.feature("Операции клиента (Customer)")
    @allure.story("Авторизация")
    @allure.title("5.3. Авторизация под клиентом")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_5_3_customer_login(self, customer_data):
        self.cust_page.open()

        with allure.step(f"Выбор клиента {customer_data['first_name']} из списка"):
            self.cust_page.select_your_name(customer_data)
            self.cust_page.click(self.cust_page.BTN_SUBMIT, "Login")

        with allure.step("Проверка приветствия на главной странице клиента"):
            check_user = self.cust_page.is_current_user(customer_data)
            full_name = f"{customer_data['first_name']} {customer_data['last_name']}"
            assert (
                check_user
            ), f"Ошибка авторизации! Ожидали увидеть приветствие для {full_name}"

    @pytest.mark.smoke
    @allure.feature("Администрирование (Manager)")
    @allure.story("Управление клиентами")
    @allure.title("5.4. Удаление клиента и проверка очистки базы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_5_4_delete_customer(self, customer_data):
        self.man_page.open()

        with allure.step("Перейти в список клиентов"):
            self.man_page.click(self.man_page.TAB_CUSTOMERS)

        with allure.step(f"Поиск клиента по имени: {customer_data['first_name']}"):
            self.man_page.search_customer(customer_data["first_name"])
            assert self.man_page.is_customer_in_table(
                customer_data["first_name"]
            ), f"Клиент {customer_data['first_name']} не найден в таблице перед удалением"

        with allure.step("Удалить клиента"):
            self.man_page.click_delete_customer(customer_data["first_name"])

        with allure.step("Очистить поиск и проверить отсутствие клиента"):
            self.man_page.search_customer()
            is_present = self.man_page.is_customer_in_table(customer_data["first_name"])
            assert (
                not is_present
            ), f"Ошибка! Клиент {customer_data['first_name']} все еще в таблице"

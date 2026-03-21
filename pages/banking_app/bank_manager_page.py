import allure
from selenium.webdriver.support import expected_conditions as EC

from base.base_page import BasePage
from config.links import Links


class BankManagerPage(BasePage):
    PAGE_PATH = Links.BANK_MANAGER_PAGE

    # --- Секция добавления клиента (Add Customer) ---
    TAB_ADD_CUSTOMER = ("css selector", "button[ng-click='addCust()']")
    FLD_FIRST_NAME = ("css selector", "input[ng-model='fName']")
    FLD_LAST_NAME = ("css selector", "input[ng-model='lName']")
    FLD_POST_CODE = ("css selector", "input[ng-model='postCd']")

    BTN_SUBMIT = ("css selector", "button[type='submit']")

    # --- Секция открытия счета (Open Account) ---
    TAB_OPEN_ACCOUNT = ("css selector", "button[ng-click='openAccount()']")
    SEL_CUSTOMER = ("id", "userSelect")
    SEL_CURRENCY = ("id", "currency")

    # --- Секция списка клиентов (Customers) ---
    TAB_CUSTOMERS = ("css selector", "button[ng-click='showCust()']")
    INPUT_SEARCH = ("css selector", "input[ng-model='searchCustomer']")
    STR_TABLE_ROWS = ("css selector", "table tbody tr")

    def DELETE_BUTTON_BY_NAME(self, name):
        return (
            "xpath",
            f"//td[contains(text(), '{name}')]/following-sibling::td/button[text()='Delete']",
        )

    # --- Методы для Add Customer ---
    def enter_data_and_send(self, data):
        with allure.step(f"Ввести данные клиента: {data['first_name']}"):
            self.send_keys(self.FLD_FIRST_NAME, data["first_name"], "имя")
            self.send_keys(self.FLD_LAST_NAME, data["last_name"], "фамилия")
            self.send_keys(self.FLD_POST_CODE, data["post_code"], "индекс")
            self.click(self.BTN_SUBMIT, "кнопка подтверждения")

    def click_add_customer(self):
        self.click(self.TAB_ADD_CUSTOMER, "вкладка Add Customer")

    # --- Методы для Open Account
    def click_open_account(self):
        with allure.step("Кликнуть на вкладку 'Open Account'"):
            self.wait.until(EC.element_to_be_clickable(self.TAB_OPEN_ACCOUNT)).click()

    def select_customer(self, customer_dict):
        full_name = f"{customer_dict['first_name']} {customer_dict['last_name']}"
        with allure.step(f"Выбрать клиента: {full_name}"):
            self.click(self.SEL_CUSTOMER, "список клиентов")
            self.select_by_text(self.SEL_CUSTOMER, full_name, "Customer")

    def select_currency(self, currency_value):
        with allure.step(f"Выбрать валюту: {currency_value}"):
            self.click(self.SEL_CURRENCY, "список валют")
            self.select_by_text(self.SEL_CURRENCY, currency_value, "Currency")

    # --- Общие методы ---
    def grab_alert(self):
        with allure.step("Перехватить alert и подтвердить"):
            alert = self.wait.until(EC.alert_is_present())
            message = alert.text
            alert.accept()
            return message

    def setup_account(self, data):
        self.click_open_account()
        self.select_customer(data)
        self.select_currency("Dollar")
        self.click(self.BTN_SUBMIT)
        self.grab_alert()

    # --- Удаление ---
    def search_customer(self, text=""):
        with allure.step(f"Поиск клиента по тексту: {text}"):
            self.find_element(self.INPUT_SEARCH).clear()
            self.find_element(self.INPUT_SEARCH).send_keys(text)

    def is_customer_in_table(self, name, timeout=None):
        with allure.step(f"Проверка наличия клиента '{name}' в таблице"):
            try:
                rows = self.find_elements(self.STR_TABLE_ROWS, timeout=timeout)
                for row in rows:
                    if name in row.text:
                        return True
            except Exception:
                return False
            return False

    def click_delete_customer(self, name):
        with allure.step(f"Нажать кнопку Delete для клиента: {name}"):
            locator = self.DELETE_BUTTON_BY_NAME(name)
            self.click(locator, f"кнопка Delete для {name}")

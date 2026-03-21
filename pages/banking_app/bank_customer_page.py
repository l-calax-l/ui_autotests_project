import allure

from base.base_page import BasePage
from config.links import Links
from utils.wait import wait_to_change


class BankCustomerPage(BasePage):

    PAGE_PATH = Links.BANK_CUSTOMER_PAGE

    # --- Логин ---
    SELECT_USER = ("id", "userSelect")
    BTN_SUBMIT = ("css selector", "button[type='submit']")
    LBL_LOGIN_ANCHOR = ("xpath", "//label[contains(text(),'Your Name')]")
    TXT_WELCOME_USER = ("css selector", "span.fontBig")

    LBL_BALANCE_VALUE = ("xpath", "//div[contains(., 'Balance')]//strong[2]")
    LBL_STATUS_MSG = ("xpath", "//span[@ng-show='message']")

    # --- Вкладки ---
    TAB_DEPOSIT = ("css selector", "button[ng-click='deposit()']")
    TAB_WITHDRAW = ("css selector", "button[ng-click='withdrawl()']")
    TAB_TRANSACTIONS = ("css selector", "button[ng-click='transactions()']")

    # --- Операции ---
    WAIT_DEPOSIT_FORM = ("xpath", "//label[contains(text(),'Amount to be Deposited')]")
    WAIT_WITHDRAW_FORM = ("xpath", "//label[contains(text(),'Amount to be Withdrawn')]")

    FLD_AMOUNT = ("css selector", "input[ng-model='amount']")

    # --- Секция транзакций ---
    TBL_HEADER = ("css selector", "thead")
    STR_TABLE_ROWS = ("css selector", "tr.ng-scope")
    CELL_DATA = ("css selector", "td[class='ng-binding']")
    BTN_RESET_TX = ("css selector", "button[ng-click='reset()']")
    BTN_BACK_TO_ACCOUNT = ("css selector", "button[ng-click='back()']")

    # --- Авторизация ---
    def select_your_name(self, customer_dict):
        name = f"{customer_dict['first_name']} {customer_dict['last_name']}"
        self.select_by_text(self.SELECT_USER, text=name)

    def is_current_user(self, customer_dict):
        full_name = f"{customer_dict['first_name']} {customer_dict['last_name']}"

        with allure.step(f"Проверить, что текущий пользователь: {full_name}"):
            try:
                self.wait.until(
                    lambda driver: full_name in self.get_text(self.TXT_WELCOME_USER),
                    message=f"Имя {full_name} не появилось в приветствии",
                )
                return True
            except:
                actual_text = self.get_text(self.TXT_WELCOME_USER)
                allure.attach(actual_text, name="Фактическое приветствие")
                return False

    def login_as_customer(self, data):
        with allure.step(f"Вход в кабинет клиента: {data['first_name']}"):
            self.open()

            self.select_your_name(data)
            self.click(self.BTN_SUBMIT, "кнопка Login")

    def get_balance(self):
        text = self.find_element(self.LBL_BALANCE_VALUE).text
        return int(text)

    def get_message(self):
        return self.find_element(self.LBL_STATUS_MSG).text

    def is_message_hidden(self):
        element = self.driver.find_element(*self.LBL_STATUS_MSG)
        return element.get_attribute("ng-hide") == "true" or not element.is_displayed()

    # --- Сценарии ---
    def make_deposit(self, amount):
        self.click(self.TAB_DEPOSIT, "Deposit")

        with allure.step(f"Ввод суммы {amount} и нажатие подтверждения"):
            self.find_element(self.WAIT_DEPOSIT_FORM, "сообщение amount")
            self.send_keys(self.FLD_AMOUNT, str(amount))
            self.click(self.BTN_SUBMIT, "отправить")

    def make_withdrawal(self, amount):
        self.click(self.TAB_WITHDRAW, "Withdraw")

        with allure.step(f"Ввод суммы {amount} и нажатие подтверждения"):
            self.find_element(self.WAIT_WITHDRAW_FORM, "сообщение amount")
            self.send_keys(self.FLD_AMOUNT, str(amount))
            self.click(self.BTN_SUBMIT, "отправить")

    def get_all_transactions_data(self):
        with allure.step("Сбор всех транзакций из таблицы"):
            rows = self.driver.find_elements(*self.STR_TABLE_ROWS)
            transactions = []

            for row in rows:
                cols = row.find_elements(*self.CELL_DATA)
                transactions.append({"amount": int(cols[1].text), "type": cols[2].text})
            return transactions

    def get_calculated_balance_from_table(self):
        data = self.get_all_transactions_data()
        actual_balance = 0

        for tx in data:
            if tx["type"] == "Credit":
                actual_balance += tx["amount"]
            elif tx["type"] == "Debit":
                actual_balance -= tx["amount"]

        return actual_balance

    # --- Wait's ---
    def wait_for_transactions_smart(self, expected_count=1):
        def get_rows():
            rows = self.driver.find_elements(*self.STR_TABLE_ROWS)
            return rows if len(rows) >= expected_count else None

        try:
            return wait_to_change(get_rows, timeout=2)
        except TimeoutError:
            self.driver.refresh()
            return wait_to_change(
                get_rows, error_message="Данные не появились после refresh"
            )

    def wait_for_balance(self, expected_value: int):
        with allure.step(f"Ожидание обновления баланса до {expected_value}"):
            return self.wait.until(
                lambda d: self.get_balance() == expected_value,
                message=f"Баланс не обновился до {expected_value}. Текущий: {self.get_balance()}",
            )

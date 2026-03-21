import random

import allure
import pytest

from base.base_test import BaseTest


@pytest.mark.banking
@pytest.mark.transaction
@allure.epic("Банковское приложение (XYZ Bank)")
@allure.feature("Операции клиента (Customer Transactions)")
class TestTransaction(BaseTest):

    @pytest.mark.smoke
    @allure.story("Пополнение счета (Deposit)")
    @allure.title("5.3.1. Успешное пополнение счета")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_5_3_1_deposit_success(self, auth_customer_with_account):
        expected_balance = 100321

        with allure.step(f"Внесение суммы {expected_balance}"):
            self.cust_page.make_deposit(expected_balance)
            current_message = self.cust_page.get_message()
            expected_message = "Deposit Successful"

            assert (
                current_message == expected_message
            ), f"Ожидалось сообщение '{expected_message}', но получено '{current_message}'"

        with allure.step("Проверка записи в таблице транзакций"):
            self.cust_page.click(self.cust_page.TAB_TRANSACTIONS)
            self.cust_page.wait_for_transactions_smart(expected_count=1)
            balance_from_table = self.cust_page.get_calculated_balance_from_table()

            assert (
                balance_from_table == expected_balance
            ), f"Сумма транзакций в таблице ({balance_from_table}) не совпадает с суммой пополнения ({expected_balance})"

    @pytest.mark.regression
    @allure.story("Пополнение счета (Deposit)")
    @allure.title("5.3.2. Неуспешное пополнение счета (сумма 0)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_5_3_2_deposit_zero(self, auth_customer_with_account):
        with allure.step("Попытка внести 0"):
            self.cust_page.make_deposit(0)

            assert (
                self.cust_page.is_message_hidden()
            ), "Ошибка! Сообщение об успехе отображается при депозите 0"

        with allure.step("Проверка отсутствия транзакции в истории"):
            self.cust_page.click(self.cust_page.TAB_TRANSACTIONS)
            transactions = self.cust_page.get_all_transactions_data()

            assert (
                len(transactions) == 0
            ), f"Ошибка! В истории найдено {len(transactions)} записей, хотя депозит 0 не должен фиксироваться"

    @pytest.mark.smoke
    @allure.story("Снятие средств (Withdrawl)")
    @allure.title("5.3.3. Успешное снятие средств")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_5_3_3_withdrawal_success(self, auth_customer_with_account):

        self.cust_page.make_deposit(1000)
        initial_balance = self.cust_page.get_balance()
        withdraw_amount = random.randint(1, initial_balance)

        with allure.step(f"Снятие суммы {withdraw_amount}"):
            self.cust_page.make_withdrawal(withdraw_amount)
            assert self.cust_page.get_message() == "Transaction successful"

        with allure.step("Проверка обновленного баланса"):
            assert self.cust_page.get_balance() == (initial_balance - withdraw_amount)

        with allure.step("Валидация типа транзакции (Debit) в истории"):
            self.cust_page.click(self.cust_page.TAB_TRANSACTIONS)
            self.cust_page.wait_for_transactions_smart(expected_count=2)
            transactions = self.cust_page.get_all_transactions_data()
            assert (
                transactions[-1]["amount"] == withdraw_amount
            ), f"Сумма последней транзакции в таблице не равна {withdraw_amount}"
            assert (
                transactions[-1]["type"] == "Debit"
            ), "Тип транзакции в таблице должен быть 'Debit'"

    @pytest.mark.regression
    @allure.story("Снятие средств (Withdrawl)")
    @allure.title("5.3.4. Неуспешное снятие (сумма больше баланса)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_5_3_4_withdraw_more_than_balance(self, auth_customer_with_account):
        large_amount = 1000000

        with allure.step(f"Попытка снять {large_amount} при недостаточном балансе"):
            self.cust_page.make_withdrawal(large_amount)
            expected_error = (
                "Transaction Failed. You can not withdraw amount more than the balance."
            )
            actual_error = self.cust_page.get_message()
            assert (
                actual_error == expected_error
            ), f"Ожидалась ошибка '{expected_error}', но получено '{actual_error}'"

        with allure.step("Проверка, что некорректная транзакция не попала в историю"):
            self.cust_page.click(self.cust_page.TAB_TRANSACTIONS)
            transactions = self.cust_page.get_all_transactions_data()
            found_bad_tx = any(tx["amount"] == large_amount for tx in transactions)
            assert (
                not found_bad_tx
            ), f"Критическая ошибка! Транзакция на {large_amount} была зафиксирована в истории, несмотря на нехватку средств"

    @pytest.mark.regression
    @allure.story("Целостность данных")
    @allure.title("5.3.5. Проверка синхронизации баланса с таблицей")
    @allure.severity(allure.severity_level.NORMAL)
    def test_5_3_5_balance_sync_check(self, auth_customer_with_account):
        self.cust_page.make_deposit(500)

        with allure.step("Получение баланса из интерфейса"):
            self.cust_page.wait_for_balance(500)
            balance_main = self.cust_page.get_balance()

        with allure.step("Расчет баланса по истории транзакций"):
            self.cust_page.click(self.cust_page.TAB_TRANSACTIONS)
            self.cust_page.wait_for_transactions_smart(expected_count=1)
            balance_table = self.cust_page.get_calculated_balance_from_table()
            assert (
                balance_main == balance_table
            ), f"Рассинхрон! Баланс в хедере ({balance_main}) не совпадает с расчетом по таблице ({balance_table})"

    @pytest.mark.regression
    @allure.story("Снятие средств (Withdrawl)")
    @allure.title("5.3.6. Снятие всех средств (в ноль)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_5_3_6_withdraw_all(self, auth_customer_with_account):
        self.cust_page.make_deposit(123)
        current_balance = self.cust_page.get_balance()

        with allure.step(f"Снятие полной суммы {current_balance}"):
            self.cust_page.make_withdrawal(current_balance)
            assert (
                self.cust_page.get_message() == "Transaction successful"
            ), "Не удалось снять всю сумму под ноль"
            final_balance = self.cust_page.get_balance()
            assert (
                final_balance == 0
            ), f"Ошибка! После снятия всей суммы баланс должен быть 0, но отображается {final_balance}"

    @pytest.mark.regression
    @allure.story("История операций")
    @allure.title("5.3.7. Очистка истории транзакций (Reset)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_5_3_7_reset_history(self, auth_customer_with_account):
        self.cust_page.make_deposit(100)
        self.cust_page.click(self.cust_page.TAB_TRANSACTIONS)
        self.cust_page.wait_for_transactions_smart(expected_count=1)

        with allure.step("Нажатие кнопки Reset в истории"):
            self.cust_page.click(self.cust_page.BTN_RESET_TX)
            transactions = self.cust_page.get_all_transactions_data()
            assert (
                len(transactions) == 0
            ), f"История не очистилась! В таблице осталось {len(transactions)} записей после нажатия Reset"

        with allure.step("Проверка обнуления баланса на главной странице"):
            self.cust_page.click(self.cust_page.BTN_BACK_TO_ACCOUNT)
            final_balance = self.cust_page.get_balance()
            assert (
                final_balance == 0
            ), f"Ошибка! После очистки истории баланс должен быть 0, но отображается {final_balance}"

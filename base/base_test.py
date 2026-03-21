import pytest

from pages.banking_app.bank_customer_page import BankCustomerPage
from pages.banking_app.bank_form_page import BankFormPage
from pages.banking_app.bank_manager_page import BankManagerPage
from pages.website_app.main_page import MainPage
from pages.website_app.reg_page import RegPage


class BaseTest:
    main_page: MainPage
    reg_page: RegPage
    form_page: BankFormPage
    man_page: BankManagerPage
    cust_page: BankCustomerPage

    @pytest.fixture(autouse=True)
    def setup(self, request, driver):
        request.cls.driver = driver
        request.cls.main_page = MainPage(driver)
        request.cls.reg_page = RegPage(driver)
        request.cls.form_page = BankFormPage(driver)
        request.cls.man_page = BankManagerPage(driver)
        request.cls.cust_page = BankCustomerPage(driver)

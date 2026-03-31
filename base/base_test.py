import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.banking_app.bank_customer_page import BankCustomerPage
from pages.banking_app.bank_form_page import BankFormPage
from pages.banking_app.bank_manager_page import BankManagerPage
from pages.sql_ex_app.sql_page import SqlPage
from pages.website_app.interactions.drop_page import DroppablePage
from pages.website_app.interactions.tabs_page import TabsPage
from pages.website_app.main.main_page import MainPage
from pages.website_app.main.reg_page import RegPage
from utils.cookies_helpers import CookieHelper


class BaseTest:
    """Базовый класс для всех тестов."""

    main_page: MainPage
    reg_page: RegPage
    form_page: BankFormPage
    man_page: BankManagerPage
    cust_page: BankCustomerPage
    drop_page: DroppablePage
    tabs_page: TabsPage

    sql_page: SqlPage
    cook_help: CookieHelper

    @pytest.fixture(autouse=True)
    def setup(self, request: pytest.FixtureRequest, driver: WebDriver) -> None:
        # --- WAY2 ---
        request.cls.driver = driver
        request.cls.main_page = MainPage(driver)
        request.cls.reg_page = RegPage(driver)
        request.cls.form_page = BankFormPage(driver)
        request.cls.man_page = BankManagerPage(driver)
        request.cls.cust_page = BankCustomerPage(driver)
        request.cls.drop_page = DroppablePage(driver)
        request.cls.tabs_page = TabsPage(driver)

        # --- SQL-EX ---
        request.cls.sql_page = SqlPage(driver)
        request.cls.cook_help = CookieHelper(driver)

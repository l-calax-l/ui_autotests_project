import allure
import pytest
from selenium import webdriver

from config.pydantic_config import settings
from data.data import ManagerPageData, RegPageData
from pages.banking_app.bank_customer_page import BankCustomerPage
from pages.banking_app.bank_manager_page import BankManagerPage
from pages.website_app.reg_page import RegPage


@pytest.fixture(scope="function", autouse=True)
def driver(request):
    options = webdriver.ChromeOptions()

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--incognito")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    if settings.headless:
        options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    request.cls.driver = driver

    yield driver

    driver.quit()


@pytest.fixture
def reg_page(driver):
    return RegPage(driver)


@pytest.fixture
def bank_customer_page(driver):
    return BankCustomerPage(driver)


@pytest.fixture(scope="function")
def bank_manager_page(driver):
    return BankManagerPage(driver)


@pytest.fixture(scope="function")
def logged_in_session(reg_page):

    reg_page.open()
    reg_page.enter_reg_data(RegPageData.VALID)
    reg_page.click(reg_page.BTN_LOGIN, "кнопка Login")
    reg_page.wait_until_invisible(reg_page.IMG_LOADING)

    yield reg_page

    if reg_page.driver.find_elements(*reg_page.LNK_LOGOUT):
        reg_page.click(reg_page.LNK_LOGOUT)


@pytest.fixture(scope="function")
def customer_data(bank_manager_page):
    with allure.step("Предусловие 1: Создать профиль пользователя"):
        bank_manager_page.open()
        bank_manager_page.click_add_customer()
        data = ManagerPageData.VALID
        bank_manager_page.enter_data_and_send(data)
        bank_manager_page.grab_alert()

    yield data

    with allure.step("Очистка: Удалить созданного клиента"):
        bank_manager_page.open()
        bank_manager_page.click(bank_manager_page.TAB_CUSTOMERS)

        bank_manager_page.search_customer(data["first_name"])

        if bank_manager_page.is_customer_in_table(data["first_name"], timeout=1):
            bank_manager_page.click_delete_customer(data["first_name"])
        else:
            allure.attach(
                "Клиент уже удален",
                name="Status",
                attachment_type=allure.attachment_type.TEXT,
            )


@pytest.fixture
def auth_customer_with_account(bank_manager_page, customer_data, bank_customer_page):
    with allure.step("Предусловие 2: Открыть счет"):
        data = customer_data.copy()
        bank_manager_page.setup_account(data)
    with allure.step("Предусловие 3: Зайти в аккаунт"):
        bank_customer_page.open()
        bank_customer_page.find_element(bank_customer_page.LBL_LOGIN_ANCHOR)
        bank_customer_page.select_your_name(data)
        bank_customer_page.click(bank_customer_page.BTN_SUBMIT)

    yield data


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver")

        if not driver and "questions" in item.funcargs:
            pass

        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Screenshot_{report.nodeid}",
                attachment_type=allure.attachment_type.PNG,
            )

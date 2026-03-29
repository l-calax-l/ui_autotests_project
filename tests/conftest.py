import allure
import pytest
from selenium import webdriver

from config.pydantic_config import settings
from data.data import ManagerPageData, RegPageData
from pages.banking_app.bank_customer_page import BankCustomerPage
from pages.banking_app.bank_manager_page import BankManagerPage
from pages.sql_ex_app.sql_page import SqlPage
from pages.website_app.reg_page import RegPage
from utils.cookies_helpers import CookieHelper
from utils.driver_factory import DriverFactory
from utils.logger import get_logger

logger = get_logger(__name__)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Браузер для запуска тестов")


@pytest.fixture(scope="function", autouse=True)
def driver(request):
    browser_name = request.config.getoption("--browser")
    if not browser_name:
        browser_name = getattr(settings, "browser", "chrome")

    logger.info(f"Инициализация WebDriver для браузера: {browser_name.upper()}")

    driver = DriverFactory.create_driver(
        browser_name=browser_name,
        is_headless=settings.headless,
        is_grid=settings.use_grid,
        grid_url=settings.selenium_remote_url
    )

    request.cls.driver = driver
    logger.info("WebDriver успешно запущен")

    yield driver

    logger.info("Завершение WebDriver")
    driver.quit()


@pytest.fixture(scope="function")
def reg_page(driver):
    logger.debug("Создание фикстуры RegPage")
    return RegPage(driver)


@pytest.fixture(scope="function")
def bank_customer_page(driver):
    logger.debug("Создание фикстуры BankCustomerPage")
    return BankCustomerPage(driver)


@pytest.fixture(scope="function")
def bank_manager_page(driver):
    logger.debug("Создание фикстуры BankManagerPage")
    return BankManagerPage(driver)


@pytest.fixture(scope="function")
def sql_page(driver):
    logger.debug("Создание фикстуры SqlPage")
    return SqlPage(driver)


@pytest.fixture(scope="function")
def cook_help(driver):
    logger.debug("Создание фикстуры CookieHelper")
    return CookieHelper(driver)


@pytest.fixture(scope="function")
def logged_in_session(reg_page):
    with allure.step("Предусловие: Логин в приложение"):
        logger.info("Предусловие: логин через RegPage")
        reg_page.open()
        reg_page.enter_reg_data(RegPageData.VALID)
        reg_page.click(reg_page.BTN_LOGIN, "кнопка Login")
        reg_page.wait_until_invisible(reg_page.IMG_LOADING)
        logger.info("Предусловие: логин успешно выполнен")

    yield reg_page

    logger.info("Очистка: попытка логаута")
    if reg_page.driver.find_elements(*reg_page.LNK_LOGOUT):
        reg_page.click(reg_page.LNK_LOGOUT)
        logger.info("Очистка: выполнен логаут")
    else:
        logger.info("Очистка: ссылка Logout не найдена, логаут пропущен")


@pytest.fixture(scope="function")
def customer_data(bank_manager_page):
    with allure.step("Предусловие 1: Создать профиль пользователя"):
        data = ManagerPageData.VALID
        logger.info(f"Предусловие 1: создаём профиль пользователя: {data}")
        bank_manager_page.open()
        bank_manager_page.click_add_customer()
        bank_manager_page.enter_data_and_send(data)
        bank_manager_page.grab_alert()
        logger.info("Предусловие 1: профиль пользователя успешно создан")

    yield data

    with allure.step("Очистка: Удалить созданного клиента"):
        logger.info("Очистка: попытка удаления созданного клиента")
        bank_manager_page.open()
        bank_manager_page.click(bank_manager_page.TAB_CUSTOMERS)

        bank_manager_page.search_customer(data["first_name"])

        if bank_manager_page.is_customer_in_table(data["first_name"], timeout=1):
            bank_manager_page.click_delete_customer(data["first_name"])
            logger.info(f"Очистка: клиент с именем {data['first_name']} успешно удалён")
        else:
            logger.info(
                f"Очистка: клиент с именем {data['first_name']} не найден, возможно уже удалён"
            )
            allure.attach(
                "Клиент уже удален",
                name="Status",
                attachment_type=allure.attachment_type.TEXT,
            )


@pytest.fixture(scope="function")
def auth_customer_with_account(bank_manager_page, customer_data, bank_customer_page):
    with allure.step("Предусловие 2: Открыть счет"):
        data = customer_data.copy()
        logger.info(f"Предусловие 2: открываем счёт для клиента: {data}")
        bank_manager_page.setup_account(data)
        logger.info("Предусловие 2: счёт для клиента успешно открыт")

    with allure.step("Предусловие 3: Зайти в аккаунт"):
        logger.info(f"Предусловие 3: логин в аккаунт для клиента: {data}")
        bank_customer_page.open()
        bank_customer_page.find_element(bank_customer_page.LBL_LOGIN_ANCHOR)
        bank_customer_page.select_your_name(data)
        bank_customer_page.click(bank_customer_page.BTN_SUBMIT)
        logger.info("Предусловие 3: клиент успешно вошёл в аккаунт")

    yield data


@pytest.fixture(scope="function")
def auth_on_sql_ex(sql_page, cook_help):
    with allure.step("Предусловие: авторизация на Sql-ex"):
        logger.info("Предусловие: начало авторизации на Sql-ex")

        sql_page.open()
        cookies_exist = cook_help.check_cookies()

        if cookies_exist:
            logger.info("Найдён файл cookies, выполняем вход по cookies")
            cook_help.load_cookies()
        else:
            logger.info(
                "Файл cookies не найден, выполняем обычный вход и сохраняем cookies"
            )
            sql_page.perform_login()
            cook_help.save_cookies()

        logger.info("Предусловие: авторизация успешно выполнена на Sql-ex")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        logger.error(f"Тест упал: {report.nodeid}")

        driver = item.funcargs.get("driver")

        if not driver and "questions" in item.funcargs:
            logger.debug(
                f"Скриншот не сделан для {report.nodeid}: драйвер отсутствует, "
                "специальный кейс 'questions'"
            )
            return

        if driver:
            logger.info(f"Снимаем скриншот для упавшего теста: {report.nodeid}")
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Screenshot_{report.nodeid}",
                attachment_type=allure.attachment_type.PNG,
            )
        else:
            logger.warning(
                f"Не удалось снять скриншот: драйвер не найден в funcargs для {report.nodeid}"
            )


def pytest_runtest_setup(item):
    logger.info("-" * 80)
    logger.info(f"START TEST: {item.nodeid}")
    logger.info("-" * 80)


def pytest_runtest_teardown(item):
    logger.info("-" * 80)
    logger.info(f"END TEST: {item.nodeid}")

import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from config.pydantic_config import settings
from utils.wait import wait_to_change


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver, settings.default_time_out, settings.poll_frequency
        )
        self.action = ActionChains(driver)

    def is_opened(self):
        with allure.step(f"Страница {self.PAGE_PATH} открыта"):
            self.wait.until(EC.url_contains(self.PAGE_PATH))

    def open(self):
        with allure.step(f"Открыть страницу {self.PAGE_PATH}"):
            self.driver.get(self.PAGE_PATH)
            self.is_opened()

    def refresh(self):
        self.driver.refresh()

    def get_current_url(self):
        return self.driver.current_url

    def make_screenshot(self, screenshot_name):
        allure.attach(
            body=self.driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG,
        )

    def find_element(self, locator, locator_name=None):
        with allure.step(f"Найти элемент '{locator_name or locator}'"):
            return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator, locator_name=None, timeout=None):
        with allure.step(f"Поиск всех элементов: {locator_name or locator}"):
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.visibility_of_all_elements_located(locator))

    def count_elements(self, locator, locator_name=None):
        with allure.step(
            f"Посчитать количество элементов по локатору {locator_name or locator}"
        ):
            return len(self.driver.find_elements(*locator))

    def scroll_to_element(self, locator, locator_name=None):
        with allure.step(f"Прокрутить до '{locator_name or locator}'"):
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )

    def click(self, locator, locator_name=None):
        with allure.step(f"Кликнуть на '{locator_name or locator}'"):
            self.wait.until(EC.element_to_be_clickable(locator)).click()

    def element_is_visible(self, locator, locator_name=None):
        with allure.step(f"Проверка: виден ли элемент '{locator_name or locator}'"):
            try:
                self.wait.until(EC.visibility_of_element_located(locator))
                return True
            except TimeoutException:
                return False

    def get_text(self, locator, locator_name=None):
        with allure.step(f"Получить текст из '{locator_name or locator}'"):
            return self.wait.until(EC.visibility_of_element_located(locator)).text

    def send_keys(self, locator, text, name=None):
        with allure.step(f"Печать текста '{text}' в {name or locator}"):
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(str(text))

    def select_by_text(self, locator, text, name=None):
        with allure.step(f"Выбрать {text} из списка '{name or locator}'"):

            select_element = self.wait.until(EC.element_to_be_clickable(locator))

            select = Select(select_element)
            select.select_by_visible_text(text)

    def wait_for_text_change(self, locator, old_text, timeout=None):
        with allure.step(
            f"Ожидание смены текста в {locator}. Старый текст: '{old_text}'"
        ):
            return wait_to_change(
                func=lambda: self.get_text(locator),
                old_text=old_text,
                timeout=timeout or settings.default_time_out,
                error_message=f"Текст элемента '{locator}' не изменился",
            )

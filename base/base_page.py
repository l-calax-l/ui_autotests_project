from typing import Optional, Union

import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from config.pydantic_config import settings
from utils.wait import wait_to_change
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """Базовый класс для всех Page Object страниц."""

    PAGE_PATH: str

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(
            driver, settings.default_time_out, settings.poll_frequency
        )
        self.action = ActionChains(driver)
        logger.debug(
            f"Инициализирована страница {self.__class__.__name__} "
            f"с URL '{self.PAGE_PATH}'"
        )

    def is_opened(self) -> None:
        with allure.step(f"Страница {self.PAGE_PATH} открыта"):
            logger.debug(f"Ожидание открытия страницы {self.PAGE_PATH}")
            self.wait.until(EC.url_contains(self.PAGE_PATH))

    def open(self) -> None:
        with allure.step(f"Открыть страницу {self.PAGE_PATH}"):
            logger.info(f"Открываем страницу {self.PAGE_PATH}")
            self.driver.get(self.PAGE_PATH)
            self.is_opened()

    def refresh(self) -> None:
        logger.info(f"Обновляем страницу {self.driver.current_url}")
        self.driver.refresh()

    def get_current_url(self) -> str:
        url = self.driver.current_url
        logger.debug(f"Текущий URL: {url}")
        return url

    def make_screenshot(self, screenshot_name: str) -> None:
        logger.info(f"Скриншот: {screenshot_name}")
        allure.attach(
            body=self.driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG,
        )

    def find_element(
        self, locator: tuple[str, str], locator_name: Optional[str] = None
    ) -> WebElement:
        name = locator_name or str(locator)
        with allure.step(f"Найти элемент '{name}'"):
            logger.debug(f"Поиск элемента '{name}' по локатору {locator}")
            return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(
        self,
        locator: tuple[str, str],
        locator_name: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> list[WebElement]:
        name = locator_name or str(locator)
        with allure.step(f"Поиск всех элементов: {name}"):
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            logger.debug(
                f"Поиск всех элементов '{name}' по локатору {locator}, timeout={timeout}"
            )
            return wait.until(EC.visibility_of_all_elements_located(locator))

    def count_elements(
        self, locator: tuple[str, str], locator_name: Optional[str] = None
    ) -> int:
        name = locator_name or str(locator)
        with allure.step(f"Посчитать количество элементов по локатору {name}"):
            count = len(self.driver.find_elements(*locator))
            logger.debug(f"Найдено {count} элементов по локатору '{name}' ({locator})")
            return count

    def scroll_to_element(
        self, locator: tuple[str, str], locator_name: Optional[str] = None
    ) -> None:
        name = locator_name or str(locator)
        with allure.step(f"Прокрутить до '{name}'"):
            logger.debug(f"Прокрутка до элемента '{name}' по локатору {locator}")
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )

    def click(
        self, locator: tuple[str, str], locator_name: Optional[str] = None
    ) -> None:
        name = locator_name or str(locator)
        with allure.step(f"Кликнуть на '{name}'"):
            logger.info(f"Клик по элементу '{name}' ({locator})")
            self.wait.until(EC.element_to_be_clickable(locator)).click()

    def element_is_visible(
        self, locator: tuple[str, str], locator_name: Optional[str] = None
    ) -> bool:
        name = locator_name or str(locator)
        with allure.step(f"Проверка: виден ли элемент '{name}'"):
            try:
                self.wait.until(EC.visibility_of_element_located(locator))
                logger.debug(f"Элемент '{name}' виден")
                return True
            except TimeoutException:
                logger.info(f"Элемент '{name}' НЕ появился за timeout")
                return False

    def get_text(
        self, locator: tuple[str, str], locator_name: Optional[str] = None
    ) -> str:
        name = locator_name or str(locator)
        with allure.step(f"Получить текст из '{name}'"):
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text
            logger.debug(f"Текст элемента '{name}' = '{text}'")
            return text

    def send_keys(
        self,
        locator: tuple[str, str],
        text: Union[str, int],
        name: Optional[str] = None,
    ) -> None:
        field_name = name or str(locator)
        with allure.step(f"Печать текста '{text}' в {field_name}"):
            logger.info(f"Ввод текста в '{field_name}': '{text}'")
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(str(text))

    def select_by_text(
        self, locator: tuple[str, str], text: str, name: Optional[str] = None
    ) -> None:
        field_name = name or str(locator)
        with allure.step(f"Выбрать {text} из списка '{field_name}'"):
            logger.info(f"Выбор значения '{text}' в селекте '{field_name}'")
            select_element = self.wait.until(EC.element_to_be_clickable(locator))
            select = Select(select_element)
            select.select_by_visible_text(text)

    def wait_for_text_change(
        self, locator: tuple[str, str], old_text: str, timeout: Optional[int] = None
    ) -> Union[str, None]:
        with allure.step(
            f"Ожидание смены текста в {locator}. Старый текст: '{old_text}'"
        ):
            logger.debug(
                f"Ожидание смены текста по локатору {locator} "
                f"со старого значения '{old_text}', timeout={timeout or settings.default_time_out}"
            )
            return wait_to_change(
                func=lambda: self.get_text(locator),
                old_text=old_text,
                timeout=timeout or settings.default_time_out,
                error_message=f"Текст элемента '{locator}' не изменился",
            )

    def blur_element(self, element: WebElement) -> None:
        with allure.step("Убрать фокус с элемента"):
            logger.debug(f"Попытка убрать фокус с элемента: '{element}'")
            self.driver.execute_script("arguments[0].blur();", element)

    def has_vertical_scroll(self) -> bool:
        with allure.step("Определить, есть ли вертикальный скролл на странице"):
            return self.driver.execute_script(
                "return document.documentElement.scrollHeight > "
                "document.documentElement.clientHeight;"
            )

import allure
import pytest

from base.base_test import BaseTest
from utils.wait import wait_to_change


@pytest.mark.website
@pytest.mark.mainpage
@allure.epic("Главная страница (Home Page)")
class TestHomePage(BaseTest):
    """Тестовый класс для проверки главной страницы сайта."""

    @pytest.mark.smoke
    @allure.feature("Отображение контента")
    @allure.story("Базовые блоки интерфейса")
    @allure.title("1.1. Проверка видимости основных блоков (Хедер, Футер, Курсы)")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_1_1_home_page_blocks_visibility(self):
        self.main_page.open()

        with allure.step("Проверить видимость ключевых блоков"):
            assert self.main_page.element_is_visible(
                self.main_page.HDR_MAIN, locator_name="хедер"
            ), f"Хедер с контактной информацией не отображается"

            assert self.main_page.element_is_visible(
                self.main_page.BTN_SLIDE_REGISTER, locator_name="кнопка регистрации"
            ), f"Кнопка регистрации не отображается"

            assert self.main_page.element_is_visible(
                self.main_page.FTR_MAIN, locator_name="футер"
            ), f"Футер не отображается"

            assert self.main_page.element_is_visible(
                self.main_page.BLOCK_COURSES, locator_name="список курсов"
            ), f"Список курсов не отображается"

    @pytest.mark.regression
    @allure.feature("Отображение контента")
    @allure.story("Контактные данные")
    @allure.title("1.2. Валидация контактов в хедере и футере")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_1_2_header_contacts_content(self):
        self.main_page.open()

        with allure.step("Проверить количество телефонов и наличие Skype/Email"):
            count_number = self.main_page.count_elements(
                self.main_page.LNK_PHONES, "номер телефона"
            )

            assert (
                count_number == 3
            ), f"Ожидалось 3 номера телефона, найдено {count_number}"

            assert self.main_page.find_element(
                self.main_page.LNK_SKYPE, "ссылка Skype"
            ), f"В хедере нет ссылки на skype"

            assert self.main_page.find_element(
                self.main_page.LNK_EMAIL, "email"
            ), f"В хедере нет ссылки на почту email"

        with allure.step("Проверить ссылки на социальные сети"):
            count_social = self.main_page.count_elements(
                self.main_page.LNK_SOCIALS, "ссылки на соц сети"
            )

            assert (
                count_social == 4
            ), f"Ожидалось 4 ссылки на соц.сети, найдено {count_social}"

    @pytest.mark.regression
    @allure.feature("Интерактивные виджеты")
    @allure.story("Слайдер курсов")
    @allure.title("1.3. Переключение слайдов кнопками Next/Prev")
    @pytest.mark.xfail(reason="Баг: Слайдер не переключается")
    def test_1_3_course_slider_navigation(self):
        self.main_page.open()
        self.main_page.scroll_to_element(
            self.main_page.TXT_ACTIVE_COURSE, "слайд с курсом"
        )

        with allure.step("Зафиксировать текущий заголовок курса"):
            self.main_page.make_screenshot("before_click_next")
            before_text = self.main_page.get_active_course_title()

        with allure.step("Нажать NEXT и проверить смену слайда"):
            self.main_page.click(self.main_page.BTN_NEXT)

            after_text = self.main_page.wait_for_text_change(
                self.main_page.TXT_ACTIVE_COURSE, before_text, timeout=2
            )
            assert before_text != after_text, "Слайдер застрял!"

        with allure.step("Нажать кнопку PREV и проверить возврат слайда"):
            self.main_page.click(self.main_page.BTN_PREV, "PREV_BUTTON")
            back_text = self.main_page.wait_for_text_change(
                self.main_page.TXT_ACTIVE_COURSE, after_text, timeout=2
            )
            assert back_text == before_text, "Слайдер застрял!"

    @pytest.mark.regression
    @allure.feature("Отображение контента")
    @allure.story("Контактные данные")
    @allure.title("1.4. Проверка футера и контактных данных (Адрес, Email, Телефоны)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_1_4_footer_contacts_content(self):
        self.main_page.open()
        with allure.step("Прокрутить страницу до футера"):
            self.main_page.scroll_to_element(self.main_page.FTR_MAIN, "футер")

        with allure.step("Проверить адрес и наличие контактных данных в футере"):
            assert self.main_page.element_is_visible(
                self.main_page.FTR_MAIN, locator_name="футер"
            )

            assert self.main_page.element_is_visible(
                self.main_page.FTR_LBL_ADDRESS, locator_name="адрес"
            )

            count_number = self.main_page.count_elements(
                self.main_page.FTR_LNK_PHONES, "телефоны"
            )

            count_email = self.main_page.count_elements(
                self.main_page.FTR_LNK_EMAILS, "email"
            )

            assert count_number == 2, f"Ожидалось 2 телефона, найдено {count_number}"
            assert count_email == 2, f"Ожидалось 2 адреса, найдено {count_email}"

    @pytest.mark.regression
    @allure.feature("Навигация и переходы")
    @allure.story("Верхнее меню")
    @allure.title("2. Проверка работы Sticky Header при скролле")
    @allure.severity(allure.severity_level.NORMAL)
    def test_2_sticky_header_visibility_on_scroll(self):
        self.main_page.open()
        with allure.step("Убедиться, что меню видно при открытии"):
            menu_is_visible = self.main_page.element_is_visible(
                self.main_page.NAV_STICKY_BAR, locator_name="меню навигации"
            )

            assert (
                menu_is_visible
            ), f"Меню навигации не отображается при открытии страницы"

        with allure.step("Скролл вниз и проверка фиксации меню"):
            self.main_page.scroll_to_element(self.main_page.FTR_MAIN, "футер")

            menu_is_visible_after = self.main_page.element_is_visible(
                self.main_page.NAV_STICKY_BAR, locator_name="меню навигации"
            )

            assert (
                menu_is_visible_after
            ), f"Меню навигации исчезло из области видимости после скролла"

    @pytest.mark.smoke
    @allure.feature("Навигация и переходы")
    @allure.story("Переход по разделам")
    @allure.title("3. Переход на страницу Lifetime Membership")
    @allure.severity(allure.severity_level.NORMAL)
    def test_3_navigation_to_lifetime_membership(self):
        self.main_page.open()
        with allure.step("Открыть меню All Courses и выбрать Lifetime Membership"):
            self.main_page.click(
                self.main_page.MENU_ALL_COURSES, locator_name="All courses"
            )

            self.main_page.click(
                self.main_page.ITEM_LIFETIME_COURSE, locator_name="Lifetime membership"
            )

        with allure.step("Проверить корректность URL и заголовка страницы"):
            current_url = self.main_page.get_current_url()
            expected_path = "lifetime-membership-club"
            assert (
                expected_path in current_url
            ), f"Ожидался '{expected_path}' в URL, получен '{current_url}'"

            current_title = self.main_page.get_text(
                self.main_page.LBL_PAGE_TITLE, "Названия курса"
            )
            expected_title = "LIFETIME MEMBERSHIP CLUB"
            assert (
                expected_title in current_title
            ), f"Заголовок не совпадает, ожидался {expected_title} получен {current_title}"

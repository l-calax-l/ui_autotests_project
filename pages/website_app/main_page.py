import allure

from base.base_page import BasePage
from config.links import Links


class MainPage(BasePage):
    """Page Object для главной страницы сайта."""

    PAGE_PATH = Links.BASE_PAGE

    # --- Хедер ---
    HDR_MAIN = ("css selector", "header#masthead")

    LNK_PHONES = ("xpath", '//a[contains(@href, "+1") or contains(@href, "+9")]')
    LNK_SKYPE = ("css selector", 'a[href*="skype"]')
    LNK_EMAIL = ("css selector", 'a[href*="mailto"]')
    LNK_SOCIALS = ("css selector", ".ast-header-social-1-wrap a")

    # --- Навигация и Меню ---
    NAV_STICKY_BAR = ("css selector", ".ast-header-sticked, .main-header-bar")
    MENU_ALL_COURSES = ("xpath", "//span[text()='All Courses']")
    ITEM_LIFETIME_COURSE = ("css selector", "#menu-item-27581")

    # Текст заголовка на целевых страницах (для ассертов)
    LBL_PAGE_TITLE = ("xpath", "//h1")

    # --- Слайдер и блоки курсов ---
    BLOCK_COURSES = ("css selector", ".elementor-element-94bce2e")
    BTN_SLIDE_REGISTER = ("css selector", ".elementor-slide-button")

    BTN_NEXT = ("css selector", ".swiper-button-next-c50f9f0")
    BTN_PREV = ("css selector", ".swiper-button-prev-c50f9f0")

    TXT_ACTIVE_COURSE = (
        "css selector",
        ".elementor-element-c50f9f0 .pp-info-box-title",
    )

    # --- Футер ---
    FTR_MAIN = ("css selector", '[data-elementor-type="footer"]')

    FTR_LBL_ADDRESS = ("xpath", "//li[.//i[contains(@class, 'fa-map-marker-alt')]]")
    FTR_LNK_PHONES = (
        "xpath",
        "//ul[@class='elementor-icon-list-items']//a[contains(@href, 'tel:')]",
    )
    FTR_LNK_EMAILS = (
        "xpath",
        "//ul[@class='elementor-icon-list-items']//a[contains(@href, 'mailto:')]",
    )

    def get_active_course_title(self) -> str:
        with allure.step("Получить текст активного курса"):
            return self.get_text(self.TXT_ACTIVE_COURSE)

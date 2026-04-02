from base.base_page import BasePage
from config.links import Links


class AlertPage(BasePage):
    """Page Object для страницы с Alerts."""

    PAGE_PATH = Links.ALERT_PAGE

    INPUT_ALERT_TAB = ("css selector", "a[href='#example-1-tab-2']")
    IFRAME_INPUT = ("css selector", "#example-1-tab-2 .demo-frame")
    BUTTON_ALERT = (
        "xpath",
        "//button[text()='Click the button to demonstrate the Input box.']",
    )
    RESULT_TEXT = ("id", "demo")

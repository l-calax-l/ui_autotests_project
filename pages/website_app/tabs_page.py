from base.base_page import BasePage
from config.links import Links


class TabsPage(BasePage):
    """Page Object страницы для работы с новыми вкладками/окнами."""

    NEW_BROWSER_TAB_LINK = ("link text", "New Browser Tab")
    IFRAME_DEFAULT = ("css selector", "#example-1-tab-1 .demo-frame")

    PAGE_PATH = Links.TABS_PAGE

    def click_new_tab_link(self):
        self.click(self.NEW_BROWSER_TAB_LINK, "New Browser Tab")

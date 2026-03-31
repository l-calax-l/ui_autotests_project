from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IEOptions


class DriverFactory:

    @staticmethod
    def create_driver(
        browser_name: str,
        is_headless: bool = False,
        is_grid: bool = False,
        grid_url: str = None,
    ):
        browser_name = browser_name.lower().strip()

        if browser_name == "chrome":
            options = ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--incognito")
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            if is_headless:
                options.add_argument("--headless")

        elif browser_name == "firefox":
            options = FirefoxOptions()
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            if is_headless:
                options.add_argument("--headless")

        elif browser_name == "edge":
            options = EdgeOptions()
            options.add_argument("--window-size=1920,1080")
            if is_headless:
                options.add_argument("--headless")

        elif browser_name == "ie":
            options = IEOptions()
            options.ignore_protected_mode_settings = True
            options.ignore_zoom_level = True
            options.require_window_focus = True

        else:
            raise ValueError(f"Браузер '{browser_name}' не поддерживается!")

        if is_grid:
            return webdriver.Remote(command_executor=grid_url, options=options)

        if browser_name == "chrome":
            return webdriver.Chrome(options=options)
        elif browser_name == "firefox":
            return webdriver.Firefox(options=options)
        elif browser_name == "edge":
            return webdriver.Edge(options=options)
        elif browser_name == "ie":
            return webdriver.Ie(options=options)

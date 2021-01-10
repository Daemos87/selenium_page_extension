from typing import Type, Optional
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from selenium_page_extension.bases import wait_interaction, logger


class WebElementWrapper :
    def __init__(self, driver: WebDriver, element: WebElement) :
        self.driver = driver
        self.element = element
        self._wait_interaction: WebDriverWait = WebDriverWait(driver, wait_interaction)

    def __getattr__(self, item) :
        return getattr(self.element, item)

    def click(self, retry_on_intercepted=False) :
        try :
            self._wait_interaction.until(
                lambda _ : self.element if self.element.is_displayed() and self.element.is_enabled() else None).click()
        except ElementClickInterceptedException as e :
            if retry_on_intercepted :
                logger.warning(e.msg)
                self.driver.execute_script("arguments[0].click()", self.element)
            else :
                logger.error(e.msg)
                raise

    def switch_to(self, page = None) -> Optional :
        if self.element.tag_name == 'iframe' :
            self.driver.switch_to.frame(self.element)
        else :
            raise ValueError(f"Cannot switch to a {self.element.tag_name}")
        if page :
            return page(self.driver)

    def reset_context(self) :
        self.driver.switch_to.default_content()

    def __enter__(self):
        self.switch_to()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset_context()

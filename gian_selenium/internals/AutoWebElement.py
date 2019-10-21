from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


@dataclass
class AutoWebElement(WebElement):
    by: By
    locator: str
    as_list: bool = False
    timeout: int = 10

    def __get__(self, instance, owner):
        if not instance:
            return self
        return WebDriverWait(instance.driver, self.timeout) \
            .until(lambda x: x.find_element(self.by, self.locator))

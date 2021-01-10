import configparser
import logging
from abc import ABC
from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from selenium_page_extension.bases import wait_presence
from selenium_page_extension.bases.WebElementWrapper import WebElementWrapper


class WebPage(ABC) :

    def __init__(self, driver: WebDriver) :
        self._driver: WebDriver = driver
        self._wait_presence: WebDriverWait = WebDriverWait(driver, wait_presence)

    def __getattribute__(self, item: str) :
        class_ref = super().__getattribute__('__class__')
        typ = class_ref.__annotations__.get(item, None)
        locator = class_ref.__dict__.get(item, None)
        message = f'cannot find element(s) identified by {locator} after {wait_presence} seconds timeout'

        # not a private member
        # and the member is initialized ( with a WebElement locator hopefully)
        if not item.startswith('_') and locator :
            if typ == WebElementWrapper :
                return WebElementWrapper(self._driver, super().__getattribute__('_wait_presence').until(
                    ec.presence_of_element_located(locator), message=message))
            elif typ == Tuple[WebElementWrapper] :
                return [WebElementWrapper(self._driver, el) for el in
                        super().__getattribute__('_wait_presence').until(ec.presence_of_all_elements_located(locator),
                                                                         message=message)]

        return super().__getattribute__(item)

from typing import Tuple
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium_page_extension.tests.fixtures.fake_page_fixture import fake_html
from selenium_page_extension.tests.fixtures.selenium_fixture import selenium_driver
from selenium_page_extension.bases.WebPage import WebPage
from assertpy import assert_that


class FakePage(WebPage) :
    """
    demo test webpage
    """
    element: WebElement = (By.ID, "button")
    elements: Tuple[WebElement] = (By.ID, "e")


class TestPage :
    """
    testing fakepage
    """
    def test_page(self, fake_html, selenium_driver) :
        """

        :param fake_html: url to the fake page to test
        :param selenium_driver: pytest fixture, return a chrome driverthat is automatically close after test
        :return:
        """
        selenium_driver.get(fake_html)
        fake_page = FakePage(selenium_driver)
        fake_page.element.click()
        assert_that(fake_page.element.get_attribute('textContent'),"Check testo bottone fake page").is_equal_to("premuto")

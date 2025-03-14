from typing import Tuple

import pytest
from assertpy import assert_that
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from selenium_page_extension import WebElementWrapper
from selenium_page_extension.decorators import webpage
from selenium.webdriver import Firefox


@webpage
class FakePage:
    """
        demo test webpage
    """
    element: WebElementWrapper = (By.ID, "button")
    elements: Tuple[WebElementWrapper] = (By.ID, "e")
    frame: WebElementWrapper = (By.ID, "frame")

    def click(self):
        self.element.click()


@webpage
class FakeFrame:
    element: WebElementWrapper = (By.ID, "button1")


@webpage
class GoogleQuery:
    searchBox: WebElementWrapper = (By.NAME, "q")
    acceptBtn: WebElementWrapper = (By.XPATH, "//form[@class='A28uDc']")
    cookieFrame: WebElementWrapper = (By.TAG_NAME, "iframe")
    resultQuery = (By.XPATH, "//span[contains(text(),{text})]")


@pytest.mark.chrome("--start-maximized")
@pytest.mark.firefox
class TestPage:

    @pytest.mark.parametrize('search_value', ['things', 'something'])
    def test_google(self, search_value: str, selenium_driver):
        selenium_driver.get("https://www.google.it")
        google = GoogleQuery(selenium_driver)
        with google.cookieFrame:
            google.acceptBtn.submit()
        google.searchBox.send_keys(search_value)
        selenium_driver.find_elements(google.resultQuery[0], google.resultQuery[1].format(text=search_value))
        google.searchBox.submit()
        assert_that(len(google.resultQuery)).is_greater_than(0)

    def test_page_click(self, fake_html, selenium_driver):
        """

        :param fake_html: url to the fake page to test
        :param selenium_driver: pytest fixture, return a chrome driver that is automatically closed after test
        :return:
        """
        selenium_driver.get(fake_html)
        fake_page = FakePage(selenium_driver)
        fake_page.click()
        assert_that(fake_page.element.get_attribute('textContent'), "Check testo bottone fake page").is_equal_to(
            "premuto")

    def test_can_get_multiple_element(self, fake_html, selenium_driver):
        selenium_driver.get(fake_html)
        fake_page = FakePage(selenium_driver)
        for el in fake_page.elements:
            print(el.get_attribute('textContent'))

    def test_cannot_switch_to_non_frame_element(self, fake_html, selenium_driver):
        selenium_driver.get(fake_html)
        fake_page = FakePage(selenium_driver)
        assert_that(fake_page.element.switch_to).raises(ValueError).when_called_with()

    def test_can_return_a_webpage(self, fake_html, selenium_driver):
        selenium_driver.get(fake_html)
        fake_page = FakePage(selenium_driver)
        assert_that(fake_page.frame.switch_to(FakeFrame)).is_instance_of(FakeFrame)

    def test_can_click_in_a_frame(self, fake_html, selenium_driver):
        selenium_driver.get(fake_html)
        fake_page = FakePage(selenium_driver)
        fake_frame = fake_page.frame.switch_to(FakeFrame)
        fake_frame.element.click()
        assert_that(fake_frame.element.get_attribute('textContent'), "Check testo bottone fake page").is_equal_to(
            "premuto")

    def test_can_click_in_a_frame_as_context_manager(self, fake_html, selenium_driver):
        selenium_driver.get(fake_html)
        fake_page = FakePage(selenium_driver)
        frame = FakeFrame(selenium_driver)
        with fake_page.frame:
            if isinstance(selenium_driver, Firefox):
                assert_that(lambda: frame.element).raises(TimeoutException).when_called_with()
            else:
                frame.element.click()
                assert_that(frame.element.get_attribute('textContent'), "Check testo bottone fake page").is_equal_to(
                    "premuto")

    def test_8(self):
        assert 8, 'problems'

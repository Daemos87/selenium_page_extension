import os

import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from gian_selenium.decorators.decorators import page
from gian_selenium.decorators.types import locator
from gian_selenium.internals.AutoWebElement import AutoWebElement


@pytest.fixture
def fake_html():
    frame_path = os.path.abspath("./frame.html")
    page_path = os.path.abspath("./page.html")

    fake_frame = """
    <html>
               <head>
               </head>
               <body>
                   <button id='button' onclick='document.getElementById("button").textContent="premuto";'> 
                    click me
                   </button>
               </body>
           </html>
    """
    fake_page = f"""
           <html>
               <head>
               </head>
               <body>
                   <iframe id='frame' src='{frame_path}'></iframe>
                   <button id='button' onclick='document.getElementById("button").textContent="premuto";'> 
                        click me
                   </button>
               </body>
           </html>
           """

    with open(f"{page_path}", "w") as pag, \
            open(f"{frame_path}", "w") as frame:
        pag.write(fake_page)
        frame.write(fake_frame)
    return page_path


class TestPage:
    driver: WebDriver

    @page
    class FakePage:
        frame: locator = (By.ID, "frame")
        element: locator = (By.ID, "button")

    @classmethod
    def setup_class(cls):
        cls.driver = Chrome(f"{os.path.abspath('../chromedriver.exe')}")

    @classmethod
    def teardown_class(cls):
        os.remove(f"{os.path.abspath('page.html')}")
        os.remove(f"{os.path.abspath('frame.html')}")
        cls.driver.quit()

    def test_page(self, fake_html):
        self.driver.get(fake_html)
        fake_page = self.FakePage(self.driver)
        # noinspection PyUnresolvedReferences
        fake_page.element.click()
        # noinspection PyUnresolvedReferences
        assert fake_page.element.get_attribute('textContent') == 'premuto'

    def test_autowebelement(self):
        assert isinstance(self.FakePage.element, AutoWebElement)
        print(self.FakePage.element)

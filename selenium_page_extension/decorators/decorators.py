from typing import Type

from selenium_page_extension.classes.WebPage import WebPage


def webpage(cls: Type[Type]) -> Type:
    return type(cls.__name__, (WebPage,), {**cls.__dict__})

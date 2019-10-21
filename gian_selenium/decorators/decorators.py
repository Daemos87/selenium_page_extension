from gian_selenium.decorators.types import locator
from gian_selenium.internals.AutoWebElement import AutoWebElement


def page(cls: type):
    for key, value in filter(lambda x: not x[0].startswith('_') and x[1] == locator,
                             cls.__annotations__.items()):
        setattr(cls, key, AutoWebElement(*cls.__dict__[key]))
    old_init = cls.__init__

    def _new_init(self, driver, *args, **kwargs):
        self.driver = driver
        old_init(self, *args, **kwargs)

    cls.__init__ = _new_init
    return cls

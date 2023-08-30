from typing import Self
from typing import ClassVar, Union

from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, WebDriverException, StaleElementReferenceException

from pydantic import BaseModel, ConfigDict


class Selector(BaseModel):
    """A selector for finding elements."""
    by: str
    value: str

    def __iter__(self) -> tuple[str, str]:
        return iter((self.by, self.value))


class Element(BaseModel):
    """Base class for all elements."""
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='forbid')

    element: WebElement
    selector: ClassVar[Union[Selector, None]] = None

    def __init__(self, **data):
        super().__init__(**data)
        self._html = self.get_html()

    def __hash__(self):
        return hash(self.element)
    
    @property
    def driver(self) -> WebDriver:
        return self.element.parent

    @classmethod
    def find(cls, driver: WebDriver):
        if not cls.selector:
            raise NotImplementedError('Element must have a selector to be found.')
        try:
            element = driver.find_element(*cls.selector)
            return cls(element=element)
        except NoSuchElementException as e:
            raise e
        
    @classmethod
    def find_all(cls, driver: WebDriver):
        if not cls.selector:
            raise NotImplementedError('Element must have a selector to be found.')
        elements = driver.find_elements(*cls.selector)
        if elements:
            return [cls(element=element) for element in elements]
        else:
            raise NoSuchElementException
    
    @classmethod
    def exists(cls, driver: WebDriver) -> bool:
        """Detect if an element exists on the page."""
        try:
            cls.find(driver=driver)
            return True
        except NoSuchElementException:
            return False
        except StaleElementReferenceException:
            return False
        
    def find_element(self, by: str, value: str) -> Self:
        element = self.element.find_element(by, value)
        return Element(element=element)
        
    def find_elements(self, by: str, value: str) -> list[Self]:
        elements = self.element.find_elements(by, value)
        if elements:
            return [Element(element=element) for element in elements]
        
    def get_attribute(self, attribute: str):
        return self.element.get_attribute(attribute)
    
    def click(self) -> None:
        self.element.click()

    def clear(self) -> None:
        self.element.clear()
    
    def scroll_to_top(self) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'start' });", self.element)

    def scroll_to_bottom(self) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'end' });", self.element)

    def send_keys(self, *value: str) -> None:
        self.element.send_keys(*value)

    def send_keys_with_emojis(self, message: str) -> None:
        """Send keys with emojis to an element. NOTE: You don't have to have emojis 
        in your message, it just adds the ability to add and send emoji characters
        to your message if you want to.
        """
        self.driver.execute_script("arguments[0].value = arguments[1]", self.element, message)

    def remove(self) -> None:
        """Remove an element from the DOM."""
        self.driver.execute_script("arguments[0].remove()", self.element)

    @property
    def driver(self) -> WebDriver:
        return self.element.parent

    @property
    def html(self) -> str:
        """Returns the innerHTML of the element. If the elements html has
        changed, """
        if self.html_has_changed():
            try:
                self.update_html()
            except WebDriverException as e:
                if not 'No node with that given id found' in str(e):
                    print(e)
        return self._html

    def update_html(self) -> None:
        self._html = self.get_html()

    def html_has_changed(self) -> bool:
        return self._html != self.get_html()

    def get_html(self) -> str:
        return self.element.get_attribute('outerHTML')

    @property
    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.html, 'html.parser')

    @property
    def text(self) -> str:
        return self.element.text

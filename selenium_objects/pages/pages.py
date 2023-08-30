import time
from typing import ClassVar, Type, Any

from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from pydantic import BaseModel, ConfigDict, model_validator


class Page(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    url: ClassVar[str]
    load_time: ClassVar[float] = 0
    driver: WebDriver

    @classmethod
    def bring(cls, driver: WebDriver, **params):
        url = cls.url
        if params:
            url = url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
        if not driver.current_url == url:
            driver.get(url)
        if cls.load_time:
            time.sleep(cls.load_time)
        return cls(driver=driver)

    def is_active(self) -> bool:
        return self.driver.current_url == self.url

    @property
    def html(self):
        return self.driver.find_element('tag name', 'html').get_attribute('outerHTML')
    
    @property
    def soup(self):
        return BeautifulSoup(self.html, 'html.parser')

    
class FormPage(Page):
    success_url: ClassVar[str]
    post_submit_wait_time: ClassVar[float] = 0


class DetailPage(Page):
    model: ClassVar[Type[Any]]
    instance: Any
    url: str

    @model_validator(mode='before')
    def autofill_url(cls, data):
        data['url'] = data['instance'].url if 'url' not in data else data['url']
        return data
    
    @model_validator(mode='before')
    def instance_type_check(cls, data):
        if not isinstance(data['instance'], cls.model):
            raise TypeError(f'Instance must be of type {cls.model.__name__}. Instance provided: {data["instance"]}')
        return data
    
    @classmethod
    def bring(cls, driver: WebDriver, instance: Any, **params):
        url = instance.url
        if params:
            url = url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
        if not driver.current_url == url:
            driver.get(url)
        if cls.load_time:
            time.sleep(cls.load_time)
        return cls(driver=driver, instance=instance)

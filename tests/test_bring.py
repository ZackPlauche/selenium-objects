from selenium import webdriver
from selenium_objects import Page

def test_bring():
    class GoogleSearchPage(Page):
        url = "https://google.com"

    driver = webdriver.Chrome()
    GoogleSearchPage.bring(driver)
    assert driver.url == GoogleSearchPage.url


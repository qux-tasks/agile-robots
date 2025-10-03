import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page):
    login = LoginPage(page)
    login.open()
    return login

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    yield page
    context.close()
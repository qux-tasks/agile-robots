import pytest
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage


def pytest_configure(config):
    html_option = config.option.htmlpath
    if html_option and not os.path.isabs(html_option):
        current_time = datetime.now().strftime("%H-%M %d-%m-%y")
        report_dir = "reports"
        new_filename = f"report-{current_time}.html"
        
        os.makedirs(report_dir, exist_ok=True)
        
        config.option.htmlpath = os.path.join(report_dir, new_filename)

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
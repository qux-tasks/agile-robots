from playwright.sync_api import Page, expect
from object_maps.login_page import Login_Page_Objects


class Users:
    ADMIN = ("Admin", "admin123")
    INVALID_PWD = ("Admin", "wrong_password")
    INVALID_LOGIN = ("wrong_login", "admin123")
    INVALID_CREDENTIALS = ("wrong_login", "wrong_password")
    LOGIN_CASE_SENSITIVITY = ("admin", "admin123")
    LOGIN_WHITESPACE_HANDLING = ("Admin ", "admin123")
    PWD_WHITESPACE_HANDLING = ("Admin", "admin123 ")
    PWD_CASE_SENSITIVITY = ("admin", "Admin123")
    EMPTY_USER = ("", "admin123")
    EMPTY_PASS = ("Admin", "")
    EMPTY_BOTH = ("", "")


class Messages:
    REQUIRED = "Required"
    INVALID_CREDENTIALS = "Invalid credentials"


class LoginPage:

    URL = "https://opensource-demo.orangehrmlive.com/"

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator(Login_Page_Objects.USER_INPUT_FIELD)
        self.password_input = page.locator(Login_Page_Objects.PWD_INPUT_FIELD)
        self.login_button = page.locator(Login_Page_Objects.LOGIN_BUTTON)
        self.error_message = page.locator(Login_Page_Objects.LOGIN_ERROR_MESSAGE)
        self.logo = page.locator(Login_Page_Objects.LOGO)
        self.branding = page.locator(Login_Page_Objects.BRANDING_IMAGE)
        self.login_title = page.locator(Login_Page_Objects.LOGIN_TITLE)
        self.credentials_info = page.locator(Login_Page_Objects.CREDENTIALS_INFO)
        self.forgot_password_link = page.locator(Login_Page_Objects.FORGOT_PWD_LINK)
        self.company_link = page.locator(Login_Page_Objects.COMPANY_LINK, has_text="OrangeHRM, Inc")
        self.footer = page.locator(Login_Page_Objects.FOOTER)
        self.username_group = page.locator(Login_Page_Objects.USERNAME_PWD_GROUP).nth(0)
        self.password_group = page.locator(Login_Page_Objects.USERNAME_PWD_GROUP).nth(1)
        self.username_required = self.username_group.locator(Login_Page_Objects.USERNAME_PWD_REQUIRED)
        self.password_required = self.password_group.locator(Login_Page_Objects.USERNAME_PWD_REQUIRED)
        self.all_required_messages = page.locator(Login_Page_Objects.USERNAME_PWD_REQUIRED)
        self.dashboard_header = page.locator(Login_Page_Objects.DASHBOARD_HEADER)

    def open(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def click_login_button(self):
        self.login_button.click()

    def click_forgot_password(self):
        self.forgot_password_link.click()

    def click_company_link(self):
        with self.page.expect_popup() as popup_info:
            self.company_link.click()
        return popup_info.value

    def enter_username(self, username: str):
        self.username_input.fill(username)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def expect_all_elements_visible(self):
        elements = [
            self.logo, 
            self.branding,
            self.login_title, 
            self.username_input,
            self.password_input, 
            self.login_button,
            self.forgot_password_link, 
            self.credentials_info, 
            self.footer, 
            self.company_link
        ]
        for el in elements:
            expect(el).to_be_visible()

    def expect_correct_attributes(self):
        expect(self.username_input).to_have_attribute("placeholder", "Username")
        expect(self.password_input).to_have_attribute("placeholder", "Password")
        expect(self.password_input).to_have_attribute("type", "password")
        expect(self.login_button).to_be_enabled()

    def expect_correct_texts(self):
        expect(self.login_title).to_contain_text("Login")
        expect(self.login_button).to_have_text(" Login ")
        expect(self.forgot_password_link).to_have_text("Forgot your password?")

    def expect_page_layout(self):
        self.expect_all_elements_visible()
        self.expect_correct_attributes()
        self.expect_correct_texts()

    def expect_error_message(self, text: str):
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(text)

    def expect_required_message_count(self, count: int):
        expect(self.all_required_messages).to_have_count(count)

    def expect_required_messages_visible(self):
        expect(self.all_required_messages).to_have_count(2)
        expect(self.username_required).to_have_text(Messages.REQUIRED)
        expect(self.password_required).to_have_text(Messages.REQUIRED)

    def expect_dashboard_visible(self):
        expect(self.dashboard_header).to_contain_text("Dashboard")

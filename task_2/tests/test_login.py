import pytest
from pages.login_page import LoginPage, Users, Messages
from object_maps.login_page import Login_Page_Objects
from playwright.sync_api import expect
import random
import string


@pytest.mark.ui
class TestLoginUI:

    def test_all_elements_present(self, login_page):
        login_page.expect_page_layout()

    def test_specific_elements_visibility(self, login_page):
        login_page.expect_all_elements_visible()
        assert login_page.username_input.input_value() == ""
        assert login_page.password_input.input_value() == ""

    def test_elements_attributes(self, login_page):
        login_page.expect_correct_attributes()

    def test_page_text_content(self, login_page):
        login_page.expect_correct_texts()
        login_page.credentials_info.locator(Login_Page_Objects.CREDENTIALS_INFO)
        expect(login_page.credentials_info).to_contain_text("Admin")
        expect(login_page.credentials_info).to_contain_text("Password")


@pytest.mark.auth
class TestLoginFunctionality:

    def test_successful_login(self, login_page):
        login_page.login(*Users.ADMIN)
        login_page.expect_dashboard_visible()

    def test_invalid_password(self, login_page):
        login_page.login(*Users.INVALID_PWD)
        login_page.expect_error_message(Messages.INVALID_CREDENTIALS)

    def test_invalid_login(self, login_page):
        login_page.login(*Users.INVALID_LOGIN)
        login_page.expect_error_message(Messages.INVALID_CREDENTIALS)

    def test_invalid_credentials(self, login_page):
        login_page.login(*Users.INVALID_CREDENTIALS)
        login_page.expect_error_message(Messages.INVALID_CREDENTIALS)

    def test_login_case_sensitivity(self, login_page):
        login_page.login(*Users.LOGIN_CASE_SENSITIVITY)
        login_page.expect_error_message(Messages.INVALID_CREDENTIALS)

    def test_pwd_case_sensitivity(self, login_page):
        login_page.login(*Users.PWD_CASE_SENSITIVITY)
        login_page.expect_error_message(Messages.INVALID_CREDENTIALS)

    def test_login_whitespace_handling(self, login_page):
        login_page.login(*Users.LOGIN_WHITESPACE_HANDLING)
        login_page.expect_error_message(Messages.INVALID_CREDENTIALS)

    def test_pwd_whitespace_handling(self, login_page):
        login_page.login(*Users.PWD_WHITESPACE_HANDLING)
        login_page.expect_error_message(Messages.INVALID_CREDENTIALS)

    def test_empty_username(self, login_page):
        login_page.login(*Users.EMPTY_USER)
        login_page.expect_required_message_count(1)
        expect(login_page.username_required).to_contain_text(Messages.REQUIRED)

    def test_empty_password(self, login_page):
        login_page.login(*Users.EMPTY_PASS)
        login_page.expect_required_message_count(1)
        expect(login_page.password_required).to_contain_text(Messages.REQUIRED)

    def test_empty_username_and_password(self, login_page):
        login_page.click_login_button()
        login_page.expect_required_messages_visible()

        login_page.enter_username("Admin")
        login_page.expect_required_message_count(1)
        expect(login_page.password_required).to_be_visible()
        expect(login_page.username_required).not_to_be_visible()

        login_page.enter_password("admin123")
        login_page.expect_required_message_count(0)

    def test_forgot_password_navigation(self, login_page):
        login_page.click_forgot_password()
        expect(login_page.page).to_have_url(
            "https://opensource-demo.orangehrmlive.com/web/index.php/auth/requestPasswordResetCode"
        )
        expect(login_page.page.locator(Login_Page_Objects.FORGOT_PWD_PAGE_LOCATOR)).to_have_text("Reset Password")

    def test_company_link_navigation(self, login_page):
        new_page = login_page.click_company_link()
        expect(new_page).to_have_url("https://www.orangehrm.com/")


@pytest.mark.security
class TestSecurity:

    def test_password_masking(self, login_page):
        login_page.enter_password("secret123")
        expect(login_page.password_input).to_have_attribute("type", "password")
        page_source = login_page.page.content()
        assert "secret123" not in page_source

    @pytest.mark.parametrize("length", [256, 1024, 5000])
    def test_long_strings_and_special_characters_do_not_crash(self, login_page, length):
        page = login_page.page

        base = "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
        long_username = base
        long_password = base
        login_page.login(long_username, long_password)

        assert not page.locator(Login_Page_Objects.TOPBAR_LOCATOR).is_visible()
        assert page.url.startswith(LoginPage.URL)

        if page.locator(Login_Page_Objects.ALERT_CONTENT_LOCATOR).count() > 0:
            msg = page.locator(Login_Page_Objects.ALERT_CONTENT_LOCATOR).inner_text()
            assert len(msg) < 500 


@pytest.mark.ux
class TestUX:

    def test_enter_key_submission(self, login_page):
        login_page.enter_username("Admin")
        login_page.enter_password("admin123")
        login_page.password_input.press("Enter")
        login_page.expect_dashboard_visible()

    def test_tab_navigation(self, login_page):
        login_page.username_input.focus()
        login_page.username_input.press("Tab")
        expect(login_page.password_input).to_be_focused()


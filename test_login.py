import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait


class LoginErrorMessageNotDisplayed(Exception):
    """Raised when the login error message is not displayed."""

    def __str__(self):
        return "The login error message is not displayed."


class LoginErrorMessageMismatch(Exception):
    """Raised when the login error message does not match the expected message."""

    def __init__(self, error_msg, expected_error_message):
        self.error_msg = error_msg
        self.expected_error_message = expected_error_message

    def __str__(self):
        return (
            f"The login error message is unrecognized: {self.error_msg}. "
            f"Expected: {self.expected_error_message}"
        )


class ErrorTypeNotFound(Exception):
    """Raised when the login error error message type is not found."""

    def __init__(self, error_type, expected_error_messages):
        self.error_type = error_type
        self.expected_error_messages = expected_error_messages

    def __str__(self):
        return (
            f"The error message type is not found: {self.error_type}. "
            f"Use one of the following types: {', '.join(self.expected_error_messages)}."
        )


class LogoutError(Exception):
    """Raised when errors occur during the logout process."""

    def __init__(self, original_exception):
        self.original_exception = original_exception

    def __str__(self):
        return f"An error occurred during logout: {self.original_exception}"


@pytest.fixture(scope="class")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture(scope="class")
def landing_page(driver):
    return LandingPage(driver)


@pytest.fixture(scope="class")
def home_page(driver):
    return HomePage(driver)


@pytest.fixture(scope="class")
def credentials():
    load_dotenv()
    hudl_email = os.getenv("HUDL_EMAIL")
    hudl_password = os.getenv("HUDL_PASSWORD")
    return hudl_email, hudl_password


class LandingPage:
    def __init__(self, driver):
        self.driver = driver

    def click_login_select(self):
        login_select = self.driver.find_element(
            By.CSS_SELECTOR, "[data-qa-id='login-select']"
        )
        login_select.click()

    def click_login_select_hudl(self):
        login_hudl = self.driver.find_element(
            By.CSS_SELECTOR, "[data-qa-id='login-hudl']"
        )
        login_hudl.click()


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_email(self, email):
        email_field = self.driver.find_element(By.ID, "email")
        email_field.send_keys(email)

    def enter_password(self, password):
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(password)

    def click_login(self):
        login_button = self.driver.find_element(By.ID, "logIn")
        login_button.click()

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def is_login_error_message(self, error_type):
        """
        Checks that the error message displayed on the login form matches
        the expected error message based on the given type.

        Args:
            driver: The Selenium WebDriver object instance.
            error_type (str): The type of error message to check.

        Returns:
            bool: True if the error message matches, False otherwise.
        """
        error_msg_selector = "[data-qa-id='undefined-text']"
        error_msg = WebDriverWait(self.driver, 10).until(
            visibility_of_element_located((By.CSS_SELECTOR, error_msg_selector))
        )
        if error_msg.is_displayed():
            expected_error_messages = {
                "email": "We don't recognize that email and/or password",
                "password": "We don't recognize that email and/or password",
                "empty": "Please fill in all of the required fields",
            }
            expected_error_message = expected_error_messages.get(error_type)
            if expected_error_message is None:
                raise ErrorTypeNotFound(error_type, expected_error_messages.keys())
            if error_msg.text != expected_error_message:
                raise LoginErrorMessageMismatch(error_msg.text, expected_error_message)
            else:
                return True
        else:
            raise LoginErrorMessageNotDisplayed()

    def login_and_check_error(self, email, password, error_type):
        """
        Login using the provided credentials and check for a specific error message.

        Args:
            email: The email to use for login.
            password: The password to use for login.
            error_type: The type of error to check for.

        Returns:
            True if the error message matches, False otherwise.
        """
        self.driver.get("https://www.hudl.com/login")

        # Login using the provided credentials
        self.login(email, password)

        # Check for the specified error
        return self.is_login_error_message(error_type)


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def is_logged_in(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-qa-id='webnav-usermenu-logout']")
            )
        )

    def logout(self):
        try:
            self.driver.get("https://www.hudl.com/logout")
            WebDriverWait(self.driver, 10).until(
                EC.url_matches("https://www.hudl.com/")
            )
        except (WebDriverException, TimeoutException) as e:
            raise LogoutError(e)


class TestLogin:
    def test_valid_login_from_the_landing_page(
        self, driver, landing_page, login_page, home_page, credentials
    ):
        """
        Tests a valid login from the landing page

        Args:
            driver: The Selenium WebDriver object instance.
        """
        # Unpack the credentials
        hudl_email, hudl_password = credentials

        driver.get("https://www.hudl.com/")

        # Go to the login page from the landing page
        landing_page.click_login_select()
        landing_page.click_login_select_hudl()

        # Submit the login form
        login_page.login(hudl_email, hudl_password)

        # Use the home page object to check login status
        assert home_page.is_logged_in()

        home_page.logout()

    def test_valid_login_from_the_login_page(
        self, driver, login_page, home_page, credentials
    ):
        """
        Test a valid login from the login page.

        Args:
            driver: The Selenium WebDriver object instance.
        """
        # Unpack the credentials
        hudl_email, hudl_password = credentials

        driver.get("https://www.hudl.com/login")

        # Submit the login form
        login_page.login(hudl_email, hudl_password)

        # Use the home page object to check login status
        assert home_page.is_logged_in()

        home_page.logout()

    def test_invalid_email(self, login_page, credentials):
        """
        Test the behavior of the login form when an invalid email is provided.
        Expects "We don't recognize that email and/or password" UI error message

        Args:
            driver: The Selenium WebDriver object instance.
        """
        # Unpack the credentials
        _, hudl_password = credentials

        # Login with an invalid email and a valid password
        assert login_page.login_and_check_error(
            email="invalid", password=hudl_password, error_type="email"
        )

    def test_invalid_password(self, login_page, credentials):
        """
        Test the behavior of the login form when an invalid password is provided.
        Expects "We don't recognize that email and/or password" UI error message

        Args:
            driver: The Selenium WebDriver object instance.
        """
        # Unpack the credentials
        hudl_email, _ = credentials

        # Login with a valid email and an invalid password
        assert login_page.login_and_check_error(
            email=hudl_email, password="invalid", error_type="password"
        )

    def test_empty_credentials(self, login_page):
        """
        Test the behavior of the login form when empty credentials are provided.
        Expects "Please fill in all of the required fields" UI error message

        Args:
            driver: The Selenium WebDriver object instance.
        """
        assert login_page.login_and_check_error(
            email="", password="", error_type="empty"
        )

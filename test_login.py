import configparser
import logging
import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginErrorMessageMismatch(Exception):
    """Raised when the login error message does not match the expected message."""

    def __init__(self, error_msg, expected_error_message):
        self.error_msg = error_msg
        self.expected_error_message = expected_error_message

    def __str__(self):
        error_message = (
            f"The login error message is unrecognized: {self.error_msg}. "
            f"Expected: {self.expected_error_message}"
        )
        logging.error(error_message)
        return error_message


class ErrorTypeNotFound(Exception):
    """Raised when the login error error message type is not found."""

    def __init__(self, error_type, expected_error_messages):
        self.error_type = error_type
        self.expected_error_messages = expected_error_messages

    def __str__(self):
        error_message = (
            f"The error message type is not found: {self.error_type}. "
            f"Use one of the following types: {', '.join(self.expected_error_messages)}."
        )
        logging.error(error_message)
        return error_message


class CheckLoginStatusError(Exception):
    """Raised when errors occur while checking the login status."""

    def __init__(self, original_exception):
        self.original_exception = original_exception

    def __str__(self):
        error_message = f"An error occurred while checking the login status: {self.original_exception}."
        logging.error(error_message)
        return error_message


class LoginError(Exception):
    """Raised when errors occur during the login process."""

    def __init__(self, original_exception):
        self.original_exception = original_exception

    def __str__(self):
        error_message = f"An error occurred during login: {self.original_exception}"
        logging.error(error_message)
        return error_message


class LogoutError(Exception):
    """Raised when errors occur during the logout process."""

    def __init__(self, original_exception):
        self.original_exception = original_exception

    def __str__(self):
        error_message = f"An error occurred during logout: {self.original_exception}"
        logging.error(error_message)
        return error_message


@pytest.fixture(scope="function")
def driver():
    """
    Fixture that sets up and tears down a WebDriver instance.

    Yields:
        A WebDriver instance.
    """
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def credentials():
    """
    Fixture that returns hudl credentials from the environment.

    Returns:
        Tuple: A tuple containing the HUDL email and password.
    """
    load_dotenv()
    hudl_email = os.getenv("HUDL_EMAIL")
    hudl_password = os.getenv("HUDL_PASSWORD")
    if hudl_email is None or hudl_password is None:
        raise EnvironmentError(
            "Required environment variables HUDL_EMAIL or HUDL_PASSWORD are not set!"
        )
    return hudl_email, hudl_password


@pytest.fixture(scope="function")
def config():
    """
    Fixture that returns URLs from the config file.

    Returns:
        Dict: A dictionary of Hudl.com URLs.
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    urls = {
        "LANDING_URL": config.get("URLs", "LANDING_URL"),
        "LOGIN_URL": config.get("URLs", "LOGIN_URL"),
        "LOGOUT_URL": config.get("URLs", "LOGOUT_URL"),
    }

    return urls


@pytest.fixture(scope="function")
def landing_page(driver):
    """
    Fixture for the landing page object.

    Args:
        driver (WebDriver): The WebDriver object used to interact with the browser.

    Returns:
        LandingPage: The landing page object.
    """
    return LandingPage(driver)


@pytest.fixture(scope="function")
def login_page(driver, config):
    """
    Fixture for the login page object.

    Args:
        driver (WebDriver): The WebDriver object used to interact with the browser.

    Returns:
        LoginPage: The login page object.
    """
    return LoginPage(driver, config)


@pytest.fixture(scope="function")
def home_page(driver, config):
    """
    Fixture for the home page object.

    Args:
        driver (WebDriver): The WebDriver object used to interact with the browser.

    Returns:
        HomePage: The home page object.
    """
    return HomePage(driver, config)


class LandingPage:
    def __init__(self, driver):
        self.driver = driver

    def click_login_dropdown(self):
        """
        Landing Page: Clicks on the login select element.
        """
        self.driver.find_element(By.CSS_SELECTOR, "[data-qa-id='login-select']").click()

    def select_hudl_from_dropdown(self):
        """
        Landing Page: Clicks on the Hudl button from the login select menu.
        """
        self.driver.find_element(By.CSS_SELECTOR, "[data-qa-id='login-hudl']").click()

    def go_to_login_page(self):
        """
        Landing Page: Navigates to the login page by clicking on the login
        select button and selecting the Hudl option.
        """
        self.click_login_dropdown()
        self.select_hudl_from_dropdown()
        WebDriverWait(self.driver, 10).until(EC.title_is("Log In"))


class LoginPage:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    def enter_email(self, email):
        """
        Login Page: Enter the given email into the email field.

        Args:
            email (str): The email to be entered.
        """
        self.driver.find_element(By.ID, "email").send_keys(email)

    def enter_password(self, password):
        """
        Login Page: Enter the given password into the password field.

        Args:
            password (str): The password to enter into the password field.
        """
        self.driver.find_element(By.ID, "password").send_keys(password)

    def click_login(self):
        """
        Login Page: Clicks the login button.
        """
        self.driver.find_element(By.ID, "logIn").click()

    def login(self, email, password):
        """
        Login Page: Logs in to Hudl using the provided email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Raises:
            LoginError: If there is an error during the login process.
        """
        try:
            WebDriverWait(self.driver, 10).until(EC.title_is("Log In"))
            self.enter_email(email)
            self.enter_password(password)
            self.click_login()
        except (WebDriverException, TimeoutException) as e:
            raise LoginError(e)

    def is_login_error_message(self, error_type):
        """
        Login Page: Checks that the error message displayed on the login form
        matches the expected error message based on the given type.

        Args:
            error_type (str): The type of error message to check.

        Returns:
            bool: True if the error message matches, False otherwise.
        """
        error_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-qa-id='undefined-text']")
            )
        )

        expected_error_messages = {
            "email": "We don't recognize that email and/or password",
            "password": "We don't recognize that email and/or password",
            "empty": "Please fill in all of the required fields",
        }

        expected_error_message = expected_error_messages.get(error_type)

        if not expected_error_message:
            raise ErrorTypeNotFound(error_type, expected_error_messages.keys())

        if error_msg.is_displayed() and error_msg.text == expected_error_message:
            return True
        else:
            raise LoginErrorMessageMismatch(error_msg.text, expected_error_message)

    def login_and_check_error(self, email, password, error_type):
        """
        Login Page: Login using the provided credentials and check for a
        specific error message.

        Args:
            email: The email to use for login.
            password: The password to use for login.
            error_type: The type of error to check for.

        Returns:
            True if the error message matches, False otherwise.
        """
        self.driver.get(self.config["LOGIN_URL"])

        # Login using the provided credentials
        self.login(email, password)

        # Check for the specified error
        return self.is_login_error_message(error_type)


class HomePage:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    def is_logged_in(self):
        """
        Home Page: Checks if the user is logged in by checking if the logout
        button is present.

        Raises:
            CheckLoginStatusError: If there is a WebDriverException or TimeoutException
            while checking the login status.

        Returns:
            bool: True if the logout button is present, False otherwise.
        """
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "[data-qa-id='webnav-usermenu-logout']")
                )
            )
        except (WebDriverException, TimeoutException) as e:
            raise CheckLoginStatusError(e)

    def logout(self):
        """
        Home Page: Logout the user from the application.

        Raises:
            LogoutError: If there is a WebDriverException or TimeoutException
            during the logout process.

        Returns:
            bool: True if the url matches LANDING_URL after logging
            out, False otherwise.
        """
        try:
            self.driver.get(self.config["LOGOUT_URL"])
            return WebDriverWait(self.driver, 10).until(
                EC.url_matches(self.config["LANDING_URL"])
            )
        except (WebDriverException, TimeoutException) as e:
            raise LogoutError(e)


class TestLogin:
    def test_valid_login_from_the_landing_page(
        self, driver, config, landing_page, login_page, home_page, credentials
    ):
        """
        Test a valid login from the landing page

        Args:
            driver: The Selenium WebDriver object instance.
            config: The local config dictionary.
            landing_page: The LandingPage object instance.
            login_page: The LoginPage object instance.
            home_page: The HomePage object instance.
            credentials: A tuple containing the HUDL email and password.
        """
        hudl_email, hudl_password = credentials
        driver.get(config["LANDING_URL"])
        landing_page.go_to_login_page()
        login_page.login(hudl_email, hudl_password)
        assert home_page.is_logged_in()
        home_page.logout()

    def test_valid_login_from_the_login_page(
        self, driver, config, login_page, home_page, credentials
    ):
        """
        Test a valid login from the login page.

        Args:
            driver: The Selenium WebDriver object instance.
            config: The local config dictionary.
            login_page: The LoginPage object instance.
            home_page: The HomePage object instance.
            credentials: A tuple containing the HUDL email and password.
        """
        hudl_email, hudl_password = credentials
        driver.get(config["LOGIN_URL"])
        login_page.login(hudl_email, hudl_password)
        assert home_page.is_logged_in()
        home_page.logout()

    def test_invalid_email(self, login_page, credentials):
        """
        Test the behavior of the login form when an invalid email is provided.

        Expects:
            "We don't recognize that email and/or password" UI error message

        Args:
            login_page: The LoginPage object instance.
            credentials: A tuple containing the HUDL email and password.
        """
        _, hudl_password = credentials

        # Login with an invalid email and a valid password
        assert login_page.login_and_check_error(
            email="invalid", password=hudl_password, error_type="email"
        )

    def test_invalid_password(self, login_page, credentials):
        """
        Test the behavior of the login form when an invalid password is provided.

        Expects:
            "We don't recognize that email and/or password" UI error message

        Args:
            login_page: The LoginPage object instance.
            credentials: A tuple containing the HUDL email and password.
        """
        hudl_email, _ = credentials

        # Login with a valid email and an invalid password
        assert login_page.login_and_check_error(
            email=hudl_email, password="invalid", error_type="password"
        )

    def test_empty_credentials(self, login_page):
        """
        Test the behavior of the login form when empty credentials are provided.

        Expects:
            "Please fill in all of the required fields" UI error message

        Args:
            login_page: The LoginPage object instance.
        """
        # Login with no email and no password
        assert login_page.login_and_check_error(
            email="", password="", error_type="empty"
        )

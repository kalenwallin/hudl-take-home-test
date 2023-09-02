import os

import chromedriver_binary  # Adds chromedriver binary to path
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope="function")
def driver():
    """
    A PyTest fixture that sets up and tears down the Selenium webdriver Chrome instance.

    Yields:
        A webdriver instance.
    """
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


class TestLogin:
    def login(self, driver, email=None, password=None):
        """
        Submits the login form using the provided email and password.

        Args:
            driver (Chrome): The Selenium WebDriver Chrome object instance.
            email: The email address to use for login. Defaults to the `HUDL_EMAIL` environment variable.
            password: The password to use for login. Defaults to the `HUDL_PASSWORD` environment variable.

        Raises:
            Exception: If the login page fails to load correctly.
        """
        # Make sure the login page is loaded correctly
        if self.test_login_page_ui(driver):
            # Load environment variables if necessary
            load_dotenv()
            if email is None:
                email = os.getenv("HUDL_EMAIL")
            if password is None:
                password = os.getenv("HUDL_PASSWORD")

            # Fill in the email
            email_field = driver.find_element(By.ID, "email")
            email_field.send_keys(email)

            # Fill in the password
            password_field = driver.find_element(By.ID, "password")
            password_field.send_keys(password)

            # Click the log in/continue button
            login_button = driver.find_element(By.ID, "logIn")
            login_button.click()
        else:
            raise Exception("Login page failed to load correctly")

    def assert_login(self, driver):
        """
        Asserts successful login if the log out anchor is in the DOM.

        Args:
            driver (Chrome): The Selenium WebDriver Chrome object instance.
        """
        # Wait for log out anchor in the DOM
        # If we can log out, we've successfully logged in
        assert WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-qa-id='webnav-usermenu-logout']")
            )
        )

    def test_valid_login_from_the_landing_page(self, driver):
        """
        Tests a valid login from the landing page

        Args:
            driver (Chrome): The Selenium WebDriver Chrome object instance.
        """
        driver.get("https://www.hudl.com/")

        # Click login dropdown
        login_select = driver.find_element(
            By.CSS_SELECTOR, "[data-qa-id='login-select']"
        )
        login_select.click()

        # Click Hudl
        login_hudl = driver.find_element(By.CSS_SELECTOR, "[data-qa-id='login-hudl']")
        login_hudl.click()

        # Login with valid default environment credentials
        self.login(driver)
        self.assert_login(driver)

    def test_valid_login_from_the_login_page(self, driver):
        """
        Test a valid login from the login page.

        Args:
            driver (Chrome): The Selenium WebDriver Chrome object instance.
        """
        driver.get("https://www.hudl.com/login")

        # Login with valid default environment credentials
        self.login(driver)
        self.assert_login(driver)

    def assert_login_error_message(self, driver, type):
        """
        Asserts that the error message displayed on the login form matches the expected error message based on the given type.

        Args:
            driver (Chrome): The Selenium WebDriver Chrome object instance.
            type (str): The type of error message to check.
        """
        error_msg_selector = "[data-qa-id='undefined-text']"
        error_msg = WebDriverWait(driver, 10).until(
            visibility_of_element_located((By.CSS_SELECTOR, error_msg_selector))
        )
        assert error_msg.is_displayed()
        error_messages = {
            "email": "We don't recognize that email and/or password",
            "password": "We don't recognize that email and/or password",
            "empty": "Please fill in all of the required fields",
        }
        try:
            assert error_msg.text == error_messages.get(type)
        except Exception as e:
            assert False, f"The login error message could not be confirmed: {e}"

    def test_invalid_email(self, driver):
        """
        Test the behavior of the login form when an invalid email is provided.
        Expects "We don't recognize that email and/or password" UI error message

        Args:
            driver (Chrome): The Selenium WebDriver Chrome object instance.
        """
        driver.get("https://www.hudl.com/login")

        # Login with an invalid email and valid default password
        self.login(driver, email="invalid")

        # Check for the invalid email error
        self.assert_login_error_message(driver, type="email")

    def test_invalid_password(self, driver):
        """
        Test the behavior of the login form when an invalid password is provided.
        Expects "We don't recognize that email and/or password" UI error message

        Args:
            driver (Chrome): The Selenium WebDriver Chrome object instance.
        """
        driver.get("https://www.hudl.com/login")

        # Attempt to login with a valid email and invalid password
        self.login(driver, password="invalid")

        # Check for the invalid password error
        self.assert_login_error_message(driver, type="password")

    def test_empty_credentials(self, driver):
        """
        Test the behavior of the login form when empty credentials are provided.
        Expects "Please fill in all of the required fields" UI error message

        Args:
            driver (Chrome): The Selenium WebDriver Chrome object instance.
        """
        driver.get("https://www.hudl.com/login")

        # Attempt to login with an empty email and password
        self.login(driver, email="", password="")

        # Check for the empty fields error
        self.assert_login_error_message(driver, type="empty")

    def test_login_page_ui(self, driver):
        """
        Test the login page user interface to load correctly.

        Args:
            driver (Chrome): The Selenium WebDriver Chrome object instance.

        Returns:
            True if all assertions pass
        """

        driver.get("https://www.hudl.com/login")

        # Assert title
        assert driver.title == "Log In"

        # Assert header
        header = driver.find_element(By.CSS_SELECTOR, ".page-title").text
        assert header == "Log In"

        # Assert labels
        email_label = driver.find_element(By.ID, "email-label").text
        assert email_label == "Email"

        password_label = driver.find_element(By.ID, "password-label").text
        assert password_label == "Password"

        # Assert inputs
        assert driver.find_element(By.ID, "email")
        assert driver.find_element(By.ID, "password")

        # Assert buttons
        login_button = driver.find_element(By.ID, "logIn")
        assert login_button.text == "Continue"

        forgot_password_button = driver.find_element(By.ID, "forgot-password")
        assert forgot_password_button.text == "Forgot Password"

        create_account_button_top = driver.find_element(By.ID, "nav-btn-page")
        assert create_account_button_top.text == "Create Account"

        create_account_button_bottom = driver.find_element(By.ID, "btn-show-signup")
        assert create_account_button_bottom.text == "Create Account"

        return True

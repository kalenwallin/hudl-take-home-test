<p align="center">
  <a href="https://github.com/kalenwallin/hudl-take-home-test">
    <img src="https://sc.hudl.com/favicon.svg" height="96">
    <h1 align="center">Hudl Interview Take-home Test</h3>
  </a>
</p>

<p align="center">A simple Hudl login test suite powered by Selenium.</p>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Developing Locally](#developing-locally)
  - [Getting started](#getting-started)
  - [Advanced Usage](#advanced-usage)
    - [Improve Testing Speeds](#improve-testing-speeds)
  - [Learn More](#learn-more)
- [Lessons Learned](#lessons-learned)

## Introduction

This repo contains a testing suite for the Hudl login system and seeks to fulfill the requirements of the **Quality Assurance Engineer II** interview take-home test.

## Developing Locally

> **Note:** The setup below is for a Windows environment.
> If you're using MacOS or Linux, the process may be the same. Please see the following guides for more information:
> - [Setting up Selenium on MacOS](https://gprivate.com/66hws)
> - [Setting up Selenium on Linux](https://gprivate.com/66hwt)

Make sure you have Chrome, ChromeDriver, and Python 3.9 installed:

- [Download Google Chrome](https://www.google.com/chrome/ "Download Google Chrome")
- [Download ChromeDriver](https://chromedriver.chromium.org/home "Download ChromeDriver")
- [Download Python 3.9](https://www.python.org/downloads/ "Download Python 3.9")

### Getting started

Clone the repo:

```bash
git clone https://github.com/kalenwallin/hudl-take-home-test
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the root directory with your credentials:

```plaintext
HUDL_EMAIL={Email}
HUDL_PASSWORD={Password}
```

All tests are located in `test_login.py` in the root directory. Run the test suite:

```bash
pytest
```

### Advanced Usage

#### Improve Testing Speeds

[Selenium encourages a fresh browser per test](https://www.selenium.dev/documentation/test_practices/encouraged/fresh_browser_per_test/ "Selenium encourages a fresh browser per test") as part of their [encouraged practices](https://www.selenium.dev/documentation/test_practices/encouraged/ "Selenium Encouraged Practices"). This can easily be achieved by setting fixture scopes to `function`, which is the default for this testing suite.

```python
@pytest.fixture(scope="function")
```

However, starting up and tearing down a browser per test method is computationally expensive and tacks on a lot of time to testing.

Since logging in is the only data change that will affect state, we just have to log out to avoid resetting the WebDriver instance. **To leverage this, set all fixture scopes to `class`.**

```python
@pytest.fixture(scope="class")
```

Doing so allows each fixture to remain active until all of `TestLogin`'s test methods are complete, thereby **increasing testing speeds by approximately 58.57%.**

### Learn More

To learn more about Python, Selenium, and PyTest, take a look at the following resources:

- [Python Documentation](https://docs.python.org/ "Learn more about using Python") - Learn more about using Python
- [Selenium Documentation](https://www.selenium.dev/ "Learn more about using Selenium") - Learn more about using Selenium
- [Selenium PyPi Documentation](https://pypi.org/project/selenium/ "Learn more about using Selenium with Python") - Learn more about using Selenium with Python
- [Selenium Best Practices](https://www.selenium.dev/documentation/test_practices/ "Selenium Best Practices") - Learn more about using Selenium in accordance with guidelines and recommendations from the Selenium Project.

---

## Lessons Learned

I picked up several best practices and troubleshooting tips through hands-on experience.

While structuring the project, I realized it's critical to set up a good .gitignore for test code. I excluded logs, reports, temp files, and the webdriver binary. This kept the repository history clean and repo size low.

On the coding side, I leveraged explicit WebDriverWait instead of sleep to synchronize with elements appearing on the page. This takes the guesswork out of waiting.

Additionally, I implemented robust exception handling and raising using try/except blocks and custom exceptions. This allowed me to catch flaky tests during the development stage when I thought I had the correct implementation.

Overall, through hands-on work, I learned techniques for best practices, synchronization, and error handling. Let me know if you need me to elaborate on any specific lessons from working on the automation project!

---

Made with [💖](https://kalenwallin.com/easter-egg "Woah, you found an Easter Egg!") in Lincoln, NE

[Kalen Wallin](https://github.com/kalenwallin/ "Kalen's GitHub Profile")

<p align="center">
  <a href="https://github.com/kalenwallin/hudltakehome">
    <img src="https://sc.hudl.com/favicon.svg" height="96">
    <h3 align="center">Hudl Interview Take-home Test</h3>
  </a>
</p>

<p align="center">A simple Hudl login test suite powered by Selenium.</p>

# Introduction

This repo contains a testing suite for the Hudl login system and seeks to fulfill the requirements of the **Quality Assurance Engineer II** interview take-home test.

# Developing Locally

Make sure you have Chrome, ChromeDriver, and Python 3.9 installed:

- [Download Google Chrome](https://www.google.com/chrome/ "Download Google Chrome")
- [Download ChromeDriver](https://chromedriver.chromium.org/home "Download ChromeDriver")
- [Download Python 3.9](https://www.python.org/downloads/ "Download Python 3.9")

## Getting started

Clone the repo:

```bash
git clone https://github.com/kalenwallin/hudl-takehome-test
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file with your credentials:

```plaintext
HUDL_EMAIL={Email}
HUDL_PASSWORD={Password}
```

Run the test suite:

```bash
pytest
```

## Advanced Usage

### Improve Testing Speeds

[Selenium encourages a fresh browser per test](https://www.selenium.dev/documentation/test_practices/encouraged/fresh_browser_per_test/ "Selenium encourages a fresh browser per test") as part of their [encouraged practices](https://www.selenium.dev/documentation/test_practices/encouraged/ "Selenium Encouraged Practices") which can easily be achieved by setting fixture scopes to `function`.

```python
@pytest.fixture(scope="function")
```

However, starting up and tearing down a browser per test is computationally expensive and tacks on a lot of time to testing. To bypass this, set all fixture scopes to `class`.

```python
@pytest.fixture(scope="class")
```

Doing so **increases testing speeds by approximately 58.57%**

## Learn More

To learn more about Python, Selenium, and PyTest, take a look at the following resources:

- [Python Documentation](https://docs.python.org/ "Learn more about using Python") - Learn more about using Python
- [Selenium Documentation](https://www.selenium.dev/ "Learn more about using Selenium") - Learn more about using Selenium
- [Selenium PyPi Documentation](https://pypi.org/project/selenium/ "Learn more about using Selenium with Python") - Learn more about using Selenium with Python
- [Selenium Best Practices](https://www.selenium.dev/documentation/test_practices/ "Selenium Best Practices") - Learn more about using Selenium in accordance with guidelines and recommendations from the Selenium Project.

---

# Lessons Learned

I picked up several best practices and troubleshooting tips through hands-on experience.

While structuring the project, I realized it's critical to set up a good .gitignore for test code. I excluded logs, reports, temp files, and the webdriver binary. This kept the repository history clean and repo size low.

On the coding side, I leveraged explicit WebDriverWait instead of sleep to synchronize with elements appearing on the page. This takes the guesswork out of waiting.

Additionally, I implemented robust exception handling and raising using try/except blocks and custom exceptions. This allowed me to catch flaky tests during the development stage when I thought I had the correct implementation.

Overall, through hands-on work, I learned techniques for best practices, synchronization, and error handling. Let me know if you need me to elaborate on any specific lessons from working on the automation project!

---

Made with [💖](https://kalenwallin.com/easter-egg "Woah, you found an Easter Egg!") in Lincoln, NE

[Kalen Wallin](https://github.com/kalenwallin/ "Kalen's GitHub Profile")

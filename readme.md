<p align="center">
  <a href="https://github.com/kalenwallin/hudltakehome">
    <img src="https://sc.hudl.com/favicon.svg" height="96">
    <h3 align="center">Hudl Interview Take-home Test</h3>
  </a>
</p>

<p align="center">A simple Hudl login test suite built with Selenium.</p>

# Introduction

This repo contains a testing suite for the Hudl login system and seeks to fulfill the requirements of the **Quality Assurance Engineer II** interview take-home test.

# Developing Locally

Make sure you have Chrome, ChromeDriver, and Python 3.9 installed:

* [Download Google Chrome](https://www.google.com/chrome/ "Download Google Chrome")
* [Download ChromeDriver](https://chromedriver.chromium.org/home "Download ChromeDriver")
* [Download Python 3.9](https://www.python.org/downloads/ "Download Python 3.9")

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

```
pytest
```

## Learn More

To learn more about Python, Selenium, and PyTest, take a look at the following resources:

* [Python Documentation](https://docs.python.org/ "Learn more about using Python") - Learn more about using Python
* [Selenium Documentation](https://www.selenium.dev/ "Learn more about using Selenium") - Learn more about using Selenium
* [Selenium PyPi Documentation](https://pypi.org/project/selenium/ "Learn more about using Selenium with Python") - Learn more about using Selenium with Python

---

# Lessons Learned

I picked up several best practices and troubleshooting tips through hands-on experience.

For example, I learned the importance of dependency management while configuring Selenium. Rather than checking in the Chromedriver binary, I used a Python library to download it dynamically based on the Chrome version. This avoided bloating the repo and prevented version mismatch errors down the line.

While structuring the project, I realized it's critical to set up a good .gitignore for test code. I excluded logs, reports, temp files, and anything generated during test runs. This kept the repository history clean.

On the coding side, I leveraged explicit WebDriverWait instead of sleep to synchronize with elements appearing on the page. This will make the tests far more stable across various environments.

Additionally, I implemented robust exception handling using try/except blocks. This allowed me to catch flaky tests during the development stage when I thought I had the correct implementation.

Overall, through hands-on work, I learned techniques for dependency management, Git best practices, synchronization, and error handling. Let me know if you need me to elaborate on any specific lessons from working on the automation project!

---

Made with 💖 in Lincoln, NE

[Kalen Wallin](https://github.com/kalenwallin/ "Kalen's GitHub Profile")

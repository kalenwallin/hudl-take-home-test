<p align="center">
  <a href="https://github.com/kalenwallin/hudltakehome">
    <img src="https://sc.hudl.com/favicon.svg" height="96">
    <h3 align="center">Hudl Interview Takehome Test</h3>
  </a>
</p>

<p align="center">A simple Hudl login test suite built with Selenium.</p>

# Introduction

This repo contains a testing suite for the Hudl login system and seeks to fulfill the requirements of the Quality Assurance Engineer I interview takehome test.

# Developing Locally

Make sure you have Chrome and Python 3.9 installed:

* [Download Google Chrome](https://www.google.com/chrome/ "Download Google Chrome")
* [Download Python 3.9](https://www.python.org/downloads/ "Download Python 3.9")

## Getting started

Clone the repo:

```bash
git clone https://github.com/kalenwallin/hudl-takehome-test
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

Made with 💖 in Lincoln, NE

[Kalen Wallin](https://github.com/kalenwallin/ "Kalen's GitHub Profile")

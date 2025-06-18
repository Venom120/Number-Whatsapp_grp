# WhatsApp Group Number Adder

This repository contains two methods for automating the process of adding numbers to a WhatsApp group.

## Screen Share Method

This method utilizes screen mirroring from a mobile device to a laptop and automates interactions using the `pyautogui` library.

**Key Characteristics:**
- Relies on screen mirroring and mouse/keyboard automation (`pyautogui`).
- Reads participant data from a Google Sheet via Google Drive API (`pydrive`, `pandas`).
- Updates a local CSV file (`Data/added.csv`) to keep track of added participants.
- Requires manual setup of screen mirroring and positioning of the WhatsApp "Add Participant" screen.

**Files:**
- [`screen share/main.ipynb`](screen/ share/main.ipynb): Jupyter notebook containing the automation logic.
- [`screen share/req.txt`](screen/ share/req.txt): Lists Python dependencies (`pydrive`, `pandas`, `csv`, `pyautogui`).
- [`screen share/client_secrets.json`](screen/ share/client_secrets.json): Google API client secrets for accessing Google Drive.

## Selenium Method

This method automates the process using WhatsApp Web and the `selenium` library for browser interaction.

**Key Characteristics:**
- Automates interactions directly within the WhatsApp Web interface using `selenium`.
- Reads participant data from a Google Sheet via Google Drive API (`pydrive`, `pandas`).
- Updates a local CSV file (`Data/added.csv`) to keep track of added participants.
- Requires configuration of browser options, user data directory, and executable path.
- More robust to screen layout changes compared to the screen share method.

**Files:**
- [`Selenium/main.ipynb`](Selenium/main.ipynb): Jupyter notebook containing the automation logic.
- [`Selenium/main.py`](Selenium/main.py): Python script version of the automation logic.
- [`Selenium/req.txt`](Selenium/req.txt): Lists Python dependencies (`pydrive`, `pandas`, `selenium`, `requests`, `webdriver-manager`, `ipykernel`).
- [`Selenium/client_secrets.json`](Selenium/client_secrets.json): Google API client secrets for accessing Google Drive.

Choose the method that best suits your needs and technical setup. The Selenium method is generally recommended for its robustness.
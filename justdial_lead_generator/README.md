# 📞 JustDial Lead Generator

This project is a **Python-based educational tool** demonstrating how to automate data extraction, parsing, and storage workflows using:
- **Selenium WebDriver** for browser automation
- **Google Sheets API** for structured data storage
- **Logging** for runtime diagnostics

⚠ **Disclaimer:**  
This repository is intended **solely for educational and personal learning purposes**.  
Scraping JustDial or any similar platform **without permission** may violate their Terms of Service and applicable laws.  
The author assumes **no responsibility** for any misuse of this code.

---

## 📚 Features

- Automated Chrome browser setup with **anti-bot tweaks** (educational example)
- Scrolling & dynamic content handling
- Extraction of:
  - Business Name
  - Contact Number(s)
  - Address
  - Ratings
  - Reviews Count
- **Google Sheets integration** for structured data export
- Local JSON backup
- Configurable logging to file and console
- Modular structure for easy maintenance

---
## 📂 Project Structure

```text
justdial_lead_generator/
│
├── scraper/
│ ├── main.py # Entry point
│ ├── justdial_scraper.py # Scraper logic
│ ├── utils.py # (Optional) helper functions
│ ├── init.py
│
├── sheets/
│ ├── sheets_service.py # Google Sheets API wrapper
│ ├── init.py
│
├── data/
│ ├── logs/ # Log output folder
│ └── scraper.log
│
├── tests/
│ ├── test_justdial_scraper.py # Pytest tests
│ ├── init.py
│
├── config/
│ ├── credentials.json # Google Service Account credentials
│
├── venv/ # Python virtual environment
├── .gitignore
└── README.md
```


---

## 🚀 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/justdial_lead_generator.git
cd justdial_lead_generator
```

### 2️⃣Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python -m scraper.main
```

### 3️⃣Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣Create a Service Account in Google Cloud Console

Enable:

- Google Sheets API

- Google Drive API

- Download the credentials JSON and save it to config/credentials.json

- Share your target Google Sheet with the Service Account email from the credentials file.

---

## 📊 Output
- Google Sheets: Data is appended to the specified sheet with headers.

- Local JSON: Results are saved in justdial_restaurants.json inside scraper/.

- Logs: Stored in data/logs/scraper.log.

 ## ⚠ Legal & Ethical Notice
- This code is not intended for commercial scraping or data harvesting.

- Respect the target website’s robots.txt, rate limits, and terms of service.

- Avoid high-frequency requests that could disrupt their services.

- Always seek permission before running automated scripts against any live service.

## 🛠 Tech Stack
- Python 3.10+

- Selenium WebDriver

- gspread (Google Sheets API)

- pytest (testing)

- logging (built-in Python module)

## 📌 Educational Goals
- This project is meant to demonstrate:

- Setting up Selenium with anti-bot configurations

- Navigating dynamic web pages

- Extracting structured data

- Writing to Google Sheets programmatically

- Managing Python project structure

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.





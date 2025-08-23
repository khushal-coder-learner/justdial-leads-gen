Installation
============

Requirements
------------

- Python >= 3.9
- Google Sheets API credentials (stored in ``config/credentials.json``)

Dependencies
------------

This project depends on:

- ``selenium`` (for browser automation and scraping)
- ``pytest`` (for testing)
- ``gspread`` (for Google Sheets integration)
- ``oauth2client`` (for Google API authorization)

Setup
-----

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/your-username/justdial-lead-generator.git
      cd lead-generator

2. Create and activate a virtual environment:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate   # Linux / macOS
      venv\Scripts\activate      # Windows

3. Install dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

Usage
=====

Running the Scraper
-------------------

To start scraping, run:

.. code-block:: bash

   python -m scraper.main

The scraper will fetch business leads (restaurants by default) from JustDial and
store the results in the ``data/`` directory (e.g., ``data/justdial_restaurants.json``).

Export to Google Sheets
-----------------------

If properly configured with Google Sheets API credentials in ``config/credentials.json``,
results can also be uploaded directly to a connected Google Sheet.

Testing
-------

Run tests with:

.. code-block:: bash

   pytest

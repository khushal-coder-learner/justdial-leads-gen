from scraper.justdial_scraper import JustDialScraper
from sheets.sheets_service import GoogleSheetWriter  # your sheets class
import json

if __name__ == "__main__":
    # Create driver (set headless=False if you want to see the browser)
    driver = JustDialScraper.create_chrome_driver(headless=True)
    scraper = JustDialScraper(driver, wait_time=10)

    # Google Sheets setup
    sheet_writer = GoogleSheetWriter(
        creds_path="config/credentials.json",  # path to your creds JSON
        sheet_name="Justdial Leads"         # your sheet name
    )

     # 🔹 Clear old sheet data and add headers
    sheet_writer.sheet.clear()
    sheet_writer.append_row(["Name", "Contact", "Address", "Rating", "Reviews"])

    try:
        url = "https://www.justdial.com/Mumbai/Restaurants"
        print(f"Loading {url} ...")
        scraper.load_page(url)
        print("Scrolling to load more listings ...")
        scraper.scroll_down(pause_time=2, max_scrolls=35)

        print("Extracting listings ...")
        listings = scraper.get_listings()
        print(f"Found {len(listings)} listings.")

        results = []
        sheet_rows = []  # batch for Google Sheets

        for idx, listing in enumerate(listings, 1):
            data = scraper.parse_listing(listing)
            print(f"{idx}. {data}")
            results.append(data)

            # Prepare row for Sheets
            sheet_rows.append([
                data["name"] or "",
                ", ".join(data["contact"]) if data["contact"] else "",
                data["address"] or "",
                data["rating"] or "",
                data["reviews"] or ""
            ])

        # Save locally as JSON
        with open("data/justdial_restaurants.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("Results saved to justdial_restaurants.json")

        # Write all rows to Google Sheets in one go
        if sheet_rows:
            sheet_writer.append_rows(sheet_rows)
            print(f"✅ {len(sheet_rows)} rows written to Google Sheets.")

    finally:
        driver.quit()

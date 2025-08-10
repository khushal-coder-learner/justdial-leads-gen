from justdial_scraper import JustDialScraper

if __name__ == "__main__":
    # Create driver (set headless=False if you want to see the browser)
    driver = JustDialScraper.create_chrome_driver(headless=False)
    scraper = JustDialScraper(driver, wait_time=10)

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
        for idx, listing in enumerate(listings, 1):
            data = scraper.parse_listing(listing)
            print(f"{idx}. {data}")
            results.append(data)

        # Optionally, save to JSON
        import json
        with open("justdial_restaurants.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("Results saved to justdial_restaurants.json")

    finally:
        driver.quit()
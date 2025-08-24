# File: test_justdial_scraper.py

"""JustDial Scraper (with anti-bot driver setup)."""

from justdial_lead_generator.scraper.logger import logger
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pytest


class JustDialScraper:
    """A scraper for extracting business listings and details from JustDial."""

    def __init__(self, driver: webdriver.Chrome, wait_time: int = 5):
        """
        Initialize the JustDialScraper.

        Args:
            driver (webdriver.Chrome): Selenium Chrome WebDriver instance.
            wait_time (int): Default wait time (in seconds) for elements to load.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_time)

    @staticmethod
    def create_chrome_driver(headless: bool = True, user_agent: str = None) -> webdriver.Chrome:
        """
        Create a Chrome WebDriver instance with anti-bot options.

        Args:
            headless (bool): Run Chrome in headless mode if True.
            user_agent (str, optional): Custom user-agent string.

        Returns:
            webdriver.Chrome: Configured Chrome WebDriver.
        """
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        # Tricks to avoid detection by anti-bot systems
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        options.add_argument("--log-level=3")
        if user_agent:
            options.add_argument(f"user-agent={user_agent}")
        else:
            # Default user-agent string
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            )

        driver = webdriver.Chrome(options=options)
        try:
            # Inject JavaScript to override properties that expose Selenium automation
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    window.navigator.chrome = {runtime: {}};
                    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                """
            })
        except Exception:
            pass
        return driver

    def load_page(self, url: str):
        """
        Load a given webpage in the browser.

        Args:
            url (str): The URL to load.
        """
        self.driver.get(url)
        time.sleep(0.5)  # Small wait to let page resources load

    def scroll_down(self, pause_time=1, max_scrolls=30):
        """
        Scroll down the page multiple times to load dynamic content.

        Args:
            pause_time (int): Delay between scrolls in seconds.
            max_scrolls (int): Maximum number of scroll actions to perform.
        """
        actions = ActionChains(self.driver)
        for i in range(max_scrolls):
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(pause_time)

    def get_listings(self):
        """
        Retrieve listing elements from the page.

        Returns:
            list: A list of Selenium WebElements representing listings.
        """
        try:
            return self.driver.find_elements(
                By.CSS_SELECTOR, 'div.resultbox_info, div.store-details.sp-detail-card'
            )
        except Exception as e:
            logger.error(f"Error finding listings: {e}")
            return []

    def parse_listing(self, listing):
        """
        Extract structured information from a single listing element.

        Args:
            listing (WebElement): A Selenium element representing a business listing.

        Returns:
            dict: Dictionary containing business details (name, address, rating, reviews, contact).
        """
        return {
            'name': self._safe_text(listing, 'h3, .resultbox_title_anchorbox h3'),
            'address': self._safe_text(listing, 'div.locatcity, span.cont_fl_addr'),
            'rating': self._safe_text(listing, 'li.resultbox_totalrate, span.green-box'),
            'reviews': self._safe_text(listing, 'li.resultbox_countrate, span.total-rate'),
            'contact': self._extract_contact(listing)
        }

    def _extract_contact(self, listing):
        """
        Extract contact numbers from a listing element.

        This method attempts multiple strategies:
        1. Direct inline numbers.
        2. Clicking "Show Number" if present.
        3. Extracting from modal popups (if numbers appear inside modals).

        Args:
            listing (WebElement): A Selenium element representing a business listing.

        Returns:
            list: List of contact numbers as strings.
        """
        contacts = []
        try:
            # First try: contact directly visible on the page
            contacts = self._extract_inline_contact(listing)
            if contacts:
                return contacts

            # Second try: look for "Show Number" button
            try:
                show_elem = listing.find_element(
                    By.XPATH, './/*[contains(text(), "Show Number") or contains(text(), "SHOW NUMBER")]'
                )
            except NoSuchElementException:
                show_elem = None

            if show_elem:
                self.driver.execute_script("arguments[0].click();", show_elem)
                contacts = self._extract_inline_contact_link(listing)
                if contacts:
                    return contacts

                # Third try: sometimes number opens inside a modal popup
                try:
                    modal = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'section.jd_modal, div.jd_modal_content'))
                    )
                    contacts = self._extract_modal_contacts(modal)
                    self._close_modal(modal)
                except TimeoutException:
                    contacts = []
        except Exception as e:
            logger.error(f"Error extracting contact: {e}")
        if len(contacts) == 0:
            logger.error(f"No contact found.")
        return contacts

    def _extract_inline_contact(self, listing):
        """
        Extract inline contact number (if directly visible) from a listing.

        Args:
            listing (WebElement): The listing element.

        Returns:
            list: List containing one phone number or empty list.
        """
        try:
            span = listing.find_element(By.XPATH, './/span[contains(@class, "callcontent")]')
            text = span.text.strip()
            # Ignore placeholder "Show Number" text
            if text and text.lower() != 'show number':
                return [text]
        except Exception:
            pass
        return []

    def _extract_inline_contact_link(self, listing):
        """
        Extract contact number from a clickable 'Show Number' link.

        This waits for the contact link (`tel:`) to appear after clicking.

        Args:
            listing (WebElement): The listing element.

        Returns:
            list: List of extracted phone numbers or empty list.
        """
        try:
            # Click "Show Number" button if it exists
            try:
                show_number_btn = listing.find_element(By.XPATH, './/a[contains(text(), "Show Number")]')
                self.driver.execute_script("arguments[0].click();", show_number_btn)
                time.sleep(1)
            except NoSuchElementException:
                pass  # No button → maybe already visible

            # Wait for a phone number link to appear
            contact_elem = WebDriverWait(listing, 5).until(
                EC.presence_of_element_located((By.XPATH, './/a[starts-with(@href, "tel:")]'))
            )

            href = contact_elem.get_attribute('href')
            if href:
                return [href.split(':', 1)[-1].strip()]
        except TimeoutException:
            print("Contact number not loaded in time.")
        except NoSuchElementException:
            pass
        return []

    def _extract_modal_contacts(self, modal_element):
        """
        Extract contact numbers from a modal popup.

        Args:
            modal_element (WebElement): The modal popup element.

        Returns:
            list: List of phone numbers extracted from the modal.
        """
        try:
            links = modal_element.find_elements(By.XPATH, './/a[contains(@href, "tel:")]')
            # Extract all numbers from tel: links
            return [l.get_attribute('href').replace('tel:', '').strip()
                    for l in links if l.get_attribute('href')]
        except Exception:
            return []

    def _close_modal(self, modal_element):
        """
        Close the contact modal if open.

        Args:
            modal_element (WebElement): The modal popup element.
        """
        try:
            close_btn = modal_element.find_element(By.CSS_SELECTOR, '.jd_modal_close, .modal_head_right')
            self.driver.execute_script("arguments[0].click();", close_btn)
            time.sleep(0.3)  # Allow UI time to close properly
        except Exception:
            pass

    def _safe_text(self, element, selector):
        """
        Safely extract text from an element using a CSS selector.

        Args:
            element (WebElement): Parent element to search within.
            selector (str): CSS selector to locate the target child element.

        Returns:
            str or None: Extracted text or None if not found.
        """
        try:
            el = element.find_element(By.CSS_SELECTOR, selector)
            return el.text.strip() if el else None
        except Exception:
            return None

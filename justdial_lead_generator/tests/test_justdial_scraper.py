import pytest
from selenium.webdriver.common.by import By
from justdial_lead_generator.scraper.justdial_scraper import JustDialScraper

# Fixtures for pytest
@pytest.fixture(scope='module')
def driver():
    drv = JustDialScraper.create_chrome_driver(headless=True)
    yield drv
    drv.quit()

@pytest.fixture
def scraper(driver):
    return JustDialScraper(driver)

INLINE_HTML = '''
<div class="resultbox_info">
  <h3 class="resultbox_title_anchor">Griddle Mama</h3>
  <div class="locatcity">Pandurang Bhudkar Marg Worli, Mumbai</div>
  <li class="resultbox_totalrate">4.4</li>
  <li class="resultbox_countrate">91 Ratings</li>
  <div class="resultbox_btnbox">
    <div class="greenfill_animate callbutton"><span class="callcontent">09972844374</span></div>
    <a href="tel:09972844374">09972844374</a>
  </div>
</div>
'''

MODAL_HTML = '''
<section class="jd_modal">
  <div class="jd_modal_content">
    <div class="jd_modal_body">
      <ul>
        <li><a href="tel:09820066471">09820066471</a></li>
        <li><a href="tel:09820058441">09820058441</a></li>
      </ul>
    </div>
    <span class="jd_modal_close"></span>
  </div>
</section>
'''

def write_sample(path, content: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def test_inline_contact_extraction(scraper, driver, tmp_path):
    path = tmp_path / "inline.html"
    write_sample(path, INLINE_HTML)
    driver.get(path.as_uri())
    listing = driver.find_element(By.CSS_SELECTOR, 'div.resultbox_info')
    contacts = scraper._extract_inline_contact(listing) or scraper._extract_inline_contact_link(listing)
    assert contacts == ['09972844374']

def test_modal_contact_extraction(scraper, driver, tmp_path):
    path = tmp_path / "modal.html"
    write_sample(path, MODAL_HTML)
    driver.get(path.as_uri())
    modal = driver.find_element(By.CSS_SELECTOR, 'section.jd_modal')
    contacts = scraper._extract_modal_contacts(modal)
    assert contacts == ['09820066471', '09820058441']


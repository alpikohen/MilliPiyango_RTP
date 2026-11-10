from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def fetch_page_source(url, wait_selector, timeout=20):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, wait_selector))
        )
        driver.implicitly_wait(2)
        return driver.page_source
    finally:
        driver.quit()

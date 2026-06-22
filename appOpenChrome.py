import config
import time
import subprocess
import config

import selenium.webdriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def openChrome():
    subprocess.Popen([
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--remote-debugging-port=9222",
        r"--user-data-dir=C:\ChromeAutomation\User Data",
        "--profile-directory=Profile 1"
    ])


def connectChrome():
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    return webdriver.Chrome(options=options)

def findTab(target, driver):
    tabs = driver.window_handles

    for i, tab in enumerate(tabs):
        driver.switch_to.window(tab)
        if target in driver.current_url:
            return tab
    return None
        
def getFirstRow(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    print(f"Panjang row adalah {len(rows)}")
    row = rows[3]
    
    cols = row.find_elements(By.TAG_NAME, "td")
    for i, col in enumerate(cols):
        print(f"Col {i} : {col.text}")
    
    try:
        btn = row.find_element(By.CSS_SELECTOR, "button[title='Open in Tag Assistant']")
        ActionChains(driver, 1000).move_to_element(btn).click(btn).perform()
    except Exception as e:
        print(f"Button tidak ditemukan di row ini : {e}")

if __name__ == "__main__":
    # Membuka chrome debugger 
    # openChrome()
    # time.sleep(5)

    # Connect ke chrome debugger
    driver = connectChrome()

    # Membuka halaman
    driver.get(
        config.BASE_URL
    )

    getFirstRow(driver)

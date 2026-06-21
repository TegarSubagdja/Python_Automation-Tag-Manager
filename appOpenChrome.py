import time
import config
import subprocess

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


if __name__ == "__main__":
    openChrome()
    time.sleep(5)

    driver = connectChrome()
    driver.get(
        "https://tagmanager.google.com/#/view_issue?issueType=7&accountId=6050129313&containerId=89256334"
    )

    time.sleep(10)

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    print(f"Jumlah row adalah {len(rows)}")
    data = []

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if cols:
            data.append({
                "url": cols[1].text,
                "status": cols[2].text
            })

            print(f"Click {cols[1].text}")
            ActionChains(driver).move_to_element(row).perform()
            button = WebDriverWait(row, 5).until(
                lambda r: r.find_element(By.CSS_SELECTOR, "button.icon--button")
            )
            button.click()
            exit()

    print(data)


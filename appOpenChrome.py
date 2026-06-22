import time
import config
import subprocess

import selenium.webdriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def open_chrome():
    subprocess.Popen([
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--remote-debugging-port=9222",
        r"--user-data-dir=C:\ChromeAutomation\User Data",
        "--profile-directory=Profile 1"
    ])


def connect_chrome():
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    while True:
        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            print("Gagal connect")
            time.sleep(1)

def switch_tab(target, driver, close_other=False):
    tabs = driver.window_handles
    matched_tab = None

    for tab in tabs:
        driver.switch_to.window(tab)
        print(f"checking url: {driver.current_url}")

        if target in driver.current_url:
            matched_tab = tab
            break

    if matched_tab is None:
        raise Exception(f"No tab found with url containing: {target}")

    if close_other:
        for tab in tabs:
            if tab != matched_tab:
                driver.switch_to.window(tab)
                driver.close()

        driver.switch_to.window(matched_tab)

    return matched_tab
        
def get_first_row(driver):

    time.sleep(3)

    rows = WebDriverWait(driver, 10, 3).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr"))
    )

    print(f"current url {driver.current_url}")
    print(f"Rows {len(rows)}")

    row = rows[3]
    
    url = row.find_elements(By.TAG_NAME, "td")[1].text
    state = row.find_elements(By.TAG_NAME, "td")[2].text

    print(f"Url : {url}")
    print(f"State : {state}")
    
    btn = row.find_element(
        By.CSS_SELECTOR,
        "button[title='Open in Tag Assistant']"
    )

    return url, state, btn


def click_view_issue(driver):
    btn = WebDriverWait(driver, 10, 0).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.wd-issues-button")
        )
    )
    ActionChains(driver, 1000).move_to_element(btn).click(btn).perform()

def click_see_untaged_pages(driver):
    btn = WebDriverWait(driver, 10, 0).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.wd-actionItem__action")
        )
    )
    ActionChains(driver, 1000).move_to_element(btn).click(btn).perform()

def click_add_urls(driver):
    btn = WebDriverWait(driver, 10, 0).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "ctui-bubble-icon-menu[title='Add URLs']")
        )
    )
    ActionChains(driver, 1000).move_to_element(btn).click(btn).perform()

    next_btn = WebDriverWait(driver, 10, 0).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'li[gil-id="tagCoverage_addUrl"]')
        )
    )
    ActionChains(driver, 1000).move_to_element(next_btn).click(next_btn).perform()

def click_domain_buttons(driver):
    btn = WebDriverWait(driver, 10, 0).until(
        EC.element_to_be_clickable(
            (By.ID, "domain-start-button")
        )
    )
    ActionChains(driver, 1000).move_to_element(btn).click(btn).perform()

def click_finish_button(driver):

    iframe = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "iframe.__TAG_ASSISTANT_BADGE")
        )
    )

    driver.switch_to.frame(iframe)
    print(f"Current url : {driver.current_url}")
    
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.wd-finish-button")
        )
    )
    ActionChains(driver, 1000).move_to_element(btn).click(btn).perform()

def click_button_continue(driver):
    btn = WebDriverWait(driver, 10, 0).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.wd-continue-debugging-button")
        )
    )
    ActionChains(driver, 1000).move_to_element(btn).click(btn).perform()

def click_and_fill_textarea(driver, url):
    cm = WebDriverWait(driver, 10, 0).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".CodeMirror")
        )
    )
    ActionChains(driver, 1000).move_to_element(cm).click(cm).perform()

    textarea = WebDriverWait(driver, 10, 0).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".CodeMirror textarea")
        )
    )
    textarea.send_keys(url)

def click_add_on_add_urls(driver):
    btn = WebDriverWait(driver, 10, 0).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']")
        )
    )
    ActionChains(driver, 1000).move_to_element(btn).click(btn).perform()

def get_setup():
    open_chrome()
    driver = connect_chrome()
    driver.get(
        config.BASE_URL
    )
    print(f"Switch tab pertama")
    switch_tab(target=config.BASE_URL, driver=driver)
    click_view_issue(driver)
    click_see_untaged_pages(driver)

    print(f"Switch tab kedua")
    switch_tab("https://tagassistant.google.com/", driver)

    click_button_continue(driver)
    exit()

    return driver

def proses_row(driver):
    while True:

            url, state, btn = get_first_row(driver)

            print(f"btn : {btn}")

            ActionChains(driver, 1000).move_to_element(btn).click(btn).perform()

            switch_tab("https://tagassistant.google.com/", driver)

            click_domain_buttons(driver)

            switch_tab(url, driver)

            click_finish_button(driver)

            switch_tab("https://tagassistant.google.com/", driver)

            click_button_continue(driver)

            switch_tab("https://tagmanager.google.com/", driver, close_other=True)

            click_add_urls(driver)

            click_and_fill_textarea(driver, url)

            click_add_on_add_urls(driver)

            return True

if __name__ == "__main__":

    driver = get_setup()

    proses_row(driver)
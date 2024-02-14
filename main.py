# This scripts logs into the BSB website and books a reading place for today
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

name = "name"
surname = "surname"
email = "email"
username = "username"
password = "password"
morning = True
afternoon = True

link = "https://www.bsb-muenchen.de/recherche-und-service/besuche-vor-ort/lesesaelearbeitsplaetze/allgemeiner-lesesaal/arbeitsplatz-im-allgemeinen-lesesaal-buchen/"\

def main():
    global afternoon, morning
    # Open the browser and go to the link
    browser = webdriver.Chrome()
    browser.get(link)

    # Wait for the page to load
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "tab2")))

    try:
        # login
        login(username, password, browser)
    except:
        # if the login fails, refresh the page and try again
        browser.refresh()
    time.sleep(3)
    while morning:
        today = browser.find_element(By.CLASS_NAME, "event-calendar__day-today")
        morning = morning_reserv(today, browser)
        if morning:
            browser.refresh()
    # Turn back to calendar page
    browser.get(link)
    while afternoon:
        today = browser.find_element(By.CLASS_NAME, "event-calendar__day-today")
        afternoon = afternoon_reserv(today, browser)
        if afternoon:
            browser.refresh()
    time.sleep(3)

def afternoon_reserv(today, browser):
    try:
        afternoon = today.find_element(By.CLASS_NAME, "cat-36")
        afternoon_button = afternoon.find_element(By.CLASS_NAME, "js-register-button")
        afternoon_button.click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "firstname")))
        fill_form(name, surname, email, browser)
        form_element = browser.find_element(By.CLASS_NAME, "js-send-form")
        form_element.submit()
        return False
    except:
        time.sleep(5)
        return True
    
def morning_reserv(today, browser):
    try:
        morning = today.find_element(By.CLASS_NAME, "cat-35")
        morning_button = morning.find_element(By.CLASS_NAME, "js-register-button")
        morning_button.click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "firstname")))
        fill_form(name, surname, email, browser)
        form_element = browser.find_element(By.CLASS_NAME, "js-send-form")
        form_element.submit()
        return False
    except:
        time.sleep(5)
        return True
        
def fill_form(name, surname, email, browser):
    # fill the form
    browser.find_element(By.ID, "firstname").send_keys(name)
    browser.find_element(By.ID, "lastname").send_keys(surname)
    browser.find_element(By.ID, "email").send_keys(email)

    # click the submit button
    form_element = browser.find_element(By.CLASS_NAME, "js-send-form")
    form_element.submit()

    return True
def login(username, password, browser):
    # Click the second tab (for LMU login)
    browser.execute_script("document.getElementById('tab2').click();")
    # enter the username and password
    browser.find_element(By.ID, "lmu-id").send_keys(username)
    browser.find_element(By.ID, "lmu-password").send_keys(password)

    # click the login button with value "Anmelden"
    form_element = browser.find_element(By.CLASS_NAME, "lmu-login")
    form_element.submit()
    return True

if __name__ == "__main__":
    main()
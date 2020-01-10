from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import shutil
import time

def webScraper(password1, password2):
    chromeOptions = webdriver.ChromeOptions()

    chromeOptions.add_experimental_option("detach", True)
    chromeOptions.add_argument("profile-directory=Profile 1")
    chromeOptions.add_argument("user-data-dir=C:\\Users\\mike9\\AppData\\Local\\Google\\Chrome\\User Data")

    driver = webdriver.Chrome(executable_path="..\\chromedriver.exe", options = chromeOptions)
    driver.implicitly_wait(10)
    try:
        #Get the pcfinancial report
        driver.get('https://secure.pcfinancial.ca/en/my/transactions')
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        driver.find_element_by_id('username').send_keys('Morkle')

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )
        driver.find_element_by_id('password').send_keys(password2)

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@type = "submit"]'))
        )
        driver.find_element_by_xpath('//button[@type = "submit"]').click()
        time.sleep(5)
        driver.find_element_by_xpath("//div[@id='main-content']/div/loader/div[2]/transaction-credit/div/div[2]/div/div[2]/button/loader/span").click()
        time.sleep(5)
        #Get the scotiabank report
        driver.get('https://www.scotiaonline.scotiabank.com/online/views/accounts/accountDetails/depositAcctDetails.bns?acctId=N6C283FC2&tabId=acctDet')

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "signon_form:userName"))
        )
        driver.find_element_by_id("signon_form:userName").send_keys("mike9251")

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "signon_form:password_0"))
        )
        driver.find_element_by_id("signon_form:password_0").send_keys(password1)
        driver.find_element_by_id("signon_form:enter_sol").click()
        time.sleep(3)
        driver.find_element_by_xpath("//img[@alt='Download Data']").click()
        time.sleep(1)
        driver.find_element_by_link_text("Microsoft Excel").click()

    finally:
        time.sleep(3)
        driver.close()

def moveFiles():
    shutil.copy("C:\\Users\\mike9\\Downloads\\pcbanking.csv", ".\\")
    shutil.copy("C:\\Users\\mike9\\Downloads\\report.csv", ".\\")
    os.remove("C:\\Users\\mike9\\Downloads\\pcbanking.csv")
    os.remove("C:\\Users\\mike9\\Downloads\\report.csv")
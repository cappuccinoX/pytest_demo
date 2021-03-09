from selenium import webdriver
import os
from time import sleep

from selenium.webdriver.support import expected_conditions as _
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)
url = 'file://%s\\demo.html' % dir_path
driver.get(url)

def test():
    # alert
    driver.find_element_by_id("alert").click()
    alert = driver.switch_to.alert
    sleep(1)
    print(alert.text)
    alert.accept()

    # confirm
    driver.find_element_by_id("confirm").click()
    confirm = driver.switch_to.alert
    sleep(1)
    print(confirm.text)
    confirm.dismiss()

    #prompt
    driver.find_element_by_id("prompt").click()
    prompt = driver.switch_to.alert
    sleep(1)
    print(prompt.text)
    prompt.accept()

    driver.get("https://www.baidu.com")

    driver.quit()

def test1():
    driver.find_element_by_id("btn").click()
    wait = WebDriverWait(driver, 3)
    wait.until(_.text_to_be_present_in_element((By.ID, 'id2'), 'id 2'))
    print('ok')
    driver.quit()

if __name__ == '__main__':
    test1()
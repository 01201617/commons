
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

if __name__=="__main__":
    driver = webdriver.Chrome()

    driver.get('https://www.sbisec.co.jp/ETGate')

    driver.find_element_by_name("user_id").send_keys("ＡＡＡ")
    driver.find_element_by_name("user_password").send_keys("AAA")
    driver.find_element_by_name("ACT_login").click()
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, "#navi01P li:nth-child(3) img").click()
    driver.implicitly_wait(10)
    driver.find_element(By.LINK_TEXT, "スクリーニング").click()
    driver.implicitly_wait(10)
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR,"iframe")))
    driver.implicitly_wait(100)
    driver.find_element(By.CSS_SELECTOR, ".SearchBoxTop > .searchbtn").click()
    driver.find_element(By.CSS_SELECTOR, ".download").click()
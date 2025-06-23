from selenium import webdriver
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == "__main__":
    user = os.getenv("USERNAME")
    options = webdriver.ChromeOptions()

    if user == "DSH":
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-data-dir=C:/Users/DSH/AppData/Local/Google/Chrome/User Data")
        options.add_argument("--profile-directory=Default")
        #options.add_argument("--remote-debugging-port=9222")

        driver = webdriver.Chrome("C:\\Users\\DSH\\.wdm\\drivers\\chromedriver\\win32\\109.0.5414.74\\chromedriver.exe")

        driver.get("https://tetris94.ru/")



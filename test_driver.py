from selenium import webdriver
from urllib.parse import quote, unquote
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__ == "__main__":
    options = webdriver.ChromeOptions ()
    # options.add_argument('--headless')
    options.binary_location = "C:\\Users\\shulya403\\Downloads\\chrome-win64\\chrome.exe"
    options.add_argument ("--window-size=1920,1080")
    #options.setBinary ("/path/to/other/chrome/binary")
    #options.add_argument ("--user-data-dir=C:/Users/shulya403/AppData/Local/Google/Chrome/User Data")
    #options.add_argument ("--profile-directory=Default")
    #options.add_argument ("--remote-debugging-port=9222")

    #driver = webdriver.Chrome(executable_path="C:\\Users\\shulya403\\.wdm\\drivers\\chromedriver\\win64\\136.0.7103.114\\chromedriver-win32\\chromedriver.exe", options=options)
    driver = webdriver.Chrome(executable_path="C:\\Users\\shulya403\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe", options=options)
    driver.get ("https://www.rbc.ru/quote/ticker/61867")
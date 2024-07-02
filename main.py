# 라이브러리 호출
import pandas as pd
import numpy as np
import re

# 셀레니움 관련 라이브러리 호출
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 옵션
chrome_options = Options()
# chrome_options.add_argument('--headless')  # GUI를 띄우지 않고 실행
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--remote-debugging-port=9222')

def run_selenium_script():
    # 웹드라이버 자동 설치 및 브라우저 실행
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.example.com")
    
    # 예제 작업: 페이지 타이틀 출력
    print(driver.title)
    
    # 브라우저 닫기
    driver.quit()



raw = pd.read_excel('/Users/master/dev/PythonPr/crawler/AccessOn/input/학술논문-08.xlsx',
                         sheet_name = '데이터-08',
                         usecols=['NO', '논문명', '논문 외국어명', 'DOI', '링크', '링크 사이트의\nCCL 등급', 'AccessON의 \nCCL 등급'])
raw['DOI'] = raw['DOI'].fillna('Missing').astype(str)

def clean_string(word):
  return re.sub(r'\s+|\W+', '', word)


if __name__ == "__main__":
    run_selenium_script()
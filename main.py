# ���̺귯�� ȣ��
import pandas as pd
import numpy as np
import re

# �����Ͽ� ���� ���̺귯�� ȣ��
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ũ�� �ɼ�
chrome_options = Options()
# chrome_options.add_argument('--headless')  # GUI�� ����� �ʰ� ����
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--remote-debugging-port=9222')

def run_selenium_script():
    # ������̹� �ڵ� ��ġ �� ������ ����
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.example.com")
    
    # ���� �۾�: ������ Ÿ��Ʋ ���
    print(driver.title)
    
    # ������ �ݱ�
    driver.quit()

if __name__ == "__main__":
    run_selenium_script()

raw_data = 
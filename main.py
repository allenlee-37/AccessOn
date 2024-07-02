# -*- coding: utf-8 -*-

# 라이브러리 호출
import os
import glob
import pandas as pd
import numpy as np
import re
import argparse
from tqdm import tqdm # tqdm 클래스 임포트

import ssl
print(ssl.OPENSSL_VERSION)

# 셀레니움 관련 라이브러리 호출
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# 웹드라이버 자체 설정을 위한 호출
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 자연어 제목 정제
def clean_string(word):
  return re.sub(r'\s+|\W+', '', word)

# PDF 파일 다운로드 삭제
def delete_pdf():
    folder_path = '/Users/master/dev/PythonPr/crawler/AccessOn'
    pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))
    # Iterate over the PDF files and delete them
    for pdf_file in pdf_files:
        os.remove(pdf_file)

# 저작권 상황 불러오기
def copyright_title(DOI, thesis_title):
    # DOI가 없을 경우, 영어 제목으로 검색
    if DOI == 'Missing':
        keyword = thesis_title # 영어 제목
        # 정확도 우선으로 영어 제목 검색한 페이지 호출
        driver.get(f"https://accesson.kisti.re.kr/main/search/searchResult.do?searchMode=simple&from=0&currentPage=1&searchApiUse=N&preFilterISSN=&simpleSchQry={keyword}&sort=_score&order=desc")

        try:
            first_result_xpath = '//*[@id="frmSearchCond"]/div[2]/div[2]/div[2]/div/div[2]/div[2]/a'
            first_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, first_result_xpath)))
            first_result.click() # 첫번째 검색 결과 클릭
        except:
            result = '*자료없음' # 클릭 불가시 '자료없음' 반환 및 함수 종료
            return result

        # 상세 페이지 제목
        try:
            title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[3]/div[1]/div[1]/div[2]')))
            title = title.text
        except: title = 'null'

        # 상세 페이지 부제목
        try:
            subtitle = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[3]/div[1]/div[1]/h3')))
            subtitle = subtitle.text
        except: subtitle = 'null'

        # 호출한 페이지와 논문의 제목 혹은 부제목(영문)이 동일한지 확인
        if clean_string(str(keyword)) == clean_string(title) or clean_string(str(keyword)) == clean_string(subtitle):
            pass    
        else:
            result = '제목 불일치' # 논문 사이트에서 오타가 난 경우도 있기 때문에 직접 확인 필요
            return result # 함수 종료

  # DOI가 있을 경우
    else:
        keyword = DOI # DOI로 직접 검색
        driver.get(f"https://accesson.kisti.re.kr/main/search/searchResult.do?searchMode=simple&from=0&currentPage=1&searchApiUse=N&preFilterISSN=&simpleSchQry={keyword}&sort=_score&order=desc")
        # 첫번째 검색결과 진입
        try:
            first_result_xpath = '//*[@id="frmSearchCond"]/div[2]/div[2]/div[2]/div/div[2]/div[2]/a'
            first_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, first_result_xpath)))
            first_result.click()
        except: # 결과 클릭이 안될 경우 자료 없는 것임
            result = '*자료없음' 
            return result

    '''
    DOI가 있는 경우와 없는 경우 모두 올바른 논문의 상세 페이지로 진입한 것 확인
    저작권의 현황을 긁어온다.
    '''
    try:
        copyright_xpath = '//*[@id="articleAside"]/div[2]/ul/li/div/p' # 저작권 xpath 경로
        copyright = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, copyright_xpath)))
        result = copyright.get_attribute('title') # 'title'로 들어가 있기 때문에 attribute로 빼온다.
        # 각 현황을 output의 양식에 맞도록 변환시켜준다. 
        if result == '저작권표시()': result = '()'
        elif result == '저작권표시(by-nc)': result = 'CC BY-NC'
        elif result == '저작권표시(by)': result = 'CC BY'
        elif result == '저작권표시(by-nc-nd)': result = 'CC BY-NC-ND'
        else: pass
    except: result = '정보없음' # 저작권 경로를 찾지 못할 경우, 저작권이 나와있지 않으므로 '정보없음' 반환
    return result

def get_accesson_status(start, end):
    '''start~end까지의 데이터를 검색하고 엑셀로 저장'''
    # 파일을 저장할 경로
    output_file_path = f'/Users/master/dev/PythonPr/crawler/AccessOn/output/AccessOn_output_file_{start}_{end}.xlsx'
    df = raw.iloc[start:end]
    thesis_title_list = df['논문 외국어명'].tolist() # 논문 외국어명 리스트
    DOI_list = df['DOI'].tolist() # 논문 DOI 리스트 

    # Tuple로 묶인 리스트로 저장하여 copyright_title(DOI, thesis_title) 함수에 입력
    keyword_list = [(x, y) for x, y in zip(DOI_list, thesis_title_list)]

    # 저작권 현황을 append할 빈 리스트
    copyright_status = []
    for DOI, thesis_title in keyword_list:
        copyright_status.append(copyright_title(DOI, thesis_title))
        progress_bar.update(1) # tqdm 업데이트 +1
        delete_pdf() # 불필요한 pdf파일 삭제
        df = df.copy()
        df.loc[:, 'CCL'] = copyright_status # 슬라이싱된 파일에 리스트를 입력

    df.to_excel(output_file_path, index=False) # df를 엑셀 파일로 저장
    print(f"DataFrame saved to {output_file_path}") # 완료 현황 프린트
    return

if __name__ == "__main__":
    '''메인 함수'''
    # 명령행 인자 부여
    parser = argparse.ArgumentParser(description='크롤러의 범위(start와 finish) 그리고 간격(jump)를 지정합니다.')
    parser.add_argument('-a', '--start', type=int, required=True, help='starting point')
    parser.add_argument('-b', '--finish', type=int, required=True,help='finish point')
    parser.add_argument('-c', '--jump', type=int, required=True, help = 'save points')
    args = parser.parse_args()

    start = args.start
    finish = args.finish
    jump = args.jump

    # 최신 크롬 드라이버 설치
    service = Service(ChromeDriverManager().install()) 
    # 크롬 드라이버 옵션
    options = Options()
    options.add_argument('--headless')  # Headless 모드로 설정
    driver = webdriver.Chrome(service=service, options=options) # 크롬 드라이버 실행
    
    # 원시 데이터 불러오기
    raw = pd.read_excel('/Users/master/dev/PythonPr/crawler/AccessOn/input/학술논문-08.xlsx',
                            sheet_name = '데이터-08',
                            usecols=['NO', '논문명', '논문 외국어명', 'DOI', '링크', '링크 사이트의\nCCL 등급', 'AccessON의 \nCCL 등급'])
    raw['DOI'] = raw['DOI'].fillna('Missing').astype(str) # DOI가 없는 열은 'Missing'으로 대체

    # tqdm 초기화
    n_iterations = finish - start  # 반복 횟수
    progress_bar = tqdm(total=n_iterations)  # tqdm 객체 생성

    # start가 finish보다 커질 때까지 반복문
    while start < finish:
        get_accesson_status(start, start+jump) # jump만큼 건너뛰면서 엑셀 저장
        start += jump # start + jump

    driver.quit() # 드라이버 종료
    progress_bar.close() # tqdm 프로그레스바 종료

    
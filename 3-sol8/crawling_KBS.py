# crawling_KBS.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 네이버 로그인 정보
NAVER_ID = 'your_naver_id'
NAVER_PW = 'your_naver_password'

def setup_driver():
    """셀레니움 웹드라이버 초기 설정"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저 창 없이 실행
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    service = Service('chromedriver')  # chromedriver 경로
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def naver_login(driver, user_id, user_pw):
    """네이버 로그인 수행"""
    driver.get('https://nid.naver.com/nidlogin.login')
    time.sleep(2)

    # ID, PW 입력
    driver.find_element(By.ID, 'id').send_keys(user_id)
    driver.find_element(By.ID, 'pw').send_keys(user_pw)
    driver.find_element(By.ID, 'pw').send_keys(Keys.RETURN)
    time.sleep(3)

def crawl_mypage_content(driver):
    """로그인 후 나만 볼 수 있는 콘텐츠 크롤링"""
    driver.get('https://www.naver.com')  # 예: 마이페이지 접근
    time.sleep(2)
    
    contents_list = []

    # 로그인 후에만 볼 수 있는 콘텐츠 예시
    try:
        # 예: '메일' 영역
        mail_element = driver.find_element(By.CLASS_NAME, 'link_mail')
        contents_list.append(mail_element.text)
    except:
        contents_list.append('메일 영역 접근 실패')

    return contents_list

def crawl_naver_mail_titles(driver):
    """보너스: 네이버 메일 제목 크롤링"""
    driver.get('https://mail.naver.com')
    time.sleep(3)

    mail_titles = []

    try:
        emails = driver.find_elements(By.CSS_SELECTOR, 'strong.mail_title')
        for email in emails[:10]:  # 최근 10개 메일
            mail_titles.append(email.text)
    except:
        mail_titles.append('메일 제목 크롤링 실패')

    return mail_titles

def main():
    driver = setup_driver()
    
    try:
        naver_login(driver, NAVER_ID, NAVER_PW)
        
        mypage_contents = crawl_mypage_content(driver)
        print('로그인 후 볼 수 있는 콘텐츠:', mypage_contents)

        mail_titles = crawl_naver_mail_titles(driver)
        print('최근 메일 제목:', mail_titles)

    finally:
        driver.quit()

if __name__ == '__main__':
    main()

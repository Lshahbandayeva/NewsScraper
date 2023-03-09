import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="milli_news",
    user="lala",
    port=5432
)

cur = conn.cursor()

def run_script():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get('https://news.milli.az/')

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search-holder')))

    link_elements = driver.find_elements(By.CSS_SELECTOR, 'div.text-holder strong.title a')

    for url in link_elements:
        link_url = url.get_attribute('href')

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link_url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'quiz-holder')))

        title = driver.find_element(By.CSS_SELECTOR, "div.quiz-holder h1")
        date = driver.find_element(By.CLASS_NAME, "date-info")
        content = driver.find_elements(By.XPATH, "//div[@class='article_text']//p")
        image = driver.find_element(By.XPATH, "//img[@class='content-img']").get_attribute("src")

        print("\n")
        print(f"Title: {title.text}")
        print(f"URL: {link_url}")
        print(f"Date: {date.text}")
        print(f"Image: {image}")
        print(f"Category: {link_url.split('/')[3]}")
        print(f"Content: ")
        for c in content:
            print(c.text)

        cur.execute(
            "INSERT INTO news (title, url, date, image, content, categories) VALUES (%s, %s, %s, %s, %s, %s)",
            (title.text, link_url, date.text, image, [c.text for c in content], link_url.split('/')[3])
        )


        conn.commit()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    driver.quit()

schedule.every().hour.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(1)

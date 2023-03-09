import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="apa_news",
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

    driver.get('https://apa.az/az/all-news')

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'content')))

    headlines = driver.find_element(By.XPATH, "//div[@class='four_columns_block mt-site']")
    urls = headlines.find_elements(By.CLASS_NAME, 'item')

    for url in urls:
        link_url = url.get_attribute('href')

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link_url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'news_main')))

        title = driver.find_element(By.CLASS_NAME, 'title_news')
        date = driver.find_element(By.CLASS_NAME, 'date')
        author = driver.find_element(By.CSS_SELECTOR, '.logo span')
        image = driver.find_element(By.XPATH, "//div[@class='main_img']/img").get_attribute("src")
        content = driver.find_elements(By.XPATH, "//div[@class='texts mb-site']//p")
        categories = driver.find_elements(By.XPATH, "//div[@class='links']//a")

        cur.execute(
            "INSERT INTO news (title, url, date, author, image, content, categories) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (title.text, link_url, date.text, author.text, image, [c.text for c in content],
             [category.text for category in categories])
        )

        conn.commit()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    driver.quit()

schedule.every().hour.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(1)

#cur.close()
#conn.close()

'''
time_limit = 24 * 60 * 60  # 24 hours
start_time = time.time()
while time.time() - start_time < time_limit:
    schedule.run_pending()
    time.sleep(1)
'''

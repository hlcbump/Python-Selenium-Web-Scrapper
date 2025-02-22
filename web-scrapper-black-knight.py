import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

# initialize web driver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)

driver.get('http://www.blackknightnation.com/')
time.sleep(2)

# data storage
data = []

news = driver.find_elements(By.XPATH, '//li[contains(@class, "mvp-blog-story-wrap")]')

for new in news:
    try:
        title = new.find_element(By.XPATH, './/h2/a').text
        category = new.find_element(By.XPATH, './/h3/a').text
        post_age = new.find_element(By.XPATH, './/span[contains(@class, "mvp-post-info-date")]').text
        author = new.find_element(By.XPATH, './/a[contains(@rel, "author")]').text

        data.append([title, category, post_age, author])

    except Exception as e:
        print(f'data extraction error')
        
driver.quit()

df_news = pd.DataFrame(data, columns=['title', 'category' , 'post_age', 'author'])

print(df_news.head())

df_news.to_csv('news.csv', index=False, encoding='utf-8', sep=';')
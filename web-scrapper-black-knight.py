import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import gspread
import random
from oauth2client.service_account import ServiceAccountCredentials
from proxies import get_free_proxies

CREDENTIALS_FILE = "google_sheets_credentials.json"

# load credentials from credentials json file
def load_credentials():
    with open(CREDENTIALS_FILE, "r") as file:
        creds = json.load(file)
    return creds

# get driver headless and with proxy
def get_driver_with_proxy():
    # get proxy
    proxy = get_free_proxies()

    # driver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f'--proxy-server=https://{proxy}')
    chrome_options.add_argument("--proxy-bypass-list=*")

    return webdriver.Chrome(options=chrome_options)

def scrape_news():
    driver = get_driver_with_proxy()
    driver.get('http://www.blackknightnation.com/')
    time.sleep(2)

    # data storage
    data = []

    # get all news
    news = driver.find_elements(By.XPATH, '//li[contains(@class, "mvp-blog-story-wrap")]')

    # iterate over news
    for new in news:
        try:
            # extract data
            title = new.find_element(By.XPATH, './/h2/a').text
            category = new.find_element(By.XPATH, './/h3/a').text
            post_age = new.find_element(By.XPATH, './/span[contains(@class, "mvp-post-info-date")]').text
            author = new.find_element(By.XPATH, './/a[contains(@rel, "author")]').text

            # store data
            data.append([title, category, post_age, author])

        except Exception as e:
            print(f'data extraction error')
            
    driver.quit()

    # create dataframe
    df_news = pd.DataFrame(data, columns=['title', 'category' , 'post_age', 'author'])

    # print head data
    print(df_news.head())

    # save data into csv
    df_news.to_csv('news.csv', index=False, encoding='utf-8', sep=';')

    return df_news

# update google sheets
def update_google_sheets(df_news):

    # get credentials
    creds_data = load_credentials()
    sheet_name = creds_data['sheet_name']

    # google sheets api config
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('google_sheets_credentials.json', scope)
    client = gspread.authorize(creds)
    
    # open the sheets
    sheet = client.open(sheet_name).sheet1
    

    # verify if the sheet is empty
    existing_data = sheet.get_all_values()
    print()
    print('actual table:', existing_data)
    if not existing_data or all(cell == "" for cell in existing_data[0]):
        sheet.clear()
        sheet.append_row(['Title', 'Category', 'Post Age', 'Author'])
    

    # fill the sheet
    for row in df_news.values.tolist():
        sheet.append_row(row)
    
    print('Google Sheets atualizado com sucesso!')

if __name__ == '__main__':
    df_news = scrape_news()
    if not df_news.empty:
        update_google_sheets(df_news)
    else:
        print('Nenhuma notícia encontrada.')
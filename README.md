## 📰 Web Scraping News from Black Knight Nation

This Python script uses Selenium, Pandas, and Google Sheets API to scrape the latest news articles from Black Knight Nation, save them as a CSV file, and update a Google Sheets spreadsheet.

---

## 📌 Features

- 🚀 Automates web browsing using Selenium.
- 🌍 Uses rotating proxies to avoid IP bans.
- 🏷 Extracts news titles, categories, publication dates, and authors.
- 📂 Saves the extracted data into a structured CSV file.
- 📊 Uses Pandas for data processing.
- 📤 Updates a Google Sheets document with the extracted data.

---

## 🚀 How It Works

1. Opens the website using Selenium with a **random proxy**.
2. Finds all news articles using XPath.
3. Extracts relevant information:
   - 🏷 **Title**
   - 📂 **Category**
   - ⏳ **Post age** (date of publication)
   - ✍ **Author**
4. Stores the extracted data in a Pandas DataFrame.
5. Saves the results in a CSV file (`news.csv`).
6. Updates Google Sheets with the extracted data.

---

## 📜 Code Explanation

### Importing Libraries

```python
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
```

- 📊 Imports **Pandas** for data handling.
- 🌐 Imports **Selenium** for web scraping.
- 🔄 Uses **random proxies** to avoid detection.
- 📤 Imports **Google Sheets API** for updating spreadsheets.

### Initializing WebDriver with Proxy

```python
def get_driver_with_proxy():
    proxy = get_free_proxies()
    print(f'Using proxy: {proxy}')

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f'--proxy-server=https://{proxy}')
    chrome_options.add_argument("--proxy-bypass-list=*")

    return webdriver.Chrome(options=chrome_options)
```

- 🛡️ **Uses a random proxy** from `get_free_proxies()`.
- 🚀 Runs Selenium in **headless mode** for efficiency.

### Extracting News Data

```python
def scrape_news():
    driver = get_driver_with_proxy()
    driver.get('http://www.blackknightnation.com/')
    time.sleep(2)

    data = []
    news = driver.find_elements(By.XPATH, '//li[contains(@class, "mvp-blog-story-wrap")]')

    for new in news:
        try:
            title = new.find_element(By.XPATH, './/h2/a').text
            category = new.find_element(By.XPATH, './/h3/a').text
            post_age = new.find_element(By.XPATH, './/span[contains(@class, "mvp-post-info-date")]').text
            author = new.find_element(By.XPATH, './/a[contains(@rel, "author")]').text
            data.append([title, category, post_age, author])
        except Exception:
            print('Data extraction error')

    driver.quit()
    df_news = pd.DataFrame(data, columns=['title', 'category', 'post_age', 'author'])
    df_news.to_csv('news.csv', index=False, encoding='utf-8', sep=';')
    return df_news
```

- 📌 Extracts **news titles, categories, dates, and authors**.
- 🔄 Stores data in a Pandas **DataFrame**.
- 💾 Saves data to a **CSV file**.

### Updating Google Sheets

```python
def update_google_sheets(df_news):
    creds_data = load_credentials()
    sheet_name = creds_data['sheet_name']
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('google_sheets_credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1

    existing_data = sheet.get_all_values()
    print('Actual table:', existing_data)
    if not existing_data or all(cell == "" for cell in existing_data[0]):
        sheet.clear()
        sheet.append_row(['Title', 'Category', 'Post Age', 'Author'])

    for row in df_news.values.tolist():
        sheet.append_row(row)
    print('Google Sheets atualizado com sucesso!')
```

- 📤 **Loads Google Sheets credentials**.
- 🔄 **Appends new data to the sheet**.
- 🛠 Clears sheet if it's empty.

---

## 📁 Output Example

A sample `news.csv` file will look like this:

| Title              | Category   | Post Age   | Author     |
|-------------------|-----------|-----------|-----------|
| Army beats Navy   | Football  | 2 days ago | John Doe  |
| New recruit joins | Basketball | 1 week ago | Jane Smith |
| Season preview   | Analysis   | 3 weeks ago | Alex Brown |

---

## 📜 License

This project is open-source and available under the **MIT License**.
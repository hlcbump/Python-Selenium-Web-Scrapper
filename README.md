## 📰 Web Scraping News from Black Knight Nation

This Python script uses Selenium and Pandas to scrape the latest news articles from Black Knight Nation and save them as a CSV file.

---

## 📌 Features

- 🚀 Automates web browsing using Selenium.
- 🏷 Extracts news titles, categories, publication dates, and authors.
- 📂 Saves the extracted data into a structured CSV file.
- 📊 Uses Pandas for data processing.

---

## 🛠️ Requirements

Ensure you have Python 3.x installed. Then, install the necessary dependencies:

```sh
pip install selenium pandas
```

Additionally, download and install the latest version of **ChromeDriver** to match your Chrome browser version.

---

## 🚀 How It Works

1. Opens the website using Selenium.
2. Finds all news articles using XPath.
3. Extracts relevant information:
   - 🏷 **Title**
   - 📂 **Category**
   - ⏳ **Post age** (date of publication)
   - ✍ **Author**
4. Stores the extracted data in a Pandas DataFrame.
5. Saves the results in a CSV file (`news.csv`).

---

## 📜 Code Explanation

### Importing Libraries

```python
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
```

- 📊 Imports **Pandas** for data handling.
- 🌐 Imports **Selenium** for web scraping.
- 🛠️ Imports necessary **Selenium components** for interacting with the webpage.

### Initializing WebDriver

```python
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)
driver.get('http://www.blackknightnation.com/')
time.sleep(2)
```

- 🖥️ Initializes the **Chrome WebDriver**.
- 🌍 Opens the **Black Knight Nation** website.
- ⏳ Waits **2 seconds** to allow page loading.

### Extracting News Data

```python
data = []
news = driver.find_elements(By.XPATH, '//li[contains(@class, "mvp-blog-story-wrap")]')
```

- 📦 Creates an **empty list** to store extracted data.
- 🔍 Finds all **news articles** using XPath.

### Looping Through News Articles

```python
for new in news:
    try:
        title = new.find_element(By.XPATH, './/h2/a').text
        category = new.find_element(By.XPATH, './/h3/a').text
        post_age = new.find_element(By.XPATH, './/span[contains(@class, "mvp-post-info-date")]').text
        author = new.find_element(By.XPATH, './/a[contains(@rel, "author")]').text

        data.append([title, category, post_age, author])

    except Exception as e:
        print(f'Data extraction error')
```

- 🔄 Loops through each **news article**.
- 📌 Extracts:
  - **Title** (h2/a)
  - **Category** (h3/a)
  - **Publication date** (mvp-post-info-date)
  - **Author** (rel="author")
- 📝 Appends the extracted data to a list.
- ⚠️ Handles errors gracefully.

### Closing WebDriver

```python
driver.quit()
```

- ❌ Closes the **browser** after extraction.

### Storing Data in CSV

```python
df_news = pd.DataFrame(data, columns=['title', 'category', 'post_age', 'author'])
print(df_news.head())
df_news.to_csv('news.csv', index=False, encoding='utf-8', sep=';')
```

- 🔄 Converts the extracted data into a **Pandas DataFrame**.
- 👀 Displays the first **5 rows** for preview.
- 💾 Saves the data as a **CSV file (`news.csv`)**.

---

## 📁 Output Example

A sample `news.csv` file will look like this:

| Title              | Category   | Post Age   | Author     |
|-------------------|-----------|-----------|-----------|
| Army beats Navy   | Football  | 2 days ago | John Doe  |
| New recruit joins | Basketball | 1 week ago | Jane Smith |
| Season preview   | Analysis   | 3 weeks ago | Alex Brown |

---

## 🏁 Running the Script

To run the script, execute:

```sh
python script.py
```

---

## ⚠️ Notes

- Ensure that **ChromeDriver** is installed and compatible with your browser version.
- You may need to **update the XPath selectors** if the website's structure changes.

---

## 📜 License

This project is open-source and available under the **MIT License**.


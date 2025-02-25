from selenium import webdriver
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Get free proxies for rotating
def get_free_proxies():

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # initialize driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://sslproxies.org')

    # proxies array
    proxies = []

    # get all rows
    rows = driver.find_elements(By.XPATH, '//table[@class="table table-striped table-bordered"]/tbody/tr')

    # iterate over rows
    for row in rows:

        # get columns
        cols = row.find_elements(By.TAG_NAME, 'td')

        # check if there are at least 2 columns
        if len(cols) >= 2:

            # extract ip and port
            ip = cols[0].text.strip()
            port = cols[1].text.strip()
            # store proxy

            proxy = f'{ip}:{port}'
            # append proxy to list
            proxies.append(proxy)

    # close driver and return
    driver.quit()
    random_proxy = random.choice(proxies)
    print(f'Proxy: {random_proxy}')
    return random_proxy
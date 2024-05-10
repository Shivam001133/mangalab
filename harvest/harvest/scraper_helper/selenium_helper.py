from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.display = Display(visible=0, size=(1200, 800))
        self.display.start()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1200x800")
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(options=chrome_options)

    def scrape(self, url, **kwargs):
        url_list = []
        js_waite = kwargs.get('js_waite', None)
        url_list_path = kwargs.get('url_list_path', None)
        img_path = kwargs.get('img_path', None)

        if url_list_path:
            self.browser.get(url)

            if js_waite:
                wait = WebDriverWait(self.browser, 10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, js_waite)))

            if img_path:
                item_list = self.browser.find_elements(By.CSS_SELECTOR, url_list_path)

                for item in item_list:
                    img_list = item.find_elements(By.CSS_SELECTOR, img_path)
                    img_url = img_list[0].get_attribute('src')

                    if img_url:
                        url_list.append(img_url)
                    else:
                        url_list.append(None)

                return url_list

            else:
                self.browser.quit()
                raise ValueError("No image path provided")

    def close(self):
        self.browser.quit()
        self.display.stop()

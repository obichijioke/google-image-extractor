from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib import parse
import time
import os
import requests
from urllib.parse import urlparse

class Scraper:
    
    def __init__(self, show_ui=False, download_path='/app/downloaded_images'):
        self.__show_ui = show_ui  # Allow this to be set by the parameter
        self.__download_path = download_path
        
        if not os.path.exists(self.__download_path):
            os.makedirs(self.__download_path)

        self.__driver = self._create_driver()

    def _create_driver(self):
        chrome_options = webdriver.ChromeOptions()
        # Remove the headless option
        # if not self.__show_ui:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com/imghp?hl=en")
        return driver

    def _load_thumbnails(self, driver):
        def get_thumbnails():
            try:
                print("\nFetching image thumbnails...")
                thumbnails = driver.find_elements(By.XPATH, "//div[@class='eA0Zlc WghbWd FnEtTd mkpRId m3LIae RLdvSe qyKxnc ivg-i PZPZlf GMCzAd']")
                print(f"🤖: Found {len(thumbnails)} image thumbnails!")
            except Exception as e:
                print("\n🔴🔴 Error while fetching image containers! 🔴🔴")
            return thumbnails
        
        thumbnails = get_thumbnails()

        while len(thumbnails) < self.__image_limit:
            print("🤖: Scrolling...")
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
            thumbnails = get_thumbnails()
            time.sleep(3)
            try:
                end_of_page = driver.find_element(By.XPATH, """//input[@class='LZ4I']""").is_displayed()
                no_more_results = driver.find_element(By.XPATH, """//div[@class='OuJzKb Yu2Dnd']""").is_displayed()
                if end_of_page:
                    driver.find_element(By.XPATH, """//input[@class='LZ4I']""").click()
                if no_more_results:
                    break
            except Exception as e:
                print("\n🔴🔴 Search more button not found! 🔴🔴")

        print(f"🤖: Found a total of {len(thumbnails)} image thumbnails!") 
        driver.execute_script("window.scrollTo(0,0)")
        time.sleep(2)
        return thumbnails

    def _accept_cookies(self, driver):
        try:
            print("Attempting to accept cookies...")
            wait = WebDriverWait(driver, 10)
            accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all')]")))
            accept_button.click()
            print("Cookies accepted successfully!")
        except (TimeoutException, NoSuchElementException):
            print("No cookie consent popup found or unable to interact with it.")

    def _get_images(self, driver):
        self._accept_cookies(driver)
        thumbnails = self._load_thumbnails(driver)
        
        wait = WebDriverWait(driver, 10)
        print("\nFetching Links...")

        images = set()
        for index in range(min(len(thumbnails), self.__image_limit)):
            try:
                thumbnails[index].click()
                time.sleep(2)
                wait.until(EC.visibility_of_element_located((By.XPATH, """//img[@class='sFlh5c FyHeAf iPVvYb']""")))
                img_window = driver.find_element(By.XPATH, """//img[@class='sFlh5c FyHeAf iPVvYb']""")
                link = img_window.get_attribute('src')
                images.add(link)
                print(link)
            except Exception as e:
                print(" \n🔴🔴 Link not found! 🔴🔴")
                continue

        print("✔️✔️✔️ Links Scraping complete! ✔️✔️✔️")
        return images

    @staticmethod
    def create_url(search_query):
        parsed_query = parse.urlencode({'q': search_query})
        url = f"https://www.google.com/search?{parsed_query}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjR5qK3rcbxAhXYF3IKHYiBDf8Q_AUoAXoECAEQAw&biw=1291&bih=590"
        return url

    def _download_image(self, url, query):
        try:
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code == 200:
                file_extension = os.path.splitext(urlparse(url).path)[1]
                if not file_extension:
                    file_extension = '.jpg'
                # Remove spaces from query and use underscores instead
                sanitized_query = query.replace(' ', '_')
                filename = f"{sanitized_query}_{int(time.time())}{file_extension}"
                filepath = os.path.join(self.__download_path, filename)
                with open(filepath, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                return filepath
        except Exception as e:
            print(f"Error downloading image: {str(e)}")
        return None

    def scrape(self, query, count):
        self.__image_limit = count
        self.__driver.get(self.create_url(query))
        
        start = time.time()
        images = self._get_images(self.__driver)
        
        print("Downloading images...")
        downloaded_images = []
        for url in images:
            filepath = self._download_image(url, query)
            if filepath:
                downloaded_images.append(filepath)
        
        end = time.time()
        print(f"Total elapsed time for {len(downloaded_images)} images is: {(end - start) / 60:.2f} mins")
        return downloaded_images

    def __del__(self):
        if hasattr(self, '__driver'):
            self.__driver.quit()
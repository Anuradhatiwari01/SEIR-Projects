import sys
import time
# Selenium is used to succesfully load and scrap javascript resources in web page
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Scraper:

    def __init__(self, url):
        if not url.startswith("http"):
            url = "https://" + url
        self.url = url

        print("Scraping Started....")
        print("Target URL: ", self.url)

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(options=options)

    def open_page(self):
        print("Opening webpage using Selenium...")
        self.driver.get(self.url)
        time.sleep(0.3)
        print("Page loaded successfully.")

    def parse_html(self):
        print()
        print("Parsing HTML content...")
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, "html.parser")
        print("HTML parsing completed.")

    def print_title(self):
        print("\nPAGE TITLE:-")

        if self.soup.title:
            print(self.soup.title.get_text().strip())
        else:
            print("No Title Found")

    def print_body(self):
        print()
        print("\nBODY TEXT:-")

        if self.soup.body:
            text = self.soup.body.get_text(" ", strip=True)
            print(text)

    def print_links(self):
        
        print()
        print("\nALL OUTLINKS:-")
        seen = set()
        links = self.soup.find_all("a")
        for tag in links:
            href = tag.get("href")
            if href:
                full_link = urljoin(self.url, href)
                if full_link not in seen:
                    print(full_link)
                    seen.add(full_link)
        print("Total unique links found:", len(seen))

    def run(self):

        self.open_page()
        self.parse_html()
        self.print_title()
        self.print_body()
        self.print_links()

        print("\nScraping completed.")
        self.driver.quit()


if len(sys.argv) != 2:
    print("Invalid input or No url given")
    sys.exit()

scraper = Scraper(sys.argv[1])
scraper.run()
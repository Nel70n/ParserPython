from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep

import csv


class ParseLink:
    def __init__(self):
        self.SITES_FOR_PARSING = [
            "bbc.com/russian", 
            "cnn.com", 
            "reuters.com", 
            "lenta.ru", 
            "ria.ru", 
            "polit.ru", 
            "apn.ru", 
            "e1.ru", 
            "regions.ru"
        ]

    def Parse_query(self, query : str, name_file : str, count_pages : int):

        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")
        with open("data//" + name_file, "w") as f:
            for self.site in self.SITES_FOR_PARSING:
                
                self.driver.get("https://searx.tiekoetter.com")

                self.query_input = self.driver.find_element(By.XPATH, "//input[@name='q']")
                self.query_input.send_keys(query + " site:" + self.site, Keys.ENTER)    

                
                self.number_page = 0
                self.writer = csv.writer(f)

                while self.number_page < count_pages:
                    try:
                        self.target_url = self.driver.find_element(
                            By.XPATH, 
                            "//div[@id='urls']/article[@class='result result-default category-general google']"
                        )

                        self.select_urls = self.driver.page_source
                        self.soup = BeautifulSoup(self.select_urls, "html.parser")
                        self.links_list = []

                        for self.link in self.soup.find_all('a'):
                            self.href_tag = self.link.get('href')
                            if self.href_tag.find('web.archive.org') == -1:
                                self.links_list.append(self.href_tag)

                        self.unique_links = set(self.links_list[2:-9])  

                        for self.link in self.unique_links:
                            self.writer.writerow(list(self.link.split(" ")))

                        self.button_next_page = self.driver.find_element(
                            By.XPATH,
                            "//form[@class='next_page']/div[@class='right']/button[@type='submit']"
                        )  
                            
                        sleep(5)
                        self.button_next_page.click()
                        self.number_page += 1
            
                    except NoSuchElementException:
                        print("[!] Not found any links!")
                        sleep(10)
                        break
            f.close()

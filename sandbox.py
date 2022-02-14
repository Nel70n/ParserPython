from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
from time import sleep

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.get("https://searx.tiekoetter.com")

print("[*] Enter query")
query = input()

query_input = driver.find_element(By.XPATH, "//input[@name='q']")
query_input.send_keys(query, Keys.ENTER)

with open("test.csv", "a") as f:
    number_pages = 1
    writer = csv.writer(f)
    while number_pages < 5:
        try:    
            target_url = driver.find_element(
                By.XPATH, 
                "//div[@id='urls']/article[@class='result result-default category-general google']"
            )

            
            select_urls = driver.page_source
            soup = BeautifulSoup(select_urls, "html.parser")
            links_list = []
            for link in soup.find_all('a'):
                href_link = link.get('href')
                if href_link.find('web.archive.org') == -1:
                    links_list.append(href_link)

            unique_links = set(links_list[2:-9])

            for link in unique_links:
                writer.writerow(list(link.split(" ")))

            next_button = driver.find_element(
                By.XPATH, 
                "//form[@class='next_page']/div[@class='right']/button[@type='submit']"
            ) 

            sleep(5)
            next_button.click()
            number_pages += 1

        except NoSuchElementException:
            print("GGf")
            f.close()
            break




'''

while True:
    try: 
        target_url = driver.find_element(By.XPATH, "//div[@id='urls']/article[@class='result result-default category-general google']")
    except NoSuchElementException:
        break
search_element = driver.find_element_by_css_selector("input#q")

search_element.send_keys("E site:bbc.com/russian", Keys.ENTER)


next_button = driver.find_element_by_xpath("//form[@class='next_page']/div[@class='right']/button[@type='submit']")
next_button.click()


'''

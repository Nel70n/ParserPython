import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep


class ParseLink:
    def __init__(self):
        # Новостные сайты для парсинга
        self.SITES_FOR_PARSING = [
            "bbc.com", 
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
        '''
         Блок парсинга новостных источников на основе открытой поисковой системы Searx
         Дополнительно к этому используются команды Google Dorks, для поиска непосредственно
         на сайте. Результат работы функции – csv файл с ссылками на статьи на основе запроса.

         На вход функции нужно ввести: запрос, имя для файла (без .csv), количество страниц, 
         которые будут парсится для каждого сайта из списка SITES_FOR_PARSING. 
         Вводить параметры нужно через ", "
        '''
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")
        with open("data//" + name_file, "w") as f:
            # Перебор по сайтам из списка
            for self.site in self.SITES_FOR_PARSING:
                # Запрашиваем сайт 
                self.driver.get("https://searx.tiekoetter.com")
                # Производим поиск ввода
                self.query_input = self.driver.find_element(By.XPATH, "//input[@name='q']")
                # Вводим в этот блок Запрос и команду google dorks site:...
                self.query_input.send_keys(query + " site:" + self.site, Keys.ENTER)    

                # Вводим счетчик страниц для подсчета 
                self.number_page = 0
                # Открываем файл 
                self.writer = csv.writer(f)

                while self.number_page < count_pages:
                    # Ищем блок на сайте, связанный с url, если его нет, выходим из цикла. 
                    # Поиск элеметов производим с помощью XPATH
                    try:
                        self.target_url = self.driver.find_element(
                            By.XPATH, 
                            "//div[@id='urls']/article[@class='result result-default category-general google']"
                        )
                        # Сохраняем файл сайта
                        self.select_urls = self.driver.page_source
                        # Вносим html код в BS
                        self.soup = BeautifulSoup(self.select_urls, "html.parser")
                        self.links_list = []
                        # Ищем все теги <a> и проходим по ссылкам в них.
                        for self.link in self.soup.find_all('a'):
                            self.href_tag = self.link.get('href')
                            # На данный момент архивы не сохраняем, ибо большинство 
                            # архивов – это копии рабочих сайтов
                            if self.href_tag.find('web.archive.org') == -1:
                                self.links_list.append(self.href_tag)

                        # Исключаем неверные ссылки и повторения
                        self.unique_links = set(self.links_list[2:-9])  

                        # Сохраняем их в файл
                        for self.link in self.unique_links:
                            self.writer.writerow(list(self.site ,self.link.split(" ")))

                        # Ищем кнопку перехода на следующую страницу
                        self.button_next_page = self.driver.find_element(
                            By.XPATH,
                            "//form[@class='next_page']/div[@class='right']/button[@type='submit']"
                        )

                        # Вносим задержку для того, чтобы браузер и сайт не блокировал по ошибке 429 (403)
                        sleep(60)
                        self.button_next_page.click()
                        self.number_page += 1
            
                    # Ошибка библиотеки selenium. Подразумевает отсутствие блока, 
                    # который ищется с помощью find_element
                    except NoSuchElementException:
                        print("[!] Not found any links!")
                        sleep(60)
                        break
            # Закрываем файл
            f.close()

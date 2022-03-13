import csv
import bs4

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup, Comment
from time import sleep
from math import log, exp

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

    def ParseQuery(self, query : str, name_file : str, count_pages : int):
        '''
         Блок парсинга новостных источников на основе открытой поисковой системы Searx
         Дополнительно к этому используются команды Google Dorks, для поиска непосредственно
         на сайте. Результат работы функции – csv файл с ссылками на статьи на основе запроса.

         На вход функции нужно ввести: запрос, имя для файла (без .csv), количество страниц,
         которые будут парсится для каждого сайта из списка SITES_FOR_PARSING.
         Вводить параметры нужно через ", "
        '''
        self.driver = webdriver.Chrome(executable_path="drivers/chromedriver.exe")
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
                        self.unique_links = set(self.links_list[2:-10])
                        # print(self.unique_links)
                        # Сохраняем их в файл
                        for self.link in self.unique_links:
                            self.row = self.site.split(" ")
                            self.row.append(self.link)
                            self.writer.writerow(self.row)

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
            self.driver.close()

class ScoringSite():
    """
     # TODO: Write documentation
    """
    def EncodingTag(self, target_tag):
        self.count = 1
        if isinstance(target_tag, bs4.element.Tag):

            for child in target_tag:
                if isinstance(child, bs4.element.Tag):
                    if child.parent.name == "body":
                        child['individual-id'] = str(self.count)
                        self.count += 1
                    else:
                        child['individual-id'] = str(child.parent['individual-id']) + '.'+str(self.count)
                        self.count += 1
                    #print(child.string)

            if target_tag.strings != None:
                    for child in target_tag:
                        self.EncodingTag(child)

    def ClearCode(self, html_content):
        self.FlagWhile = True
        while self.FlagWhile:
            if html_content.script != None:
                self.r = html_content.script.extract()
            else:
                self.FlagWhile = False
        for element in html_content(text=lambda text: isinstance(text, Comment)):
            element.extract()

        for i in html_content.descendants:
            if type(i) == bs4.element.Tag and len(i.attrs.keys()) != 0:
                listkey = list(i.attrs.keys())
                for attr in listkey:
                    if attr != "href":
                        del (i[attr])
        return html_content

    def ScoringTag(self, html_content):

        self.LCb  = 0
        self.Cb   = 0
        for child in html_content.descendants:
            if isinstance(child, bs4.element.Tag):
                    if child.get('href') == None: # блок тегов без ссылок
                        self.LinkFlag = False
                    else: # блок тегов с ссылками
                        self.LinkFlag = True

            if (type(child) == bs4.element.NavigableString and len(child) != 1):
                    # Считаем параметры для всего блока вызова
                    self.Cb += len(child.text)
                    if self.LinkFlag: # Считаем параметры для тегов с ссылками
                        self.LCb += len(child.text)


        for child in html_content.descendants:
            self.Ti      = 0 # Количество тегов в прямом ребенке body
            self.Ci      = 0 # Количество символов в теге всего ребенка
            self.LCi     = 0 # Количество символов в гиперссылках
            self.noneLCi = 0 # Количестов не гиперссылочных символов
            self.LTi     = 0 # Количество тэгов гипрессылок

            if isinstance(child, bs4.element.Tag):
                #print(child)
                if child.get('href') == None: # блок тегов без ссылок
                    child['Link'] = "No"
                    self.LinkFlag = False
                else: # блок тегов с ссылками
                    child['Link'] = "Yes"
                    self.LinkFlag = True

                for SubChild in child.descendants:
                    if type(SubChild) == bs4.element.Tag:
                        self.Ti += 1
                    if (type(SubChild) == bs4.element.NavigableString and len(SubChild) != 1):
                        # Считаем параметры для всего блока вызова
                        self.Ci += len(SubChild.text)
                        if self.LinkFlag: # Считаем параметры для тегов с ссылками
                            self.LCi += len(SubChild.text)

                            self.LTi += 1
                        else: # Считаем параметры для тега без ссылок
                            self.noneLCi += len(SubChild.text)
                if self.Ci == 0 or self.Cb == 0:
                    #stack.append(0)
                    child['Score'] = 0
                else:
                    if self.Cb == 0:
                        self.Cb = 1

                    if self.Ti == 0:
                        self.Ti = 1

                    if self.LCi == 0:
                        self.LCi = 1

                    if self.LTi == 0:
                        self.LTi = 1

                    if self.noneLCi == 0:
                        self.noneLCi = 1


                    child['Score'] = (self.Ci/self.Ti)*log(self.Ci*self.Ti/(self.LCi*self.LTi), \
                    log((self.Ci/self.noneLCi)*self.LCi + (self.LCb/self.Cb) * self.Ci + exp(1)))
                    #stack.append(scoring)
                    self.DataFromSites.append((self.Ci/self.Ti)*log(self.Ci*self.Ti/(self.LCi*self.LTi), log((self.Ci/self.noneLCi)*self.LCi + (self.LCb/self.Cb) * self.Ci + exp(1))))
                    child['Param'] = str((self.LCb, self.Cb, self.Ci, self.Ti, self.LCi, self.noneLCi, self.LTi))
                #print(f'self.LCb : {self.LCb}\nall (self.Cb): {self.Cb}\nCi {self.Ci}\nTi: {self.Ti}\nLCi: {self.LCi}\nnoneLCi: {self.noneLCi}\nLTi: {self.LTi}\n')
        return html_content

    def ViewStatistic(self, ScoreList, site):
        with open("Score " + site + ".csv", "a", encoding='utf-8') as f:
            write = csv.writer(f)
            write.writerow(list(site.split(" ")))
            write.writerow(ScoreList)
            f.close()

    def StartWork(self, patch_file : str):
        self.driver = webdriver.Chrome(executable_path="drivers/chromedriver.exe")
        with open(patch_file, "r", encoding='utf-8') as f:
            self.reader = csv.reader(f)
            for line in self.reader:
                self.driver.get(line[1])
                self.DataFromSites = []
                s = self.driver.page_source
                self.soup = BeautifulSoup(s, "html.parser")
                self.ClearFile = self.ClearCode(self.soup.body)
                self.EncodingTag(self.ClearFile)
                self.SaveFile = self.ScoringTag(self.ClearFile)
                with open("data//result " + line[0]+ ".html", "w", encoding='utf-8') as g:
                    g.writelines(str(self.SaveFile.prettify()))
                    g.close()

                with open("data//scoring data.csv", "a", encoding='utf-8') as r:
                    self.write = csv.writer(r)
                    self.write.writerow(str(line[0]).split(" "))
                    self.write.writerow(self.DataFromSites)
                    r.close()
                sleep(60)
            self.driver.close()

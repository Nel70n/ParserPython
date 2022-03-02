from tkinter import W
import bs4
import csv

from bs4 import BeautifulSoup, Comment
from h11 import Data
from mysqlx import View
from selenium import webdriver
from math import log, exp
from datetime import datetime
from time import sleep


def ClearCode(html_content):
    FlagWhile = True

    while FlagWhile:
        if html_content.script != None:
            r = html_content.script.extract()
        else:
            FlagWhile = False
    for element in html_content(text=lambda text: isinstance(text, Comment)):
        element.extract()
        
    for i in html_content.descendants:
        if type(i) == bs4.element.Tag and len(i.attrs.keys()) != 0:
            listkey = list(i.attrs.keys())
            for attr in listkey:
                if attr != "href":
                    del (i[attr])
    return html_content

def ScoringTag(html_content):

    LCb  = 0
    Cb   = 0
    for child in html_content.descendants:  
        if isinstance(child, bs4.element.Tag):
                if child.get('href') == None: # блок тегов без ссылок
                    LinkFlag = False
                else: # блок тегов с ссылками
                    LinkFlag = True

        if (type(child) == bs4.element.NavigableString and len(child) != 1):
                # Считаем параметры для всего блока вызова
                Cb += len(child.text)
                if LinkFlag: # Считаем параметры для тегов с ссылками
                    LCb += len(child.text)
   
    
    for child in html_content.descendants:  
        Ti      = 0 # Количество тегов в прямом ребенке body
        Ci      = 0 # Количество символов в теге всего ребенка
        LCi     = 0 # Количество символов в гиперссылках
        noneLCi = 0 # Количестов не гиперссылочных символов
        LTi     = 0 # Количество тэгов гипрессылок

        if isinstance(child, bs4.element.Tag):
            #print(child)   
            if child.get('href') == None: # блок тегов без ссылок
                child['Link'] = "No"
                LinkFlag = False
            else: # блок тегов с ссылками
                child['Link'] = "Yes"
                LinkFlag = True

            for SubChild in child.descendants:
                if type(SubChild) == bs4.element.Tag:
                    Ti += 1
                if (type(SubChild) == bs4.element.NavigableString and len(SubChild) != 1):
                    # Считаем параметры для всего блока вызова
                    Ci += len(SubChild.text)
                    if LinkFlag: # Считаем параметры для тегов с ссылками
                        LCi += len(SubChild.text)
                        
                        LTi += 1
                    else: # Считаем параметры для тега без ссылок
                        noneLCi += len(SubChild.text)
            if Ci == 0 or Cb == 0:
                #stack.append(0)
                child['Score'] = 0
            else:
                if Cb == 0: 
                    Cb = 1
                
                if Ti == 0:
                    Ti = 1
                
                if LCi == 0:
                    LCi = 1

                if LTi == 0:
                    LTi = 1
                
                if noneLCi == 0:
                    noneLCi = 1

                
                child['Score'] = (Ci/Ti)*log(Ci*Ti/(LCi*LTi), log((Ci/noneLCi)*LCi + (LCb/Cb) * Ci + exp(1)))
                #stack.append(scoring)
                DataFromSites.append(child['Score'])
                child['Param'] = str((LCb, Cb, Ci, Ti, LCi, noneLCi, LTi))
            #print(f'LCb : {LCb}\nall (Cb): {Cb}\nCi {Ci}\nTi: {Ti}\nLCi: {LCi}\nnoneLCi: {noneLCi}\nLTi: {LTi}\n')  
    return html_content

def ViewStatistic(ScoreList, site):
    with open("Score " + site + ".csv", "a", encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(list(site.split(" ")))
        write.writerow(ScoreList)
        f.close()

driver = webdriver.Chrome(executable_path="drivers/chromedriver.exe")
with open("data//datas.csv", "r", encoding='utf-8') as f:
    reader = csv.reader(f)
    for line in reader:
        driver.get(line[1])
        DataFromSites = []
        s = driver.page_source
        soup = BeautifulSoup(s, "html.parser")
        ClearFile = ClearCode(soup.body)
        SaveFile = ScoringTag(ClearFile)
        with open("data//result " + line[0]+ ".html", "w", encoding='utf-8') as g:
            g.writelines(str(SaveFile.prettify()))
            g.close()



driver.close()


print(DataFromSites)

'''    
        with open("data//acoring data.csv", "a", encoding='utf-8') as r:
            wrte = csv.writer(r)
            wrte.writerow(str(line[0]).split(" "))
            wrte.writerow(DataFromSites)
            r.close()
        sleep(30)        
'''
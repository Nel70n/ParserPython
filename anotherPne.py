#-*- coding: utf-8 -*-
import bs4
import csv


from bs4 import BeautifulSoup, Comment
from selenium import webdriver
from math import log, exp 
from datetime import datetime
        

def RecTwo(child_content):
    rec_soup = BeautifulSoup(str(child_content), "lxml-xml")

    Ti      = 0 # Количество тегов в прямом ребенке body
    Ci      = 0 # Количество символов в теге всего ребенка
    LCi     = 0 # Количество символов в гиперссылках
    noneLCi = 0 # Количестов не гиперссылочных символов
    LTi     = 0 # Количество тэгов гипрессылок
    
    for child in rec_soup.descendants:
        if (type(child) == bs4.element.Tag) or (type(child) == bs4.element.NavigableString and len(child) != 1):
            if type(child) == bs4.element.Tag:
                Ti += 1 
                if child.get('href') == None: # блок тегов без ссылок
                    LinkFlag = False
                else: # блок тегов с ссылками
                    LinkFlag = True


            if type(child) == bs4.element.NavigableString:
                # Считаем параметры для всего блока вызова
                Ci += len(child.text)
                if LinkFlag: # Считаем параметры для тегов с ссылками
                    LCi += len(child.text)
                    LTi += 1
                    pass
                else: # Считаем параметры для тега без ссылок
                    noneLCi += len(child.text)
                    pass
    # print(f'child:\nlen all text {Ci}\nall tags: {Ti}\nNumber chars in links: {LCi}\nNumber chars non links: {noneLCi}\nNumbers tag links: {LTi}\n')
    return {"Ti" : Ti, "Ci" : Ci, "LCi" : LCi, "noneLCi" : noneLCi, "LTi" : LTi, "code" : str(child_content)}

def Score(dict_data : dict):
    number_children = len(dict_data["Ti"])
    LCb = sum(dict_data["LCi"])
    Cb  = sum(dict_data["Ci"])
    result = []
    max_value = 0
    for i in range(number_children):
        if dict_data["Ti"][i] == 0 or dict_data["Ci"][i] == 0:
            result.append(0)
            continue

        if Cb == 0:
            Cb = 1
        
        if dict_data["LCi"][i] == 0:
            dict_data["LCi"][i] = 1

        if dict_data["LTi"][i] == 0:
            dict_data["LTi"][i] = 1

        if dict_data["noneLCi"][i] == 0:
            dict_data["noneLCi"][i] = 1

        content = ""
        for element in dict_data["code"][i]:
            content += element

        result = [(dict_data["Ci"][i]/dict_data["Ti"][i])*log(dict_data["Ci"][i]*dict_data["Ti"][i]/(dict_data["LCi"][i]*dict_data["LTi"][i]),\
            log((dict_data["Ci"][i]/dict_data["noneLCi"][i])*dict_data["LCi"][i] + (LCb/Cb) * dict_data["Ci"][i] + exp(1))),
            content]
        if result[0] > max_value:
            final = result.copy()
    return final

def TextFromSite(html_code : str):
    TextFile = ""
    HtmlSoup = BeautifulSoup(str(html_code), "html.parser")
    for child in HtmlSoup.descendants:
        if type(child) == bs4.element.NavigableString and len(child) > 5:
            print(child.text)
            TextFile += str(child.text).replace("\n", "")

    return TextFile

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
                del (i[attr])  
    return html_content 

def DirectlyChildren(BodyData):
    for child in BodyData.children:
        if len(child) != 1:
            preDict = RecTwo(child)
            for param in (preDict.keys()):
                DictParam[param].append(preDict[param])
    return DictParam


# Отмерка времени
start_time = datetime.now()	
#drive = webdriver.Chrome(executable_path="drivers/chromedriver.exe")
#drive.get("https://www.e1.ru/text/gorod/2015/10/16/53034111/")
drive = webdriver.Chrome(executable_path="drivers/chromedriver.exe")
drive.get("C:/Users/right/Documents/GitHub/ParserPython/data/fff.html")

s = drive.page_source

DictParam = {
    "Ti" : [], 
    "Ci" : [], 
    "LCi" : [], 
    "noneLCi" : [], 
    "LTi": [],
    "code" : []
}

#HtmlData = str(drive.page_source)
HtmlData = str(s)
soup = BeautifulSoup(HtmlData, "lxml-xml")
#body = ClearCode(soup.body)
body = ClearCode(soup)

DictParam = DirectlyChildren(body)

resuilsList = Score(DictParam)

"""with open("data//file_test.csv", "w", encoding='utf-8') as f:
    writer = csv.writer(f)
    for line in resuilsList:
        writer.writerow(resuilsList)
    f.close()
#print(TextFromSite(resuilsList[1]))
"""
f = open("data//fff.txt", "w", encoding='utf-8')
ddd = BeautifulSoup(resuilsList[1], 'html.parser')
f.writelines(ddd.prettify())
f.close()

ScoreAll = []
for children in soup.descendants:
    if isinstance(children, bs4.element.Tag):
        res = RecTwo(children)
        res = DirectlyChildren(res)
        ScoreAll.append(Score(res))

print(datetime.now() - start_time)
drive.close()
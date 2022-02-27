#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import bs4
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
    return {"Ti" : Ti, "Ci" : Ci, "LCi" : LCi, "noneLCi" : noneLCi, "LTi" : LTi}

def Score(dict_data : dict):
    number_children = len(dict_data["Ti"])
    LCb = sum(dict_data["LCi"])
    Cb  = sum(dict_data["Ci"])
    result = []
    for i in range(number_children):
        if dict_data["Ti"][i] == 0 or dict_data["Ci"][i] == 0:
            result.append(0)
        elif dict_data["LCi"][i] == 0 and dict_data["LTi"][i] == 0:
            result.append(
                (dict_data["Ci"][i]/dict_data["Ti"][i])*log(dict_data["Ci"][i]*dict_data["Ti"][i]/(1*1),\
                log((dict_data["Ci"][i]/dict_data["noneLCi"][i])*1 + (LCb/Cb) * dict_data["Ci"][i] + exp(1)))
            )
        elif dict_data["LCi"][i] == 0:
            result.append(
                (dict_data["Ci"][i]/dict_data["Ti"][i])*log(dict_data["Ci"][i]*dict_data["Ti"][i]/(1*dict_data["LTi"][i]),\
                log((dict_data["Ci"][i]/dict_data["noneLCi"][i])*1 + (LCb/Cb) * dict_data["Ci"][i] + exp(1)))
            )
        elif dict_data["LTi"][i] == 0:
            result.append(
                (dict_data["Ci"][i]/dict_data["Ti"][i])*log(dict_data["Ci"][i]*dict_data["Ti"][i]/(dict_data["LCi"][i]*1),\
                log((dict_data["Ci"][i]/dict_data["noneLCi"][i])*dict_data["LCi"][i] + (LCb/Cb) * dict_data["Ci"][i] + exp(1)))
            )
        else:
            result.append(
                (dict_data["Ci"][i]/dict_data["Ti"][i])*log(dict_data["Ci"][i]*dict_data["Ti"][i]/(dict_data["LCi"][i]*dict_data["LTi"][i]),\
                log((dict_data["Ci"][i]/dict_data["noneLCi"][i])*dict_data["LCi"][i] + (LCb/Cb) * dict_data["Ci"][i] + exp(1)))
            )

    return result


        

start_time = datetime.now()	

# drive = webdriver.Chrome("drivers/chromedriver.exe")

# drive.get("https://www.bbc.com/russian/news-59386453")

HtmlData = '''
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html lang="ru">
 <head>
  <meta charset="utf-8"/>
  <title>
   Название сайта
  </title>
 </head>
 <body>
	<div id="main text">

        <div id="digital information">
            <h1>Заголовок 1</h1>
            <p> С другой стороны сложившаяся структура организации представляет собой интересный эксперимент проверки системы обучения кадров, соответствует насущным потребностям. Товарищи! реализация намеченных плановых заданий в значительной степени обуславливает создание направлений прогрессивного развития. </p>
            <p> С другой стороны сложившаяся структура организации представляет собой интересный эксперимент проверки системы обучения кадров, соответствует насущным потребностям. Товарищи! реализация намеченных плановых заданий в значительной степени обуславливает создание направлений прогрессивного развития. </p>
            <a href="#">Kmkrv</a>
        </div>

	</div>
	<div name='part two'>

        <div if="footet">
            <p>footer one</p>
            <p>footer two</p>
            
        </div>
        <a href="#">Dude</a>

	</div>
 </body>
</html>
'''

# HtmlData = drive.page_source.encode('utf-8')

soup = BeautifulSoup(HtmlData, "lxml-xml")
body = soup.body
# print(type(body))
DictParam = {
    "Ti" : [], 
    "Ci" : [], 
    "LCi" : [], 
    "noneLCi" : [], 
    "LTi": []
}
for child in body.children:
    if len(child) != 1:
        preDict = RecTwo(child)
        for param in (preDict.keys()):
            DictParam[param].append(preDict[param])
        
resuilsList = Score(DictParam)
print(resuilsList)

print(datetime.now() - start_time)
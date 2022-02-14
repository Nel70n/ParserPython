# ParserPython
 
 Задача:
 Автоматизация OSINT. 
 Парсинг открытой информации в Интернет (статьи, форумы, ...) как текстовой, так и графической (возможно в будущем и видео). 
 Обнаружение статей, относящихся к предприятию. 
 Построение графа знаний о предприятии, обнаружение чувствительной информации (персональные данные, коммерческая тайна, компрометирующая информация). 

 Алгоритм работы с информацией.
    1. Поиск с помощью поисковых систем ссыллок по тематике. 
        a. классификация ссылок по уникальности и зависимости
        b. исключение повторений по URL
        c. проверка на доступность
    2. Обработка данных со страницы:
        a. разделение страницы на наборы блоков
        b. исключение маловажных объектов
        c. объединение схожих объектов
        d. адаптация рекомендуемых статей/новостей
    

Поиск ссылок на по новостным источникам:
    На первое время сделал вывод, что с помощью google Dorks можно парсить новости с сайтов, оз

    Набор новостных ссылок:
    (RU/ENG):
        1. site:bbc.com 
        2. site:cnn.com 
        3. site:reuters.com 
        4. www.wnnetwork.com (недоступно)
        5. vanderbilt.edu (архив телевизионной информации. Сложен в парсинге, нужна регистрация. Пока не использую)
    (RU):
        1. site:lenta.ru
        2. site:ria.ru
        3. site:polit.ru
        4. site:apn.ru
        5. site:e1.ru
        6. site:regions.ru
    (ENG):
        <В доработке>




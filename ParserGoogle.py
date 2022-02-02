import requests
from bs4 import BeautifulSoup
import urllib.parse 

print("Use the query:", end=" ")
query = input().replace(" ", "+")

url        = "https://google.com/search?q=" + query
USER_AGENT = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"

headers = {
    "user_agent": USER_AGENT
}
response = requests.request("GET", url, headers=headers)

if response.status_code == 200:
    print("[*] OK! ")
    soup = BeautifulSoup(response.content, "html.parser")

file = open("ParserGoogle.txt", "w", encoding='utf-8')
for link in soup.find_all('a'):
    if link.get('href').find('/url?q=') != -1:
        
        edit_file = link.get('href').replace("/url?q=", "")[:link.get('href').replace("/url?q=", "").find("&sa")]
        edit_file = urllib.parse.unquote(edit_file)
        file.write(edit_file + '\n')

#TODO1: Реализовать это в класс и произвести считывание всех ссылок с запроса.
#TODO2: Производить запись в CSV файл
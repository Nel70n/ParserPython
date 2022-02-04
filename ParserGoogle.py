import requests
from bs4 import BeautifulSoup
import urllib.parse 
import csv

class ParseLink:

    def CreateQuery(self, query: str, type_doc: str, site: str):
        self.file_type = "+filetype:" + type_doc
        self.inver = "+-" + site
        self.url   = "https://google.com/search?q=" + self.ConverQuery(query) + self.file_type + self.inver

    def ConverQuery(self, no_conv_query):
        return no_conv_query.replace(" ", "+")

    def CreateResponse(self, name_file):
        self.USER_AGENT = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        self.headers = {
            "user_agent": self.USER_AGENT
        }

        flag = True
        self.start = 0
        while flag:
            self.url_try = self.url + "&start=" + str(self.start)
            self.response = requests.request("GET", self.url_try, headers=self.headers)
            if self.response.status_code == 200:
                print("[*] OK! ")
                
                self.soup = BeautifulSoup(self.response.content, "html.parser")

            with open(name_file, 'a') as f:
                self.writer = csv.writer(f)
                self.ListLinks = []
                for link in self.soup.find_all('a'):
                    if link.get('href').find('/url?q=') != -1:
                        self.edit_file = link.get('href').replace("/url?q=", "")[:link.get('href').replace("/url?q=", "").find("&sa")]
                        self.edit_file = urllib.parse.unquote(self.edit_file)
                        self.ListLinks.append(list(self.edit_file.split(" ")))
                
                if len(self.ListLinks) != 3:
                    for link in self.ListLinks[:-3]: 
                        self.writer.writerow(link)
                else:
                    flag = False
            self.start += 10

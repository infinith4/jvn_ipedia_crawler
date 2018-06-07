import urllib3
from bs4 import BeautifulSoup 

class UrlUtil:
    def __init__(self, reqUrl, proxyUrl):
        self.reqUrl = reqUrl
        self.proxyUrl = proxyUrl

    def RequestUrl(self):
        try :
            urlList=[]
            url = self.reqUrl

            http = urllib3.ProxyManager(proxy_url = self.proxyUrl, maxsize=10)
            res = http.request('GET', url)
            while True:
                soup = BeautifulSoup(res.data, 'html.parser')
                table = soup.findAll("table",{"class":"result_class"})[0]
                rows = table.findAll("tr")
                for i in rows:
                    td = i.findAll("td")
                    if td != None and len(td) != 0:
                        print(td[0].findAll('a')[0].get("href"))
                        urlList.append(td[0].findAll('a')[0].get("href"))
                nextPage = soup.findAll("a",{"title":"next page"})
                if len(nextPage) > 0:
                    print(nextPage[0])
                    print(nextPage[1])
                    res = http.request('GET', "https://jvndb.jvn.jp/search/" + nextPage[0].get('href'))
                else:
                     break   
            return urlList
        except Exception as ex:
            print("アクセスに失敗しました。")
            print(ex)

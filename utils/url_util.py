import urllib3
from bs4 import BeautifulSoup 

class UrlUtil:
    def __init__(self, req_url):
        self.req_url = req_url

    def RequestUrl(self):
        try :
            urlList=[]
            url = "https://jvndb.jvn.jp/search/index.php?mode=_vulnerability_search_IA_VulnSearch&lang=ja&keyword=python&useSynonym=1&vendor=&product=&datePublicFromYear=&datePublicFromMonth=&datePublicToYear=&datePublicToMonth=&dateLastPublishedFromYear=&dateLastPublishedFromMonth=&dateLastPublishedToYear=&dateLastPublishedToMonth=&cwe=&searchProductId="
            http = urllib3.PoolManager()
            res = http.request('GET', url)
            soup = BeautifulSoup(res.data, 'html.parser')
            #netPage = soup.findAll("a",{"title":"next page"})

            table = soup.findAll("table",{"class":"result_class"})[0]
            rows = table.findAll("tr")
            for i in rows:
                td = i.findAll("td")
                if td != None and len(td) != 0:
                    print(td[0].findAll('a')[0].get("href"))
                    urlList.append(td[0].findAll('a')[0].get("href"))
            return urlList
        except Exception as ex:
            print("アクセスに失敗しました。")
            print(ex)

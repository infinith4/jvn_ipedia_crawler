from utils import url_util
from bs4 import BeautifulSoup 
import urllib3

urlUtil = url_util.UrlUtil("")
urlList = urlUtil.RequestUrl()
http = urllib3.PoolManager()
for url in urlList:
    jvnUrl = "https://jvndb.jvn.jp" + url
    res = http.request('GET', jvnUrl)
    print(jvnUrl)
    soup = BeautifulSoup(res.data, 'html.parser')
    table = soup.findAll("table",{"class":"vuln_table_clase"})[0]
    rows = table.findAll("tr")
    rowIndex = 0
    for i in rows:
        td = i.findAll("td")
        if td != None and len(td) != 0:
            solution = td[0].select("a[name^='solution']")
            if solution != None and len(solution) != 0:
                if "対策" in solution[0].get_text():
                    tr = rows[rowIndex + 1].get_text()
                    if "ベンダより正式な対策が公開されています。" in tr:
                        print("OK")
        rowIndex = rowIndex + 1
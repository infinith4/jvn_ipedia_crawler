from utils import url_util
from bs4 import BeautifulSoup 
import urllib3
import logging.config
import yaml

logging.config.fileConfig("logging_debug.conf")
logger = logging.getLogger()

try:
    conf = open("jvn_crawler.yml", "r+")
    confdata = yaml.load(conf)
    # proxyUrl = ""
    # jvnBaseUrl = ""
    # jvnRequestUrl = ""
    proxyUrl = confdata['PROXY_URL']
    jvnBaseUrl = confdata['JVN_BASE_URL']
    jvnRequestUrl = confdata['JVN_REQUEST_URL']

    urlUtil = url_util.UrlUtil(jvnRequestUrl, proxyUrl)
    urlList = urlUtil.RequestUrl()
    http = urllib3.ProxyManager(proxy_url = proxyUrl, maxsize=10)
    for url in urlList:
        jvnUrl = jvnBaseUrl + url
        logger.info(jvnUrl)
        res = http.request('GET', jvnUrl)
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
                        logger.info("## 対策")
                        if "ベンダより正式な対策が公開されています。" in tr:
                            logger.info(tr)
                            logger.info("OK")
                        else:
                            logger.info(tr)
            rowIndex = rowIndex + 1
except Exception as ex:
    logger.error(ex)
    print(ex)
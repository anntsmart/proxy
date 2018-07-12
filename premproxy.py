import requests
import re
from lxml import etree
import jsbeautifier
import time


def getip(num):
    header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
    proxy = {"http" : "127.0.0.1:1080"}
    for i in range(1,num):
        s = requests.Session()
        url = "https://premproxy.com/list/ip-port/%s.htm" % str(i)
        #print url
        content = s.get(url,proxies=proxy,headers=header,timeout=5).content
        #print content
        selector = etree.HTML(content)
        jquery = ("https://premproxy.com" + re.findall(r'<script src="/js1/jq.js"></script><script src="(.*?)></script></head>',content)[0]).replace('"','')
        #print jquery
        js_content = s.get(jquery,proxies=proxy).content
        js_filter = jsbeautifier.beautify(js_content)
        #print js_filter
        texts = selector.xpath('//*[@id="ipportlist"]/li/text()')
        for i in texts:
            pat = re.compile(r'' + i + '(.*?)</span></li>')
            result = (re.findall(pat,content))[0].replace('<span class="','').replace('">','')
            num = js_filter.find(result)
            pat_js = r'%s\\\'\)\.html\((.*?)\)' % result
            try:
                port = (re.findall(pat_js,js_filter[num:],re.S))[0]
                print i+port
            except:
                pass
            #time.sleep(5)
            #print result


            
        '''
        pat_texts = r'<ul id="ipportlist">(.*?)</span></li></ul>'
        result_texts = re.findall(pat_texts,content,re.S)
        #print result_texts
        '''


if __name__=="__main__":
    nums = raw_input("Input numbers:")
    getip(int(nums))
    

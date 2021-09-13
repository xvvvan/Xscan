# -*- coding: utf-8 -*-
import requests,re
method = ['http://','https://']
dic = ['','/console/login/LoginForm.jsp']
def webtitle(url):
    for m in method:
        for d in dic:
            try:

                urls = m+url+d
                # print(urls)
                r = requests.get(urls,timeout=3)
                # result=result.decode('utf-8')
                r.encoding=r.apparent_encoding
                # print(r.text)
                # print(r.text)
                response = r.text
                # print(r.read())
                title = re.findall('<title>.*</title>',response)
                title = title[0].replace('<title>','').replace('</title>','')
                # print(title)
                if title:
                    return title
            except:
                pass
    return 'None'
        # <title>百度一下，你就知道</title>

if __name__ == '__main__':
    a = webtitle('10.243.75.41:7001')
    print(a)

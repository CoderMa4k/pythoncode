from urllib.request import urlopen
from urllib import request
import urllib
from bs4 import BeautifulSoup
sum = 0
all = int(input('请输入要爬取的页数：'))
for x in range(1,all):
    re = request.Request('http://588ku.com/beijing/0-31-dnum-0-%d/'%x)
    re.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
    gethtml = urlopen(re)
    data = gethtml.read().decode('utf8')
    soup = BeautifulSoup(data,'lxml')
    imgs = soup.find_all('img', {'class': 'lazy'})

    for img in imgs:
        name = img['alt']
        imgsrc = img['data-original'].split('!')[0]
        # 文件路径一定要注意 直接写此目录下的文件名就好不要加斜杠  /file 错误
        request.urlretrieve(imgsrc, 'file/%s.jpg' % name)
        sum = sum + 1
        print('爬取图片成功,一共爬取了%d张图片'%sum)
        #print(imgsrc)
        #print(img)
        #print(soup.prettify())
        # 在写入和读取的过程中可以进行编码 在第三个参数上加上 encoding = 'utf8/gbk'
        # w = open('1.html','w',encoding='utf8')
        # w.write(data)
        # w.close()
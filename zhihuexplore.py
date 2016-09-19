from urllib.request import urlopen
import re
import pymysql.cursors
from bs4 import BeautifulSoup
connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '123456',
    db = 'zhihu',
    charset = 'utf8mb4'
)
keys = ['python','java','nodejs','javascript','c++','react','android''html']
try:
    with connection.cursor() as cursor:
        sql = "insert into urls values(%s,%s,%s)"
        for key in keys:
            data = urlopen('http://www.zhihu.com/search?type=content&q=%s' % key)
            html_data = data.read().decode('utf-8')
            soup = BeautifulSoup(html_data, 'lxml')
            # find_all('标签',)后面的可以是用{}括起来
            urlList = soup.find_all('a', {'class': 'js-title-link'})
            # 标签对象['属性']
            for s in urlList:
                href = 'www.zhihu.com' + s['href']
                cursor.execute(sql,(0,s.get_text(),href))
                connection.commit()
finally:
    connection.close()

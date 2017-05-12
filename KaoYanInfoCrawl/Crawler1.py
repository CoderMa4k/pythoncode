from bs4 import BeautifulSoup
import requests
import re
import xlwt
def getInfo(page,sheet):
    url = 'http://www.kaoshidian.com/course/public-0-0-0-0-0-0-1-' + str(page) + '.html'
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc,'lxml')
    course_list = soup.find_all(class_='allcurseConntent-item-ul')
    for c in range(1,len(course_list)):
        title = re.findall('<a.*?title="(.*?)"',course_list[c-1].prettify(),re.S)
        price = course_list[c-1].find('em',class_='font-v font-s18 mar_r10 c_red').text[1:]
        sheet.write(c+(page-1)*19,0,str(title[0]))
        sheet.write(c+(page-1)*19,1,str(price))
def main():
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('sheet')
    sheet.write(0,0,'商品名称')
    sheet.write(0,1,'商品价格')
    for i in range(1,26):
        print('爬取第' + str(i) + '页')
        getInfo(i,sheet)
    workbook.save('t.xls')
if __name__ == '__main__':
    main()

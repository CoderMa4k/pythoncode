from  selenium  import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re
import time
import xlwt
browser = webdriver.Chrome();
browser.get('https://www.tmall.com/')
wait = WebDriverWait(browser, 10)

input = wait.until(
   EC.presence_of_element_located((By.CSS_SELECTOR, "#mq"))
)
submit = wait.until(
   EC.presence_of_element_located((By.CSS_SELECTOR, "#mallSearch > form > fieldset > div > button"))
)
input.send_keys('考研课程')  ## 可以修改任意关键字
submit.click()
total = wait.until(
   EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div > div.ui-page > div > b.ui-page-skip > form > input[type="hidden"]:nth-child(3)'))
)
pages = int(total.get_attribute('value'))
print(pages)
def get_products(result):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_ItemList .product')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#J_ItemList .product').items()
    for item in items:
       result = result + item.html()
    return result
result=''
workbook = xlwt.Workbook()
def output(result,pages):
    test=re.findall('</b>(.*?)</em>.*?title="(\w+考研\w+)"',result,re.S)
    sheet = workbook.add_sheet('sheet'+str(pages))
    print(test)
    sheet.write(0,0,'商品名称')
    sheet.write(0,1,'商品的价格')
    for i in range(1,len(test)):
        sheet.write(i,0,test[i][1])
        sheet.write(i,1,test[i][0])
def next_page(i,result):
    try:
        page_select = wait.until(
           EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div > div.ui-page > div > b.ui-page-skip > form > input.ui-page-skipTo'))
        )
        page_submit = wait.until(
           EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div > div.ui-page > div > b.ui-page-skip > form > button'))
        )
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#content > div > div.ui-page > div > b.ui-page-num > b.ui-page-cur'),str(i-1)))
        # 清空
        time.sleep(1)
        result = result + get_products(result)
        output(result, i)
        # content > div > div.ui-page > div > b.ui-page-num > b.ui-page-cur
        time.sleep(1)
        page_select.clear()
        page_select.send_keys(i)
        page_submit.click()
    except Exception:
        page_submit = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#content > div > div.ui-page > div > b.ui-page-skip > form > button'))
        )
        page_submit.click()
        next_page(i+1,result)
for i in range(2, pages+1):
    next_page(i, result)
workbook.save('test.xls')
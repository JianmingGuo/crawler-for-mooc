from selenium import webdriver
from pyquery import PyQuery as pq
from itertools import  chain
import time
from lxml.html import etree
import xlwt

def getPageUrl(pageSource):
    code = pq(pageSource)
    href = code("#j-courseCardListBox a")
    urlList = []
    for i in href:
        temp = str(code(i).attr("href"))
        if temp.__contains__("www") and not temp.__contains__("https"):
            urlList.append("http:" + temp)
    urlList = list(set(urlList))
    return urlList

def getAllUrl(pageSourceUrl):
    chrome = webdriver.PhantomJS(executable_path="D:\\software\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
    webdriver.PhantomJS()
    chrome.get(pageSourceUrl)
    allUrl=[]
    count=1
    while (True):
        allUrl=chain(allUrl,getPageUrl(chrome.page_source))
        print(count)
        print(chrome.find_element_by_class_name("ux-pager_btn__next").get_attribute("class"))
        chrome.find_element_by_link_text("下一页").click()
        time.sleep(3)
        # if (chrome.find_element_by_class_name("ux-pager_btn__next").get_attribute("class") == "ux-pager_btn ux-pager_btn__next z-dis"):
        if(count==41):
            allUrl = chain(allUrl, getPageUrl(chrome.page_source))
            print(count)
            break
        count+=1
    chrome.quit()
    return allUrl




def get_result(source):
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    data5=[]

    chrome = webdriver.PhantomJS(executable_path="D:\\software\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")

    for i in source:


        # url = "https://www.icourse163.org/course/USTB-299003/"
        # html=requests.get(url).content

        chrome.get(i)
        time.sleep(1)
        html = chrome.page_source

        info = etree.HTML(html)

        title_path = "/html/body/div[4]/div[2]/div[1]/div/div[3]/div/div[1]/div[1]/span[1]"
        time_path = "/html/body/div[4]/div[2]/div[1]/div/div[3]/div/div[2]/div/div[1]/div[2]/div[1]/span[2]"
        course_path = "/html/body/div[4]/div[2]/div[1]/div/div[3]/div/div[2]/div/div[1]/div[3]/span[2]"
        num_path = "/html/body/div[4]/div[2]/div[1]/div/div[3]/div/div[2]/div/div[2]/div[1]/span"
        tea_path="/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div[1]"

        # path1="/html/body/div[4]/div[2]/div[1]/div/div[3]/div/div[2]/div/div[1]/div[@class]/div[@class]/span[2]"
        # path2=

        title = info.xpath(title_path)
        time1 = info.xpath(time_path)
        course = info.xpath(course_path)
        num = info.xpath(num_path)
        tea=info.xpath(tea_path)

        print(title[0].text,time1[0].text,course[0].text,num[0].text,tea[0].text)

        data1.append(title[0].text)
        data2.append(time1[0].text)
        data3.append(course[0].text)
        data4.append(num[0].text)
        data5.append(tea[0].text)


    len=data1.__len__()
    workbook=xlwt.Workbook(encoding='utf-8')
    test=workbook.add_sheet('test')
    for j in range(0,len):
        test.write(j,0,data1[j])
        test.write(j,1,data2[j])
        test.write(j,2,data3[j])
        test.write(j,3,data4[j])
        test.write(j,4,data5[j])

    workbook.save('result.xls')

if __name__=="__main__":
    allUrl = getAllUrl("https://www.icourse163.org/category/guojiajingpin")
    source = list(allUrl)
    for i in source:
        if (i[5] == 'h'):
            source.remove(i)

    get_result(source)
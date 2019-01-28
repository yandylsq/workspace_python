# encoding:utf-8
import re  # 使用正则 匹配想要的数据
import requests  # 使用requests得到网页源码
import csv
import time
from lxml import etree

# 得到主函数传入的链接
def getHtmlText(url):
    try:  # 异常处理
        #伪装头部，虽然不伪装也可以，但是有时会导致服务器未响应，访问多了需要更换ip
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        #  得到你传入的URL链接  设置超时时间3秒
        r = requests.get(url=url, headers=headers, timeout=3)
        # 判断它的http状态码
        r.raise_for_status()
        # 设置它的编码 encoding是设置它的头部编码 apparent_encoding是从返回网页中分析它的编码格式
        r.encoding = r.apparent_encoding
        # 返回源代码
        return r.text
    except: # 发生异常返回空
        return ''

# 解析你的网页信息
def parsePage(ilt, html):
    # 异常处理
    try:
        # 日期
        dates = html.xpath("/html/head/title/text()")
        # 标题
        titles = html.xpath("/html/body/h2/text()")
        # 内容
        contents = html.xpath("/html/body/h2/following-sibling::div[1]/text()")
        
        print(dates[0] + "的数据...")
        newContents = [];
        tmpContent = ""
        isSelected = 0
        newsNum = 0
        selectedIndexs = []
        i = 0
        for i in range(len(contents)-2):
            if contents[i+1].find("专栏") > -1 :
                newsNum = newsNum + 1
            if contents[i].find("第1版") > -1 and contents[i+1].find("专栏") > -1 :
                isSelected = 1
                selectedIndexs.append(newsNum - 1)
            if isSelected == 1:
                tmpContent += contents[i]
            if isSelected == 1 and contents[i+2].find("专栏") > -1:
                newContents.append(tmpContent)
                tmpContent = ""
                isSelected = 0

        # 如果最后一个是第1版，添加最后一个
        if isSelected == 1:
            tmpContent += contents[i]
            tmpContent += contents[i+1]
            tmpContent += contents[i+2]
            newContents.append(tmpContent)   
        
        # 得到这个内容放入主函数中的列表
        for i in range(len(newContents)):
            date = dates[0]
            content = newContents[i]
            title = titles[selectedIndexs[i]]
            ilt.append([date, title, content])
    except :  # 发生异常输出空字符串
        print ('发生异常:' + html.xpath("/html/head/title/text()"))
        

# 定义主函数 main
def main():
    csvfile = open('news.csv', 'w',newline='',encoding='utf-8')  #打开一个new.csv的文件进行数据写入，没有则自动新建
    writer = csv.writer(csvfile)
    writer.writerow(['日期', '标题' , '文章内容']) #写入一行作为表头

    baseUrl = "http://rmrb.zhouenlai.info/人民日报/";
    url = "http://rmrb.zhouenlai.info/%E4%BA%BA%E6%B0%91%E6%97%A5%E6%8A%A5/index.php";
    htmlText = getHtmlText(url);
    yearHtml = etree.HTML(htmlText);
    #年份链接
    yearList = yearHtml.xpath('//*[@id="listing"]/div/a/@href')
    infoList = [] # 自定义的空列表用来存放你的到的数据
    errorList = []
    print("开始获取...")
    for y in yearList:
        try:
            if y.find("../") > -1:
                continue
            year = re.sub("\D", "", y)
            if year < '1980' or year > '2003':
                continue
            yurl = baseUrl + y
            monthHtml = etree.HTML(getHtmlText(yurl));
            if monthHtml is None or monthHtml == '':
                continue
            monthList = monthHtml.xpath('//*[@id="listing"]/div/a/@href')
            for m in monthList:
                try:
                    if m.find("../") > -1:
                        continue
                    month = re.sub("\D", "", m)
#                     if month != '06':
#                         continue
                    murl = baseUrl + year + "/" + m
                    dayHtml = etree.HTML(getHtmlText(murl));
                    if dayHtml is None or dayHtml == '':
                        continue
                    dayList = dayHtml.xpath('//*[@id="listing"]/div/a/@href')
                    for d in dayList:
                        try:
                            if d.find("../") > -1:
                                continue
                            durl = baseUrl + year + "/" + month + "/" + d
                            html = etree.HTML(getHtmlText(durl));
                            if html is None or html == '':
                                continue
                            parsePage(infoList, html) 
                            if len(infoList) >= 5000:
                                writer.writerows(infoList)
                                infoList = []
                                # break
                        except:
                            errorList.append(d)
                            continue
                except:
                    errorList.append(y)
                    continue
        except:
            errorList.append(y)
            continue
    print(errorList)
    if len(infoList) > 0:
        writer.writerows(infoList)
        infoList = []
    time.sleep(3)  # 休眠3秒
    csvfile.close() #循环结束，数据爬取完成，关闭文件
    print("爬取结束！");

main() # 调用主函数

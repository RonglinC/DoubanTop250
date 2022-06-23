# -*- coding = utf-8 -*-
# @Time : 6/16/2022 2:05 PM
# @Author : Ronglin
# @File : douban.py
# @Software : PyCharm

from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import sqlite3



def main():
    url="https://movie.douban.com/top250?start="
    # 爬取网页
    datalist=getdata(url)
    savepath="doubantop250.xls"
    # 保存数据
    saveData(datalist, savepath)

    #askURL(url)

findLink = re.compile(r'<a href="(.*?)">') #compile is to build a rule object ( a string model)
findImag = re.compile(r'<img.*src=.*="(.*?)".*/>',re.S)
# movieName
findTitle = re.compile(r'<span class="title">(.*)</span>')
# movieScore
findRating = re.compile(r'span class="rating_num" property="v:average">(.*)</span>')
# how many people rating
findJudge = re.compile(r'<span>(\d*)people comment</span>')
# quote
findQuote = re.compile(r'<span class="inq">(.*)</span>')
# find information about movie
findBd = re.compile(r'<p class="">(.*)</p>',re.S)

# 爬取网页
def getdata(url):
    datalist=[]
    for i in range(0,10): #获取页面信息函数，10次，一页25条
        aurl = url + str(i*25)
        html = askURL(aurl) #save the html code we get

        #解析数据
        soup = BeautifulSoup(html,"html.parser")
        #look for the string and form the list
        for item in soup.find_all('div',class_="item"):
            #print(item)
            data = [] #the information of one single movie
            item = str(item)

            # re use to search the special string
            link = re.findall(findLink,item)[0] # get the link of the movie
            data.append(link)

            img = re.findall(findImag,item)[0]
            data.append(img)

            title = re.findall(findTitle,item)
            if len(title) == 2:
                ctitle = title[0]
                data.append(ctitle)
                etitle = title[1].replace("/","")
                data.append(etitle)
            else:
                data.append(title[0])
                #leave space
                data.append(' ')
            rating = re.findall(findRating,item)[0]
            data.append(rating)

            judgenum = re.findall(findJudge,item)
            data.append(judgenum)

            inq = re.findall(findQuote,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")

            bd= re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)
            bd = re.sub('/'," ",bd)
            data.append(bd.strip())

            # put one movie's information into datalist
            datalist.append(data)
    #print(datalist)
    return datalist


# 得到指定url网页内容
def askURL(url):
    head = {           # 向豆瓣发送消息，伪装用的
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
               # 用户代理表示告诉豆瓣服务器，我们是什么类型的机器，浏览器（本质告诉浏览器，我们接受什么水平的文件）
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html



def saveData(datalist,savepath):
    print("save")
    workbook = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = workbook.add_sheet('DoubanTop250',cell_overwrite_ok=True)
    col = ("movie link", "movie image", "movie chinese name","movie title","rating","ratingNum","summary", "bd")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,len(datalist)):
        print("Num.%d" % (i+1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i+1, j, data[j])
    workbook.save(savepath)





    


if __name__ == "__main__":
    main()
    print("scrapy successful")

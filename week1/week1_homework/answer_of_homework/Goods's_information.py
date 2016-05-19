#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
def get_message(url):
    #print(url)
    wb_date = requests.get(url)
    id = (url.split('/')[-1])[:14]#截取商品ID得到对应的id，一共15位
    views = get_totols(id)

    soup = BeautifulSoup(wb_date.text,'lxml')

    categories = soup.select('#header > div.breadCrumb.f12 > span:nth-of-type(3) > a') #类目
    titles = soup.select('#content > div.person_add_top.no_ident_top >div.per_ad_left > div.col_sub.mainTitle > h1')#标题
    times = soup.select('#index_show > ul.mtit_con_left.fl > li.time')#发布时间
    prices = soup.select('#content > div.person_add_top.no_ident_top >div.per_ad_left > div.col_sub.sumary > ul >'
                         ' li:nth-of-type(1) > div.su_con > span')#价格
    olds = soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul >'
                       ' li:nth-of-type(2) > div.su_con > span')#成色
    areas1 = soup.select('#content > div.person_add_top.no_ident_top >'
                         ' div.per_ad_left > div.col_sub.sumary > ul >'
                         ' li:nth-of-type(3) > div.su_con > span >'
                         ' a:nth-of-type(1)')#区域1
    areas2 = soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left >'
                         ' div.col_sub.sumary > ul > li:nth-of-type(3) > div.su_con > span > a:nth-of-type(2)')#区域2
    for category,title,time,price,old,area1,area2 in zip(categories,titles,times,prices,olds,areas1,areas2):
        data = {
            '类目':category.get_text(),
            '标题':title.get_text(),
            '发布时间':time.get_text(),
            '价格':price.get_text(),
            '成色':old.get_text().strip(),
            '区域':area1.get_text()+'-'+area2.get_text(),
            '浏览量':views
        }
        print(data)
        return None
#去除列表中重复连接
def delRepeat(list):
    for x in list:
        while list.count(x)>1:
            del list[list.index(x)]
    #print(list)
    return list

#获取有效连接列表
def get_links(url):
    links = []
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    href = soup.select(' tr > td.t > a')
    for link in href:
        if 'http://bj.58.com/pingbandiannao/' in link.get('href'):
            #判断路径里是否有关键字  去除推荐的和转转的连接
            #部分推荐无法有效去除（也手动在标签里筛选过，但似乎没有好的辨识标志）
            links.append(link.get('href'))#将连接加入到列表中去

    links = delRepeat(links)#去重

    for wb_link in links:
        get_message(wb_link)
        time.sleep(1)  # 防止反爬技巧之一

#获取浏览量的方法
def get_totols(id):
    headers ={
            'Referer':'http://bj.58.com/pingbandiannao/25390255065933x.shtml?adtype='
                      '1&PGTID=0d305a36-0000-1576-ef5f-2547f6476ccf&entinfo=25390255065933_0&psid='
                      '132996494191831950071360497&iuType=q_2&ClickID=2',
        #针对58网站就头部referer有判断的应对，人工访问信息，防止反爬技巧之二
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Cookie':'bj58_id58s="c19BMUtfcUdITnA1ODU4Mw=="; id58=c5/njVc56DRPBRJ9BO59Ag==; als=0; __utma='
                 '253535702.423222974.1463666994.1463666994.1463666994.1; __utmz=253535702.1463666994.1.1.utmcsr='
                 '(direct)|utmccn=(direct)|utmcmd=(none); 58home=wuhai; myfeet_tooltip=end; bangbigtip2=1; ipcity='
                 'wuhai%7C%u4E4C%u6D77; 58tj_uuid=0c52f1f5-7b9b-4dd7-81af-d2bb5426d2a9; new_session=0; new_uv=3; '
                 'utm_source=; spm=; init_refer=http%253A%252F%252Fbj.58.com%252Fpbdn%252F0%252F; final_history='
                 '26070179017526%2C25390255065933%2C24063857671738%2C26057897956784%2C25896821493035; sessionid='
                 '7d224bdd-5534-4102-acbc-9a43514cf79e; bj58_new_session=0; bj58_init_refer="http://bj.58.com/pbdn/0/"; '
                 'bj58_new_uv=38'
    }
    api = 'http://jst1.58.com/counter?infoid={}&userid=&uname=&sid=516903216&lid=1&px=&cfpath=5,38484'.format(id)
    #这里使用了api接口
    js = requests.get(api,headers=headers)
    views = js.text.split('=')[-1]
    #print(views)
    return views
full_url = ['http://bj.58.com/pbdn/{}/'.format(str(i)) for
            i in range(0, 10, 1)]#抓取前10页
for link in full_url:
    get_links(link)
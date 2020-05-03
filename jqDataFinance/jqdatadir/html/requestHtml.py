#!/usr/bin/env python
# -*- coding:utf-8 -*-
import io
import asyncio
import aiohttp

from requests_html import HTMLSession, HTML
import time
from selenium import webdriver

# python爬取网页报错提示状态码404，可是在浏览器里可以打开网页
# 使用 谷歌浏览器 ->Network -> 点击放大镜搜索,找到相应的URL  右键->copy request head  ,"Cookie":
cookieOldTwo = "Hm_lvt_f66b37722f586a240d4621318a5a6ebe=1558099402; __utma=74597006.1812144867.1558145024.1558145024.1558145024.1; __utmz=74597006.1558145024.1.1.utmcsr=i.meituan.com|utmccn=AffProg|utmcmd=wandie|utmctr=61452.cps.22156087|utmcct=i.meituan.com/?source=wandie&urpid=61452.155814502486.22156087.0&_rdt=1&utm_campaign=AffProg&utm_medium=wandie&utm_source=www.meituan.com&utm_content=www.meituan.com%2Fmeishi%2F170619598&utm_term=61452.cps.22156087&noguide=1; uuid=63a7fe5faa5346e28008.1558105457.1.0.0; PHPSESSID=lfgdfpb7j191ig61q1otlj9uk6; Hm_lpvt_f66b37722f586a240d4621318a5a6ebe=1558099463; __utmc=74597006; pgv_pvi=6563513344; pgv_si=s5767523328; us=wandie; ut=61452.155814502553.22156087.0; IJSESSIONID=a5mc7xlh9gnd1nkwt404h8mer; iuuid=DE5C68C5917C04BF1AF9C6FCE62F9342BC64F7094A8DB5D01451ECDF251C99B6; latlng=23.120954,113.38942,1558145024563; ci=277; cityname=%E5%B9%BF%E5%B7%9E; _lx_utm=utm_campaign%3DAffProg%26utm_medium%3Dwandie%26utm_source%3Di.meituan.com%26utm_content%3Di.meituan.com%252F%253Fsource%253Dwandie%2526urpid%253D61452.155814502486.22156087.0%2526_rdt%253D1%2526utm_campaign%253DAffProg%2526utm_medium%253Dwandie%2526utm_source%253Dwww.meituan.com%2526utm_content%253Dwww.meituan.com%25252Fmeishi%25252F170619598%2526utm_term%253D61452.cps.22156087%2526noguide%253D1%26utm_term%3D61452.cps.22156087; _lxsdk_cuid=16ac8ae3e7c99-09ebbb3d32a9748-11656d4a-1fa400-16ac8ae3e7ec8; _lxsdk=DE5C68C5917C04BF1AF9C6FCE62F9342BC64F7094A8DB5D01451ECDF251C99B6; i_extend=H__a100001__b1; noguide=1; webp=1; ci3=1; rvct=277; client-id=21715f70-8319-42a9-9c0a-61e0057b0556; lat=22.5923; lng=113.09767; _hc.v=f79c991a-30d1-b77a-b2e0-f9032918f971.1558145649; _lxsdk_s=16ac9a0ce99-76b-448-444%7C%7C2"
headerTwo = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3505.400"
    , "Proxy-Connection": "keep-alive"
    , "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    , "Upgrade-Insecure-Requests": "1", "Cookie": cookieOldTwo}


async def request(url):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    async with aiohttp.ClientSession() as session:
        # async with session.get(url, headers={
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}) as response:
        # return await response.text()
        async with session.get(url, headers=headerTwo) as response:
            # print(response.request_info)
            return await response.text()


def requestDoc(doc):
    html = HTML(html=doc)
    print(html.links)


def toRequestHtml(url):
    print(url)
    session = HTMLSession()
    # r = session.get(url)
    r = session.request("GET", url, headers=headerTwo)
    # r.html.render()
    print(r.html.html)

    # 获取页面上的所有链接。
    # all_links =  r.html.links
    # print(all_links)
    about = r.html.find('div.list-item-desc-top')
    # about = r.html.find('a',containing='www.meituan')
    for i, title in enumerate(about):
        aElement = title.html.find('a')
        nextUrl = f'https:{aElement.attrs["href"]}'
        nextHtml = session.get(nextUrl)
        print(f'{i + 1} [{aElement.text}](https:{aElement.attrs["href"]})')
        nextAbout = nextHtml.html.find('div.d-left')
        for j, nextTitle in enumerate(nextAbout):
            print(f'{j + 1} [{nextTitle.text}]')
    # print(about)
    # print(about.absolute_links)  # 获得新闻链接
    # print("============================================= ",about.text)

    # 获取页面上的所有链接，以绝对路径的方式。
    # all_absolute_links = r.html.absolute_links
    # print(all_absolute_links)


def requestBySelenium(url):
    browser = webdriver.Firefox(executable_path="D:\\\\ProgramData\\Anaconda3\\venv\\Lib\\geckodriver.exe")
    browser.get(url)
    # print(browser.page_source)
    requestDoc(browser.page_source)
    # toRequestHtml(url)


def testCodeOne():
    session = HTMLSession()
    r = session.get('https://www.jianshu.com/u/7753478e1554')
    # r.html.render(scrolldown=50, sleep=.2)
    # r.html.render(sleep=.2)
    titles = r.html.find('a.title')
    for i, title in enumerate(titles):
        print(f'{i + 1} [{title.text}](https://www.jianshu.com{title.attrs["href"]})')


def testCodeTwo():
    session = HTMLSession()
    # 爬取天涯论坛帖子
    url = 'http://bbs.tianya.cn/post-culture-488321-1.shtml'
    r = session.get(url)
    # 楼主名字
    author = r.html.find('div.atl-info span a', first=True).text
    # 总页数
    div = r.html.find('div.atl-pages', first=True)
    links = div.find('a')
    total_page = 1 if links == [] else int(links[-2].text)
    # 标题
    title = r.html.find('span.s_title span', first=True).text

    with io.open(f'{title}.txt', 'x', encoding='utf-8') as f:
        for i in range(1, total_page + 1):
            s = url.rfind('-')
            r = session.get(url[:s + 1] + str(i) + '.shtml')
            # 从剩下的里面找楼主的帖子
            items = r.html.find(f'div.atl-item[_host={author}]')
            for item in items:
                content: str = item.find('div.bbs-content', first=True).text
                # 去掉回复
                if not content.startswith('@'):
                    f.write(content + "\n")


# url = "https://s.1688.com/company/company_search.htm?spm=a261p.8650809.0.0.77a26328qfdrQ3&keywords=%B6%AB%DD%B8&button_click=top&earseDirect=false&n=y&netType=1%2C11&_source=sug"
url = "https://jm.meituan.com/s/%E7%BE%8E%E9%A3%9F/"


# requestBySelenium(url)
# toRequestHtml(url)
# testCodeOne()
# testCodeTwo()

# https://github.com/kennethreitz/requests-html/issues/229
async def main(urlPamar):
    res = await request(urlPamar)
    res = HTML(html=res)
    about = res.find('div.list-item-desc-top a')
    for i, title in enumerate(about):
        nextUrl = f'https:{title.attrs["href"]}'
        nextHtml = await request(nextUrl)
        print(f'{i + 1} [{title.text}](https:{title.attrs["href"]})')
        try:
            startIndex = nextHtml.index(f'"address":')
            endIndex = nextHtml.index(f',"extraInfos"')
            print(nextHtml[startIndex:endIndex])
        except ValueError:
            if nextHtml.__contains__("验证中心"):
                print("需要验证")
            else:
                print(nextHtml)
        finally:
            pass


asyncio.get_event_loop().run_until_complete(main(url))

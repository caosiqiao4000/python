#!/usr/bin/env python
# -*- coding:utf-8 -*-
import io
import asyncio
import aiohttp
import json, re
from jqdata.html.requestHtml import  main

import requests

# python爬取网页报错提示状态码404，可是在浏览器里可以打开网页
# 使用 谷歌浏览器 ->Network -> 点击放大镜搜索,找到相应的URL  右键->copy request head
cookieOldTwo = "Hm_lvt_f66b37722f586a240d4621318a5a6ebe=1558099402; __utma=74597006.1812144867.1558145024.1558145024.1558145024.1; __utmz=74597006.1558145024.1.1.utmcsr=i.meituan.com|utmccn=AffProg|utmcmd=wandie|utmctr=61452.cps.22156087|utmcct=i.meituan.com/?source=wandie&urpid=61452.155814502486.22156087.0&_rdt=1&utm_campaign=AffProg&utm_medium=wandie&utm_source=www.meituan.com&utm_content=www.meituan.com%2Fmeishi%2F170619598&utm_term=61452.cps.22156087&noguide=1; uuid=63a7fe5faa5346e28008.1558105457.1.0.0; PHPSESSID=lfgdfpb7j191ig61q1otlj9uk6; Hm_lpvt_f66b37722f586a240d4621318a5a6ebe=1558099463; __utmc=74597006; pgv_pvi=6563513344; pgv_si=s5767523328; us=wandie; ut=61452.155814502553.22156087.0; IJSESSIONID=a5mc7xlh9gnd1nkwt404h8mer; iuuid=DE5C68C5917C04BF1AF9C6FCE62F9342BC64F7094A8DB5D01451ECDF251C99B6; latlng=23.120954,113.38942,1558145024563; ci=277; cityname=%E5%B9%BF%E5%B7%9E; _lx_utm=utm_campaign%3DAffProg%26utm_medium%3Dwandie%26utm_source%3Di.meituan.com%26utm_content%3Di.meituan.com%252F%253Fsource%253Dwandie%2526urpid%253D61452.155814502486.22156087.0%2526_rdt%253D1%2526utm_campaign%253DAffProg%2526utm_medium%253Dwandie%2526utm_source%253Dwww.meituan.com%2526utm_content%253Dwww.meituan.com%25252Fmeishi%25252F170619598%2526utm_term%253D61452.cps.22156087%2526noguide%253D1%26utm_term%3D61452.cps.22156087; _lxsdk_cuid=16ac8ae3e7c99-09ebbb3d32a9748-11656d4a-1fa400-16ac8ae3e7ec8; _lxsdk=DE5C68C5917C04BF1AF9C6FCE62F9342BC64F7094A8DB5D01451ECDF251C99B6; i_extend=H__a100001__b1; noguide=1; webp=1; ci3=1; rvct=277; client-id=21715f70-8319-42a9-9c0a-61e0057b0556; lat=22.5923; lng=113.09767; _hc.v=f79c991a-30d1-b77a-b2e0-f9032918f971.1558145649; _lxsdk_s=16ac9a0ce99-76b-448-444%7C%7C2"
headerTwo = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3505.400"
    , "Proxy-Connection": "keep-alive"
    , "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    , "Upgrade-Insecure-Requests": "1", "Cookie": cookieOldTwo}


async def fetch_async(url, actionCdoe):
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headerTwo) as r:  # 异步上下文管理器
            # async with aiohttp.request("GET", url, headers=headers) as r:
            reponse = await r.text(encoding="utf-8")  # 或者直接await r.read()不编码，直接读取，适合于图像等无法编码文件
            print(len(reponse))
            if actionCdoe == 1:
                handle_json(reponse)

def handle_json(jsonData):
    patt = r'(id((?!id).)+?),"showType"'  # 匹配id后与showType之前的字符
    pattern = re.compile(patt)
    result = pattern.findall(jsonData)
    print(result.__len__())
    for index, oneDate in enumerate(result):
        # print(index, type(oneDate[0]), oneDate[0])
        jsonA = "{\"" + oneDate[0] + "}"
        dict = json.loads(jsonA)
        print(dict.get("id"), dict.get("title"), dict.get("latitude"))
        print(index, type(oneDate), dict.get("title"))
        main("https://www.meituan.com/meishi/"+str(dict.get("id")))


async def func1(url, params, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as r:  # 异步上下文管理器
            with open(filename, "wb") as fp:  # 普通上下文管理器
                while True:
                    chunk = await r.content.read(10)
                    if not chunk:
                        break
                    fp.write(chunk)


tasks = [fetch_async(
    'http://apimobile.meituan.com/group/v4/poi/pcsearch/277?uuid=608d4b484c434be9be71.1558098781.1.0.0&userid=-1&limit=32&offset=128&cateId=-1&q=%E6%B1%9F%E9%97%A8%E5%B8%82%E8%93%AC%E6%B1%9F%E5%8C%BA%E7%BE%8E%E9%A3%9F',
    1)]

event_loop = asyncio.get_event_loop()
results = event_loop.run_until_complete(asyncio.gather(*tasks))
event_loop.close()

# 爬取链家网内容尝试
# https://www.youtube.com/watch?v=SGHSuRv0MKE

import requests
import parsel
import csv

for pg in range(1, 92):  # 控制页数
    print(f'\n-------- {pg} --------') #f 是占位符
    # 1.找到数据所对应的链接地址
    url = f'https://sjz.lianjia.com/ershoufang/kaifaqu1/pg{pg}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

    # 2.发送指定链接地址的请求（代码） request
    response = requests.get(url=url, headers=headers)
    # print(response) 返回获取网页的对象内容
    html_data = response.text  # str 字符串类型 目前只能正则 可以转换 xpath或css选择器
    # print(html_data) 此时返回的是text文本形式
    # 3.解析出我们需要的数据 parsel
    # 3.1转化数据类型
    selector = parsel.Selector(html_data)
    # print(selector)

    # 数据提取 之后 可能涉及数据的二次提取
    lis = selector.css('.clear.LOGCLICKDATA')  # 涉及css选择器的内容

    for li in lis:
        # 单个标签
        title = li.css('.title a::text').get()  # 房子标题
        # 多个标签同时存在
        address = li.css('.positionInfo a::text').getall()  # 房子地址
        address = '- '.join(address)
        # 没有标签
        introduce = li.css('.houseInfo::text').get()  # 介绍
        # 如何划分更细的内容
        starinfo = li.css('.followInfo::text').get().split('/')  # 关注人数
        star = starinfo[0]
        startime = starinfo[1]

        tags = li.css('.tag span::text').getall()  # 房子相关信息
        tags = ' | '.join(tags)

        totalPrice = li.css('.totalPrice.totalPrice2 span::text').get() + '万元'  # 总价

        unitPrice = li.css('.unitPrice span::text').get()  # 单价

        # 往文件里追加数据
        # 4.数据的保存
        with open('二手房Pages.csv', 'a', encoding='utf_8_sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([title, address, introduce, star, startime, tags, totalPrice, unitPrice])
        # print(unitPrice)

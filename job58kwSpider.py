from urllib import request
import random
from urllib.parse import quote
from lxml import etree
import redis
import json


class KwSpider:
    """关键字爬虫类
    用户关键字爬取豆瓣图书信息
    Attributes:
        kw 用户关键字
    """
    def __init__(self, kw):
        # destination url
        self.url = "https://sz.58.com/job/"   # 深圳地区
        # keyword
        self.kw = kw
        # User-Agent list
        self.ua_list = [
            # "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C;"
            # " .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
            # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
            "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        ]
        self.proxy_list = [
            {"http": "111.177.186.143:9999"},
            {"http": "114.106.151.118:9999"},
            {"http": "111.177.168.207:9999"},
            {"http": "121.232.148.27:9000"},
        ]
        self.jobs = []

    def get_response(self, url, page=1, data_type="str", coding="utf-8"):
        """sending request and return response data
            :parameter:
                url: destination url contains keyword
                data_type: return data type variable value is "str","binary" and the default value is str
                coding:the encoding of the sit
                page: 页数
            :return  return str if data_type is str else return binary data

        """
        # 中文需要url编码
        url = url + "pn" + str(page) + "/?final=1&jump=1&key=" + quote(self.kw)
        print(url)
        req = request.Request(url)
        # random proxy
        proxy = random.choice(self.proxy_list)
        print("代理:" + str(proxy))
        httpproxy_handler = request.ProxyHandler(proxy)
        # create opener
        opener = request.build_opener(httpproxy_handler)
        # add User-Agent
        req.add_header("User-Agent", random.choice(self.ua_list))
        # send Request
        response = opener.open(req)
        if response.getcode() != 200:
            print("请求失败: %d " % response.getcode())
            return ""
        # response data
        html = response.read()
        if data_type == "binary":
            return html
        else:
            return html.decode(coding)

    def get_total_page(self, html):
        """返回总页数
            :param html html字符串
            :return 总页数
        """
        html = etree.HTML(html)
        total_page = html.xpath("//span[@class='num_operate']/i[@class='total_page']/text()")[0]
        return int(total_page)

    def parse_jobs(self, html):
        """解析岗位信息"""
        if html:
            html = etree.HTML(html)
            # 职位名称
            job_name = html.xpath(
                "//div[@class='leftCon']/ul/li/div[@class='item_con job_title']"
                "/div[contains(@class,'job_name')]/a/span[@class='name']/text()")

            page_list_len = list(job_name).__len__()
            # print("列表长度%d" % page_list_len)
            for i in range(1, page_list_len+1):    # 其实没必要这样获取 就这样了吧 没太多考虑
                item = {}
                # 工资
                salary_parser = "//div[@class='leftCon']/ul/li[%d]/div[@class='item_con job_title']" \
                                "/p[@class='job_salary']/text()" % i
                # 很坑 有些是培训机构
                salary = html.xpath(salary_parser)  # 没有这项的就是培训机构
                if not salary:
                    continue

                # 福利 每个岗位都有多个福利
                job_wel_parser = "//div[@class='leftCon']/ul/li[%d]/div[@class='item_con job_title']" \
                                 "/div[contains(@class,'job_wel')]/span/text()" % i
                job_wel = html.xpath(job_wel_parser)

                # 公司名称
                company_parser = "//div[@class='leftCon']/ul/li[%d]/div[@class='item_con job_comp']" \
                                 "/div[@class='comp_name']/a/@title" % i
                company = html.xpath(company_parser)[0]

                # 学历要求
                education_parser = "//div[@class='leftCon']/ul/li[%d]/div[@class='item_con job_comp']" \
                                   "/p[@class='job_require']/span[2]/text()" % i
                education = html.xpath(education_parser)[0]
                item['job_name'] = job_name[i-1]
                item['salary'] = salary
                item['company'] = company
                item['education'] = education
                item['job_wel'] = job_wel
                print(i, item)
                self.jobs.append(item)

    def run(self):
        """start work  可以使用进程或者线程提高效率 我懒得弄了 """
        # 请求第一页
        html = self.get_response(url=spider.url, data_type="str")
        self.parse_jobs(html)
        # 获取总页数
        total_page = self.get_total_page(html=html)
        print("总页数%d" % total_page)
        if total_page >= 2:
            for pn in range(2, total_page+1):
                html = self.get_response(url=self.url, page=pn, data_type='str')

                # # 保存本地测试
                # f = open("58java2.html", "a+")
                # f.write(html)
                # break
                self.parse_jobs(html)
        jobs = self.get_jobs()
        if len(jobs) > 0:
            self.store_redis()

    def get_jobs(self):
        return self.jobs

    def store_redis(self):
        """数据保存到redis 服务器没安装mongodb 先用这redis吧"""
        try:
            redis_client = redis.Redis(host='119.29.204.27', port=9502)
            flag = redis_client.set(self.kw, json.dumps(self.jobs))
            if flag:
                print("保存数据到redis成功")
        except ConnectionRefusedError:
            print("服务拒绝连接")
            exit(0)


if __name__ == '__main__':
    keyword = input("please enter the keyword：")
    # Determine if the keyword is empty
    if keyword.strip(' ') == '':
        print("please enter a key")
        exit(0)

    print("spider is running....please wait")
    spider = KwSpider(kw=keyword.strip(" "))
    spider.run()
    print("spider is finished")








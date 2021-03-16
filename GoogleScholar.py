import urllib.request as request    # 用于请求数据
import requests    # 用于请求数据
from urllib import parse    # 用于encodeURIComponent编码与解码
import random    # 用于随机生成ua
import os    # 用于文件路径相关的操作
import gzip    # 用于解压谷歌学术返回的数据
import io   # 用于字符流操作
from lxml import etree    # 用于xpath解析
import re    # 用于处理正则表达式
import time    # 用来延时，有效防止被封
import urllib.error    # 用来处理url请求错误
import pandas as pd    # 用于将字典列表转换为DataFrame并将其导出到Excel文件
import http.cookiejar as cookielib    # 用于处理cookie
from retrying import retry    # 用于url打开错误重试
import gc    # 用于垃圾回收

# 读取所有agents
def read_agents(filename):
    agents=[]
    agents_file=open(filename,'r',encoding='utf-8')
    for r in agents_file.readlines():
        data="".join(r.split('\n'))
        agents.append(data)
    agents_file.close()
    del agents_file
    del data
    gc.collect()
    return agents

# 读取所有域名
def read_domains(filename):
    domains = []
    domains_file = open(filename,'r',encoding='utf-8')
    for r in domains_file.readlines():
        data="".join(r.split('\n'))
        domains.append(data)
    domains_file.close()
    del domains_file
    del data
    gc.collect()
    return domains

# 读取所有代理ip
def read_ips(filename):
    ips = []
    ips_file = open(filename, 'r', encoding='utf-8')
    for r in ips_file.readlines():
        data="".join(r.split('\n'))
        ips.append(data)
    ips_file.close()
    del ips_file
    del data
    gc.collect()
    return ips

# 自定义代理
def select_proxy(proxy_type='socks-client'):
    proxies = {}
    if proxy_type == 'http':
        # 代理设置：http(s)代理
        proxies = {
            'https': 'https://127.0.0.1:2173',
            'http': 'http://127.0.0.1:2173'
        }
    elif proxy_type == 'socks-remote':
        # 代理设置：socks5代理（远程服务器）
        proxies = {
            'socks5': 'socks5://user:pass@host:port',
            'socks5': 'socks5://user:pass@host:port'
        }
    elif proxy_type == 'socks-client':
        # 代理设置：socks5代理（客户端在本机）
        proxies = {
            'http': 'socks5://127.0.0.1:2080',
            'https': 'socks5://127.0.0.1:2080'
        }
    elif proxy_type == 'no':
        # 代理设置：不使用代理
        proxies = {}
    else:
        pass
    return proxies

# 指定url，获取网页内容
@retry(stop_max_attempt_number=5, wait_random_min=10, wait_random_max=20)    # 请求失败自动重试
def get_data(url, headers, proxies):
    # 使用urllib
    # print('--------------正在使用urllib获取数据--------------')
    print('获取网页数据...')
    cookie = cookielib.CookieJar()    # 写到最后才发现好多网站需要cookie，索性就在这儿设置了
    request.build_opener()
    opener = request.build_opener(request.ProxyHandler(proxies), urllib.request.HTTPCookieProcessor(cookie))    # 设置代理和cookie处理器
    request.install_opener(opener)    # 安装代理
    req = request.Request(url, headers=headers)    # 设置请求
    # response = request.urlopen(req)    # 打开url
    # 准备使用try，有点小毛病，待改进
    try:
        response = request.urlopen(req)    # 打开url
        print("Connection Succeeded!")
        # print(response.read().decode())    # 输出响应内容，由于返回的是压缩文件，这种方式已经不行了
        # 根据不同的编码格式处理数据
        if response.info().get('Content-Encoding') == 'gzip':
            data = gzip.decompress(response.read()).decode("utf-8")    # 如果是压缩格式则解压
        else:
            data = response.read()
        # print(data)    # 输出处理后的数据
        del cookie
        del opener
        response.close()
        del response
        gc.collect()
        return data
    except urllib.error.URLError as e:
        print('GoogleScholar.get_data()：' + str(e.reason))
    return

# 解析得到的数据
def parse_data(html, page_count, detailFlag):
    article_list = []
    # agents = read_agents(r'D:/Learning Materials/Python/GoogleScholarGUI/agents.txt')
    agents = read_agents(r'./config/agents.txt')
    agent = random.choice(agents)
    # 请求头设置
    headers = {
        'user-agent': agent
    }
    # proxies = select_proxy('socks-client')    # 获取代理地址
    proxies = select_proxy('no')
    # 循环提取每一篇文章的内容
    for i in range(0, 10):
        print('----------第{}篇文章----------'.format(i))
        section_xpath = '//div[@data-rp="' + str(page_count*10 + i) + '"]'
        # section_xpath = '//div[@data-rp="1"]'
        # print(section_xpath)
        section = html.xpath(section_xpath)    # 获取到一篇文章的区域
        # print(section[0])    # 输出获取到的区域
        # print(etree.tostring(section[0]))    # 输出获取到的区域的完整内容
    
        # 需要解析以下数据
        # Title、Journal、Authors、Year、Citation、Empirical
        # Abstract    先爬一部分，后面再根据链接爬
        # PDF Link    目前先爬pdf链接，以后再写下载pdf
        title_area = section[0].xpath(section_xpath + '//h3')    # 取得标题所在的元素
        # print(title_area)
        title = title_area[0].xpath('string(.)').strip()    # 取出title
        # print(etree.tostring(title_area[0]))
        print('Title: ' + title)    # 输出标题    

        # 获取论文链接
        paper_link = section[0].xpath(section_xpath + '//h3//a/@href')    # 取得论文的链接
        print('PaperLink: ' + paper_link[0])

        # 提取作者，期刊，年份，网站，事实上作者，期刊是不完整的，需要进一步爬取
        authors_area = section[0].xpath(section_xpath + '//div[@class="gs_a"]')    # 选取作者和期刊所在区域
        authors_journal_year_site = authors_area[0].xpath('string(.)').strip()    # 取出authors_journal_year_site区域的内容
        # print('authors_journal_year_site: ' + authors_journal_year_site)    # 输出authors_journal_year_site区域的内容
        authors_journal_year_site_list = authors_journal_year_site.split('-', 2)    # 对authors_journal_year_site区域的内容切分
        # print('authors_journal_year_site_list: ' + str(authors_journal_year_site_list))    # 输出切分后的结果
        try:
            journal = "".join(authors_journal_year_site_list[1].split('\xa0')[0]).lstrip()    # 从切分后的结果中提取journal
        except Exception:
            journal = ''
        print('Journal: ' + journal)    # 输出journal
        try:
            authors = "".join(authors_journal_year_site_list[0].split('\xa0')[0])    # 从切分的结果中提取authors
        except Exception:
            authors = ''
        print('Authors: ' + authors)    # 输出authors
        try:
            site = "".join(authors_journal_year_site_list[2].split())    # 从切分的结果中提取论文发布网站
        except Exception:
            site = '0'
        print('Site: ' + site)    # 输出论文发布网站
        try:
            year = re.findall(r'\b\d{4}\b', authors_journal_year_site)[0]    # 提取论文发表年份
        except Exception:
            year = '0'
        print('Year: ' + year)    # 输出论文发表年   
    
        # 提取引用次数
        try:
           citation_area = section[0].xpath(section_xpath + '//div[@class="gs_fl"]/a[3]')    # 选取引用次数所在区域
           # print(etree.tostring(citation_area[0]))
           citation = citation_area[0].xpath('string(.)').strip().split('：', 1)[1]    # 提取引用次数所在区域的文本
        except Exception:
            citation = '0'
        print('Citation: ' + citation)
    
        # 提取论文摘要，这个摘要不完整，待补全
        abstract_area = section[0].xpath(section_xpath + '//div[@class="gs_rs"]')    # 取出abstract所在的区域
        abstract = abstract_area[0].xpath('string(.)').strip()    # 取出abstract
        print('Abstract: \n' + abstract)
    
        # 提取pdf链接
        pdf_link_area = section[0].xpath(section_xpath + '//div[contains(@class, "gs_ggsd")]')    #取出pdf链接所在区域
        pdf_link = [""]
        if len(pdf_link_area) != 0:
            pdf_link = pdf_link_area[0].xpath(section_xpath + '//div[contains(@class, "gs_or_ggsm")]/a/@href')    # 取得pdf链接
            # print(etree.tostring(pdf_link[0]))
        print('PDF link: ' + pdf_link[0])

        # 根据论文的链接提取上面不完整的信息
        # 由于论文可能来源于不同的网站，下面的处理有点繁琐~
        # 需要提取的内容：作者、期刊、摘要
        if detailFlag:
            if "sciencedirect" in paper_link[0]:
                # 论文是ScienceDirect家的
                # 还是加个头吧，伪装的像一点，这个网站经常访问
                new_headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding':' gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'DNT': '1',
                    'Host': 'nav.sciencedirect.com',
                    'Sec-Fetch-Dest': 'iframe',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-site',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
                }
                try:
                    paper_data = get_data("".join(paper_link), headers, proxies)
                    paper_html = etree.HTML(paper_data)
                    journal_area = paper_html.xpath('//a[@class="publication-title-link"]')    # 获取期刊所在区域
                    journal = journal_area[0].xpath('string(.)').strip()    # 获取期刊
                    print('Journal: ' + journal)
                    author_group = paper_html.xpath('//a[contains(@class, "author")]')    # 获取作者所在区域
                    authors_list = []
                    for i in range(len(author_group)):
                        authors_list.append(author_group[0].xpath('string(.)').strip())    # 获取作者
                    # print('Authors: ' + str(authors_list))
                    authors =  ";".join(str(author) for author in authors_list)
                    # print(authors)
                    pattern="[A-Z]"
                    authors = re.sub(pattern, lambda x:" " + x.group(0), authors)
                    print('Authors: ' + authors)
                    abstract_area = paper_html.xpath('//div[contains(@class, "abstract")]')    # 获取摘要所在区域
                    abstract = abstract_area[0].xpath('string(.)').strip()    # 从摘要所在区域获得摘要
                    abstract = abstract[8:]
                    print('Abstract: ' + abstract)
                except Exception:
                    print(paper_link)
            elif "sagepub" in paper_link[0]:
                # 论文是SAGE journal家的
                # 动态网页，太难爬了，先放着
                print('请手动填写详细内容: ' + "".join(paper_link))
            elif "wiley" in paper_link[0]:
                # # 论文是wiley家的
                try:
                    paper_data = get_data("".join(paper_link), headers, proxies)
                    paper_html = etree.HTML(paper_data)
                    author_group = paper_html.xpath('//div[@class="accordion-tabbed"]//span')    # 获取作者所在区域
                    authors_list = []
                    for i in range(len(author_group)):
                        authors_list.append(author_group[0].xpath('string(.)').strip())    # 获取作者
                    # print('Authors: ' + str(authors_list))
                    authors =  ";".join(str(author) for author in authors_list)
                    # print(authors)
                    pattern="[A-Z]"
                    authors = re.sub(pattern, lambda x:" " + x.group(0), authors)
                    print('Authors: ' + authors)
                    abstract_area = paper_html.xpath('//div[contains(@class, "article-section__content")]')    # 获取摘要所在区域
                    abstract = abstract_area[0].xpath('string(.)').strip()    # 从摘要所在区域获得摘要
                    print('Abstract: ' + abstract)
                except Exception:
                    print(paper_link)
            elif "google" in paper_link[0]:
                # 论文是谷歌家的，狗贼谷歌，这个是pdf，真爬不下来了
                print('狗贼谷歌！')
            elif "springer" in paper_link[0]:
                # 论文是springer家的
                # 他家使用代理容易连接失败，重新生成一个代理
                try:
                    new_proxy = select_proxy('no')
                    paper_data = get_data("".join(paper_link), headers, new_proxy)
                    paper_html = etree.HTML(paper_data)
                    author_group = paper_html.xpath('//li[@class="c-author-list__item"]')    # 获取作者所在区域
                    authors_list = []
                    for i in range(len(author_group)):
                        authors_list.append(author_group[i].xpath('string(.)').strip()[:-1])    # 获取作者
                    # print('Authors: ' + str(authors_list))
                    authors =  ";".join(str(author) for author in authors_list)
                    # print(authors)
                    pattern="[A-Z]"
                    authors = re.sub(pattern, lambda x:" " + x.group(0), authors)
                    print('Authors: ' + authors)
                    abstract_area = paper_html.xpath('//div[@class="c-article-section__content"]')    # 获取摘要所在区域
                    abstract = abstract_area[0].xpath('string(.)').strip()    # 从摘要所在区域获得摘要
                    print('Abstract: ' + abstract)
                except Exception:
                    print(paper_link)
            elif "emerald" in paper_link[0]:
                # 论文是emerald家的, 果然不出所料，依然需要cookie
                try:
                    paper_data = get_data("".join(paper_link), headers, proxies)
                    paper_html = etree.HTML(paper_data) 
                    author_group = paper_html.xpath('//a[@class="contrib-search"]')    # 获取作者所在区域
                    authors_list = []
                    for i in range(len(author_group)):
                        authors_list.append(author_group[i].xpath('string(.)').strip()[:-1])    # 获取作者
                    # print('Authors: ' + str(authors_list))
                    authors =  ";".join(str(author) for author in authors_list)
                    # print(authors)
                    pattern="[A-Z]"
                    authors = re.sub(pattern, lambda x:" " + x.group(0), authors)
                    print('Authors: ' + authors)
                    abstract_area = paper_html.xpath('//section[@id="abstract"]')    # 获取摘要所在区域
                    abstract = abstract_area[0].xpath('string(.)').strip()    # 从摘要所在区域获得摘要
                    abstract = abstract[9:]
                    abstract = abstract.replace("\n", "").replace("\r", "").replace("  ", "")
                    print('Abstract: ' + abstract)
                except Exception:
                    print(paper_link)
            else:
                # 让我看看还有哪个狗贼不让我爬
                print(paper_link)

        # 构造字典，加入文章列表
        article_dict = {'Title': title, 'Journal': journal, 'Authors': authors, 'Year': year, 'Citation': citation, 'Abstract': abstract, "PDF Link": pdf_link[0]}
        # print('ArticleDict: ' + str(article_dict))
        article_list.append(article_dict)

        delay_time = random.randint(25,35)    # 延时随机数
        print('开始延时 {}s，程序没有崩，请耐心等待...'.format(delay_time))
        time.sleep(delay_time)    # 随机延时一段时间，对付狗贼谷歌
        print('为您延时 ' + str(delay_time) + 's 成功！')    # 随机延迟，防止反爬识别
        print('-------------------------------------------------------------------------------')
    del agents,agent,headers,proxies,section_xpath,section,title_area,title,paper_link,authors_area,authors_journal_year_site,authors_journal_year_site_list,journal,authors,site,year,citation_area,citation,abstract_area,abstract,pdf_link_area,pdf_link,article_dict
    gc.collect()
    return article_list

# 保存数据到Excel
def sava_to_excel(article_list, file_path):
    #将字典列表转换为DataFrame
    dataframe = pd.DataFrame(list(article_list))
    #指定字段顺序
    order = ['Title', 'Journal', 'Authors', 'Year', 'Citation', 'Abstract', "PDF Link"]
    dataframe = dataframe[order]
    #将列名替换为相应列名
    columns_map = {
       'Title': 'Title', 
       'Journal': 'Journal', 
       'Authors': 'Authors', 
       'Year': 'Year', 
       'Citation': 'Citation', 
       'Abstract': 'Abstract', 
       "PDF Link": 'PDF Link'
    }
    dataframe.rename(columns = columns_map,inplace = True)
    #指定生成的Excel表格名称
    # file_path = pd.ExcelWriter('GoogleScholar.xlsx')
    #替换空单元格
    dataframe.fillna(' ',inplace = True)
    write_file = pd.ExcelWriter(file_path)
    if os.path.isfile(write_file):
        # 读取原始内容，追加新内容
        origin_data = pd.read_excel(write_file, engine='openpyxl')
        dataframe = origin_data.append(dataframe, ignore_index=True, sort=False)
    #输出
    dataframe.to_excel(write_file,encoding = 'utf-8',index = False)
    #保存表格
    write_file.save()
    del dataframe
    del order
    del columns_map
    gc.collect()
    return

# 计算大约需要多长时间
def cal_time(pages):
    sum = 0
    for i in range(pages):
        for j in range(10):
            sum += random.randint(20, 30)
            sum += 10
    return sum/60


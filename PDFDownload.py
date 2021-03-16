import urllib.request    # 用于网络连接，即PDF下载
import os    # 用于文件操作，例如删除、重命名
import pandas as pd    # 用于Excel读取及Dataframe转换
from copy import deepcopy    # 用于字典的深拷贝
from retrying import retry    # 用于下载错误重试
import gc    # 用于解决内存泄漏
import Interface

# 读取要下载的PDF列表
def read_file(filename):
    dataframe = pd.read_excel(filename)    # 读取Excel
    # print(dataframe)
    rows = dataframe.shape[0]    # 读取行数
    # print(rows)
    # 提取Title、Journal、Authors、Year、Citation、Abstract、PDF Link， 并抓换为list
    article_list = []
    for i in range(rows):
        title = str(dataframe.iat[i, 0])
        title.replace('\n', '')
        title.replace('\r', '')
        # journal = str(dataframe.iat[i, 1])
        # authors = str(dataframe.iat[i, 2])
        # year = str(dataframe.iat[i, 3])
        # citation = str(dataframe.iat[i, 4])
        # abstract = str(dataframe.iat[i, 5])
        # pdf_link = str(dataframe.iat[i, 6])
        # print(title + ' ' + journal + ' ' + authors + ' ' + year + ' ' + citation + ' ' + abstract + ' ' + pdf_link)
        article_dict = {'Title': title, 'Journal': str(dataframe.iat[i, 1]), 'Authors': str(dataframe.iat[i, 2]), 
                        'Year': str(dataframe.iat[i, 3]), 'Citation': str(dataframe.iat[i, 4]), 'Abstract': str(dataframe.iat[i, 5]), 
                        "PDF Link": str(dataframe.iat[i, 6])}
        article_list.append(article_dict)
    # print(len(article_list))
    del dataframe
    del rows
    del title
    del article_dict
    gc.collect()
    return article_list

# 写数据到Excel
def sava_to_excel(article_list, filename):
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
    file_path = pd.ExcelWriter(filename)
    #替换空单元格
    dataframe.fillna(' ',inplace = True)
    if os.path.isfile(file_path):
        # 读取原始内容，追加新内容
        dataframe = pd.read_excel(file_path).append(dataframe, ignore_index=True, sort=False)
    #输出
    dataframe.to_excel(file_path,encoding = 'utf-8',index = False)
    #保存表格
    file_path.save()
    del dataframe
    del order
    del columns_map
    return

# 下载文件
def get_file(article, path):
    filename = '/' + article['Title']
    url = article['PDF Link']
    print('开始下载' + url)
    # print(filename)    # 输出文件名
    # print(url)    # 输出要下载的URL
    error_article = {}

    # 打开链接
    openurl_flag = False
    try:
        data = urllib.request.urlopen(url)
        openurl_flag = True
    except Exception:
        print('URL打开失败，继续下载下一个。')
        error_article = deepcopy(article)
    finally:
        gc.collect()

    # 下载文件
    if openurl_flag:
        try:
            pdf_file = open(path + filename + '.pdf', 'wb')
            block_sz = 8192
            while True:
                buffer = data.read(block_sz)
                if not buffer:
                    break
                pdf_file.write(buffer)
            pdf_file.close()
            data.close()
            del data
            gc.collect()
            print(path + filename + '.pdf')
            print ("Sucessful to download" + " " + filename)
        except Exception:
            print('下载出错，继续下载下一个。')
            error_article = deepcopy(article)
    del filename
    del url
    del openurl_flag
    gc.collect()
    return error_article

def download_file(Ui_Widget, article_list, path):
    print('开始下载文件！共有{}项需要下载。'.format(len(article_list)))
    error_article_list = []
    for article in article_list:
        Ui_Widget.pauseFlag.wait()    # 判断线程是否暂停
        # 判断是否点击了取消按钮
        if Ui_Widget.exitFlag.isSet():
            return
        error_article = get_file(article, path)
        if error_article:
            error_article_list.append(error_article)
    if error_article_list:
        sava_to_excel(error_article_list, 'Excels/Red_Error.xlsx')
    print('\n下载完成！')
    del error_article_list
    gc.collect()
    return

from lxml import etree
text = '''
<div>
    <ul>
         <li class="item-0"><a href="https://ask.hellobi.com/link1.html">first item</a></li>
         <li class="item-1"><a href="https://ask.hellobi.com/link2.html">second item</a></li>
         <li class="item-inactive"><a href="https://ask.hellobi.com/link3.html">third item</a></li>
         <li class="item-1"><a href="https://ask.hellobi.com/link4.html">fourth item</a></li>
         <li class="item-0"><a href="https://ask.hellobi.com/link5.html">fifth item</a>
         <li class="li li-first"><a href="https://ask.hellobi.com/link.html">sixth item</a></li>
         <li class="li li-first" name="item"><a href="https://ask.hellobi.com/link.html">seventh item</a></li>
     </ul>
 </div>
'''
html = etree.HTML(text)
result = etree.tostring(html)
print('-----解析节果-----')
# print(result.decode('utf-8'))    # 输出解析后的节果

# 从文件中解析html
# html = etree.parse('./test.html', etree.HTMLParser())
# result = etree.tostring(html)
# print(result.decode('utf-8'))    # 输出解析后的节果

# 所有节点
print('-----所有节点-----')
result = html.xpath('//*')
print(result)

# 所有li节点
print('-----所有li节点-----')
result = html.xpath('//li')
print(result)
print(result[0])

# 子节点
print('-----子节点-----')
result = html.xpath('//li/a')    #  li 节点的所有直接 a 子节点
print(result)

result = html.xpath('//ul//a')    # ul 节点下的所有子孙 a 节点
print(result)

# 父节点
print('-----父节点-----')
result = html.xpath('//a[@href="https://ask.hellobi.com/link4.html"]/../@class')
print(result)

result = html.xpath('//a[@href="https://ask.hellobi.com/link4.html"]/parent::*/@class')
print(result)

# 属性匹配
print('-----属性匹配-----')
result = html.xpath('//li[@class="item-0"]')
print(result)

# 文本获取
print('-----文本获取-----')
result = html.xpath('//li[@class="item-0"]/text()')
print(result)

result = html.xpath('//li[@class="item-0"]/a/text()')
print(result)

result = html.xpath('//li[@class="item-0"]//text()')
print(result)

# 属性获取
print('-----属性获取-----')
result = html.xpath('//li/a/@href')
print(result)

# 属性多值匹配
print('-----属性多值匹配-----')
result = html.xpath('//li[@class="li"]/a/text()')    # 无法匹配
print(result)

result = html.xpath('//li[contains(@class, "li")]/a/text()')
print(result)

# 多属性匹配
print('-----多属性匹配-----')
result = html.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')    # class=li并且name=item
print(result)

# 按序选择
print('-----按序选择-----')
result = html.xpath('//li[1]/a/text()')    # 第一个
print(result)
result = html.xpath('//li[last()]/a/text()')    # 最后一个
print(result)
result = html.xpath('//li[position()<3]/a/text()')    # 前两个
print(result)
result = html.xpath('//li[last()-2]/a/text()')    # 倒数第三个
print(result)

# 节点轴选择
print('-----节点轴选择-----')
result = html.xpath('//li[1]/ancestor::*')    # 所有祖先节点
print(result)
result = html.xpath('//li[1]/ancestor::div')    # 所有祖先节点中的div
print(result)
result = html.xpath('//li[1]/attribute::*')    # 所有属性
print(result)
result = html.xpath('//li[1]/child::a[@href="https://ask.hellobi.com/link1.html"]')    # 子节点中href为...的节点
print(result)
result = html.xpath('//li[1]/descendant::span')    # 所有孙子节点中的span
print(result)
result = html.xpath('//li[1]/following::*[2]')    # 当前节点之后的所有节点，这里我们虽然使用的是 * 匹配，但又加了索引选择，所以只获取了第二个后续节点。
print(result)
result = html.xpath('//li[1]/following-sibling::*')    # 当前节点之后的所有同级节点，这里我们使用的是 * 匹配，所以获取了所有后续同级节点
print(result)
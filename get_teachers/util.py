import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_soup(url):
    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功
    # 确保使用正确的编码
    response.encoding = 'utf-8'
    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

def get_div_a2url(soup,base_url="https://smxy.shou.edu.cn", name="div", parm="frag", parm_value="窗口2"):


    # 查找指定的<div>标签
    target_div = soup.find(name, {parm: parm_value})

    # 如果找不到目标div，返回空列表
    if not target_div:
        return []

    # 查找目标<div>标签下的所有<a>标签
    a_tags = target_div.find_all('a')

    # 提取所有<a>标签的href属性
    urls = [urljoin(base_url, a.get('href')) for a in a_tags if a.get('href') and is_valid_url(urljoin(base_url, a.get('href')))]

    return urls
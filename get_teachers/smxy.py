import re

import requests

from config import smxy
from get_teachers.util import *

if __name__=="__main__":

    urls_leave_teacher=get_div_a2url(get_soup(smxy))
    url_result=[]
    for url_leave_teacher in urls_leave_teacher:

        soup = get_soup(url_leave_teacher)
        url_leave_result=[]
        em_tag = soup.find('em', class_='all_pages')

        for list_num in range(int(em_tag.text)):
            urls_page = get_div_a2url(get_soup(url_leave_teacher.replace("list.htm", f"list{list_num+1}.htm")), parm_value="窗口3")
            filtered_urls = [url for url in urls_page if url.endswith('/page.htm')] # 当前页面的老师url
            url_leave_result.extend(filtered_urls)
        url_result.extend(url_leave_result)
    print(url_result)

    for url in url_result:
        soup=get_soup(url)
        # 查找需要提取的内容，例如所有段落文字
        paragraphs = soup.find_all('p')

        contact_info=None
        # 打印提取的文字内容
        for index,p in enumerate(paragraphs):
            text=p.get_text()
            # 使用正则表达式匹配联系方式后的文字部分
            match = re.search(r'联系(.+)', text, re.DOTALL)

            if match:
                contact_info=[p.get_text() for p in paragraphs[index+1:]]
        if contact_info:
            merged_string = ' '.join(contact_info)
            clean_text = re.sub(r'\xa0', ' ', merged_string)
            print(clean_text)
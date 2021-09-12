import re
import requests
from selenium import webdriver


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text

    @staticmethod
    def douban_get_key(url, return_json=True):
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # browser = webdriver.Chrome(chrome_options=options)
        browser = webdriver.Chrome()
        browser.get(url)
        books = browser.find_elements_by_class_name("sc-bZQynM")[:3]
        hrefs = [x.find_element_by_tag_name('a').get_attribute('href') for x in books if
                 x.find_element_by_tag_name('a')]
        # 获取链接后，请求链接得到详细信息
        data_list = []
        for href in hrefs:
            browser.get(href)
            info_data = browser.find_element_by_xpath('//*[@id="info"]').text
            if not info_data:
                continue
            j_data = {
                'image': browser.find_element_by_id('mainpic').find_element_by_tag_name('a').get_attribute('href'),
                'title': browser.find_element_by_xpath('//*[@id="wrapper"]/h1/span').text.strip(),
                'author': re.search(r'作者: (.*)', info_data).group(1) if re.search(r'作者: (.*)', info_data) else '',
                'publisher': re.search(r'出版社: (.*)', info_data).group(1) if re.search(r'出版社: (.*)', info_data) else '',
                'pubdate': re.search(r'出版年: (.*)', info_data).group(1) if re.search(r'出版年: (.*)', info_data) else '',
                'pages': int(re.search(r'页数: (\d+)', info_data).group(1) if re.search(r'页数: (\d+)', info_data) else 0),
                'price': re.search(r'定价: (.*)', info_data).group(1) if re.search(r'定价: (.*)', info_data) else '',
                'binding': re.search(r'装帧: (.*)', info_data).group(1) if re.search(r'装帧: (.*)', info_data) else '',
                'isbn': re.search(r'ISBN: (.*)', info_data).group(1),
                'summary': browser.find_element_by_class_name('intro').text.strip(),
            }
            data_list.append(j_data)
        browser.quit()
        return {
            "total": len(data_list),
            "books": data_list
        }

    @staticmethod
    def douban_get_isbn(url, return_json=True):
        # options = webdriver.ChromeOptions()
        # options.add_argument('--no-sandbox')
        # options.add_argument('--headless')
        # browser = webdriver.Chrome(chrome_options=options)
        browser = webdriver.Chrome()
        browser.get(url)
        books = browser.find_elements_by_class_name("sc-bZQynM")[:3]
        href = [x.find_element_by_tag_name('a').get_attribute('href') for x in books if
                x.find_element_by_tag_name('a')]
        if not href:
            return
        href = href[0]
        # 获取链接后，请求链接得到详细信息
        browser.get(href)
        info_data = browser.find_element_by_xpath('//*[@id="info"]').text
        if not info_data:
            return
        j_data = {
            'image': browser.find_element_by_id('mainpic').find_element_by_tag_name('a').get_attribute('href'),
            'title': browser.find_element_by_xpath('//*[@id="wrapper"]/h1/span').text.strip(),
            'author': re.search(r'作者: (.*)', info_data).group(1),
            'publisher': re.search(r'出版社: (.*)', info_data).group(1),
            'pubdate': re.search(r'出版年: (.*)', info_data).group(1),
            'pages': int(re.search(r'页数: (\d+)', info_data).group(1)),
            'price': re.search(r'定价: (.*)', info_data).group(1),
            'binding': re.search(r'装帧: (.*)', info_data).group(1),
            'isbn': re.search(r'ISBN: (.*)', info_data).group(1),
            'summary': browser.find_element_by_class_name('intro').text.strip(),
        }
        browser.quit()
        return j_data

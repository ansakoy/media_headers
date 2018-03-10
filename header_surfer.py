# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class HeadersSurfer(object):

    def __init__(self, file_handler):
        self.handler = file_handler

    def get_page(self, url, limits=None):
        response = requests.get(url).content
        if limits:
            return response[limits[0]: limits[1]]
        else:
            return response

    def get_area(self, content, tag, **kwargs):
        soup = BeautifulSoup(content, 'lxml')
        area = soup(tag, **kwargs)[0]
        return area

    def get_header_blocks(self, area, tag, **kwargs):
        soup = BeautifulSoup(area, 'lxml')
        headers = soup(tag, **kwargs)
        return headers

    def get_text(self, area, tag, index=0, **kwargs):
        soup = BeautifulSoup(area, 'lxml')
        text = soup(tag, **kwargs)[index].text
        return text

    def get_href(self, area, tag, **kwargs):
        soup = BeautifulSoup(area, 'lxml')
        href = soup(tag, **kwargs)[0].get('href')
        return href

    def write_to_txt(self, string):
        self.handler.write(string)


# r = requests.get('https://www.wsj.com').text
# print type(r)

if __name__ == '__main__':
    # surfer = HeadersSurfer('fh')
    # surfer.get_page('https://www.economist.com', limits=(0, 100000))
    pass

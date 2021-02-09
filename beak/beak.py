#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import lxml.html
from requests import Session


class Beak:
    def __init__(self):
        self.session = Session()
        self.headers = {
            'Content-Type':
            'application/x-www-form-urlencoded',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/88.0.4324.96 Safari/537.36',
        }

    def search(self, query):
        form_data = {'q': query}
        url = "https://html.duckduckgo.com/html/"
        new_results = True

        known_links = set()

        while new_results:
            response = self.session.post(url, headers=self.headers, data=form_data)
            html = response.content.decode('utf-8')
            root = lxml.html.document_fromstring(html)

            for result_element in root.xpath("//div[contains(@class, 'result__body')]"):
                result = {
                    'title':
                    ''.join(result_element.xpath(".//h2[@class='result__title']//text()")).strip(),
                    'link':
                    result_element.xpath(".//a[@class='result__a']/@href")[0],
                    'snippet':
                    ''.join(result_element.xpath(".//a[@class='result__snippet']//text()"))
                }

                if result['link'] in known_links:
                    new_results = False
                    continue

                known_links.add(result['link'])
                yield result

            input_items = root.xpath("//div[@class='nav-link'][1]/form/input")
            for index, input_item in enumerate(input_items):
                if index == 0:
                    continue
                form_data[input_item.xpath("./@name")[0]] = input_item.xpath("./@value")[0]
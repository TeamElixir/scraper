# -*- coding: utf-8 -*-
import scrapy
import os


class CriminalSpider(scrapy.Spider):
    name = 'criminal'
    # allowed_domains = ['https://caselaw.findlaw.com/summary/search/?court=us-supreme-court']
    start_urls = ['https://caselaw.findlaw.com/summary/search/?court=us-supreme-court&topic=cs_19&search=Search']

    i = 0

    def parse(self, response):
        links = response.css('tr.srpcaselawtr b a::attr(href)').extract()
        for link in links:
            self.i += int(1)
            print("i after incrementing:", str(self.i))
            scrapy.Request(link, callback=self.read_more)

    def read_more(self, response):
        print("read_more: ", str(self.i))
        read_more_link = response.css('div.btn_read a::attr(href)').extract_first()
        scrapy.Request(read_more_link, callback=self.extract_text)

    def extract_text(self, response):
        print("extract_text: ", str(self.i))
        cwd = os.getcwd()
        directory = cwd + "/cases"
        content = response.css('div.caselawcontent.searchable-content *::text').extract()
        content = ' '.join(content)
        file_name = directory + "/" + str(self.i) + ".txt"
        print("------------------------------------")
        # print(content)
        print("------------------------------------")
        self.write_to_file(content, file_name)

    def write_to_file(self, content, file_name):
        print("write_to_file: ", str(self.i))
        text_file = open(file_name, "w+")
        text_file.write(str(content))
        text_file.flush()
        text_file.close()

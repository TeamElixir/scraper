# -*- coding: utf-8 -*-
import scrapy
import os


class CriminalSpider(scrapy.Spider):
    name = 'criminal'
    # allowed_domains = ['https://caselaw.findlaw.com/summary/search/?court=us-supreme-court']
    start_urls = ['https://caselaw.findlaw.com/summary/search/?court=us-supreme-court&topic=cs_19&search=Search']

    def parse(self, response):
        links = response.css('tr.srpcaselawtr b a::attr(href)').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.read_more)

        next_page = response.css('a.pgnum::attr(href)').extract()[-1]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def read_more(self, response):
        read_more_link = response.css('div.btn_read a::attr(href)').extract_first()
        yield scrapy.Request(read_more_link, callback=self.extract_text)

    def extract_text(self, response):
        case_title = ' '.join(response.css('div.caselawTitle.baseIncluder.section *::text').extract()).strip()
        cwd = os.getcwd()
        directory = cwd + "/cases"
        content = response.css('div.caselawcontent.searchable-content *::text').extract()
        content = ' '.join(content)
        file_name = directory + "/" + str(case_title) + ".txt"
        self.write_to_file(content, file_name)
        print(file_name)

    def write_to_file(self, content, file_name):
        text_file = open(file_name, "w+")
        text_file.write(str(content))
        text_file.flush()
        text_file.close()

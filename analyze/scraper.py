# This is a sample Python script.
import json
import sys
import time

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# export PKG_CONFIG_PATH="/usr/local/opt/libxml2/lib/pkgconfig"
import scrapy

from langdetect import detect
from scrapy.crawler import CrawlerProcess


class SiteInfo:
    documents = []
    line_count = 0

    @classmethod
    def add_document(cls, document):
        document_en = [line for line in document if SiteInfo.is_english(line)]
        cls.documents.append(document_en)

    @staticmethod
    def is_english(sentence):
        try:
            lang = detect(sentence)
            return lang == 'en'  # 'en' is the ISO 639-1 code for English
        except:
            return False


class MySpider(scrapy.Spider):
    name = 'myspider'
    custom_settings = {
        "DEPTH_LIMIT": 1
    }
    max_crawl_time = 30
    max_line_count = 2000

    # Maximum depth for crawling

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_time = time.time()

    def parse(self, response):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > self.max_crawl_time:
            self.logger.warning(f"Time limit ({self.max_crawl_time} seconds) reached. Stopping crawling.")
            raise scrapy.exceptions.CloseSpider('Time limit reached')
        if SiteInfo.line_count > self.max_line_count:
            self.logger.warning(f"Line limit ({self.max_line_count}) reached. Stopping crawling.")
            raise scrapy.exceptions.CloseSpider('Time limit reached')

        # Extract and yield text from the current page
        page_text = response.css('p::text, div::text, span::text').getall()
        page_text = [text.strip() for text in page_text if text.strip()]
        document = set()
        for text in page_text:
            SiteInfo.line_count += 1
            document.add(text)
        SiteInfo.add_document(document)

        next_pages = response.css("a::attr(href)").getall()
        for next_page in next_pages:
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)


# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    start_url = sys.argv[1]
    save_to = sys.argv[2]
    process = CrawlerProcess()
    process.crawl(MySpider, start_urls=[start_url])
    process.start()

    delimiter = ' '

    with open(save_to, 'w') as json_file:
        json.dump(SiteInfo.documents, json_file)

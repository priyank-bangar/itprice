import scrapy
from ..items import ItpriceItem

class ItpriceSpider(scrapy.Spider):
    name = 'itprice'
    start_urls = [
        'https://itprice.com/'
    ]

    def parse(self, response, **kwargs):
        top_search_link = response.css('#dropdown-menu1 li a::attr(href)')
        for li_tag in top_search_link:
            # Remove if condition to extract all top search links
            if 'hp' in li_tag.extract():
                yield scrapy.Request(li_tag.extract(), callback=self.top_search_model_page)
    
    def top_search_model_page(self, response):
        model_link = response.css('#sort > tbody a::attr(href)')
        for td_tag in model_link:
            # Remove if condition to extract all model link
            if td_tag.extract() == 'https://itprice.com/hp-price-list/dl380.html':
                yield scrapy.Request(td_tag.extract(), callback=self.extract_page)
    
    def extract_page(self, response):
        product = ItpriceItem()
        table_to_extract = response.css('#choice_product > tbody > tr')
        for tr_tags in table_to_extract:
            if 'not found' in tr_tags.css('td::text').extract()[0]:
                yield None
            product['product_number'] = tr_tags.css('a.pull-left::text').extract()[0].strip()
            product['description'] = tr_tags.css('.descr::text')[0].extract().strip()
            product['list_price'] = tr_tags.css('.descr+ .text-right::text')[0].extract().strip()
            our_price_temp = tr_tags.css('.white-space-nowrap::text').extract()
            if our_price_temp:
                product['our_price'] = our_price_temp[0].strip().strip('(').strip()
            else:
                product['our_price'] = None
            yield product
        
        next_page_url, last_page_number = response.css('#page1 a')[-1].css('::attr(href)').extract()[0].rsplit('=')
        for next_page_number in range(2, int(last_page_number)+1):
            yield response.follow(f"{next_page_url}={next_page_number}", callback=self.extract_page)

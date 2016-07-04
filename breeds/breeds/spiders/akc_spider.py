import scrapy
from breeds.items import dog_item

class size_spider(scrapy.Spider):
    """ use `scrapy crawl akc -o akc.json` to run this spider """
    name = "akc"
    allowed_domains = ["akc.org"]
    start_urls = ["http://www.akc.org/dog-breeds/"]

    def parse(self, response):

        top_atoz = response.xpath('//ul[@class="pagination"]')[0]
        atoz = top_atoz.xpath(".//li/a/@href").extract()

        for letter in atoz:
            url = response.urljoin(letter)
            yield scrapy.Request(url, callback=self.breeds_on_page)
        # end for

    # end def parse

    def breeds_on_page(self,response):

        # extract relative urls
        rurls = response.xpath("//h2/a/@href").extract()
        # construct absolute urls
        for rurl in rurls:
            url = response.urljoin(rurl)
            yield scrapy.Request(url, callback=self.extract_breed_info)
        # end for rurl

    # end def breeds_on_page

    def extract_breed_info(self,response):

        breed = response.xpath("//h1/text()").extract()[0]

        try:
            rank_node = response.xpath('//div[@class="bigrank"]')[0]
            rank  = int( rank_node.xpath("text()").extract()[0] )
        except:
            rank = -1
        # end try

        try:
            mytype_node = response.xpath('//div[@class="type"]')
            mytype = mytype_node.xpath("img/@alt").extract()[0]
        except:
            mytype = "unknown"
        # end try

        try:
            detail_node = response.xpath('//div[@class="description"]')
            energy = detail_node.xpath('span[@class="energy_levels"]/text()').extract()[0]
            energy = energy.replace("\n","").replace("ENERGY","").strip()
            mysize = detail_node.xpath('span[@class="size"]/text()').extract()[0]
            mysize = mysize.replace("\n","").replace("size","").strip()
        except:
            energy = "unknown"
            mysize = "unknown"
        # end try

        entry = dog_item()
        entry["breed"] = breed
        entry["rank"]  = rank
        entry["group"] = mytype
        entry["size"]  = mysize
        entry["energy"]= energy
        yield entry

    # end def 
# end class size_spider

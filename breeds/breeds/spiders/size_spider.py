import scrapy
from breeds.items import dog_item

class size_spider(scrapy.Spider):
    """ use `scrapy crawl size -o size.json` to run this spider """
    name = "size"
    allowed_domains = ["dogbreedslist.info"]
    start_urls = ["http://www.dogbreedslist.info/"]

    def parse(self, response):

        # search entire response and select <div class="main-l>
        category_tab = response.xpath('//div[@class="main-l"]')

        # select <dl> <dt>Size</dt> ... </dl>
        size_tab = category_tab.xpath('dl[dt="Size"]')

        # loop size catogory and pass page to data extraction function
        for mysize in size_tab.xpath("dd"):

            url = mysize.xpath("a/@href").extract()[0]
            size_text = mysize.xpath("a/text()").extract()[0]
            extra_info = {"size":size_text}

            yield scrapy.Request(url, callback=lambda x:
                self.extract_breed_info(x,extra_info)
            )
        # end for url

    # end def parse

    def extract_breed_info(self,response,extra_info=dict()):

        # each dog is in a <div class="list"> tab
        dogs = response.xpath('//div[@class="list"]')
        # each list tab has 
        #  list-01: left = picture, right rankings
        #    right-t = breed, right-c = pop,hyp,int, right-b = origin
        #  list-02: <span> Rank </span> <p> # </p>
        #  list-03: <p> Gentle </p> <p> Intelligent </p> etc.
        #  list-04: <span> Hypoallergenic </span> <p> # </p>
        #  list-05: <span> Rank (Intelligence) </span> <p> # </p>
        # ! we really only need to scrape list-01

        for dog in dogs:
            # start collecting data
            entry = dog_item()

            breed = dog.xpath('.//div[@class="right-t"]/p/a/text()').extract()[0]
            entry["breed"] = breed
            entry.update(extra_info)

            # hand data over to scrapy
            yield entry
        # end for dog

        # look for the "Next" button, follow if found
        next_button = response.xpath('//li[a/text()="Next"]')
        if len(next_button)>0:
            # get relative url
            next_url = next_button[0].xpath(".//@href").extract()[0]
            # get absolute url
            next_url = response.urljoin(next_url)
            # give myself a call
            yield scrapy.Request(next_url, callback=lambda x:
                self.extract_breed_info(x,extra_info)
            )
        # end if

    # end def 
# end class size_spider

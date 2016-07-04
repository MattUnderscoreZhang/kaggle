import scrapy
from breeds.items import dog_item

class dog_detail_spider(scrapy.Spider):
    """ use `scrapy crawl dd -o dog_detail.json` to run this spider """
    name = "dd"
    allowed_domains = ["dogbreedslist.info"]
    start_urls = ["http://www.dogbreedslist.info/"]

    def parse(self, response):

        atoz = response.xpath('//div[@class="atoz"]')[0]
        for url in atoz.xpath('.//@href').extract():
            yield scrapy.Request(url,callback=self.extract_breed_info)
        # end for

    # end def parse

    def extract_breed_info(self,response):

        # each dog is in a <div class="list"> tab
        dogs = response.xpath('//div[@class="list"]')

        for dog in dogs:

            # go to details page
            detail_url = dog.xpath(
                './/div[@class="right-b"]/span/a/@href'
            ).extract()[0]

            # read details page
            yield scrapy.Request(detail_url,self.read_dog_details)

        # end for dog

        # look for the "Next" button, follow if found
        next_button = response.xpath('//li[a/text()="Next"]')
        if len(next_button)>0:
            # get relative url
            next_url = next_button[0].xpath(".//@href").extract()[0]
            # get absolute url
            next_url = response.urljoin(next_url)
            # give myself a call
            yield scrapy.Request(next_url, callback=self.extract_breed_info)
        # end if

    # end def 

    def read_dog_details(self,response):
        dog_data = dog_item()

        entry = {}

        # look entries rated with a number of stars, extract the name and rating
        rated_characteristics = response.xpath('//span[contains(@class,"star")]')
        for character in rated_characteristics:
            name  = character.xpath('../../td[@class="left"]/text()').extract()[0]
            value_text = character.xpath("text()").extract()[0]
            value = float(value_text.split()[0])
            entry[name] = value
        # end for

        # basic fields
        fields_of_interet = ["Popularity","Name","Size"#,"Type"
                ,"Life span","Temperament","Height","Weight"
                ,"Puppy Price"]
        for field in fields_of_interet:
            field_text = "\""+field+"\""
            node = response.xpath('//td[contains(text(),%s)]'%field_text)
            label = node.xpath('text()').extract()[0]
            value = " ".join( node.xpath("../td/text()").extract()[1:] )
            #entry[field] = value
            entry[label] = value
        # end for field

        dog_data["detail"] = entry
        yield dog_data
    # end def read_dog_details

# end class size_spider

import scrapy
from dmoz.items import DogItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dogbreedslist.info"]
    root_url = "http://www.dogbreedslist.info/"
    sub_urls = [
"Tags-A.html",
"Tags-A/list_29_1.html",
"Tags-A/list_29_2.html",
"Tags-A/list_29_3.html",
"Tags-B.html",
"Tags-B/list_30_1.html",
"Tags-B/list_30_2.html",
"Tags-B/list_30_3.html",
"Tags-C.html",
"Tags-C/list_31_1.html",
"Tags-C/list_31_2.html",
"Tags-D.html",
"Tags-D/list_32_1.html",
"Tags-D/list_32_2.html",
"Tags-E.html",
"Tags-F.html",
"Tags-G.html",
"Tags-H.html",
"Tags-I.html",
"Tags-J.html",
"Tags-K.html",
"Tags-L.html",
"Tags-M.html",
"Tags-N.html",
"Tags-O.html",
"Tags-P.html",
"Tags-P/list_44_1.html",
"Tags-P/list_44_2.html",
"Tags-Q.html",
"Tags-R.html",
"Tags-S.html",
"Tags-S/list_47_1.html",
"Tags-S/list_47_2.html",
"Tags-T.html",
"Tags-U.html",
"Tags-V.html",
"Tags-W.html",
"Tags-X.html",
"Tags-Y.html",
"Tags-Z.html"
]
    start_urls = []

    for sub_url in sub_urls:
        if "list" not in sub_url:
            sub_url = sub_url.replace(".html","")
        # end if
        start_urls.append(root_url + sub_url )
    # end for 

    def parse(self, response):

        for right in response.xpath('//div[@class="right"]'):
            item = DogItem()

            # extract breed name
            rightt = right.xpath('div[@class="right-t"]')
            for para in rightt.xpath('p'):
                breed = para.xpath('a/text()').extract()[0]
            # end for 
            item["Breed"] = breed

            # extract popularity
            #for rightc in 
            rightc = right.xpath('div[@class="right-c"]')
            for character in rightc.xpath('div'):
                try:
                    trait = character.xpath("span/text()").extract()[0]
                    value = character.xpath("p/text()").extract()[0]
                except:
                    print("failed at breed: %s" % breed)
                # end try
                item[trait] = value
            # end for 

            yield item



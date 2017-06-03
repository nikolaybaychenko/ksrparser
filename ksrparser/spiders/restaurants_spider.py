import scrapy


class RestaurantSpider(scrapy.Spider):
    name = 'restaurant'

    start_urls = ['http://www.kela.fi/web/en/meal-subsidy-student-restaurants']
    region_base_url = 'http://www.kela.fi'
    restaurants_base_url = 'https://asiointi.kela.fi/opiskelijaravintolahaku/'

    # TODO: pass region name
    def parse(self, response):
        # follow links by regions
        regions = response.css('section.kelafi-article ul')[0].css('li a::attr(href)').extract()
        for href in regions:
            yield response.follow(self.region_base_url + href, self.parse_cities)

    # TODO: pass city name
    def parse_cities(self, response):
        # follow links by cities
        cities = response.css('section.kelafi-article ul')[0].css('li a::attr(href)').extract()
        for href in cities:
            yield response.follow(href, self.parse_restaurants)

    def parse_restaurants(self, response):
        # follow links by restaurants
        restaurants = response.css('table a::attr(href)').extract()
        for href in restaurants:
            yield response.follow(self.restaurants_base_url + href, self.parse_restaurant)

    def parse_restaurant(self, response):

        #def extract_with_css(query):
        #    return response.css(query).extract_first().strip()

        yield {
            'restaurant': response.css('table tr td b::text').extract_first().strip(),
            'street_address': response.css('table tr')[1].css('td::text')[2].extract().strip(),
            'postal_code': response.css('table tr')[2].css('td::text')[2].extract().strip(),
            'post_office': response.css('table tr')[3].css('td::text')[2].extract().strip(),
            'restaurants_web': response.css('table tr')[4].css('td::text')[2].extract().strip(),
            'restaurants_operator': response.css('table tr')[5].css('td::text')[2].extract().strip(),
            'operators_web': response.css('table tr')[6].css('td::text')[2].extract().strip(),
        }

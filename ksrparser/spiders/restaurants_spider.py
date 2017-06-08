import scrapy


class RestaurantSpider(scrapy.Spider):
    name = 'restaurant'

    # In English
    # start_urls = ['http://www.kela.fi/web/en/meal-subsidy-student-restaurants']
    # In Finnish
    start_urls = ['http://www.kela.fi/ateriatuki-opiskelijaravintolahaku']
    region_base_url = 'http://www.kela.fi'
    restaurants_base_url = 'https://asiointi.kela.fi/opiskelijaravintolahaku/'

    def parse(self, response):
        regions = response.css('section.kelafi-article ul')[0].css('li')
        for region in regions:
            region_name = region.css('a::text').extract_first()
            region_href = region.css('a::attr(href)').extract_first()
            yield response.follow(self.region_base_url + region_href, self.parse_cities, meta={'region_name': region_name})

    def parse_cities(self, response):
        region_name = response.meta['region_name']
        cities = response.css('section.kelafi-article ul')[0].css('li')
        for city in cities:
            city_name = city.css('a::text').extract_first()
            city_href = city.css('a::attr(href)').extract_first()
            yield response.follow(city_href, self.parse_restaurants, meta={'region_name': region_name, 'city_name': city_name})

    def parse_restaurants(self, response):
        region_name = response.meta['region_name']
        city_name = response.meta['city_name']
        restaurants = response.css('table a::attr(href)').extract()
        for href in restaurants:
            yield response.follow(self.restaurants_base_url + href, self.parse_restaurant, meta={'region_name': region_name, 'city_name': city_name})

    def parse_restaurant(self, response):
        yield {
            'Restaurant': response.css('table tr td b::text').extract_first().strip(),
            'Region': response.meta['region_name'],
            'City': response.meta['city_name'],
            'Street address': response.css('table tr')[1].css('td::text')[2].extract().strip(),
            'Postal code': response.css('table tr')[2].css('td::text')[2].extract().strip(),
            'Post office': response.css('table tr')[3].css('td::text')[2].extract().strip(),
            'Restaurants operator': response.css('table tr')[5].css('td::text')[2].extract().strip()
        }

import scrapy
from ImdbMovies.items import ImdbmoviesItem


imdb_url = 'http://www.imdb.com'


class ImdbMoviesSpider(scrapy.Spider):

    name = "imdbMoviesSpider"
    start_urls = ['https://www.imdb.com/movies-coming-soon/?ref_=nv_mv_cs_4']

    def parse(self, response):
        for td in response.css('td.overview-top'):
            movie_link = imdb_url+td.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=movie_link, callback=self.parse_movies_metadata)

        next_page = response.css('div.sort a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(imdb_url + next_page, self.parse)

    def parse_movies_metadata(self, response):

        movie = ImdbmoviesItem()

        movie['link'] = response.url
        try:
            movie['title'] = response.xpath('//h1[@itemprop="name"]/text()').extract_first().strip()
        except (TypeError, AttributeError):
            movie['title'] = None
        try:
            movie['rate'] = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
        except (TypeError, AttributeError):
            movie['rate'] = None
        try:
            movie['duration'] = response.xpath('//time[@itemprop="duration"]/text()').extract_first().strip()
        except (TypeError, AttributeError):
            movie['duration'] = None
        try:
            movie['director'] = response.xpath('//span[@itemprop="director"]/a/span/text()').extract_first()
        except (TypeError, AttributeError):
            movie['director'] = None
        try:
            movie['stars'] = response.xpath('//span[@itemprop="actors"]/a/span/text()').extract()
        except (TypeError, AttributeError):
            movie['stars'] = None
        try:
            movie['photos'] = [imdb_url+href for href in response.xpath('//div[@class="mediastrip"]/a/@href').extract()]
        except (TypeError, AttributeError):
            movie['photos'] = None
        try:
            movie['actors'] = response.xpath('//td[@itemprop="actor"]/a/span/text()').extract()
        except (TypeError, AttributeError):
            movie['actors'] = None
        try:
            movie['storyline'] = response.xpath('//span[@itemprop="description"]/text()').extract_first().strip()
        except (TypeError, AttributeError):
            movie['storyline'] = None
        try:
            movie['genres'] = [value.strip() for value in response.xpath('//div[@itemprop="genre"]/a/text()').extract()]
        except (TypeError, AttributeError):
            movie['genres'] = None

        div_txt_block = response.xpath('//div[@id="titleDetails"]/div[@class="txt-block"]')
        for div in div_txt_block:
            h4_text = div.xpath('.//h4/text()').extract_first()
            if h4_text == 'Country:':
                try:
                    movie['country'] = div.xpath('.//a/text()').extract()
                except (TypeError, AttributeError):
                    movie['country'] = None
            elif h4_text == 'Language:':
                try:
                    movie['language'] = div.xpath('.//a/text()').extract()
                except (TypeError, AttributeError):
                    movie['language'] = None
            elif h4_text == 'Release Date:':
                rel_date_href = div.xpath('.//span[@class="see-more inline"]/a/@href').extract_first()
                rel_date_link = response.url.replace('?ref_=cs_ov_tt', rel_date_href)
                request = scrapy.Request(url=rel_date_link, callback=self.parse_movies_reledate)
                request.meta['movie'] = movie
                yield request
            elif h4_text == 'Production Co:':
                company_href = div.xpath('.//span[@class="see-more inline"]/a/@href').extract_first()
                company_link = response.url.replace('?ref_=cs_ov_tt', company_href)
                request = scrapy.Request(url=company_link, callback=self.parse_movies_company)
                request.meta['movie'] = movie
                yield request
        

    def parse_movies_reledate(self, response):

        movie = response.meta['movie']

        trs = response.xpath('//table[@id="release_dates"]/tr')
        rel_date_list = []
        for tr in trs:
            rel_date_dict = {}
            rel_date_dict['country'] = tr.xpath('.//a/text()').extract_first()
            rel_date_dict['date'] = tr.xpath('.//td[@class="release_date"]/text()').extract_first()
            rel_date_list.append(rel_date_dict)
        try:
            movie['releaseDate'] = rel_date_list
        except (TypeError, AttributeError):
            movie['releaseDate'] = None
        

    def parse_movies_company(self, response):

        movie = response.meta['movie']

        try:
            movie['production'] = response.xpath(
                '(//div[@id="company_credits_content"]/ul[@class="simpleList"])[1]/li/a/text()').extract()
        except (TypeError, AttributeError):
            movie['production'] = None
        li_text = response.xpath('(//div[@id="company_credits_content"]/ul[@class="simpleList"])[2]/li')
        try:
            movie['distributor'] = [i.strip().replace(' ', '') for i in li_text.xpath('string(.)').extract()]
        except (TypeError, AttributeError):
            movie['distributor'] = None
        yield movie

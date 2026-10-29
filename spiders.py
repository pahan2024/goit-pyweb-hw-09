import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        # Списки для збереження результатів
        self.quotes_data = []
        self.authors_data = []
        # Множина для унікальності авторів
        self.seen_authors = set()

    def parse(self, response):
        """Парсинг головної сторінки з цитатами."""
        for quote in response.css("div.quote"):
            tags = quote.css("div.tags a.tag::text").getall()
            author = quote.css("small.author::text").get().strip()
            text = quote.css("span.text::text").get().strip()

            self.quotes_data.append({"tags": tags, "author": author, "quote": text})

            # Перехід на сторінку автора, якщо ми його ще не парсили
            author_url = quote.css("span a::attr(href)").get()
            if author_url and author not in self.seen_authors:
                self.seen_authors.add(author)
                yield response.follow(author_url, callback=self.parse_author)

        # Перехід на наступну сторінку цитат (пагінація)
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        """Парсинг сторінки конкретного автора."""
        fullname = response.css("h3.author-title::text").get().strip()
        born_date = response.css("span.author-born-date::text").get().strip()
        born_location = response.css("span.author-born-location::text").get().strip()
        description = response.css("div.author-description::text").get().strip()

        self.authors_data.append(
            {
                "fullname": fullname,
                "born_date": born_date,
                "born_location": born_location,
                "description": description,
            }
        )

import json
import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"
    start_urls = ["http://quotes.toscrape.com"]

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.quotes_data = []
        self.authors_data = {}
        self.visited_authors = set()

    def parse(self, response):
        for quote in response.css("div.quote"):
            tags = quote.css("div.tags a.tag::text").getall()
            author_name = quote.css("small.author::text").get()
            text = quote.css("span.text::text").get()

            if author_name:
                author_name = author_name.strip()

            self.quotes_data.append(
                {
                    "tags": tags,
                    "author": author_name,
                    "quote": text.strip() if text else "",
                }
            )

            author_url = quote.css("span a::attr(href)").get()
            if author_url and author_name:
                if author_name not in self.visited_authors:
                    self.visited_authors.add(author_name)
                    yield response.follow(
                        author_url,
                        callback=self.parse_author,
                        cb_kwargs={"author_name": author_name},
                    )

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response, author_name):
        born_date = response.css("span.author-born-date::text").get()
        born_location = response.css("span.author-born-location::text").get()
        description = response.css("div.author-description::text").get()

        # Фікс для Alexandre Dumas: замість імені з h3 (яке містить дефіс),
        # ми використовуємо точне ім'я із цитати (author_name), щоб JSON-файли ідеально збігалися!
        self.authors_data[author_name] = {
            "fullname": author_name,
            "born_date": born_date.strip() if born_date else "",
            "born_location": born_location.strip() if born_location else "",
            "description": description.strip() if description else "",
        }

    def closed(self, reason):
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(self.quotes_data, f, ensure_ascii=False, indent=4)

        with open("authors.json", "w", encoding="utf-8") as f:
            json.dump(list(self.authors_data.values()), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "LOG_LEVEL": "INFO",
            "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        }
    )
    process.crawl(QuotesSpider)
    process.start()

import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders import QuotesSpider

def main():
    # Налаштування процесу Scrapy
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    
    # Реєстрація павука
    crawler = process.create_crawler(QuotesSpider)
    process.crawl(crawler)
    
    print("🚀 Запуск скрапінгу сайту quotes.toscrape.com...")
    process.start()  # Скрипт зупиниться тут до завершення парсингу
    
    # Отримання зібраних даних з об'єкта павука
    spider_instance = crawler.spider
    
    # Запис цитат у quotes.json
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(spider_instance.quotes_data, f, ensure_ascii=False, indent=2)
    print("💾 Файл quotes.json успішно збережено.")

    # Запис авторів у authors.json
    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(spider_instance.authors_data, f, ensure_ascii=False, indent=2)
    print("💾 Файл authors.json успішно збережено.")
    
    print("\n Скрапінг успішно завершено! Файли готові до імпорту в MongoDB.")

if __name__ == '__main__':
    main()

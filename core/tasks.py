from celery import shared_task
from scrapy.crawler import CrawlerProcess
from core.spider import DadrahSpider


@shared_task
def example_task():
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })
    process.crawl(DadrahSpider)
    process.start()


example_task.delay()
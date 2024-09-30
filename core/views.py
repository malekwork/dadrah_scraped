from django.http import HttpResponse
from django.views import generic
from scrapy.crawler import CrawlerProcess

from core.models import Question, Lawyer
from core.spider import DadrahSpider
import json


def scrape_hacker_news(request):
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })
    process.crawl(DadrahSpider)
    process.start()
    with open("items.json", "r") as f:
        data = f.read()
    return HttpResponse(data, content_type='application/json')


class QuestionList(generic.ListView):
    queryset = Question.objects.all()
    template_name = 'core/index.html'
    paginate_by = 3


class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = 'core/question_detail.html'
    context_object_name = 'question'


class LawyerDetailView(generic.DetailView):
    model = Lawyer
    template_name = 'core/lawyer_detail.html'
    context_object_name = 'lawyer'
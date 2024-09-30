import scrapy
from core.models import Question, Answer, Lawyer


class DadrahSpider(scrapy.Spider):
    name = "dadrah"
    start_urls = ["https://www.dadrah.ir/consulting-catalog.php"]
    page = 0
    pages_to_scrape = 2
    question_dates = []
    question_counter = -1

    def parse(self, response):
        self.page += 1
        self.question_dates = response.css('span.pull-right::text').getall()

        question_links = self.extract_question_links(response)

        for link in question_links:
            full_url = response.urljoin(link)
            self.question_counter += 1
            yield scrapy.Request(full_url, callback=self.parse_question)

        self.question_counter = -1
        next_page_url = response.css("a#page_a_link::attr(href)").get()
        if next_page_url and self.page < self.pages_to_scrape:
            yield response.follow(next_page_url, self.parse)

    def extract_question_links(self, response):
        """Extract the links of the questions from the main page."""
        links = response.css('a.btn.btn-success[role="button"]')
        return [link.attrib['href'] for link in links if "ادامه ی مطلب و پاسخ ها ..." in link.get()]

    def parse_question(self, response):
        """Parse each question page to extract the details."""
        question_id = self.extract_question_id(response.url)
        question_title = self.extract_question_title(response)
        question_text = self.extract_question_text(response)

        lawyer_names, lawyer_ids, lawyer_cities = self.extract_lawyer_details(response)
        answers_texts = self.extract_answers_text(response)

        question = self.build_question(
            date=self.question_dates[self.question_counter],
            title=question_title,
            text=question_text
        )

        self.build_answers(
            question,
            lawyer_names,
            lawyer_ids,
            lawyer_cities,
            answers_texts
        )

    def extract_question_id(self, url):
        """Extract the question ID from the URL."""
        return url.split('requestID=')[-1]

    def extract_question_title(self, response):
        title = response.xpath('/html/body/div[1]/div[1]/div[1]/div/div[1]/h3').get()
        return title.split('-')[-1].strip()[:-5]

    def extract_question_text(self, response):
        text = response.css('div.card-body::text').get()
        return ' '.join(text.split()).strip()

    def extract_lawyer_details(self, response):
        """Extract lawyer names, IDs, and cities from the question page."""
        lawyer_names = [' '.join(name.split()).strip() for name in
                        response.css('a.text-decoration-none:not([target]):not(.btn):not(.text-color)::text').getall()
                        if 'مشاهده سوابق' not in name and name.strip()]

        lawyer_ids = [link for link in response.css(
            'a.text-decoration-none:not([target]):not(.btn):not(.text-color)::attr(href)').getall()
                      if 'مشاهده سوابق' not in link and link.strip()]

        cities = [city.replace('استان:', '').strip() for city in
                  response.css('div.text-md-start::text').getall() if city.strip()]

        return lawyer_names, lawyer_ids, cities

    def extract_answers_text(self, response):
        return [' '.join(text.split()).strip() for text in response.css('div.media div p::text').getall()]

    def build_answers(self,question, lawyer_names, lawyer_ids, cities, answers_texts):
        for i in range(len(answers_texts)):
            lawyer, created = Lawyer.objects.get_or_create(
                id=lawyer_ids[i],
                defaults={'name': lawyer_names[i], 'city': cities[i]}
            )

            Answer.objects.create(
                question=question,
                text=answers_texts[i],
                lawyer= lawyer
            )

    def build_question(self, date, title, text):
        return Question.objects.create( date=date, title=title, text=text)


"""
    def build_question_json_output(self, question, answers):
        Format the output for the question and its answers.
        return {
            'question': {
                'ID': question.id,
                'title': question.title,
                'text': question.text,
                'answers': [
                    {
                        'text': answer.text,
                        'lawyer': {
                            'ID': answer.lawyer.id,
                            'name': answer.lawyer.name,
                            'city': answer.lawyer.city,
                        }
                    } for answer in answers
                ]
            }
        }
"""

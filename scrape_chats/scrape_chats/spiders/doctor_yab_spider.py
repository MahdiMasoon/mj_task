from pathlib import Path

import scrapy


class ChatsSpider(scrapy.Spider):
    name = "chats"

    page_count = 0
    page_limit = 5

    start_urls = [
        "https://doctor-yab.ir/faq/?page=1"
    ]

    def parse(self, response):

        for chat in response.css("ul.questions li"):

            post_link = response.urljoin(chat.css("h3 a::attr(href)").get())
            answered = chat.css("i.fa-check").get() is not None

            if answered:
                yield scrapy.Request(post_link, callback=self.parse_chat)

        next_page = response.css("li.PagedList-skipToNext a::attr(href)").get()

        if next_page is not None and self.page_count < self.page_limit:

            next_page = response.urljoin(next_page)
            self.page_count = self.page_count + 1
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_chat(self, response):

        title = response.css("div>h1::text").get().strip()

        question = ' '.join(response.css("div.faq-text::text").getall()).strip()

        answers = []

        for answer in response.css("ul.ans li"):

            dr_name = answer.css("b.name-dr::text").get().strip()
            dr_exp = answer.css("span.dr-t::text").get().strip()
            answer_text = ' '.join(answer.css("p::text").getall()).strip()

            answers.append(
                {
                    'dr_name': dr_name,
                    'dr_exp': dr_exp,
                    'answer_text': answer_text
                }
            )

        yield {
            'title': title,
            'question': question,
            'answers': answers
        }


from pathlib import Path

import scrapy


class ChatsSpider(scrapy.Spider):
    name = "chats"

    page_count = 0
    page_limit = 2

    start_urls = [
        "https://doctor-yab.ir/faq/?page=1"
    ]

    def parse(self, response):

        for chat in response.css('ul.questions li'):

            post_link = response.urljoin(chat.css("h3 a::attr(href)").get())
            answered = chat.css("i.fa-check").get() is not None

            yield {
                "title": chat.css("h3 a::text").get().strip(),
                "question": chat.css("h3+span::text").get(),
                "link": post_link,
                "answered": answered,
            }

        next_page = response.css("li.PagedList-skipToNext a::attr(href)").get()

        if next_page is not None and self.page_count < self.page_limit:

            next_page = response.urljoin(next_page)
            self.page_count = self.page_count + 1
            yield scrapy.Request(next_page, callback=self.parse)
